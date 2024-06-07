from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
from langchain_community.vectorstores import Redis

from .config import INDEX_NAME, INDEX_SCHEMA, REDIS_URL


def ingest_documents():
    print("Ingesting data...")

    loader = TextLoader(file_path="/app/llm/data/rabbit_story.txt")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
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
