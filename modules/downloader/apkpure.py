import os
import cloudscraper
import random
from tqdm import tqdm
from modules.logger.log import Logger

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
]


def downloadApp(package_name):
    logger = Logger()
    logger.startLoggingSession()
    try:
        scraper = cloudscraper.create_scraper()
        dnldPath = f"data/apk/{package_name}.apk"

        if os.path.isfile(dnldPath):
            logger.log(f"{package_name} already exists, skipping download.")
            return

        base = "https://d.apkpure.com/b/APK/{package_name}?version=latest"
        headers = {"User-Agent": random.choice(user_agents)}
        os.makedirs(os.path.dirname(dnldPath), exist_ok=True)

        response = scraper.get(
            base.format(package_name=package_name), headers=headers, stream=True
        )

        if response.status_code == 200:
            total_size_in_bytes = int(response.headers.get("content-length", 0))
            progress_bar = tqdm(
                total=total_size_in_bytes,
                unit="iB",
                unit_scale=True,
                bar_format="{l_bar}•{bar}• {n_fmt}/{total_fmt}",
                desc=f"Downloading {package_name}",
            )

            with open(dnldPath, "wb") as file:
                for data in response.iter_content(chunk_size=1024):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                raise Exception(f"Incomplete download: {package_name}")
            else:
                logger.log(f"Downloaded {package_name} successfully.")

        else:
            raise Exception(f"HTTP Error: {response.status_code} for {package_name}")

    except Exception as e:
        logger.log(f"Error downloading {package_name}: {e}", isError=True)

    finally:
        logger.stopLoggingSession()
