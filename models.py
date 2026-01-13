from pydantic import BaseModel

class Product(BaseModel):
    id:int
    name:str
    price:float
    description:str
    quantity:int

    # def __init__(self, id:int, name:str, price:float, description:str, quantity:int):
    #     self.id = id
    #     self.name = name
    #     self.price = price
    #     self.description = description
    #     self.quantity = quantity
