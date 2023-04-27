import os
import requests
from bs4 import BeautifulSoup

# Define the base URL to scrape
base_url = "https://www.gesetze-im-internet.de/Teilliste_{}.html"

# Define the list of alphabet letters to loop through
alphabet_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

# Create a folder to save the PDF files
if not os.path.exists("law_pdf"):
    os.mkdir("law_pdf")

# Loop through each alphabet letter
count = 0
for letter in alphabet_letters:
    # Construct the URL to scrape for the current letter
    url = base_url.format(letter)

    # Make a GET request to the URL
    response = requests.get(url)

    # Use BeautifulSoup to parse the HTML content of the response
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the links in the HTML that point to PDF files
    pdf_links = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))

    # Loop through the PDF links and download each one
    for link in pdf_links:
        # Construct the URL of the PDF file
        pdf_url = "https://www.gesetze-im-internet.de/" + link["href"]

        # Get the filename of the PDF file
        filename = os.path.basename(pdf_url)

        # Set the output path to the 'law_pdf' folder
        output_path = os.path.join("law_pdf", filename)

        # Make a GET request to download the PDF file
        pdf_response = requests.get(pdf_url)

        # Save the PDF file to disk
        with open(output_path, "wb") as f:
            f.write(pdf_response.content)

            # Increment the count if a PDF file is downloaded
            count += 1
            print(f"{filename} downloaded successfully!")

# Print the count of downloaded PDF files
print(f"Total downloaded PDF files: {count}")
