import logging
import time

from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates
from llm import chain, ingest
from orm import crud, database, models
from orm.database import get_db
from orm.schemas import ChatRequest
from sqlalchemy.orm import Session

app = FastAPI()

templates = Jinja2Templates(directory="pages")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/db")
async def init_all(db: Session = Depends(get_db)):
    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    crud.create_users(db)

    users = db.query(models.User).all()
    return {"users": users}


@app.post("/chat")
async def chat(chat_request: ChatRequest):
    user_message = chat_request.query

    # try:
    rag_chain = chain.init_chain()

    start_time = time.time()
    completion = chain.get_completion_from_messages(rag_chain, user_message)
    end_time = time.time()
    time_taken = end_time - start_time

    logging.info(f"Time taken: {time_taken:.2f}")
    logging.info(completion)

    # except Exception as e:
    #     logging.error(e)
    #     return {"error": str(e)}

    return {
        "result": completion,
        "execution_time": time_taken,
    }


@app.get("/ingest")
async def ingest_docs():
    # try:
    ingest.ingest_documents()
    # except Exception as e:
    #     logging.error(e)
    #     return {"error": str(e)}

    return {"message": "Success"}
