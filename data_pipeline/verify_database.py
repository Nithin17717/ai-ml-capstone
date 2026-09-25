import sqlite3
import pandas as pd

connection = sqlite3.connect("books.db")

print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

# Check tables
tables = pd.read_sql("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""", connection)

print("\nTables:")
print(tables)

# Check category count
category_count = pd.read_sql("""
    SELECT COUNT(*) AS category_count
    FROM categories
""", connection)

print("\nCategory count:")
print(category_count)

# Check book count
book_count = pd.read_sql("""
    SELECT COUNT(*) AS book_count
    FROM books
""", connection)

print("\nBook count:")
print(book_count)

# Test JOIN
join_result = pd.read_sql("""
    SELECT
        b.book_id,
        b.title,
        b.price_gbp,
        b.price_inr,
        b.rating,
        b.in_stock,
        c.category_name
    FROM books b
    JOIN categories c
        ON b.category_id = c.category_id
    LIMIT 10
""", connection)

print("\nJOIN result:")
print(join_result.to_string(index=False))

connection.close()