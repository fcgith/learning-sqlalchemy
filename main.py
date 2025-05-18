import uvicorn
from fastapi import FastAPI
from app.routers import auth, categories, reviews
from app.routers import users
from app.routers import products
from app.infrastructure.database import Base, engine
import app.models.init

Base.metadata.create_all(bind=engine)

app = FastAPI(prefix="/api")
app.include_router(auth.router, tags=["auth"], prefix="/auth")
app.include_router(users.router, tags=["users"], prefix="/users")
app.include_router(categories.router, tags=["categories"], prefix="/categories")
app.include_router(products.router, tags=["products"], prefix="/products")
app.include_router(reviews.router, tags=["reviews"], prefix="/reviews")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)
