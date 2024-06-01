import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://epay-stg.um.edu.my/?lang=en"

try:
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    exit(1)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract relevant information
data = []

# Extract text from all paragraph tags
for paragraph in soup.find_all('p'):
    text = paragraph.get_text(strip=True)
    if text:
        data.append(text)
        print(f"Extracted text from <p>: {text}")

# Extract text from all div tags
for div in soup.find_all('div'):
    text = div.get_text(strip=True)
    if text:
        data.append(text)
        print(f"Extracted text from <div>: {text}")

# Extract text from specific div classes
# Add your specific class names here
specific_classes = ['specific-class', 'another-class']

for class_name in specific_classes:
    for div in soup.find_all('div', class_=class_name):
        text = div.get_text(strip=True)
        if text:
            data.append(text)
            print(f"Extracted text from <div class='{class_name}'>: {text}")

# Extract text from all li tags
for li in soup.find_all('li'):
    text = li.get_text(strip=True)
    if text:
        data.append(text)
        print(f"Extracted text from <li>: {text}")

# Check if data was extracted
if not data:
    print("No data was extracted.")
else:
    print(f"Extracted {len(data)} items.")

# Save data to a text file
output_file = 'um_epay_scraped_data.txt'
try:
    with open(output_file, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")
    print(f"Scraped data saved to '{output_file}'")
except IOError as e:
    print(f"File write failed: {e}")
