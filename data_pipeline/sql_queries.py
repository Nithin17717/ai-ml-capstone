import sqlite3
import pandas as pd


DATABASE = "books.db"


# Connect to SQLite database
connection = sqlite3.connect(DATABASE)


queries = {

    "Query 1 - WHERE":
    """
    SELECT
        title,
        price_gbp,
        rating,
        in_stock
    FROM books
    WHERE rating >= 4;
    """,

    "Query 2 - ORDER BY":
    """
    SELECT
        title,
        price_gbp,
        price_inr
    FROM books
    ORDER BY price_inr DESC;
    """,

    "Query 3 - LIMIT":
    """
    SELECT
        title,
        price_gbp,
        rating
    FROM books
    ORDER BY price_gbp DESC
    LIMIT 10;
    """,

    "Query 4 - DISTINCT":
    """
    SELECT DISTINCT
        rating
    FROM books
    ORDER BY rating;
    """,

    "Query 5 - BETWEEN":
    """
    SELECT
        title,
        price_gbp,
        price_inr
    FROM books
    WHERE price_gbp BETWEEN 20 AND 40
    ORDER BY price_gbp;
    """,

    "Query 6 - JOIN":
    """
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
}


# Store all query results
output_file = "sql_query_outputs.md"

with open(output_file, "w", encoding="utf-8") as output:

    output.write("# SQL Query Results\n\n")

    for query_name, query in queries.items():

        print("\n" + "=" * 70)
        print(query_name)
        print("=" * 70)

        print("\nSQL:")
        print(query.strip())

        # Execute query using pandas
        result = pd.read_sql(query, connection)

        print("\nOutput:")
        print(result.to_string(index=False))

        # Save query and output
        output.write(f"## {query_name}\n\n")

        output.write("### SQL Query\n\n")
        output.write("```sql\n")
        output.write(query.strip())
        output.write("\n```\n\n")

        output.write("### Output\n\n")
        output.write("```\n")
        output.write(result.to_string(index=False))
        output.write("\n```\n\n")


connection.close()

print("TASK 5 COMPLETE")
print(f"SQL queries executed: {len(queries)}")
print(f"Queries and outputs saved to: {output_file}")