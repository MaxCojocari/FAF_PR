from flask import request, jsonify
from models.database import db
from models.electro_scooter import ElectroScooter
from __main__ import app
from flasgger import swag_from

@app.route('/api/electro-scooters', methods=['POST'])
@swag_from('swagger_yaml/post.yaml')
def create_electro_scooter():
    try:
        data = request.get_json()
        
        name = data['name']
        battery_level = data['battery_level']
        
        electro_scooter = ElectroScooter(name=name, battery_level=battery_level)
        
        db.session.add(electro_scooter)
        db.session.commit()
        
        return jsonify({"message": "Electro Scooter created successfully"}), 201
    
    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400

@app.route('/api/electro-scooters', methods=['GET'])
@swag_from('swagger_yaml/get_all.yaml')
def get_electro_scooters():
    all_scooters = ElectroScooter.query.all()
    return jsonify([scooter.as_dict() for scooter in all_scooters]), 200

@app.route('/api/electro-scooters/<int:scooter_id>', methods=['GET'])
@swag_from('swagger_yaml/get.yaml')
def get_electro_scooter_by_id(scooter_id):
    scooter = ElectroScooter.query.get(scooter_id)
    
    if scooter is not None:
        return scooter.as_dict(), 200 
    else:
        return jsonify({"error": "Electro Scooter not found"}), 404

@app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
@swag_from('swagger_yaml/put.yaml')
def update_electro_scooter(scooter_id):
    try:
        scooter = ElectroScooter.query.get(scooter_id)
        
        if scooter is not None:
            data = request.get_json()
            
            scooter.name = data.get('name', scooter.name)
            scooter.battery_level = data.get('battery_level', scooter.battery_level)
            
            db.session.commit()
            return jsonify({"message": "Electro Scooter updated successfully"}), 200
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
@swag_from('swagger_yaml/delete.yaml')
def delete_electro_scooter(scooter_id):
    try:
        scooter = ElectroScooter.query.get(scooter_id)
        
        if scooter is not None:
            password = request.headers.get('X-Delete-Password')
            
            if password == '12345678':
                db.session.delete(scooter)
                db.session.commit()
                return jsonify({"message": "Electro Scooter deleted successfully"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500