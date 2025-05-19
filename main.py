import uvicorn
import app.models.__init__ as ini
from fastapi import FastAPI
from app.routers import auth, categories, reviews, discounts, orders
from app.routers import users
from app.routers import products
from app.routers.support import support
from app.infrastructure.database import Base, engine


print("=============== create_all() ===============")
Base.metadata.create_all(bind=engine)


app = FastAPI(prefix="/api")

app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(categories.router, tags=["Categories"], prefix="/categories")
app.include_router(products.router, tags=["Products"], prefix="/products")
app.include_router(reviews.router, tags=["Reviews"], prefix="/reviews")
app.include_router(discounts.router, tags=["Discounts"], prefix="/discounts")
app.include_router(orders.router, tags=["Orders"], prefix="/orders")
app.include_router(support.router, tags=["Support"], prefix="/support")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)
