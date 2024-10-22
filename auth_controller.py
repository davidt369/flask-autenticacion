from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from models import Usuario, db
from datetime import timedelta

class AuthController:

    @staticmethod
    def register(data):
        nombre = data.get('nombre')
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        if not nombre or not correo or not contrasena:
            return jsonify({"error": "Faltan datos"}), 400

        if Usuario.query.filter_by(correo=correo).first():
            return jsonify({"error": "Correo ya registrado"}), 400

        hashed_password = generate_password_hash(contrasena)
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contrasena=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        access_token = create_access_token(identity=nuevo_usuario.id, expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(identity=nuevo_usuario.id, expires_delta=timedelta(days=7))

        return jsonify({
            "mensaje": "Registro exitoso",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201

    @staticmethod
    def login(data):
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        if not correo or not contrasena:
            return jsonify({"error": "Faltan datos"}), 400

        usuario = Usuario.query.filter_by(correo=correo).first()

        if not usuario or not check_password_hash(usuario.contrasena, contrasena):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        if not usuario.activo:
            return jsonify({"error": "Usuario inactivo"}), 403

        access_token = create_access_token(identity=usuario.id, expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(identity=usuario.id, expires_delta=timedelta(days=7))

        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    @staticmethod
    def refresh_token(identity):
        access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=30))
        return jsonify({"access_token": access_token}), 200
