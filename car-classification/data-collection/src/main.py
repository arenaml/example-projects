from scraper import Scraper
from metadata import Database, Metadata
from uploader import Uploader


def main():
    db = Database()
    scraper = Scraper()
    uploader = Uploader()

    urls = scraper.get_urls()

    for i, url in enumerate(urls):
        if not db.image_exists(url):
            metadata = Metadata()
            make, model, img_url, img_filename = scraper.scrape_page(url)
            metadata.product_url = url
            metadata.make = make
            metadata.model = model
            metadata.image_url = img_url
            metadata.image_filename = img_filename
            img_data = scraper.get_image_data(img_url)
            uploader.save_image(img_data, img_filename, make)
            db.add_to_db(metadata)
        print(f"{i+1}/{len(urls)} images collected...", end="\r")


if __name__ == "__main__":
    main()
