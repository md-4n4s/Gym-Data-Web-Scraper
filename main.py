import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://titan-fitness-club-website.vercel.app/"

headers = {
    # Identify the client making request
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)

# Raise an exception if request returend an error status
response.raise_for_status()

# Parse html of the web
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

# pages with data type set is created to avoid storing duplicate pages
pages = set()

for link in links:
    pages.add(link["href"])

img_urls = set()
subscriptions = {}

for page in pages:

    # GET request is sent for every page found
    response = requests.get(urljoin(url,page), headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    for image in images:
        img_urls.add(urljoin(url,image["src"]))

    # If path ends with "/Plan.html"
    if os.path.basename(page) == "Plan.html":
        plans = soup.find_all(class_="box")

        for plan in plans:
            plan_name = plan.find("h1") if plan.find("h1") else plan.find("h2")

            subscriptions[plan_name.text.strip()] = re.sub(r"[^\d$]","",plan.find("button").text.strip()) # Only digits and '$' is saved, everything else is removed

print("Available Subscriptions:")
print(subscriptions)

# images folder is created, uses already existed folder if available
os.makedirs("images", exist_ok=True)

for img_url in img_urls:

    # Image is requested from server
    img = requests.get(img_url, headers=headers, timeout=10)
    img.raise_for_status()

    # Filename is extracted from url for example /gym.png
    filename = os.path.basename(img_url)

    # New path is set for the picture for example /images/gym.png is added
    filepath = os.path.join("images", filename)

    # Filepath is opened in write binary mode to save images in binary
    with open(filepath, "wb") as f:
        f.write(img.content)
