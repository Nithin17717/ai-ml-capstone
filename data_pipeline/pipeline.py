import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"
MIN_BOOKS = 60
MIN_CATEGORIES = 3


def get_soup(url):
    """Fetch a URL and return its BeautifulSoup object."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_category_links():
    """Get category names and URLs from the website."""
    soup = get_soup(BASE_URL)

    categories = {}

    for link in soup.select("div.side_categories ul li ul li a"):
        category_name = link.get_text(strip=True)
        category_url = urljoin(BASE_URL, link.get("href"))

        categories[category_name] = category_url

    return categories


def scrape_category(category_name, category_url):
    """Scrape all books from one category, including pagination."""
    books = []
    current_url = category_url

    while current_url:
        soup = get_soup(current_url)

        for article in soup.select("article.product_pod"):
            title = article.h3.a.get("title", "").strip()

            price_element = article.select_one(".price_color")
            price = price_element.get_text(strip=True) if price_element else ""

            rating_element = article.select_one("p.star-rating")

            if rating_element:
                rating_classes = rating_element.get("class", [])
                star_rating = next(
                    (
                        class_name
                        for class_name in rating_classes
                        if class_name in ["One", "Two", "Three", "Four", "Five"]
                    ),
                    ""
                )
            else:
                star_rating = ""

            availability_element = article.select_one(".availability")
            availability = (
                availability_element.get_text(" ", strip=True)
                if availability_element
                else ""
            )

            books.append({
                "title": title,
                "price": price,
                "star_rating": star_rating,
                "availability": availability,
                "category": category_name
            })

        next_link = soup.select_one("li.next a")

        if next_link:
            current_url = urljoin(current_url, next_link.get("href"))
        else:
            current_url = None

    return books


def scrape_books():
    """Scrape enough categories to obtain at least 60 books."""
    categories = get_category_links()

    print(f"Found {len(categories)} categories.")

    all_books = []

    for category_name, category_url in categories.items():
        print(f"Scraping category: {category_name}")

        category_books = scrape_category(category_name, category_url)
        all_books.extend(category_books)

        print(f"  Books found: {len(category_books)}")
        print(f"  Total books collected: {len(all_books)}")

        if len(all_books) >= MIN_BOOKS:
            break

    df = pd.DataFrame(all_books)

    return df


if __name__ == "__main__":
    df = scrape_books()

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    print(f"Total books scraped: {len(df)}")
    print(f"Categories scraped: {df['category'].nunique()}")

    print("\nFirst 10 records:")
    print(df.head(10).to_string(index=False))

    print("\nBooks per category:")
    print(df["category"].value_counts())