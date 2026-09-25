"""
Module 3 - Tasks 3, 4 and 5
LangGraph + Pydantic + FastAPI Zepto Support Assistant.

Default behavior:
    MOCK_LLM=1

The default mock mode is fully deterministic and does not call
any external LLM.
"""

import json
import os
import urllib.request
from pathlib import Path
from typing import TypedDict
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END
from prompt import build_prompt


# CONFIGURATION

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

print("MODULE 3 - ZEPTO SUPPORT ASSISTANT")
print(f"MOCK_LLM = {MOCK_LLM}")


# PYDANTIC OUTPUT SCHEMA

class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


def call_real_llm(prompt_text: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is required when MOCK_LLM=0."
        )

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt_text,
            }
        ],
        "temperature": 0,
    }

    request = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    return data["choices"][0]["message"]["content"]


def generate_validated_response(
    prompt_text: str,
    sources: list[str],
) -> AskResponse:
    corrective_instruction = ""

    for attempt in range(1, 4):
        try:
            full_prompt = prompt_text

            if corrective_instruction:
                full_prompt += (
                    "\n\nCORRECTIVE INSTRUCTION:\n"
                    + corrective_instruction
                )

            raw_response = call_real_llm(full_prompt)
            cleaned_response = raw_response.strip()

            if cleaned_response.startswith("```"):
                cleaned_response = (
                    cleaned_response
                    .replace("```json", "", 1)
                    .replace("```", "")
                    .strip()
                )

            parsed_response = json.loads(cleaned_response)

            response = AskResponse.model_validate(
                parsed_response
            )

            return response

        except (
            json.JSONDecodeError,
            ValidationError,
            KeyError,
            TypeError,
        ) as error:

            print(
                f"\nLLM validation failed "
                f"(attempt {attempt}/3): {error}"
            )

            if attempt < 3:
                corrective_instruction = (
                    "Your previous response failed schema validation. "
                    "Return ONLY valid JSON with exactly these fields: "
                    '"answer" (string), '
                    '"sources" (array of strings), '
                    '"confidence" (number between 0 and 1). '
                    "Do not include markdown or additional fields."
                )

    return AskResponse(
        answer=(
            "[ERROR] LLM response failed Pydantic "
            "schema validation after 3 attempts."
        ),
        sources=sources,
        confidence=0.0,
    )


# LANGGRAPH STATE

class SupportState(TypedDict, total=False):
    query: str
    intent: str
    retrieved_documents: list[str]
    retrieved_ids: list[str]
    answer: str
    sources: list[str]
    confidence: float


# MODELS AND CHROMADB

print("\nLoading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")

print("\nConnecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name="zepto_policies"
)

print(f"Collection: {collection.name}")
print(f"Documents available: {collection.count()}")


# NODE 1 - CLASSIFY INTENT

POLICY_KEYWORDS = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
]


def classify_intent(state: SupportState) -> SupportState:
    query = state["query"]
    query_lower = query.lower()

    if MOCK_LLM:
        is_policy = any(
            keyword in query_lower
            for keyword in POLICY_KEYWORDS
        )

        intent = (
            "policy_question"
            if is_policy
            else "general_question"
        )

        print("\n[NODE] classify_intent")
        print(f"Query: {query}")
        print(f"Intent: {intent}")

        return {
            "intent": intent
        }

    raise NotImplementedError(
        "Real LLM classification is optional. "
        "Use MOCK_LLM=1 for the graded deterministic mode."
    )


# NODE 2 - RETRIEVE AND ANSWER

def retrieve_and_answer(state: SupportState) -> SupportState:
    query = state["query"]

    print("\n[NODE] retrieve_and_answer")
    print(f"Query: {query}")

    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_ids = results["ids"][0]
    retrieved_documents = results["documents"][0]

    print("\nTop 3 retrieved documents:")

    for i, (doc_id, document) in enumerate(
        zip(retrieved_ids, retrieved_documents),
        start=1,
    ):
        print(f"{i}. {doc_id}")
        print(f"   {document[:150]}...")

    context_parts = []

    for doc_id, document in zip(
        retrieved_ids,
        retrieved_documents,
    ):
        context_parts.append(
            f"[{doc_id}] {document}"
        )

    context = "\n\n".join(context_parts)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    if MOCK_LLM:
        top_chunk_snippet = retrieved_documents[0][:200]

        answer = (
            "Based on the retrieved context: "
            f"{top_chunk_snippet}"
        )

        response = AskResponse(
            answer=answer,
            sources=retrieved_ids,
            confidence=1.0,
        )

        print("\nMock validated response:")
        print(response.model_dump())

        return {
            "retrieved_documents": retrieved_documents,
            "retrieved_ids": retrieved_ids,
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
        }

    response = generate_validated_response(
        prompt_text=prompt,
        sources=retrieved_ids,
    )

    return {
        "retrieved_documents": retrieved_documents,
        "retrieved_ids": retrieved_ids,
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
    }


# NODE 3 - DIRECT ANSWER

def direct_answer(state: SupportState) -> SupportState:
    query = state["query"]

    print("\n[NODE] direct_answer")
    print(f"Query: {query}")

    if MOCK_LLM:
        answer = (
            "I can only answer questions about Zepto policies right now."
        )

        response = AskResponse(
            answer=answer,
            sources=[],
            confidence=1.0,
        )

        print("\nMock validated response:")
        print(response.model_dump())

        return {
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
        }

    prompt = build_prompt(
        query=query,
        context="",
    )

    response = generate_validated_response(
        prompt_text=prompt,
        sources=[],
    )

    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
    }


# CONDITIONAL ROUTING

def route_intent(state: SupportState) -> str:
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# BUILD LANGGRAPH

graph_builder = StateGraph(SupportState)

graph_builder.add_node(
    "classify_intent",
    classify_intent,
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer,
)

graph_builder.add_node(
    "direct_answer",
    direct_answer,
)

graph_builder.add_edge(
    START,
    "classify_intent",
)

graph_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

graph_builder.add_edge(
    "retrieve_and_answer",
    END,
)

graph_builder.add_edge(
    "direct_answer",
    END,
)

graph = graph_builder.compile()


# FASTAPI APPLICATION

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline deterministic Zepto policy support assistant",
    version="1.0.0",
)


@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(request: AskRequest) -> AskResponse:
    result = graph.invoke(
        {
            "query": request.query
        }
    )

    response = AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )

    return response


# LOCAL TESTS

def run_test(query: str) -> None:
    print(f"TEST QUERY: {query}")

    result = graph.invoke(
        {
            "query": query
        }
    )

    response = AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )

    print("\nFINAL VALIDATED RESULT")
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":

    print("\nRunning local graph tests...")

    run_test(
        "How much does priority delivery cost?"
    )

    run_test(
        "What is the capital of France?"
    )

    print("TASKS 3 + 4 + 5 APPLICATION READY")
    print("TypedDict state")
    print("3 LangGraph nodes")
    print("Conditional routing")
    print("ChromaDB top-3 retrieval")
    print("Deterministic MOCK_LLM mode")
    print("Pydantic output validation")
    print("FastAPI POST /ask")