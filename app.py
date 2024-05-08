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

    year = request.json['year']
    type = request.json['type']

    image = request.json['image']

    if not brand or not model or not color or not year or not type or not image:
        return jsonify({'message': 'missing data'}), 400

    db.insert_one({
        '_id': str(uuid4()),

        'brand': brand,
        'model': model,
        'color': color,

        'year': year,
        'type': type,

        'image': image
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

    year = request.json['year']
    type = request.json['type']

    image = request.json['image']

    if not brand or not model or not color or not year or not type or not image:
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

            'image': image
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


if __name__ == '__main__':
    app.run(debug=True)
