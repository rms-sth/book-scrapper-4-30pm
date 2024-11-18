# python -m pip install requests
# => get data from web (html, json, xml)
# python -m pip install beautifulsoup4
# => parse html

# git config --global user.name "FIRST_NAME LAST_NAME"
# git config --global user.email "MY_NAME@example.com"

import sqlite3
import requests
from bs4 import BeautifulSoup

URL = "http://books.toscrape.com/"


def create_database():
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            currency TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_book(title, price, currency):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, price, currency) VALUES (?, ?, ?)
    """,
        (title, price, currency),
    )
    conn.commit()
    conn.close()


def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return

    # Set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text

        #  Extract currency and numeric part
        # The first character should be the currency symbol (e.g., £)
        currency = price_text[0]
        price = price_text[1:]

        insert_book(title, price, currency)


create_database()
scrape_books(URL)
