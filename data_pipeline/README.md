# Module 1 - Data Pipeline

## Overview

This module implements an end-to-end data pipeline using data scraped from Books to Scrape.

The pipeline performs:

1. Web scraping using Requests and BeautifulSoup
2. Data cleaning using pandas
3. GBP to INR conversion
4. SQLite database creation
5. SQL querying
6. Pandas validation using `pd.read_sql()` and `pd.merge()`

The final dataset contains 69 books from 3 categories.

---

# 1. Project Structure

```text
data_pipeline/
│
├── pipeline.py
├── verify_database.py
├── sql_queries.py
├── sql_query_outputs.md
├── pandas_validation.py
├── pandas_validation_output.md
└── books.db