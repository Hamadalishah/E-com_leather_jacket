from fastapi import FastAPI
from .database.db import create_table
from contextlib import asynccontextmanager
from .rout import product_rout,imag_rout
from .review_routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from .search.search_rout import router3

@asynccontextmanager
async def lifespan(app: FastAPI):
    # print(f"connection_string: {connection_string}")
    print("Table created")
    create_table()
    print("Table created successfully")
    yield
    print("Application shutdown")
    


app = FastAPI(lifespan=lifespan)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_rout.router)
app.include_router(imag_rout.router)
app.include_router(router)
app.include_router(router3)

@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}

