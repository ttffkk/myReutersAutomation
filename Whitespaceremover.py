import requests
from bs4 import BeautifulSoup
import os
import subprocess

# Function to remove whitespaces and special characters
def remove_special_characters(text):
    return ''.join(e for e in text if e.isalnum())

# Function to remove "Acquire Licensing Rights" but keep the content after it
def remove_acquire_licensing_rights(text):
    # Find the position of "Acquire Licensing Rights"
    index = text.find("Acquire Licensing Rights")
    
    # If found, return the text before it, otherwise, return the original text
    return text[:index] if index != -1 else text

# Read URLs from a text file
with open('urls.txt', 'r') as url_file:
    urls = url_file.readlines()

# Process each URL
for url in urls:
    url = url.strip()  # Remove leading/trailing whitespace
    
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

            # Check if the first paragraph contains "Acquire Licensing Rights"
            if paragraphs and paragraphs[0].text.startswith("Acquire Licensing Rights"):
                # Remove "Acquire Licensing Rights" from the first paragraph
                paragraphs[0] = paragraphs[0].text.replace("Acquire Licensing Rights", "", 1)

            # Combine the h1 text and paragraphs into one string
            content = h1_text + '\n\n'
            for paragraph in paragraphs:
                content += paragraph.get_text() + '\n\n'

            # Write the content to the file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Content saved to {filename}")
            
            # Run AWS Polly to convert the text to speech
            aws_command = f'aws polly start-speech-synthesis-task --engine standard --language-code en-US --output-format mp3 --output-s3-bucket-name reuters-mp3-readout --output-s3-key-prefix {h1_cleaned} --text-type text --voice-id Joanna --text file://{filename}'

            result = subprocess.run(aws_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0:
                print("Text converted to speech successfully.")
            else:
                print("Error converting text to speech:", result.stderr)
                
        else:
            print("No h1 tag found on the page.")
    else:
        print("Failed to retrieve the web page at:", url)
