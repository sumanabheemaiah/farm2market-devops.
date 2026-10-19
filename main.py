
from fastapi import FastAPI

app = FastAPI(title="Farm2Market Inventory API")


@app.get("/")
def home():
    return {"message": "Farm2Market API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    return {
        "products": [
            {"id": 1, "name": "Tomatoes", "quantity": 100},
            {"id": 2, "name": "Potatoes", "quantity": 75},
        ]
    }
