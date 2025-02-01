from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from .database.db import create_table, get_session
from contextlib import asynccontextmanager
from .rout import product_rout, imag_rout
from .review_routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from .search.search_rout import router3
from .scema.product_model import ProductRead
from .scema.schema import Product
from sqlalchemy.orm import selectinload
from typing import  List
from sqlmodel import Session, select, SQLModel
from sqlalchemy import func
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure uvicorn logger is also set to DEBUG
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Application startup")
    print("Table created")
    create_table()
    print("Table created successfully")
    yield
    logger.debug("Application shutdown")
    print("Application shutdown")
# Add this BEFORE creating FastAPI app
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "your-app": {"handlers": ["default"], "level": "DEBUG"},
    },
})

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



class ProductListResponse(SQLModel):
    products: List[ProductRead]
    totalCount: int

    class Config:
        from_attributes = True
#
# 
@app.get("/product", response_model=ProductListResponse)
def get_products(page: int = 1, per_page: int = 10, session: Session = Depends(get_session)):
    # Calculate the offset for pagination
    offset = (page - 1) * per_page
    
    # Statement to load products with images and reviews (pagination applied)
    statement = (
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.reviews))  # type: ignore
        .offset(offset)
        .limit(per_page)
    )
    
    # Execute the query and fetch products
    products = session.exec(statement).all()

    # Correct way to get the total count of products (use func.count)
    total_count = session.execute(select(func.count(Product.id))).scalar()  # type: ignore

    # Return the paginated products and total count
    return {"products": products, "totalCount": total_count}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

