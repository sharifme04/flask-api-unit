"""Reads all the books from the Flask API, 10 books at a time.

Usage: python3 client.py [BASE_URL]
Example: python3 client.py https://your-codio-url-5000.codio.io
"""
import json
import sys
import urllib.request

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
LIMIT = 10


def fetch_page(page):
    url = f"{BASE_URL}/api/books?page={page}&limit={LIMIT}"
    with urllib.request.urlopen(url) as response:
        total = int(response.headers.get("X-Total-Count", 0))
        return json.load(response), total


def main():
    all_books = []
    page = 1
    while True:
        books, total = fetch_page(page)
        all_books.extend(books)
        print(f"Page {page}: got {len(books)} books ({len(all_books)}/{total})")
        if not books or len(all_books) >= total:
            break
        page += 1

    print(f"Done. Read {len(all_books)} books.")


if __name__ == "__main__":
    main()
