import pathlib
from typing import List, Tuple
from urllib3.response import HTTPResponse
import requests
from bs4 import BeautifulSoup
from uploader import Uploader


class Scraper:
    def __init__(self):
        self.page_url = "https://www.cazoo.co.uk/cars/?page="
        self.base_url = "https://www.cazoo.co.uk"
        self.urls = []
        self.uploader = Uploader()

    @staticmethod
    def get_total_pages(soup: BeautifulSoup) -> str:
        return (
            soup.find("nav", {"aria-label": "Pagination"})
            .find_all("a")[-2]
            .attrs["href"]
            .split("=")[-1]
        )

    def extract_urls(self, soup: BeautifulSoup) -> List[str]:
        return [
            self.base_url + a.attrs["href"]
            for a in soup.find_all("a", {"data-test-id": "card-wrap-link"})
        ]

    @staticmethod
    def get_make_model(soup: BeautifulSoup) -> Tuple[str, str]:
        _, _, make, model, _ = (
            soup.find("nav", {"data-test-id": "breadcrumb"})
            .find_all("li")[-1]
            .find("a")
            .attrs["href"]
            .split("/")
        )
        make = make.replace(" ", "-")
        model = model.replace(" ", "-")
        return make, model

    def get_urls(self) -> List[str]:
        soup = self.get_html(self.page_url + "1")
        total_pages = self.get_total_pages(soup)
        self.urls += self.extract_urls(soup)
        print(f"1/{total_pages} url pages...", end="\r")

        for i in range(2, int(total_pages) + 1):
            soup = self.get_html(self.page_url + str(i))
            self.urls += self.extract_urls(soup)
            print(f"{i}/{total_pages} url pages...", end="\r")

        return self.urls

    @staticmethod
    def get_html(url: str) -> BeautifulSoup:
        r = requests.get(url)
        return BeautifulSoup(r.content, "html.parser")

    @staticmethod
    def get_image_url(soup: BeautifulSoup) -> str:
        return soup.find("img", {"data-test-id": "default-hero-image"}).attrs["src"]

    @staticmethod
    def get_image_data(img_url: str) -> HTTPResponse | None:
        r_img = requests.get(img_url, stream=True)
        if r_img.status_code == 200:
            return r_img.raw
        else:
            return None

    @staticmethod
    def get_image_filename(img_url: str) -> str:
        return pathlib.Path(img_url).name

    def scrape_page(self, url: str) -> Tuple[str, str, str, str]:
        soup = self.get_html(url)
        make, model = self.get_make_model(soup)
        img_url = self.get_image_url(soup)
        img_filename = self.get_image_filename(img_url)
        return make, model, img_url, img_filename
