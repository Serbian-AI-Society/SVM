from langchain.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from .config import INDEX_NAME, INDEX_SCHEMA, REDIS_URL


# Make this look better in the docs.
class Question(BaseModel):
    __root__: str


def init_chain() -> RunnableParallel:
    # Init Embeddings
    # embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    embedder = OpenAIEmbeddings()

    # Connect to pre-loaded vectorstore
    # run the ingest.py script to populate this
    vectorstore = Redis.from_existing_index(
        embedding=embedder, index_name=INDEX_NAME, schema=INDEX_SCHEMA, redis_url=REDIS_URL
    )
    # TODO allow user to change parameters
    retriever = vectorstore.as_retriever(search_type="mmr")

    # Define our prompt
    template = """
    Use the following pieces of context from the stort about the rabbit
    to answer the question. Do not make up an answer if there is no
    context provided to help answer it. Include the 'source' and 'start_index'
    from the metadata included in the context you used to answer the question

    Context:
    ---------
    {context}

    ---------
    Question: {question}
    ---------

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    # RAG Chain
    model = ChatOpenAI(model_name="gpt-4o")
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | model
        | StrOutputParser()
    ).with_types(input_type=Question)

    return chain


def get_completion_from_messages(chain: RunnableParallel, user_message: str) -> str:
    return chain.invoke(user_message)
