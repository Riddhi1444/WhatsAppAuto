from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def split_text_into_chunks(text, max_length):
    words = text.split()  # Split the text into words
    chunks = []
    current_chunk = ""

    for word in words:
        # If adding the next word exceeds max_length, save the current chunk
        if len(current_chunk) + len(word) + 1 > max_length:  # +1 for space
            chunks.append(current_chunk.strip())  # Append the chunk and strip extra spaces
            current_chunk = word  # Start a new chunk
        else:
            current_chunk += " " + word  # Add word to the current chunk

    if current_chunk:  # Append the last chunk
        chunks.append(current_chunk.strip())

    return chunks

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/rsdan/Onedrive/Desktop/whatsapp-automation/Profile")  # New profile directory
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")

wait = WebDriverWait(driver, 300)
target = '"Auto"'

# Read lyrics file
with open('lyrics.txt', 'r') as lyrics:
    text = lyrics.read()

# Split text into chunks of up to 20 characters without breaking words
chunks = split_text_into_chunks(text, 20)

# Locate the target chat
x_arg = f'//span[contains(@title,{target})]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
group_title.click()

# Send the messages chunk by chunk
inp_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
for chunk in chunks:
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
    input_box.send_keys(chunk + Keys.ENTER)
    time.sleep(1.5)  # Delay between messagesfrom selenium import webdriver