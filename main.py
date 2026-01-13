from fastapi import FastAPI, Depends
from models import Product
from database import session
import database_models
from database import engine
from sqlalchemy.orm import Session
app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to Orion Innovation"


products=[
    Product(id=1,name="Asus",price=999.9,description="Normal Laptop",quantity=10),
    Product(id=2, name="Nvidia", price=899.9, description="Gaming Laptop", quantity=23),
    Product(id=3, name="Lenovo", price=239.9, description="Business Laptop", quantity=6),
    Product(id=4, name="Dell", price=76.9, description="Budget Laptop", quantity=5),
    Product(id=5, name="Hp", price=249.9, description="Work Laptop", quantity=7),

]
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()
init_db()

@app.get("/products")

def show_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).all()


    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "Product not found"


@app.post("/product")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    products.append(product)
    return product

@app.put("/product")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.price=product.price
        db_product.description=product.description
        db_product.quantity=product.quantity
        db.commit()
        return "Product Updated"
    return "Product not found"

@app.delete("/product")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"

    else:
        return "Product not found"
#
# from fastapi.middleware.cors import CORSMiddleware
#
# app = FastAPI()
#
# # Add this CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


