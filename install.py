# PYMailer Installer & Updater
# © 2026 Atif's Codeworks

import os
import zipfile
import urllib.request
import shutil
import subprocess
import sys

REPO_ZIP_URL = "https://github.com/exotic-atif/pymailer/archive/refs/heads/main.zip"
RAW_VER_URL = "https://raw.githubusercontent.com/exotic-atif/pymailer/main/.ver"

ZIP_NAME = "pymailer_temp.zip"
LOCAL_VER_FILE = ".ver"

REQUIRED_LIBS = [
    "PyQt6",
    "python-dotenv"
]


def get_remote_version():
    try:
        with urllib.request.urlopen(RAW_VER_URL) as response:
            return response.read().decode().strip()
    except:
        return None


def get_local_version():
    if os.path.exists(LOCAL_VER_FILE):
        with open(LOCAL_VER_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def version_tuple(v):
    return tuple(map(int, v.split(".")))


def download_repo():
    print("Downloading latest PYMailer...")
    urllib.request.urlretrieve(REPO_ZIP_URL, ZIP_NAME)
    print("Download complete.\n")


def extract_repo(overwrite=False):
    print("Extracting files...\n")

    with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall()

    extracted_folder = "pymailer-main"

    for item in os.listdir(extracted_folder):
        src = os.path.join(extracted_folder, item)
        dst = os.path.join(os.getcwd(), item)

        if os.path.exists(dst):
            if overwrite:
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            else:
                continue

        shutil.move(src, dst)

    shutil.rmtree(extracted_folder)
    os.remove(ZIP_NAME)

    print("Installation complete.\n")


def check_dependencies():
    print("Checking required dependencies...\n")

    missing = []

    for lib in REQUIRED_LIBS:
        try:
            __import__(lib.replace("-", "_"))
        except ImportError:
            missing.append(lib)

    if not missing:
        print("All dependencies are already installed.\n")
        return True

    print("The following libraries are required but not installed:\n")
    for lib in missing:
        print(f" - {lib}")

    confirm = input("\nPress 'y' to install them now or 'n' to abort: ").strip().lower()

    if confirm != "y":
        print("Installation aborted due to missing dependencies.\n")
        return False

    print("\nInstalling dependencies...\n")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        print("\nDependencies installed successfully.\n")
        return True
    except Exception as e:
        print("\nFailed to install dependencies.")
        print(str(e))
        return False


def main():
    print("Checking PYMailer version...\n")

    remote_ver = get_remote_version()
    if not remote_ver:
        print("Could not fetch remote version. Check your internet connection.")
        return

    local_ver = get_local_version()

    if local_ver:
        print(f"Installed version: {local_ver}")
    else:
        print("No existing installation found.")
        print("This will be a fresh install.")

    print(f"Latest version: {remote_ver}\n")

    # Same version
    if local_ver == remote_ver:
        print("You already have the latest version.\n")
        return

    # Local newer than remote
    if local_ver and version_tuple(local_ver) > version_tuple(remote_ver):
        print("Your local version is newer than the repository version.")
        print("Installation skipped.\n")
        return

    # Update available
    if local_ver and version_tuple(local_ver) < version_tuple(remote_ver):
        print("Update available.")
        confirm = input("Do you want to update? (y/n): ").strip().lower()
        if confirm != "y":
            print("Update skipped.\n")
            return

        download_repo()
        extract_repo(overwrite=True)

        if not check_dependencies():
            return

        print("Update completed successfully.\n")
        return

    # Fresh install
    confirm = input("Install PYMailer? (y/n): ").strip().lower()
    if confirm != "y":
        print("Installation cancelled.\n")
        return

    download_repo()
    extract_repo(overwrite=True)

    if not check_dependencies():
        return

    print("Installation completed successfully.\n")
    print("Run the setup.py (Ignore if already done.)\n")


if __name__ == "__main__":
    main()
