from fastapi import FastAPI
from .database.db import create_table
from contextlib import asynccontextmanager
from .rout import product_rout,imag_rout
from .review_routes.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # print(f"connection_string: {connection_string}")
    print("Table created")
    create_table()
    print("Table created successfully")
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(product_rout.router)
app.include_router(imag_rout.router)
app.include_router(router)

@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}