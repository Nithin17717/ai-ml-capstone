# AI/ML Capstone Project

A three-module AI/ML capstone covering data engineering, exploratory
data analysis, machine learning, and a small GenAI/RAG support
assistant.

## Project Overview

The project is divided into three modules:

## Module 1 – Data Pipeline (data_pipeline/)
Web scraping
Data cleaning
Data enrichment
SQLite database
SQL queries
Pandas validation

## Module 2 – Analytics (analytics/)
Titanic dataset EDA
Data preprocessing
Classification
Imbalanced data handling
Hyperparameter tuning
Regression
Model persistence

## Module 3 – Support Assistant (support_assistant/)
Text embeddings
ChromaDB vector retrieval
LangGraph workflow
Pydantic validation
FastAPI API
Docker containerization



## Project Structure

``` text
A:\Project
├── data_pipeline/
│   ├── pipeline.py
│   ├── verify_database.py
│   ├── sql_queries.py
│   ├── pandas_validation.py
│   ├── sql_query_outputs.md
│   ├── pandas_validation_output.md
│   ├── README.md
│   └── books.db
├── analytics/
│   ├── eda.py
│   ├── modeling.py
│   ├── titanic.csv
│   ├── charts/
│   ├── model/
│   │   └── titanic_survival_pipeline.joblib
│   ├── task5_interpretations.md
│   └── README.md
├── support_assistant/
│   ├── docs/
│   │   ├── doc_01.txt ... doc_08.txt
│   ├── ingestion.py
│   ├── prompt.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── chroma_db/
│   └── README.md
├── .gitignore
└── README.md
```

## Environment Setup

Create and activate the Python environment:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Module 3 requirements:

``` text
chromadb
sentence-transformers
langgraph
fastapi
uvicorn
pydantic
```

Install them with:

``` powershell
pip install -r requirements.txt
```



# Module 1 --- Data Pipeline

## Objective

Module 1 builds a complete data pipeline using live product data from
`https://books.toscrape.com/`.

The pipeline:

1.  Scrapes book data using Requests and BeautifulSoup.
2.  Cleans and normalizes the data.
3.  Converts GBP prices to INR.
4.  Stores the result in a normalized SQLite database.
5.  Executes SQL queries.
6.  Reproduces SQL analysis using pandas.

## Pipeline

``` text
Books to Scrape
       ↓
Requests + BeautifulSoup
       ↓
Raw scraped data
       ↓
Cleaning and normalization
       ↓
GBP → INR enrichment
       ↓
SQLite normalized database
       ↓
SQL queries
       ↓
Pandas validation
```

## Final Dataset

The pipeline produced:

-   69 books
-   3 categories
-   Travel
-   Mystery
-   Historical Fiction

Exchange rate used:

``` text
1 GBP = 105.50 INR
```

The cleaned data includes `price_gbp`, `price_inr`, `rating`, and
`in_stock`.

## Database

Normalized SQLite tables:

### `categories`

``` text
category_id
category_name
```

### `books`

``` text
book_id
title
price_gbp
price_inr
rating
in_stock
category_id
```

`category_id` connects books to categories.

## SQL Analysis

The SQL implementation demonstrates:

-   WHERE
-   ORDER BY
-   LIMIT
-   DISTINCT
-   BETWEEN
-   JOIN

Results are saved in `data_pipeline/sql_query_outputs.md`.

## Pandas Validation

The pandas implementation uses `pd.read_sql()` and `pd.merge()`.

The SQL JOIN and pandas merge results matched:

``` text
Are SQL JOIN and pandas.merge() results equal? True
```

## Running Module 1

``` powershell
cd data_pipeline
python pipeline.py
python verify_database.py
python sql_queries.py
python pandas_validation.py
```



# Module 2 --- Titanic EDA and Machine Learning

## Objective

Module 2 performs exploratory data analysis and machine learning using
the Titanic dataset.

The workflow covers:

-   dataset loading
-   missing-value analysis
-   cleaning
-   outlier analysis
-   distributions
-   survival analysis
-   correlation
-   preprocessing
-   classification
-   class imbalance
-   hyperparameter tuning
-   regression
-   model persistence

## Dataset Cleaning

Original dataset:

``` text
891 rows × 15 columns
```

Final cleaned dataset:

``` text
889 rows × 14 columns
```

Missing-value rules:

-   Less than 5%: drop affected rows
-   5--30%: impute
-   More than 30%: drop the column

Results:

-   2 rows removed for `embarked`/`embark_town`
-   `age` imputed with the median
-   `deck` dropped because approximately 77.22% was missing
-   final dataset has no missing values

## Outlier Analysis

Age:

