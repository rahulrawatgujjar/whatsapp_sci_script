# upload_images.py
def main():
    import os
    import time
    import csv
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from choose_folder import get_folder
    from notification import notify_user


    print("\n🔄 Starting image upload process...\n")

    # ==== CONFIG ====
    GROUP_NAME = "My Dataset"


    UPLOAD_FROM_FOLDER=get_folder()

    IMAGE_FOLDER = f"/home/rahulrawatr320/Desktop/dataset/12_models_dresden_2/dresden_codes/data/test/{UPLOAD_FROM_FOLDER}"
    # IMAGE_FOLDER= "/home/rahulrawatr320/Desktop/code/image_folder"
    LOG_FILE = "upload_log.csv"

    # ==== SETUP SELENIUM WITH WEBDRIVER-MANAGER ====
    options = Options()
    options.add_argument("--user-data-dir=./User_Data")  # Reuse session
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")

    print("🔐 Waiting for WhatsApp Web login...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
    )

    # ==== SEARCH FOR GROUP ====
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
    )
    search_box.click()
    time.sleep(1)
    search_box.send_keys(GROUP_NAME)
    search_box.send_keys(Keys.ENTER)

    # notify user to clear the chat
    notify_user("Please clear the chat before uploading images.")

    time.sleep(40) # Wait for group to load, adjust as needed

    # delete previous log file if exists
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("✅ Previous log file deleted.")
        notify_user("Previous log file deleted. Starting fresh upload.")

    # ==== PREPARE CSV LOG ====
    with open(LOG_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "Filename"])

    # ==== UPLOAD IMAGES ====
    image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    for index, img in enumerate(image_files, 1):
        print(f"📤 Uploading: {img}")

        print("✅ Chat loaded, locating attach button...")

        attach_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus-rounded']/ancestor::button"))
        )

        driver.execute_script("arguments[0].click();", attach_button)


        image_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
        )
        image_path = os.path.abspath(os.path.join(IMAGE_FOLDER, img))
        image_input.send_keys(image_path)

        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Send']"))
        )
        send_button.click()

        with open(LOG_FILE, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([index, img])

        time.sleep(3)

    time.sleep(10)

    print("✅ All images uploaded and logged to CSV.")
    driver.quit()

    # verify all images are uploaded
    with open(LOG_FILE, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) - 1 == len(image_files):  # -1 for header
            print(f"✅ All {len(image_files)} images successfully logged in CSV.")
            notify_user(f"✅ Upload complete! All {len(image_files)} images have been uploaded and logged to CSV.")
        else:
            print("❌ Some images were not logged correctly. Please check the log file.")
            notify_user("❌ Upload incomplete! Please check the log file for details.")