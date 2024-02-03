Simple backend running ECommerce application using fastapi and mongodb


# Requirements

pip install fastapi motor uvicorn

# Running the server for development

uvicorn main:app --reload



# Sample products to add to collection 

This list is commented in 26th line of main.py

Uncomment and copy these sample data below before making POST request to ':/products' 

[{'name': 'Phone','price': 10000,'quantity': 1  }, {'name': 'Shirt','price': 200,'quantity': 4 }, {'name': 'Jeans','price': 400,'quantity': 3  },  {    name: 'Bottles',    price: 20,    quantity: 5  },  {    name: 'Pen',    price: 20,    quantity: 50  },]


# Sample document in orders collection

{
    _id: ObjectId(''),
    createdOn: ISODate("2024-02-03T04:01:05.501Z"),
    items: [
      { productId: '43gfdbdfbf..', boughtQuantity: 3 },
      { productId: '66gvdssdvd..', boughtQuantity: 1 }
    ],
    totalAmount: 70000,
    userAddress: { city: 'x', country: 'u', zipCode: '4001' }
}

productId used to fetch price of product from products collection



# API Calls

GET /products 


With Query Parameters  
/products?limit=3&offset=2&min_price=1000&max_price=10000


POST /orders

Request Body example schema
{
  "items": [
    {
      "productId": "string",
      "boughtQuantity": 0
    }
  ],
  "userAddress": {
    "city": "string",
    "country": "string",
    "zipCode": "string"
  }
}
