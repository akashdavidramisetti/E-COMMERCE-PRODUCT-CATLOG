from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql # type: ignore

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Akashdavid@143",
        database="ecommerce"
    )

# Models for response data
class Product(BaseModel):
    ProductName: str
    Price: float
    CategoryName: str
    StockQuantity: int

# Get all products
@app.get("/products", response_model=list[Product])
async def get_products():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor for dictionary-like rows
    cursor.execute("""
        SELECT Products.ProductName, Products.Price, Categories.CategoryName, Products.StockQuantity
        FROM Products
        JOIN Categories ON Products.CategoryID = Categories.CategoryID
    """)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

# Search products by category
@app.get("/products/search/{category}", response_model=list[Product])
async def search_products_by_category(category: str):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = """
        SELECT Products.ProductName, Products.Price, Categories.CategoryName, Products.StockQuantity
        FROM Products
        JOIN Categories ON Products.CategoryID = Categories.CategoryID
        WHERE Categories.CategoryName = %s
    """
    cursor.execute(query, (category,))
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

# Main entry point for running the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
