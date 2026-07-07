import os
import logging
import pandas as pd
import asyncio
from playwright.async_api import async_playwright


# LOGGER
logger = logging.getLogger("MapsCrawler")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        "crawler_process.log",
        mode="a",
        encoding="utf-8"
    )

    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)


# SET DATA
KEYWORDS = [
    "Cafe",
    "Restoran",
]

DATASET_WILAYAH = {
    "Jawa Barat": [
        "Depok",
    ]
}

CSV_FILENAME = "master_dataset_umkm.csv"



# CRAWLER
async def crawl_single_query(page, search_query, all_extracted_urls, csv_filename):
    try:
        search_box = page.locator('input[role="combobox"]')
        await search_box.wait_for()
        await search_box.fill("")
        logger.info(f"Search : {search_query}")
        await search_box.fill(search_query)
        await search_box.press("Enter")
        feed = page.locator('div[role="feed"]')
        await feed.wait_for(timeout=15000)
        await page.wait_for_selector(
            'a[href*="/maps/place/"]',
            timeout=10000
        )

        previous_count = 0
        attempts = 0
        max_attempts = 3

        while True:

            await feed.evaluate(
                "node => node.scrollTo(0, node.scrollHeight)"
            )

            await page.wait_for_timeout(2500)

            extracted_data = await page.evaluate("""
            () => {
                const links = document.querySelectorAll(
                    'a[href*="/maps/place/"]'
                );

                const data = [];

                links.forEach(link => {

                    const nama =
                        link.getAttribute('aria-label')
                        || 'Tidak ada nama';

                    const url =
                        link.getAttribute('href')
                        || '-';

                    data.push({
                        "Nama UMKM": nama,
                        "URL": url
                    });
                });

                return data;
            }
            """)

            data_baru = []

            for item in extracted_data:
                if item["URL"] not in all_extracted_urls:
                    all_extracted_urls.add(item["URL"] )
                    item["Keyword Pencarian"] = (search_query)
                    data_baru.append(item)
            if data_baru:
                df = pd.DataFrame(data_baru)
                file_exists = os.path.isfile(
                    csv_filename
                )
                df.to_csv(
                    csv_filename,
                    mode="a",
                    index=False,
                    header=not file_exists
                )
                logger.info(
                    f"{len(data_baru)} data baru disimpan"
                )
            new_count = await page.locator('a[href*="/maps/place/"]').count()
            logger.info(f"Scrolling... ({new_count})")

            if new_count == previous_count:
                attempts += 1
                if attempts >= max_attempts:
                    logger.info(
                        "Scroll selesai"
                    )
                    break
            else:
                attempts = 0
                previous_count = new_count

    except Exception as e:
        logger.error(
            f"Error {search_query}: {e}"
        )


# MAIN
async def main_crawler_engine():

    all_extracted_urls = set()
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=1000
        )
        page = await browser.new_page(
            viewport={
                "width": 1600,
                "height": 900
            }
        )

        await page.goto(
            "https://www.google.com/maps",
            wait_until="domcontentloaded"
        )

        for provinsi, daftar_kota in DATASET_WILAYAH.items():
            logger.info(
                f"\n===== {provinsi.upper()} ====="
            )
            for kota in daftar_kota:
                for keyword in KEYWORDS:
                    query = f"{keyword} {kota}"
                    await crawl_single_query(
                        page,
                        query,
                        all_extracted_urls,
                        CSV_FILENAME
                    )
                    await asyncio.sleep(2)
        await browser.close()
    logger.info(
        f"Total URL unik: {len(all_extracted_urls)}"
    )


# Entry Point
if __name__ == "__main__":
    asyncio.run(main_crawler_engine())