from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


class KnowledgeDriver:
    def __init__(self):
        self.driver = self._create_driver()
        self.urls_for_knowledge = ["https://docs.neonevm.org/docs/quick_start",
                                   "https://docs.starknet.io",
                                   "https://docs.wormhole.com/wormhole",
                                   "https://docs.sui.io"
                                   ]
        self.blog_urls = ["https://wormhole.com/blog",
                          "https://neonevm.org/blog"
                          ]

    def _create_driver(self):
        chromedriver_path = '/usr/bin/chromedriver'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=ChromeService(chromedriver_path), options=chrome_options) # ChromeDriverManager().install()

    def is_driver_started(self):
        try:
            _ = self.driver.current_url
            return True
        except Exception as e:
            print(f"Driver not started: {e}")
            return False

    def update_all_data(self):
        urls = self._update_all_urls()
        blog_posts = self._update_blog_posts()
        self.driver.close()
        return urls.union(blog_posts)

    def _read_urls_from_file(self, file_path):
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file.readlines()]
        return urls

    def _update_all_urls(self):
        if not self.is_driver_started():
            self.driver = self._create_driver()
        urls_over_protocol = set()

        for link in self.urls_for_knowledge:
            splited_url = link.split("/")
            startswith = f"{splited_url[0]}//{splited_url[2]}"

            def __crawl_page(url):
                try:
                    self.driver.get(url)
                    self.driver.implicitly_wait(10)
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    links = soup.find_all("a")
                    for link in links:
                        href = link.get("href")
                        if href and not href.startswith("#"):
                            absolute_url = urljoin(url, href)
                            href = href.split("#")[0]
                            if absolute_url.startswith(startswith) and absolute_url not in urls_over_protocol:
                                urls_over_protocol.add(absolute_url)
                                # Recursively crawl the linked page
                                __crawl_page(absolute_url)
                except Exception as e:
                    print(f"Error {str(e)}")

            __crawl_page(link)
        return urls_over_protocol

    def _update_blog_posts(self):
        if not self.is_driver_started():
            self.driver = self._create_driver()
        blog_posts = set()
        for link in self.blog_urls:
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


if __name__ == "__main__":
    kn = KnowledgeDriver()
    urls = kn.update_all_data()
    print(urls)
