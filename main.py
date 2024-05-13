from uuid import uuid4
from pydantic import BaseModel

from fastapi import FastAPI

from pymongo import MongoClient

app = FastAPI(
    title='Car API',
    description='Car API with FastAPI and MongoDB',
)


class Car(BaseModel):
    brand: str
    model: str
    color: str

    year: int
    type: str

    image: str
    stock: int

    price: int
    discount: int


client = MongoClient('mongodb://localhost:27017/')
db = client['current']['car']


# car crud

@app.post('/car', description="Create a new car")
async def create_car(car: Car):
    db.insert_one({
        '_id': str(uuid4()),

        'brand': car.brand,
        'model': car.model,
        'color': car.color,

        'year': car.year,
        'type': car.type,

        'image': car.image,
        'stock': car.stock,

        'price': car.price,
        'discount': car.discount
    })

    return {'message': 'created'}, 200


@app.get('/car/{_id}')
async def read_car(_id: str):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    return document, 200


@app.put('/car/{_id}')
async def update_car(_id: str, car: Car):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    db.update_one({'_id': _id}, {
        '$set': {
            'brand': car.brand,
            'model': car.model,
            'color': car.color,

            'year': car.year,
            'type': car.type,

            'image': car.image,
            'stock': car.stock,

            'price': car.price,
            'discount': car.discount
        }
    })

    return {'message': 'updated'}, 200


@app.delete('/car/{_id}')
async def delete_car(_id):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    db.delete_one({'_id': _id})

    return {'message': 'deleted'}, 200


# car search


@app.get('/car/')
async def read_car():
    cars = list(db.find())

    if not cars:
        return {'message': 'cars not found'}, 404

    return cars, 200
