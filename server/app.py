# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Earthquake
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# View to get all earthquakes
@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    earthquake_list = [{'id': e.id, 'location': e.location, 'magnitude': e.magnitude, 'date': e.date} for e in earthquakes]
    return make_response(jsonify(earthquake_list), 200)

# View to create a new earthquake
@app.route('/earthquakes', methods=['POST'])
def create_earthquake():
    data = request.get_json()
    new_earthquake = Earthquake(location=data['location'], magnitude=data['magnitude'], date=data['date'])
    db.session.add(new_earthquake)
    db.session.commit()
    return make_response(jsonify({'message': 'Earthquake added successfully'}), 201)

# View to get a specific earthquake by id
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        response = {'id': earthquake.id, 'location': earthquake.location, 'magnitude': earthquake.magnitude, 'date': earthquake.date}
        return make_response(jsonify(response), 200)
    return make_response(jsonify({'error': 'Earthquake not found'}), 404)

# View to update an earthquake by id
@app.route('/earthquakes/<int:id>', methods=['PUT'])
def update_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        data = request.get_json()
        earthquake.location = data.get('location', earthquake.location)
        earthquake.magnitude = data.get('magnitude', earthquake.magnitude)
        earthquake.date = data.get('date', earthquake.date)
        db.session.commit()
        return make_response(jsonify({'message': 'Earthquake updated successfully'}), 200)
    return make_response(jsonify({'error': 'Earthquake not found'}), 404)

# View to delete an earthquake by id
@app.route('/earthquakes/<int:id>', methods=['DELETE'])
def delete_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        db.session.delete(earthquake)
        db.session.commit()
        return make_response(jsonify({'message': 'Earthquake deleted successfully'}), 200)
    return make_response(jsonify({'error': 'Earthquake not found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
