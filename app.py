from uuid import uuid4

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cars'

mongo = PyMongo(app)

db = mongo.db.dev


# car crud

@app.route('/car', methods=['POST'])
def create_car():
    brand = request.json['brand']
    model = request.json['model']
    color = request.json['color']

    year = int(request.json['year'])
    type = request.json['type']

    image = request.json['image']
    stock = int(request.json['stock'])

    price = int(request.json['price'])
    discount = int(request.json['discount'])

    if not brand or not model or not color or not year or not type or not image or not stock or not price or not discount:
        return jsonify({'message': 'missing data'}), 400

    db.insert_one({
        '_id': str(uuid4()),

        'brand': brand,
        'model': model,
        'color': color,

        'year': year,
        'type': type,

        'image': image,
        'stock': stock,

        'price': price,
        'discount': discount
    })

    return jsonify({'message': 'created'}), 200


@app.route('/car/<_id>', methods=['GET'])
def read_car(_id):
    car = db.find_one({'_id': _id})

    if not car:
        return jsonify({'message': 'car not found'}), 404

    return jsonify(car), 200


@app.route('/car/<_id>', methods=['PUT'])
def update_car(_id):
    brand = request.json['brand']
    model = request.json['model']
    color = request.json['color']

    year = int(request.json['year'])
    type = request.json['type']

    image = request.json['image']
    stock = int(request.json['stock'])

    price = int(request.json['price'])
    discount = int(request.json['discount'])

    if not brand or not model or not color or not year or not type or not image or not stock or not price or not discount:
        return jsonify({'message': 'missing data'}), 400

    car = db.find_one({'_id': _id})

    if not car:
        return jsonify({'message': 'car not found'}), 404

    db.update_one({'_id': _id}, {
        '$set': {
            'brand': brand,
            'model': model,
            'color': color,

            'year': year,
            'type': type,

            'image': image,
            'stock': stock,

            'price': price,
            'discount': discount
        }
    })

    return jsonify({'message': 'updated'}), 200


@app.route('/car/<_id>', methods=['DELETE'])
def delete_car(_id):
    car = db.find_one({'_id': _id})

    if not car:
        return jsonify({'message': 'car not found'}), 404

    db.delete_one({'_id': _id})

    return jsonify({'message': 'deleted'}), 200


# car search


@app.route('/car/', methods=['GET'])
def read_car():
    cars = list(db.find())

    if not cars:
        return jsonify({'message': 'cars not found'}), 404

    return jsonify(cars), 200


if __name__ == '__main__':
    app.run(debug=True)
