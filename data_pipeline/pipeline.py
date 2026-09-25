import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
MIN_BOOKS = 60
MIN_CATEGORIES = 3


# ============================================================
# TASK 1 — SCRAPING
# ============================================================

def get_soup(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_category_links():
    soup = get_soup(BASE_URL)

    categories = {}

    for link in soup.select("div.side_categories ul li ul li a"):
        category_name = link.get_text(strip=True)
        category_url = urljoin(
            BASE_URL,
            link.get("href")
        )

        categories[category_name] = category_url

    return categories


def scrape_category(category_name, category_url):
    books = []
    current_url = category_url

    while current_url:

        soup = get_soup(current_url)

        for article in soup.select("article.product_pod"):

            # Title
            title = article.h3.a.get(
                "title",
                ""
            ).strip()

            # Price
            price_element = article.select_one(
                ".price_color"
            )

            price = (
                price_element.get_text(strip=True)
                if price_element
                else ""
            )

            # Star rating
            rating_element = article.select_one(
                "p.star-rating"
            )

            if rating_element:

                rating_classes = rating_element.get(
                    "class",
                    []
                )

                star_rating = next(
                    (
                        class_name
                        for class_name in rating_classes
                        if class_name in [
                            "One",
                            "Two",
                            "Three",
                            "Four",
                            "Five"
                        ]
                    ),
                    ""
                )

            else:
                star_rating = ""

            # Availability
            availability_element = article.select_one(
                ".availability"
            )

            availability = (
                availability_element.get_text(
                    " ",
                    strip=True
                )
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

        # Next page
        next_link = soup.select_one(
            "li.next a"
        )

        if next_link:
            current_url = urljoin(
                current_url,
                next_link.get("href")
            )
        else:
            current_url = None

    return books


def scrape_books():

    categories = get_category_links()

    print(
        f"Found {len(categories)} categories."
    )

    all_books = []
    categories_scraped = 0

    for category_name, category_url in categories.items():

        print(
            f"Scraping category: {category_name}"
        )

        category_books = scrape_category(
            category_name,
            category_url
        )

        all_books.extend(category_books)
        categories_scraped += 1

        print(
            f"  Books found: {len(category_books)}"
        )

        print(
            f"  Total books collected: "
            f"{len(all_books)}"
        )

        # Make sure BOTH requirements are met
        if (
            len(all_books) >= MIN_BOOKS
            and categories_scraped >= MIN_CATEGORIES
        ):
            break

    return pd.DataFrame(all_books)


# ============================================================
# TASK 2 — DATA CLEANING
# ============================================================

def clean_data(df):

    df = df.copy()

    # --------------------------------------------------------
    # 1. Price
    # price → price_gbp (float)
    # --------------------------------------------------------

    df["price_gbp"] = (
        df["price"]
        .str.replace("£", "", regex=False)
        .str.replace("Â", "", regex=False)
        .str.strip()
    )

    df["price_gbp"] = pd.to_numeric(
        df["price_gbp"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # 2. Star rating
    # One → 1
    # Two → 2
    # Three → 3
    # Four → 4
    # Five → 5
    # --------------------------------------------------------

    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["star_rating"].map(
        rating_mapping
    )

    # --------------------------------------------------------
    # 3. Availability
    # "In stock" → True
    # anything else → False
    # --------------------------------------------------------

    df["in_stock"] = (
        df["availability"]
        .str.contains(
            "In stock",
            case=False,
            na=False
        )
    )

    # --------------------------------------------------------
    # 4. Handle numeric parsing failures
    # --------------------------------------------------------

    # Price failure → median price
    if df["price_gbp"].isna().any():

        median_price = df["price_gbp"].median()

        df["price_gbp"] = df["price_gbp"].fillna(
            median_price
        )

    # Rating failure → median rating
    if df["rating"].isna().any():

        median_rating = df["rating"].median()

        df["rating"] = df["rating"].fillna(
            median_rating
        )

    # Rating should be an integer
    df["rating"] = (
        df["rating"]
        .round()
        .astype(int)
    )

    return df


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # -------------------------
    # Task 1 — Scrape
    # -------------------------

    raw_df = scrape_books()

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    print(
        f"Total books scraped: {len(raw_df)}"
    )

    print(
        f"Categories scraped: "
        f"{raw_df['category'].nunique()}"
    )

    # -------------------------
    # Task 2 — Clean
    # -------------------------

    cleaned_df = clean_data(raw_df)

    print("\n" + "=" * 60)
    print("TASK 2 - CLEANING COMPLETE")
    print("=" * 60)

    print("\nFirst 10 cleaned records:")

    print(
        cleaned_df[
            [
                "title",
                "price_gbp",
                "rating",
                "in_stock",
                "category"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    # -------------------------
    # Data types
    # -------------------------

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)

    print(
        cleaned_df[
            [
                "price_gbp",
                "rating",
                "in_stock"
            ]
        ].dtypes
    )

    # -------------------------
    # Missing values
    # -------------------------

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print(
        cleaned_df[
            [
                "price_gbp",
                "rating",
                "in_stock"
            ]
        ].isnull().sum()
    )