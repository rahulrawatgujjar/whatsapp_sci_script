# download_images.py
def main():

    import os
    import time
    import csv
    import pyautogui
    from pathlib import Path
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from choose_folder import get_folder
    from notification import notify_user

    print("\n🔄 Starting image download process...\n")

    # ==== CONFIG ====
    GROUP_NAME = "My Dataset"


    FOLDER_TO_DOWNLOAD= get_folder()

    DOWNLOAD_DIR = f"/home/rahulrawatr320/Desktop/dataset/12_models_dresden_2_whatsapp/data/test/{FOLDER_TO_DOWNLOAD}"
    # DOWNLOAD_DIR= "/home/rahulrawatr320/Desktop/code/download_images"
    LOG_FILE = "upload_log.csv"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # ==== LOAD FILENAMES FROM CSV ====
    renames = []
    with open(LOG_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            renames.append(row["Filename"])

    # ==== SETUP SELENIUM ====
    options = Options()
    options.add_argument("--user-data-dir=./User_Data")
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")

    print("🔐 Waiting for WhatsApp Web login...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
    )

    # ==== OPEN GROUP ====
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
    )
    search_box.click()
    time.sleep(1)
    search_box.send_keys(GROUP_NAME)
    search_box.send_keys(Keys.ENTER)

    # ==== WAIT FOR GROUP HEADER ====
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//header"))
        )
        print("📥 Group chat loaded.")
    except:
        print("❌ Group not found.")
        driver.quit()
        exit()


    # notify user to refresh the images
    notify_user("Please refresh the Images in the group")

    # ==== OPEN STACKED IMAGE GALLERY ====
    print("🖱️ Automatically clicking on the stacked image...")
    time.sleep(2)
    pyautogui.moveTo(1578, 899, duration=0.5)
    time.sleep(1)
    pyautogui.click()
    print("✅ Clicked stacked image. Waiting for gallery to open...")

    # ==== WAIT FOR GALLERY TO LOAD ====
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'blob:')]"))
        )
        print("🖼️ Gallery view detected. Starting download...")
    except:
        print("❌ Gallery not detected.")
        driver.quit()
        exit()

    # ==== WAIT BEFORE STARTING DOWNLOADS ====
    print("⏳ Waiting a bit before starting downloads...")
    notify_user("Starting image downloads in 15 seconds. Please do not interfere.")
    time.sleep(2)
    print("✅ Starting downloads now.")

    # ==== DOWNLOAD LOOP ====
    count = 0

    while count < len(renames):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'blob:')]"))
            )

            download_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[@aria-label='Download'] | //span[@data-icon='download']/ancestor::button"
                ))
            )
            download_btn.click()
            count += 1
            print(f"⬇️ Downloaded image {count}")
            time.sleep(2)

            # Rename the downloaded file
            downloaded_files = sorted(Path(DOWNLOAD_DIR).glob("*"), key=os.path.getmtime)
            last_file = downloaded_files[-1]

            new_name = renames[count - 1]
            new_path = Path(DOWNLOAD_DIR) / new_name
            last_file.rename(new_path)
            print(f"📝 Renamed to {new_name}")

            # Move to next image
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error: {str(e).splitlines()[0]}")
            break


    driver.quit()


    # verify all images are downloaded
    if count == len(renames):
        print(f"✅ All {count} images successfully downloaded and renamed.")
        notify_user(f"✅ Download complete! {count} images downloaded and renamed.")
    else:
        print(f"❌ Some images were not downloaded. Expected {len(renames)}, got {count}.")
        notify_user(f"❌ Download incomplete! Expected {len(renames)} images, but only {count} were downloaded.")

