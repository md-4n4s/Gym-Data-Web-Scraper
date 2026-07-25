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

soup = BeautifulSoup(response.content, "html.parser")

