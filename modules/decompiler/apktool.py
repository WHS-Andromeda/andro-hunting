import subprocess
import os
from modules.logger.log import Logger


def decompileApkUsingApktool(package_name):
    logger = Logger()
    logger.startLoggingSession()

    apkPath = f"./data/apk/{package_name}.apk"
    outputDirectory = f"./data/decompiled/apktool_{package_name}/"
    command = f"java -jar apktool.jar d {apkPath} -o {outputDirectory}"

    if os.path.isdir(outputDirectory):
        logger.log(
            f"Output directory already exists for {package_name}, skipping decompilation."
        )
        logger.stopLoggingSession()
        return True

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        logger.log("Decompilation completed successfully.")
        logger.log(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.log(f"Failed to decompile the APK for {package_name}: {e}", isError=True)
        logger.log(e.stdout, isError=True)
        return False
    finally:
        logger.stopLoggingSession()
