import requests
from bs4 import BeautifulSoup

# Prompt for a URL
url = input("Enter a URL: ")

# Send an HTTP GET request to the server
response = requests.get(url)

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Prettify the parsed HTML
prettified_html = soup.prettify()

# Print the prettified HTML
print(prettified_html)
