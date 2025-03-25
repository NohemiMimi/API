### Functions.py

import BackEnd.GlobalInfo.ResponseMessages as ResponseMessage
import BackEnd.GlobalInfo.Keys as Colabskey
from pymongo import MongoClient
from flask import jsonify, request
from bson import ObjectId

# Conexión a MongoDB Atlas
if Colabskey.dbconn is None:
    mongoConnect = MongoClient(Colabskey.strConnection)
    Colabskey.dbconn = mongoConnect[Colabskey.strDBConnection]

dbUsuario = Colabskey.dbconn["usuario"]
dbValvula = Colabskey.dbconn["estadoValvula"]



def fnAuthPost(usuario, password):
    try:
        objQuery = dbUsuario.find_one({"nombre": usuario, "contraseña": password})
        print("Resultado de la consulta:", objQuery)
        if objQuery:
            return jsonify({"Acreditado": True, "mensaje": "Inicio de sesión exitoso"})
        else:
            return jsonify({"Acreditado": False, "mensaje": "Usuario o contraseña incorrectos"})
    except Exception as e:
        print("Error en fnAuthPost:", e)
        return jsonify({"Acreditado": False, "mensaje": "Error en el servidor"})


def fnRegisterUser(usuario, password):
    try:
        print(f"Registrando nuevo usuario: {usuario}")
        if dbUsuario.find_one({"nombre": usuario}):
            return jsonify({"mensaje": "El usuario ya existe", "success": False})
        new_user = {"nombre": usuario, "contraseña": password}
        dbUsuario.insert_one(new_user)
        return jsonify({"mensaje": "Usuario registrado correctamente", "success": True})
    except Exception as e:
        print("Error al registrar usuario:", e)
        return jsonify({"mensaje": "Error en el servidor", "success": False})


def control_valvula():
    try:
        # Obtener el documento actual
        doc = dbValvula.find_one({}, {"estado": 1})

# Verificar si el campo existe antes de actualizarlo
        if doc and "estado" in doc:
            nuevo_estado = not doc["estado"]  # Niega el valor actual

    # Actualizar el campo en la base de datos
        dbValvula.update_one({}, {"$set": {"estado": nuevo_estado}})
        return jsonify({"message": f"Válvula cambiada correctamente"}), 200
    except Exception as e:
        print("Error en control_valvula:", e)
        return jsonify({"message": "Error interno del servidor"}), 500
    
def GetValvula():
    try:
        doc = dbValvula.find_one({}, {"estado": 1})
        if doc and "estado" in doc:
            return jsonify({"estado": doc["estado"]})
        else:
            return jsonify({"message": "No se encontró la válvula"}), 404
    except Exception as e:
        print("Error en GetValvula:", e)
        return jsonify({"message": "Error interno del servidor"}), 500
    

def fnProgramarRiego(abrir, cerrar, dias):
    try:
        if not abrir or not cerrar or not dias:
            return jsonify({"message": "Faltan datos requeridos"}), 400

        # Crear el documento para guardar en la base de datos
        nuevo_registro = {
            "abrir": abrir,
            "cerrar": cerrar,
            "dias": dias
        }

        # Guardar en la colección "programacion_riego"
        dbProgramacion = Colabskey.dbconn["programacion_riego"]
        dbProgramacion.insert_one(nuevo_registro)

        return jsonify({"message": "Riego programado correctamente"}), 200
    except Exception as e:
        print("Error en fnProgramarRiego:", e)
        return jsonify({"message": "Error interno del servidor"}), 500
    
def guardar_humedad(humedad):
    try:
        # Conectar a la colección "humedad"
        dbHumedad = Colabskey.dbconn["humedad"]

        # Crear el documento a insertar
        nuevo_registro = {
            "humedad": humedad
        }

        # Insertar en la base de datos
        dbHumedad.insert_one(nuevo_registro)

        return jsonify({"message": "Dato de humedad guardado correctamente"}), 200
    except Exception as e:
        print("Error en guardar_humedad:", e)
        return jsonify({"message": "Error interno del servidor"}), 500