from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autosalon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Brand {self.name}>'

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Color {self.name}>'

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    model = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Car {self.model}>'

db.create_all()

@app.route('/brand', methods=['POST'])
def create_brand():
    data = request.get_json()
    new_brand = Brand(name=data['name'])
    db.session.add(new_brand)
    db.session.commit()
    return jsonify({'message': 'New brand created'}), 201

@app.route('/brand/<int:id>', methods=['GET'])
def get_brand(id):
    brand = Brand.query.get_or_404(id)
    return jsonify({'name': brand.name}), 200

@app.route('/brand/<int:id>', methods=['PUT'])
def update_brand(id):
    brand = Brand.query.get_or_404(id)
    data = request.get_json()
    brand.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Brand updated'}), 200

@app.route('/brand/<int:id>', methods=['DELETE'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return jsonify({'message': 'Brand deleted'}), 200

@app.route('/car', methods=['POST'])
def create_car():
    data = request.get_json()
    new_car = Car(brand_id=data['brand_id'], color_id=data['color_id'], model=data['model'])
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'New car created'}), 201

@app.route('/car/<int:id>', methods=['GET'])
def get_car(id):
    car = Car.query.get_or_404(id)
    return jsonify({'brand_id': car.brand_id, 'color_id': car.color_id, 'model': car.model}), 200

@app.route('/car/<int:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.get_json()
    car.brand_id = data['brand_id']
    car.color_id = data['color_id']
    car.model = data['model']
    db.session.commit()
    return jsonify({'message': 'Car updated'}), 200

@app.route('/car/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
