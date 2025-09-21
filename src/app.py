"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object (copiado de la página inicial de app.py)
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object (copiado de la página inicial de app.py)
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints (copiado de la página inicial de app.py)
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET /members - Obtener todos los miembros de la familia (copiado de la página inicial de app.py)
@app.route('/members', methods=['GET'])
def get_all_members():
    """
    Endpoint para obtener todos los miembros de la familia
    """
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

# GET /members/<int:member_id> - Obtener un miembro específico
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    """
    Endpoint para obtener un miembro específico por ID
    """
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Miembro no encontrado"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

# POST /members - Agregar un nuevo miembro
@app.route('/members', methods=['POST'])
def add_member():
    """
    Endpoint para agregar un nuevo miembro a la familia
    """
    try:
        # Obtener los datos del request
        member_data = request.get_json()
        
        # Validación del código para saber si se enviaron los datitos
        if not member_data:
            return jsonify({"error": "No se enviaron datos"}), 400
        
        # Validación de los campos donde se recoge la info
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in member_data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Validación de datitos
        if not isinstance(member_data["age"], int) or member_data["age"] <= 0:
            return jsonify({"error": "La edad debe ser un número entero positivo"}), 400
        
        if not isinstance(member_data["lucky_numbers"], list):
            return jsonify({"error": "lucky_numbers debe ser una lista"}), 400
        
        # Agregar los miembros
        new_member = jackson_family.add_member(member_data)
        return jsonify(new_member), 200
        
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

# DELETE /members/<int:member_id> - Eliminar miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """
    Endpoint para eliminar un miembro de la familia
    """
    try:
        # El código verifica si el miembro existe antes de intentar eliminarlo
        if jackson_family.get_member(member_id) is None:
            return jsonify({"error": "Miembro no encontrado"}), 404
        
        # Así dmos la posibilidad de eliminar el miembro
        success = jackson_family.delete_member(member_id)
        
        if success:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "No se pudo eliminar el miembro"}), 500
            
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

# This only runs if `$ python src/app.py` is executed (copiado de la página inicial de app.py)
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)