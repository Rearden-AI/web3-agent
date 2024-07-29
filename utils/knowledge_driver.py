import os
import json
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException

logger = logging.getLogger("Knowledge driver")


class KnowledgeDriver:
    def __init__(self, discord_auth: str):
        self.driver = self._create_driver()
        self.discord_auth = discord_auth

    def _create_driver(self):
        chromedriver_path = '/usr/bin/chromedriver'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(service=ChromeService(chromedriver_path), options=chrome_options)

    def is_driver_started(self):
        try:
            _ = self.driver.current_url
            return True
        except Exception as e:
            print(f"Driver not started: {e}")
            return False

    def parse_all_links(self, initial_page: str | dict):
        if not self.is_driver_started():
            self.driver = self._create_driver()

        urls_over_protocol = set()

        def __crawl_page(page: str | dict):
            # logger.info(f"Crawling {url}")
            if isinstance(page, str):
                url = page

                splited_url = url.split("/")
                base_url = f"{splited_url[0]}//{splited_url[2]}"
            else:
                url = page["url"]
                base_url = page["starts_with"]

            urls_over_protocol.add(url)

            try:
                self.driver.get(url)

                links = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "A"))
                )

                def __get_href(element):
                    try:
                        return element.get_attribute("href")
                    except:
                        return None

                links = list(map(__get_href, links))
                links = list(filter(lambda x: True if x else False, links))

                for link in links:
                    link = link.split("#")[0]
                    if link.endswith("/"):
                        link = link[:-1]
                    if (
                        link.startswith(base_url)
                        and link not in urls_over_protocol
                        and not link.endswith(".pdf")
                    ):
                        __crawl_page(page={"url": link, "starts_with": base_url})
            except TimeoutException:
                pass
            except Exception:
                logger.exception("Failed to crawl")

        __crawl_page(page=initial_page)

        self.driver.close()

        return urls_over_protocol

    def update_blog_posts(self, link):
        if not self.is_driver_started():
            self.driver = self._create_driver()
        blog_posts = set()
        splited_url = link.split("/")
        startswith = f"{splited_url[0]}//{splited_url[2]}"
        self.driver.get(link)
        self.driver.implicitly_wait(10)
        while True:
            try:
                see_more_button = self.driver.find_element(By.XPATH,
                                                           "//div[@class='w-fit cursor-pointer mx-auto cursor-pointer']")
                see_more_button.click()
                self.driver.implicitly_wait(10)  # Wait for new content to load
            except (NoSuchElementException, ElementClickInterceptedException):
                break  # No more "See More" button or couldn't click it
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '/blog/' in href and href not in blog_posts:
                full_url = f"{startswith}{href}" if href.startswith('/') else href
                blog_posts.add(full_url)

        return blog_posts

    def update_discord_faq(self, link: str, protocol_name: str):
        if not self.is_driver_started():
            self.driver = self._create_driver()
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
            'headers': {
                'Authorization': self.discord_auth
            }
        })
        self.driver.get(link)
        self.driver.implicitly_wait(10)  # Wait for the page to load
        page = self.driver.find_elements(By.CSS_SELECTOR, 'pre')  # Replace with actual CSS selector for threads
        data = json.loads(page[0].text)
        if isinstance(data, dict) and data.get("message") == '401: Unauthorized':
            logger.critical(f"Discord unauthorized!")
            return False
        path = os.path.join("vectorstore_updater_app", "knowledge", f"{protocol_name}_discord.txt")
        with open(path, "w") as file:
            file.write(f"Protocol: {protocol_name}")
            if protocol_name in ('wormhole'):
                threads = data.get('threads')
                answer = data.get('first_messages')
                for i in range(len(threads)):
                    file.write(f"thread: {threads[i].get('name')}, answer: {answer[i].get('content')}")

            elif protocol_name in ('neon'):
                content = data[0].get('content')
                embeds = data[0].get('embeds')
                file.write(f"\n Content: {content}")
                for embed in embeds:
                    file.write(f"{embed.get('description')}")
        return True

if __name__ == "__main__":
    import time
    discord_auth = ""
    kn = KnowledgeDriver(discord_auth=discord_auth)
    start = time.time()
    link = "https://docs.wormhole.com/wormhole"
    urls = kn.parse_all_links(link)
    disco = kn.update_discord_faq(link="https://discord.com/api/v9/channels/1075310129798459492/threads/search?archived=true&sort_by=last_message_time&sort_order=desc&limit=25&tag_setting=match_some&offset=0", protocol_name="wormhole")
    end = time.time()
    print("the time of execution: ", (end - start))
    print(urls)
    print(f"url length {len(urls)}")
    print(f"faq disco updated: {disco}")
