# download_images.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ==== CONFIG ====
GROUP_NAME = "My Dataset"



# ==== SETUP SELENIUM ====
options = Options()
options.add_argument("--user-data-dir=./User_Data")

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




time.sleep(10000)

driver.quit()
print("hello")