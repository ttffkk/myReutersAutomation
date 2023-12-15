import requests
from bs4 import BeautifulSoup
import os
import subprocess
import logging


# Function to remove special characters and whitespace
def remove_special_characters(text):
    return ''.join(e for e in text if e.isalnum())


# Function to process a single URL
def process_url(uri):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    # Send a GET request to the URL
    response = requests.get(uri, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the h1 tag
        h1_tag = soup.find('h1')

        if h1_tag:
            # Get the text inside the h1 tag
            h1_text = h1_tag.get_text()

            # Remove special characters and whitespace from h1 text
            h1_cleaned = remove_special_characters(h1_text)

            # Create a directory for storing the files if it doesn't exist
            if not os.path.exists("output"):
                os.makedirs("output")

            # Create a file with the h1 tag as the filename
            filename = os.path.join("output", f"{h1_cleaned}.log")

            # Find all paragraph tags
            paragraphs = soup.find_all('p')

            # Check if any <p> tag contains "Acquire Licensing Rights" and exclude it
            paragraphs = [p for p in paragraphs if "Acquire Licensing Rights" not in p.get_text()]

            # Combine the h1 text and paragraphs into one string
            content = h1_text + '\n\n'
            for paragraph in paragraphs:
                content += paragraph.get_text() + '\n\n'

            # Remove content after "Reporting"
            index = content.find("Reporting")
            if index != -1:
                content = content[:index]

            # Write the content to the file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Content saved to {filename}")
            subprocess.run(["python", "Delivery.py", h1_cleaned, filename])
        else:
            print("No h1 tag found on the page.")
            logging.debug('No H1 Tag could be found on ' + uri)
    else:
        logging.debug('Error code ' + str(response.status_code) + " " + uri)
        print(f"Failed to retrieve the web page at URL: {uri}" + f" Error code {response.status_code}")
        logging.debug('Failed to retrieve the web page at URL: ' + uri)


# Read URLs from a file (e.g., urls.txt)
with open("urls.txt", "r") as url_file:
    urls = url_file.read().splitlines()

logging.basicConfig(filename='app.tods', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
# Process each URL
for url in urls:
    process_url(url)

z = False
while not z:
    z = bool(input("Can you confirm you read the logs"))
