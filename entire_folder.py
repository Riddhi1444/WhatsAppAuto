import os
import time
import pandas as pd
from tkinter import Tk, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Function to select Excel file
def select_excel_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring the dialog to the front
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", ".xlsx;.xls"), ("All Files", ".")]
    )
    return file_path

# Dynamic path setup
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current directory
chrome_profile = os.path.join(base_dir, "Profile")  # Profile folder in current directory
chromedriver_path = os.path.join(base_dir, "chromedriver.exe")  # Path to chromedriver in current folder

# Ask the user to select the Excel file
excel_path = select_excel_file()
if not excel_path:
    print("No file selected. Exiting.")
    exit()

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile}")  # Use dynamic profile folder
service = Service(chromedriver_path)  # Use dynamic chromedriver path
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")

wait = WebDriverWait(driver, 300)

# Read the Excel file
data = pd.read_excel(excel_path)

# Loop through each row in the Excel file
for index, row in data.iterrows():
    target = row['Recipient']  # Target name
    document_path = row['FilePath']  # File or folder path

    if not os.path.isabs(document_path):
        document_path = os.path.join(base_dir, document_path)  # Handle relative paths

    # Locate the target chat
    try:
        x_arg = f'//span[contains(@title,"{target}")]'
        group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        group_title.click()

        # Check if the path is a file or a folder
        if os.path.isfile(document_path):
            files_to_send = [document_path]
        elif os.path.isdir(document_path):
            files_to_send = [os.path.join(document_path, f) for f in os.listdir(document_path)]
        else:
            print(f"Invalid path: {document_path}")
            continue

        for file_path in files_to_send:
            if os.path.isfile(file_path):
                # Locate the attachment button and click it
                attachment_button_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button/span'
                attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, attachment_button_xpath)))
                attachment_button.click()

                # Locate the hidden input element for the document upload
                file_input_xpath = '//input[@accept="*"]'  # File input accepts all file types
                file_input = wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
                file_input.send_keys(file_path)  # Send the file path

                # Wait for the Send button to appear
                time.sleep(2)  # Ensure file has time to upload fully
                send_button_xpath = '//span[@data-icon="send"] | //div[@role="button" and @aria-label="Send"]'

                try:
                    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
                    send_button.click()
                    print(f"Document sent successfully to {target}: {file_path}")
                except Exception as e:
                    print(f"Failed to click the Send button for {target}: {str(e)}")
            else:
                print(f"Skipping invalid file: {file_path}")

    except Exception as e:
        print(f"Failed to locate or send message to {target}: {str(e)}")

# Close browser
time.sleep(10)
driver.quit()