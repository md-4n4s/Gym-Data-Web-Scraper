import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://titan-fitness-club-website.vercel.app/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

pages = set()

for link in links:
    pages.add(link["href"])

img_urls = set()

for page in pages:
    response = requests.get(urljoin(url,page), headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    for image in images:
        img_urls.add(image["src"])

