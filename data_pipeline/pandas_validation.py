import sqlite3
import pandas as pd


DATABASE = "books.db"

# Connect to database
connection = sqlite3.connect(DATABASE)


print("=" * 70)
print("TASK 6 - PANDAS VALIDATION")
print("=" * 70)


# PART 1 — READ SQL RESULTS USING pd.read_sql()

print("\n1. Reading SQL results using pd.read_sql()")


# Query 1 - High-rated books
query_high_rated = """
SELECT
    title,
    price_gbp,
    rating
FROM books
WHERE rating >= 4
ORDER BY rating DESC;
"""

high_rated_df = pd.read_sql(
    query_high_rated,
    connection
)

print("\nHigh-rated books:")
print(high_rated_df.to_string(index=False))


# Query 2 - Books between £20 and £40
query_price_range = """
SELECT
    title,
    price_gbp,
    price_inr
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp;
"""

price_range_df = pd.read_sql(
    query_price_range,
    connection
)

print("\nBooks priced between £20 and £40:")
print(price_range_df.to_string(index=False))


# PART 2 — READ TABLES INTO DATAFRAMES


print("2. Loading tables into pandas")


books_df = pd.read_sql(
    "SELECT * FROM books",
    connection
)

categories_df = pd.read_sql(
    "SELECT * FROM categories",
    connection
)

print("\nBooks DataFrame:")
print(books_df.head().to_string(index=False))

print("\nCategories DataFrame:")
print(categories_df.to_string(index=False))


# PART 3 — REPRODUCE SQL JOIN USING pd.merge()


print("3. Reproducing SQL JOIN using pd.merge()")



pandas_join_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)


pandas_join_df = pandas_join_df[
    [
        "book_id",
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_name"
    ]
]


pandas_join_df = pandas_join_df.sort_values(
    by="price_gbp",
    ascending=False
).head(10)


print("\nPandas JOIN result:")
print(
    pandas_join_df.to_string(index=False)
)


# PART 4 — SQL JOIN FOR COMPARISON

sql_join_query = """
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
ORDER BY b.price_gbp DESC
LIMIT 10;
"""

sql_join_df = pd.read_sql(
    sql_join_query,
    connection
)


print("\nSQL JOIN result:")
print(
    sql_join_df.to_string(index=False)
)


# PART 5 — CHECK EQUIVALENCE


print("4. Checking SQL JOIN vs Pandas JOIN")



sql_join_df = sql_join_df.reset_index(drop=True)
pandas_join_df = pandas_join_df.reset_index(drop=True)


joins_are_equal = sql_join_df.equals(
    pandas_join_df
)


print(
    f"\nAre SQL JOIN and pandas.merge() results equal? "
    f"{joins_are_equal}"
)


if joins_are_equal:
    print(
        "SUCCESS: SQL JOIN and pandas.merge() "
        "produced equivalent results."
    )
else:
    print(
        "WARNING: SQL JOIN and pandas.merge() "
        "results are different."
    )


# SAVE OUTPUT

output_file = "pandas_validation_output.md"

with open(output_file, "w", encoding="utf-8") as output:

    output.write("# Task 6 - Pandas Validation\n\n")

    output.write("## 1. pd.read_sql() - High Rated Books\n\n")
    output.write("```text\n")
    output.write(
        high_rated_df.to_string(index=False)
    )
    output.write("\n```\n\n")

    output.write(
        "## 2. pd.read_sql() - Price Range\n\n"
    )
    output.write("```text\n")
    output.write(
        price_range_df.to_string(index=False)
    )
    output.write("\n```\n\n")

    output.write(
        "## 3. pandas.merge() JOIN Result\n\n"
    )
    output.write("```text\n")
    output.write(
        pandas_join_df.to_string(index=False)
    )
    output.write("\n```\n\n")

    output.write(
        "## 4. SQL JOIN Result\n\n"
    )
    output.write("```text\n")
    output.write(
        sql_join_df.to_string(index=False)
    )
    output.write("\n```\n\n")

    output.write(
        "## 5. Equivalence Check\n\n"
    )

    output.write(
        f"SQL JOIN equals pandas.merge(): "
        f"**{joins_are_equal}**\n"
    )


connection.close()


print("TASK 6 COMPLETE")

print(
    f"Validation output saved to: {output_file}"
)