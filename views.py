from flask import Blueprint, request
from auth_controller import AuthController
from auth_decorators import jwt_authentication_required, role_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return AuthController.register(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return AuthController.login(data)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_authentication_required
def refresh():
    usuario_id = get_jwt_identity()
    return AuthController.refresh_token(usuario_id)

@auth_bp.route('/admin', methods=['GET'])
@role_required('administrador')
def admin_route():
    return jsonify({"mensaje": "Bienvenido, administrador"}), 200

# Optional routes for activating/deactivating users
@auth_bp.route('/user/<int:user_id>/activate', methods=['PUT'])
@role_required('administrador')
def activate_user(user_id):
    from models import Usuario, db
    usuario = Usuario.query.get_or_404(user_id)
    usuario.activo = True
    db.session.commit()
    return jsonify({"mensaje": "Usuario activado"}), 200

@auth_bp.route('/user/<int:user_id>/deactivate', methods=['PUT'])
@role_required('administrador')
def deactivate_user(user_id):
    from models import Usuario, db
    usuario = Usuario.query.get_or_404(user_id)
    usuario.activo = False
    db.session.commit()
    return jsonify({"mensaje": "Usuario desactivado"}), 200
