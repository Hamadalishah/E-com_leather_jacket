from typing import Optional
from sqlmodel import SQLModel,create_engine, Session
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

connection_string:Optional[str] = os.getenv('DATABASE_URL')
if not connection_string:
    raise ValueError("DATABASE_URL environment variable not set")


connection = str(connection_string).replace(
    "postgresql", "postgresql+psycopg2"
)
engine = create_engine(connection,connect_args={"sslmode":"require"},pool_recycle=300,pool_size=10,echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session


    
    