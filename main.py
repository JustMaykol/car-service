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
    description: str

    year: int
    type: str

    image: str
    stock: int

    price: int
    discount: int


client = MongoClient('mongodb://localhost:27017/')
db = client['current']['car']


# car crud

@app.post(
    '/car',
    description='Create a new car entry.',
    response_description='Confirmation message with the created car ID.'
)
async def create_car(car: Car):
    car_id = str(uuid4())

    db.insert_one({
        '_id': car_id,

        'brand': car.brand,
        'model': car.model,

        'color': car.color,
        'description': car.description,

        'year': car.year,
        'type': car.type,

        'image': car.image,
        'stock': car.stock,

        'price': car.price,
        'discount': car.discount
    })

    return {'message': f'created: {car_id}'}, 200


@app.get(
    '/car/{car_id}',
    description='Retrieve details of a specific car by its ID.',
    response_description='Details of the car if found, or a message indicating the car was not found.'
)
async def read_car(car_id: str):
    document = db.find_one({'_id': car_id})

    if not document:
        return {'message': f'car \'{car_id}\'  not found'}, 404

    return document, 200


@app.put(
    '/car/{car_id}',
    description='Update details of a specific car by its ID.',
    response_description='Confirmation message with the updated car ID.'
)
async def update_car(car_id: str, car: Car):
    document = db.find_one({'_id': car_id})

    if not document:
        return {'message': f'car \'{car_id}\' not found'}, 404

    db.update_one({'_id': car_id}, {
        '$set': {
            'brand': car.brand,
            'model': car.model,

            'color': car.color,
            'description': car.description,

            'year': car.year,
            'type': car.type,

            'image': car.image,
            'stock': car.stock,

            'price': car.price,
            'discount': car.discount
        }
    })

    return {'message': f'updated: {car_id}'}, 200


@app.delete(
    '/car/{car_id}',
    description='Delete a car entry by its ID.',
    response_description='Confirmation message with the deleted car ID.'
)
async def delete_car(car_id):
    document = db.find_one({'_id': car_id})

    if not document:
        return {'message': 'car not found'}, 404

    db.delete_one({'_id': car_id})

    return {'message': f'deleted: {car_id}'}, 200


# car search


@app.get(
    '/cars/',
    description='Retrieve details of all cars.',
    response_description='List of cars if available, or a message indicating no cars are found.'
)
async def read_cars():
    cars = list(db.find())

    if not cars:
        return {'message': 'empty'}, 404

    return cars, 200