``` text
Q1 = 22
Q3 = 35
IQR = 13
Lower bound = 2.5
Upper bound = 54.5
Outliers = 65
```

Fare:

``` text
Q1 = 7.9
Q3 = 31
IQR = 23.1
Lower bound = -26.76
Upper bound = 65.66
Outliers = 114
```

Fare showed a right-skewed distribution.

## Correlation

Strongest absolute off-diagonal correlations:

``` text
pclass ↔ fare = -0.548
sibsp ↔ parch =  0.415
```

## Classification

Features:

``` text
pclass, sex, age, sibsp, parch, fare, embarked
```

Target:

``` text
survived
```

Class distribution:

``` text
Class 0: 549 (61.75%)
Class 1: 340 (38.25%)
```

Stratified split:

``` text
Training: 711
Testing: 178
```

Preprocessing used a `ColumnTransformer` with median imputation and
scaling for numeric features, and most-frequent imputation plus one-hot
encoding for categorical features.

## Classification Results

### Logistic Regression

``` text
Accuracy  = 0.8090
Precision = 0.7833
Recall    = 0.6912
F1        = 0.7344
AUC       = 0.8610
```

### Decision Tree

``` text
Accuracy  = 0.7640
Precision = 0.7600
Recall    = 0.5588
F1        = 0.6441
AUC       = 0.8374
```

### Random Forest

``` text
Accuracy  = 0.8202
Precision = 0.7812
Recall    = 0.7353
F1        = 0.7576
AUC       = 0.8179
```

## Class Imbalance

Class-weight balancing:

``` text
Precision = 0.7183
Recall    = 0.7500
F1        = 0.7338
```

SMOTE was applied only to the training data:

``` text
Class 0 = 439
Class 1 = 439
```

SMOTE results:

``` text
Precision = 0.7353
Recall    = 0.7353
F1        = 0.7353
```

## Random Forest Grid Search

Parameters searched:

``` text
n_estimators = [100, 200]
max_depth = [None, 5, 10]
max_features = ["sqrt", "log2"]
cv = 5
scoring = f1
```

Best parameters:

``` text
max_depth = 5
max_features = sqrt
n_estimators = 200
```

Best CV F1:

``` text
0.7408
```

Tuned test results:

``` text
Accuracy  = 0.8315
Precision = 0.8654
Recall    = 0.6618
F1        = 0.7500
```

## Regression

Linear regression predicted `fare` from:

``` text
survived, pclass, sex, age, sibsp, parch, embarked
```

Results:

``` text
MAE          = 21.0986
RMSE         = 41.7021
R²           = 0.3482
Adjusted R²  = 0.3091
```

Residual analysis showed a maximum-to-minimum residual standard
deviation ratio of approximately 8.48.

## Saved Model

Saved pipeline:

``` text
analytics/model/titanic_survival_pipeline.joblib
```

The persisted pipeline contains preprocessing and the classifier as one
combined object.

Test raw input:

``` text
pclass=3
sex=female
age=25
sibsp=0
parch=0
fare=15.0
embarked=S
```

Test result:

``` text
Prediction = 1
Survival probability = 0.6100
```

## Running Module 2

``` powershell
cd analytics
python eda.py
python modeling.py
```



# Module 3 --- Zepto Support Assistant

## Objective

Module 3 implements a small GenAI-style Zepto policy support assistant.

The graded baseline is fully offline and deterministic.

Components:

-   Sentence Transformers
-   `all-MiniLM-L6-v2`
-   ChromaDB
-   LangGraph
-   Pydantic
-   FastAPI

Default:

``` text
MOCK_LLM=1
```

No external LLM call is made in this mode.

## Architecture

``` text
User Query
    ↓
FastAPI POST /ask
    ↓
classify_intent
    ↓
┌───────────────────┴──────────────────┐
│                                      │
policy_question                  general_question
│                                      │
↓                                      ↓
retrieve_and_answer                direct_answer
│                                      │
↓                                      ↓
ChromaDB                         fixed mock answer
│
↓
Top 3 policy chunks
│
↓
Pydantic validation
│
↓
JSON response
```

## Corpus

The assistant contains 8 policy documents:

``` text
doc_01.txt
doc_02.txt
doc_03.txt
doc_04.txt
doc_05.txt
doc_06.txt
doc_07.txt
doc_08.txt
```

They are embedded with:

``` text
all-MiniLM-L6-v2
```

and stored in:

``` text
chroma_db/
```

Collection:

``` text
zepto_policies
```

The collection contains all 8 documents.

## Ingestion

``` powershell
cd support_assistant
python ingestion.py
```

The ingestion process loads the 8 documents, creates chunks, generates
384-dimensional embeddings, stores them in ChromaDB, verifies the
collection, and runs a sample retrieval.

