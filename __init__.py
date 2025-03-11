from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt
)
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clé privée
jwt = JWTManager(app)

# Fake users (à remplacer par une vraie base de données)
USERS = {
    "test": {"password": "test", "role": "user"},
    "admin": {"password": "admin", "role": "admin"},
}

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Création d'une route qui vérifie l'utilisateur et retourne un Jeton JWT si ok.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Vérifier si l'utilisateur existe
    user = USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Générer un token avec le rôle de l'utilisateur
    access_token = create_access_token(
        identity=username, 
        expires_delta=timedelta(hours=1),
        additional_claims={"role": user["role"]}
    )
    return jsonify(access_token=access_token)

# Vérifier si l'utilisateur a un rôle spécifique
def role_required(required_role):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", None)

            if user_role != required_role:
                return jsonify({"msg": "Accès refusé : permission insuffisante"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Route protégée par un jeton valide accessible uniquement aux admins
@app.route("/admin", methods=["GET"])
@role_required("admin")
def admin_panel():
    return jsonify({"msg": "Bienvenue dans l'admin !"}), 200

# Route protégée standard (accessible à tous les utilisateurs connectés)
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
