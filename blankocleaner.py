import requests
from bs4 import BeautifulSoup
import os

# Function to remove whitespaces and special characters
def remove_special_characters(text):
    return ''.join(e for e in text if e.isalnum())

# Input URL from the command line
url = input("Enter the URL: ")

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the h1 tag
    h1_tag = soup.find('h1')

    if h1_tag:
        # Get the text inside the h1 tag
        h1_text = h1_tag.get_text()

        # Remove whitespaces and special characters from h1 text
        h1_cleaned = remove_special_characters(h1_text)

        # Create a directory for storing the files if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")

        # Create a file with the h1 tag as the filename
        filename = os.path.join("output", f"{h1_cleaned}.txt")

        # Find all paragraph tags
        paragraphs = soup.find_all('p')

        # Check if the first paragraph contains a picture description
        if paragraphs and paragraphs[0].text.startswith("[1/"):
            # Exclude the first paragraph
            paragraphs = paragraphs[1:]

        # Combine the h1 text and paragraphs into one string
        content = h1_text + '\n\n'
        for paragraph in paragraphs:
            content += paragraph.get_text() + '\n\n'

        # Remove content after "Reporting by"
        index = content.find("Reporting by")
        if index != -1:
            content = content[:index]

        # Write the content to the file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Content saved to {filename}")
    else:
        print("No h1 tag found on the page.")
else:
    print("Failed to retrieve the web page. Check the URL and try again.")