## Retrieval

Policy questions retrieve the top 3 documents using cosine similarity.

Test query:

``` text
How much does priority delivery cost?
```

Retrieved documents:

``` text
doc_01
doc_05
doc_03
```

Mock answer format:

``` text
Based on the retrieved context: <top retrieved chunk>
```

## Structured Prompt

`prompt.py` contains:

``` text
ROLE
CONTEXT
TASK
FORMAT
LENGTH
NEGATIVE CONSTRAINT
FEW-SHOT EXAMPLE
```

Run:

``` powershell
python prompt.py
```

## LangGraph

Three named nodes are implemented:

``` text
classify_intent
retrieve_and_answer
direct_answer
```

The graph starts at `classify_intent` and conditionally routes to the
retrieval or direct-answer node.

## Intent Classification

Mock mode treats a query as a policy question when it contains:

``` text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

Otherwise it is a general question.

## General Questions

Mock response:

``` text
I can only answer questions about Zepto policies right now.
```

Sources:

``` json
[]
```

## Pydantic Schema

Response:

``` json
{
  "answer": "string",
  "sources": ["string"],
  "confidence": 1.0
}
```

`confidence` is constrained to 0--1.

The mock path uses deterministic validation with confidence `1.0`.

The optional real-LLM path retries schema validation up to three total
attempts. After a validation failure, a corrective instruction requires
valid JSON with `answer`, `sources`, and `confidence`. After all
attempts fail, a clearly marked error response is returned.

## FastAPI

Start locally:

``` powershell
uvicorn main:app --host 0.0.0.0 --port 7860
```

Endpoint:

``` text
POST /ask
```

Request:

``` json
{
  "query": "How much does priority delivery cost?"
}
```

Example response:

``` json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials...",
  "sources": ["doc_01", "doc_05", "doc_03"],
  "confidence": 1.0
}
```

General-question request:

``` json
{
  "query": "What is the capital of France?"
}
```

Response:

``` json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Local Verification

``` powershell
python main.py
```

The application successfully verified both a policy query and an
unrelated general query in deterministic mock mode.

## Docker

The service includes a Dockerfile.

Build:

``` powershell
docker build -t zepto-support-assistant .
```

Run:

``` powershell
docker run --rm -p 7860:7860 zepto-support-assistant
```

The container is configured for:

``` text
0.0.0.0:7860
```

### Docker Build Note

Docker Desktop was tested locally. The build successfully reached
dependency installation, project copying, and the ChromaDB ingestion
stage. The final image export took an unusually long time in the local
Docker Desktop environment.

The local Python/FastAPI application was successfully verified
independently.



# Git

A feature branch was used:

``` text
feature/module-1
```

The project was developed with multiple commits and is intended to be
merged into `main`.

Example final commands:

``` powershell
git status
git add .
git commit -m "Complete AI ML capstone project"
git checkout main
git merge feature/module-1
git push origin main
```

# Verification Summary

## Module 1

``` text
69 books
3 categories
SQLite normalized database
SQL queries
Pandas validation
SQL JOIN == pandas.merge() → True
```

## Module 2

``` text
Titanic EDA
Missing-value handling
Outlier analysis
Correlation analysis
Logistic Regression
Decision Tree
Random Forest
Class imbalance analysis
SMOTE
GridSearchCV
Linear Regression
Residual analysis
Persisted ML pipeline
```

## Module 3

``` text
8 corpus documents
all-MiniLM-L6-v2 embeddings
ChromaDB
Top-3 cosine retrieval
Structured prompt
3 LangGraph nodes
Conditional routing
TypedDict state
Pydantic validation
Deterministic MOCK_LLM mode
FastAPI POST /ask
Optional real-LLM validation retries
Dockerfile
```

# Default Module 3 Mode

Use:

``` powershell
$env:MOCK_LLM="1"
```

This mode is deterministic, offline, reproducible, and does not require
an external LLM API.

The optional real-LLM path can be enabled with:

``` powershell
$env:MOCK_LLM="0"
```

and requires the configured LLM API credentials.

# End-to-End Flow

``` text
Web Data
   ↓
Data Cleaning
   ↓
SQL / Pandas
   ↓
EDA
   ↓
Machine Learning
   ↓
Model Evaluation
   ↓
Model Persistence
   ↓
Embeddings
   ↓
Vector Retrieval
   ↓
LangGraph
   ↓
Pydantic Validation
   ↓
FastAPI
   ↓
Docker
```

This capstone demonstrates an end-to-end progression from data
engineering and analytics through classical machine learning and a
deterministic retrieval-based support assistant.
