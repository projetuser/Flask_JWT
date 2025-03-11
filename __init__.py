from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from datetime import timedelta, datetime

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Création d'une route qui vérifie l'utilisateur et retourne un Jeton JWT si ok.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Vérification des identifiants
    if username == "admin" and password == "admin":
        roles = ["admin"]
    elif username == "user" and password == "userpass":
        roles = ["user"]
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Créer le jeton avec les rôles appropriés
    access_token = create_access_token(identity=username, additional_claims={"roles": roles}, expires_delta=timedelta(hours=1))
    return jsonify(access_token=access_token)

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route admin protégée uniquement accessible pour les utilisateurs ayant le rôle "admin"
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    # Récupérer les rôles depuis le JWT
    claims = get_jwt()
    roles = claims.get("roles", [])

    # Vérifier si l'utilisateur a le rôle "admin"
    if "admin" not in roles:
        return jsonify({"msg": "Accès refusé, rôle 'admin' requis"}), 403
    
    return jsonify(msg="Bienvenue sur la route Admin ! Vous avez le rôle 'admin'."), 200

if __name__ == "__main__":
    app.run(debug=True)
