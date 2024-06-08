from langchain.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough

from .config import INDEX_NAME, INDEX_SCHEMA, REDIS_URL


# Make this look better in the docs.
class Question(BaseModel):
    __root__: str


class PrintContext(Runnable):
    def invoke(self, input1, input2):
        print("Input1:", input1)
        print("Input2:", input2)
        return input1


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
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Define our prompt
    template = """
    Ti si korisni asistent koji zna mnogo o restoranima i može da preporučiš gde da se jede.
    Na osnovu ponudjenih restorana izaberi nekoliko koji najbolje odgovaraju korisnikovom upitu
    i koji su najbolje ocenjeni.
    Uvek prikazi sledece:
    ime restorana,
    ocenu i zvezdicu pored ocene,
    cenovni rang,
    google maps url,
    sazetak dostupnih jela,
    šta ljudi kažu o restoranu.
    Ako ne mozes da pronadjes restoran koji odgovara korisnikovom upitu, nemoj ga predlagati.
    Ako imas dovoljno predloga koji zadovoljavaju kriterijume, predlozi 5 restorana.
    Sortiraj restorane po oceni opadajuće.
    Uvek odgovaraj na srpskom jeziku.

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
    model = ChatOpenAI(
        model_name="gpt-4o", api_key="sk-proj-YbbqGIKc845hfvwMHOo3T3BlbkFJQxgvepamvTYPajdLhWW4"
    )
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        # | PrintContext()
        | prompt
        | model
        | StrOutputParser()
    ).with_types(input_type=Question)

    return chain


def get_completion_from_messages(chain: RunnableParallel, user_message: str) -> str:
    return chain.invoke(user_message)
