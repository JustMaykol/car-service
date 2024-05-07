from uuid import uuid4
from bcrypt import gensalt, hashpw, checkpw

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'

mongo = PyMongo(app)

db = mongo.db.current


# TODO: expand user schema to include email, phone, etc.


@app.route('/login', methods=['POST'])
def login():
    name = request.json['name']
    password = request.json['password']

    user = db.find_one({'name': name})

    if not user:
        return jsonify({'message': 'invalid credentials'}), 401

    if not checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'invalid credentials'}), 401

    return jsonify({'user': user['id']}), 200


# user crud

@app.route('/user', methods=['POST'])
def create_user():
    name = request.json['name']
    password = request.json['password']

    if db.find_one({'name': name}):
        return jsonify({'message': f'{name} already exists'}), 401

    db.insert_one({
        'id': str(uuid4()),
        'name': name,
        'password': hashpw(password.encode('utf-8'), gensalt(14))
    })

    return jsonify({'message': f'{name} created'}), 200


@app.route('/user/<id>', methods=['GET'])
def read_user(id):
    user = db.find_one({'id': id})

    if not user:
        return jsonify({'message': 'user not found'}), 404

    user.pop('_id')
    user.pop('password')

    return jsonify(user), 200


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    password = request.json['password']

    user = db.find_one({'id': id})

    if not user:
        return jsonify({'message': 'user not found'}), 404

    db.update_one({'id': id}, {
        '$set': {
            'name': name,
            'password': hashpw(password.encode('utf-8'), gensalt(14))
        }
    })

    return jsonify({'message': f'{name} updated'}), 200


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.find_one({'id': id})

    if not user:
        return jsonify({'message': 'user not found'}), 404

    db.delete_one({'id': id})

    return jsonify({'message': 'user deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
