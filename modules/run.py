# modules/run.py
from modules.decompiler.apktool import decompileApkUsingApktool
from modules.downloader.playstore import playstore_download
from modules.parser.deeplink import parseDeeplinks
from modules.parser.smali import extractSmaliData
from modules.filter.deeplink import filterDeeplinks
from modules.filter.param import filterParams
from modules.tester.test import testDeeplink
from modules.setup.apktool import setup_apktool
from modules.logger.log import Logger
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()
REDIRECT_URL = os.getenv("REDIRECT_URL")


def run(package_name):
    logger = Logger()
    logger.startLoggingSession()

    csv_dir = "./data/csv/"

    try:
        logger.log(f"Starting process for {package_name}")
        print(
            """
 █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗██╗███╗   ██╗ ██████╗ 
██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝ 
███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║█████╗███████║██║   ██║██╔██╗ ██║   ██║   ██║██╔██╗ ██║██║  ███╗
██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██║██║╚██╗██║██║   ██║
██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝      ██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        """
        )

        logger.log("Setting up apktool...")
        setup_apktool()

        logger.log("Downloading APK...")
        playstore_download(package_name)

        logger.log("Decompiling APK using apktool...")
        if not decompileApkUsingApktool(package_name):
            raise Exception("Decompilation failed")

        logger.log("Parsing deeplinks...")
        deeplinks = parseDeeplinks(
            package_name,
            csv_dir,
            f"./data/decompiled/apktool_{package_name}/AndroidManifest.xml",
            f"./data/decompiled/apktool_{package_name}/res/values/strings.xml",
        )
        if not deeplinks:
            logger.log("No deeplinks found or error in parsing.", isError=True)
            raise Exception("Deeplink parsing failed or no deeplinks found")
        deeplinks = filterDeeplinks(deeplinks)
        logger.log("Deeplinks parsed and filtered successfully.")

        logger.log("Extracting Smali data...")
        params, addURIs, UriParses, addJsIfs, method = extractSmaliData(
            f"./data/decompiled/apktool_{package_name}", deeplinks
        )
        params = filterParams(params)
        logger.log(f"[getQueryParameter]: {params}")
        logger.log(f"[addURI]: {addURIs}")
        logger.log(f"[parse]: {UriParses}")
        logger.log(f"[Javascript Interface]: {method}")
        logger.log(f"[addJavascriptInterface]: {addJsIfs}")

        logger.log("Testing deeplinks...")
        testDeeplink(deeplinks, params, REDIRECT_URL)
        logger.log(f"Process completed successfully for {package_name}")

    except Exception as e:
        logger.log(
            f"An error occurred during processing {package_name}: {e}", isError=True
        )

    finally:
        logger.stopLoggingSession()


def multiRun(package_list):
    for package_name in package_list:
        run(package_name)
