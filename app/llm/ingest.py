import json

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Redis

from .config import INDEX_NAME, INDEX_SCHEMA, REDIS_URL

DATA_PATH = "/app/llm/data/selected_restaurants_broad_scope.json"


def get_price_level(price_level: int) -> str:
    if price_level == 1:
        return "$"
    elif price_level == 2:
        return "$$"
    elif price_level == 3:
        return "$$$"
    elif price_level == 4:
        return "$$$$"
    else:
        return ""


def ingest_documents():
    print("Ingesting data...")

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    # Create LangChain documents from DataFrame with metadata
    documents = []
    for idx, restaurant_info in enumerate(data):
        combined_string = (
            f"Google maps URL: https://www.google.com/maps/place/?q=place_id:{restaurant_info['place_id']}\n"
            f"Address: {restaurant_info['formatted_address']}\n"
            f"Name: {restaurant_info['name']}\n"
            f"Cenovni rang: {get_price_level(restaurant_info['price_level'])}\n"
            f"Rating: {restaurant_info['rating']}\n"
            f"Reviews: {restaurant_info['reviews']}\n"
            f"website_summary: {restaurant_info['website_summary']}\n"
            f"wolt_summary: {restaurant_info['wolt_summary']}\n"
        )
        metadata = {
            "Rating": restaurant_info["rating"],
            "Name": restaurant_info["name"],
        }
        documents.append(Document(page_content=combined_string, metadata=metadata))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
    chunks = text_splitter.split_documents(documents)
    print("Done preprocessing. Created", len(chunks), "chunks.")

    embedder = OpenAIEmbeddings()
    _ = Redis.from_texts(
        # appending this little bit can sometimes help with semantic retrieval
        # especially with multiple companies
        texts=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
        embedding=embedder,
        index_name=INDEX_NAME,
        index_schema=INDEX_SCHEMA,
        redis_url=REDIS_URL,
    )

    print("Done ingesting data.")


if __name__ == "__main__":
    ingest_documents()
