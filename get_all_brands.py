import logging

import pandas as pd
from cells.net import fix_relative_url
from playwright.sync_api import sync_playwright


logger = logging.getLogger("brands")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(filename=f"{logger.name}.txt", encoding="utf-8", delay=True))

DOMAIN = "https://car.autohome.com.cn/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def get_all_brands():
    bucket = []
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(DOMAIN)

        doms = page.locator("#cartree").locator("h3").all()
        for d in doms:
            d.click(delay=300)  #
            page.wait_for_load_state("domcontentloaded")
            for item in page.locator("#cartree").locator("ul dl dd").all():
                element_a = item.locator("a")
                car_series_title = item.inner_text().strip()
                car_series_id = element_a.get_attribute("id").strip()
                car_series_uri = element_a.get_attribute("href").strip()

                log = f"{car_series_title},{car_series_id},{fix_relative_url(DOMAIN, car_series_uri)}"
                bucket.append(log)
                print(log)
                logger.info(log)

    pd.DataFrame([i.split(",") for i in bucket]).to_csv("brands.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    get_all_brands()
