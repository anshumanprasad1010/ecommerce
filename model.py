from pydantic import BaseModel


class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zipCode: str

class Order(BaseModel):
    items: list[OrderItem]
    userAddress: UserAddress