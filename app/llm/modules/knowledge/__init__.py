import os


def get_links(urls_file: str):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    links_path = os.path.join(__location__, urls_file)
    if not os.path.exists(links_path):
        return []
    with open(links_path, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    return lines