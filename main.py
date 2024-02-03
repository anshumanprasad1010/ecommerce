from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from model import OrderItem, Order, UserAddress
from datetime import datetime
from bson import ObjectId

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Welcome To Shopping World"}

# Connect to MongoDB using motor
client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/db")
db = client["db"]
products_collection = db.products
orders_collection = db["orders"]



#Pushing sample documents
@app.post("/products")
async def push_products():
    result = await products_collection.insert_many(#[{'name': 'Phone','price': 10000,'quantity': 1},{'name': 'Shirt','price': 200,'quantity': 4},{'name': 'Jeans','price': 400,'quantity': 3},] \
        )
    print(len(result.inserted_ids,))

    return "Inserted Records"


#List products
@app.get("/products")
async def list_products(
    limit: int = Query(10, description="Number of records per page", ge=1, le=100),
    offset: int = Query(0, description="Number of records to skip", ge=0),
    min_price: float = Query(None, description="Minimum price filter"),
    max_price: float = Query(None, description="Maximum price filter"),
):
    # MongoDB Aggregation Pipeline for filtering and pagination
    pipeline = [
        {
            "$facet": {
                "metadata": [
                    {"$count": "total"},
                    {"$addFields": {"limit": limit, "offset": offset}},
                ],
                "data": [
                    {"$skip": offset},
                    {"$limit": limit},
                    {"$project": {"_id":{f"$toString": "$_id"}, "name": 1, "price": 1, "quantity": 1}},
                ],
            }
        }
    ]
   
    # Apply price filters if provided
    if min_price is not None:
        pipeline[0]["$facet"]["data"].insert(0, {"$match": {"price": {"$gte": min_price}}})
    if max_price is not None:
        pipeline[0]["$facet"]["data"].insert(0, {"$match": {"price": {"$lte": max_price}}})
    
    result = await products_collection.aggregate(pipeline).to_list(1)
   
    # Prepare response
    response_data = {
        "data": result[0]['data'],
        "page": {
            "limit": result[0]["metadata"][0]["limit"],
            "nextOffset": offset + limit if offset + limit < result[0]["metadata"][0]["total"] else None,
            "prevOffset": offset - limit if offset - limit >= 0 else None,
            "total": result[0]["metadata"][0]["total"],
        },
    }

    return JSONResponse(content=response_data)



#Create Order
@app.post("/orders")
async def create_order(item: Order):

    its = item.items  
    total_price = 0
    user_list = []
    for it in its:
        user_list.append(it.model_dump())
        r = ObjectId(it.productId)
        res= await products_collection.find_one({'_id': r})
        total_price = total_price + res['price'] * it.boughtQuantity
    
    
    #Prepare order document
    order_data = {
        "createdOn": datetime.utcnow(),
        "items": user_list,
        "totalAmount": total_price,
        "userAddress": item.userAddress.model_dump(),
    }

    #Insert order into MongoDB using motor
    result = await orders_collection.insert_one(order_data)

    #Check if order is successfully inserted
    if result.inserted_id:
        return JSONResponse(content={"message": "Order created successfully"})
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
