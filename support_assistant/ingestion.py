import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


# TASK 1 - DOCUMENT INGESTION, EMBEDDING AND CHROMADB

print("MODULE 3 - TASK 1")
print("DOCUMENT INGESTION + EMBEDDINGS + CHROMADB")


# 1. PATHS

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"


# 2. LOAD ALL DOCUMENTS

documents = []
document_ids = []
metadatas = []

for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):
    text = file_path.read_text(encoding="utf-8").strip()

    documents.append(text)
    document_ids.append(file_path.stem)

    metadatas.append({
        "source": file_path.name
    })

print(f"\nDocuments loaded: {len(documents)}")

for doc_id in document_ids:
    print(f"  - {doc_id}")


# 3. SIMPLE CHUNKING

# Each document is short enough to use as one chunk.
chunks = documents
chunk_ids = document_ids

print(f"\nChunks created: {len(chunks)}")


# 4. LOAD EMBEDDING MODEL

print("\nLoading embedding model:")
print("all-MiniLM-L6-v2")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully.")


# 5. GENERATE EMBEDDINGS

print("\nGenerating embeddings...")

embeddings = embedding_model.encode(
    chunks,
    show_progress_bar=True
)

print("Embeddings generated successfully.")
print(f"Embedding shape: {embeddings.shape}")


# 6. CREATE CHROMADB CLIENT

print("\nCreating ChromaDB database...")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# 7. CREATE / RESET COLLECTION

collection_name = "zepto_policies"

try:
    chroma_client.delete_collection(
        name=collection_name
    )
    print("Existing collection removed.")
except Exception:
    pass

collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={
        "hnsw:space": "cosine",
        "description": "Zepto support policy documents"
    }
)


# 8. STORE CHUNKS + EMBEDDINGS

collection.add(
    ids=chunk_ids,
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\nDocuments stored in ChromaDB.")


# 9. VERIFY COLLECTION

stored_data = collection.get()

print("\nCHROMADB VERIFICATION")

print(
    f"Collection name: {collection.name}"
)

print(
    f"Stored documents/chunks: "
    f"{len(stored_data['ids'])}"
)

print("\nStored IDs:")

for stored_id in stored_data["ids"]:
    print(f"  - {stored_id}")


# 10. TEST QUERY

test_query = "How much does priority delivery cost?"

print("\nTEST QUERY")
print(test_query)

query_embedding = embedding_model.encode(
    [test_query]
)

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)

print("\nTOP 3 RETRIEVED CHUNKS")

for i, (doc_id, document) in enumerate(
    zip(
        results["ids"][0],
        results["documents"][0]
    ),
    start=1
):
    print(f"\n{i}. {doc_id}")
    print(document[:200] + "...")


# 11. FINAL VERIFICATION

assert len(documents) == 8
assert len(embeddings) == 8
assert len(stored_data["ids"]) == 8

print("TASK 1 COMPLETE")

print("✓ All 8 documents loaded")
print("✓ 8 chunks created")
print("✓ all-MiniLM-L6-v2 embeddings generated")
print("✓ Embeddings stored in ChromaDB")
print("✓ ChromaDB contains all 8 documents")
print("✓ Test retrieval completed")