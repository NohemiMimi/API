### Directions.py

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from BackEnd import Functions as CallMethod
import BackEnd.GlobalInfo.ResponseMessages as ResponseMessages

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/mensaje", methods=["GET"])
@cross_origin(allow_headers=["Content-Type"])
def mensaje():
    try:
        return {"mensaje": "hola que hace?"}
    except Exception as e:
        print("No jalo mijo", e)
        return jsonify(ResponseMessages.err500)

@app.route('/register', methods=['POST'])
@cross_origin(allow_headers=["Content-Type"])
def register():
    try:
        data = request.json
        usuario = data.get("user")
        password = data.get("pass")
        return CallMethod.fnRegisterUser(usuario, password)
    except Exception as e:
        print("Error en el registro de usuario:", e)
        return jsonify({"mensaje": "Error en el servidor", "success": False})

@app.route('/logueo', methods=['POST'])
@cross_origin(allow_headers=["Content-Type"])
def logueo():
    try:
        usuario = request.json['user']
        password = request.json['pass']
        return CallMethod.fnAuthPost(usuario, password)
    except Exception as e:
        print("Error en logueo", e)
        return jsonify(ResponseMessages.err500)

@app.route('/control-valvula', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def control_valvula():
    try:
        data = request.json
        return CallMethod.control_valvula()
    except Exception as e:
        print("Error en control-valvula", e)
        return jsonify({"message": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
