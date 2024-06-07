import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

USER_NAME = os.getenv("DB_USER_NAME")
PASSWORD = os.getenv("DB_PASSWORD")
SERVER = os.getenv("DB_SERVER_NAME")
PORT = os.getenv("DB_PORT")
DATABASE_NAME = os.getenv("DB_DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_table_schema(table_name):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    return {column.name: str(column.type) for column in table.columns}
