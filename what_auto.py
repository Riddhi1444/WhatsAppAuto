import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Dynamic path setup
base_dir = os.path.dirname(os.path.abspath(_file_))
chrome_profile = os.path.join(base_dir, "Profile")
chromedriver_path = os.path.join(base_dir, "chromedriver.exe")

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile}")  # Profile folder in current directory
service = Service(chromedriver_path)  # Path to chromedriver in current folder
driver = webdriver.Chrome(service=service, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 300)

# Target contact and message
target = '"Riddhi"'
message = "Hello"
number_of_times = 3

# Locate the target contact
contact_path = f'//span[contains(@title,{target})]'
contact = wait.until(EC.presence_of_element_located((By.XPATH, contact_path)))
contact.click()

# Send the message multiple times
for x in range(number_of_times):
    message_box_path = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
    message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
    message_box.send_keys(message + Keys.ENTER)
    print(f"Message {x+1} sent")
    time.sleep(1.5)