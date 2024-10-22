from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from models import Usuario

def jwt_authentication_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        if not usuario.activo:
            return jsonify({"error": "Usuario inactivo"}), 403
        return func(*args, **kwargs)
    return wrapper

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            usuario_id = get_jwt_identity()
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404
            if usuario.rol != required_role:
                return jsonify({"error": "Acceso denegado"}), 403
            if not usuario.activo:
                return jsonify({"error": "Usuario inactivo"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
