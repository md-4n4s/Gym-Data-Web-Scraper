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
subscriptions = {}

for page in pages:
    response = requests.get(urljoin(url,page), headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    for image in images:
        img_urls.add(urljoin(url,image["src"]))

    if os.path.basename(page) == "Plan.html":
        plans = soup.find_all(class_="box")

        for plan in plans:
            plan_name = plan.find("h1") if plan.find("h1") else plan.find("h2")

            subscriptions[plan_name.text.strip()] = re.sub(r"[^\d$]","",plan.find("button").text.strip())

print("Available Subscriptions:")
print(subscriptions)

os.makedirs("images", exist_ok=True)

for img_url in img_urls:
    img = requests.get(img_url, headers=headers, timeout=10)
    img.raise_for_status()

    filename = os.path.basename(img_url)

    filepath = os.path.join("images", filename)

    with open(filepath, "wb") as f:
        f.write(img.content)