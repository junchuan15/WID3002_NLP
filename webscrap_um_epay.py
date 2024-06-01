import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Selenium WebDriver
options = Options()
options.headless = True  # Run headless browser
driver = webdriver.Chrome()


# URL to scrape
url = "https://epay-stg.um.edu.my/?lang=en"

# Open the webpage
driver.get(url)

# Wait for the page to load
time.sleep(3)

# Function to scrape data from the current page
def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = []

    # Define general selectors to target common HTML structures
    general_selectors = ['div', 'section', 'p', 'li']

    # Extract text from general selectors
    for selector in general_selectors:
        for element in soup.find_all(selector):
            text = element.get_text(strip=True)
            if text:
                data.append(text)

    return data

# Initial scrape of the main page
data = scrape_page(driver)

# Function to click through links and scrape each page
def click_and_scrape_links(driver, data):
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        try:
            # Open link in a new tab
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .click(link) \
                .key_up(Keys.CONTROL) \
                .perform()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            data.extend(scrape_page(driver))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"Failed to click link: {e}")

# Click through all the links on the main page
click_and_scrape_links(driver, data)

# Close the driver
driver.quit()

# Clean up data by removing unnecessary whitespace and non-informative text
cleaned_data = []
for item in data:
    cleaned_item = ' '.join(item.split())  # Remove excessive whitespace
    if cleaned_item and not any(exclusion in cleaned_item.lower() for exclusion in ['log in', 'register', 'home', 'about us']):
        cleaned_data.append(cleaned_item)

# Check if data was extracted
if not cleaned_data:
    print("No data was extracted.")
else:
    print(f"Extracted {len(cleaned_data)} items.")

# Save cleaned data to a text file
output_file = 'um_epay_cleaned_data2.txt'
try:
    with open(output_file, 'w', encoding='utf-8') as file:
        for item in cleaned_data:
            file.write(f"{item}\n")
    print(f"Cleaned data saved to '{output_file}'")
except IOError as e:
    print(f"File write failed: {e}")
