from flask import Flask, render_template, jsonify, request, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('formulaire.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    
    # Vérification des identifiants
    if username == "admin" and password == "admin":
        roles = ["admin"]
    elif username == "user" and password == "userpass":
        roles = ["user"]
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Créer le jeton avec les rôles appropriés
    access_token = create_access_token(identity=username, additional_claims={"roles": roles}, expires_delta=timedelta(hours=1))
    
    # Stocker le jeton dans un cookie
    response = make_response(jsonify(access_token=access_token))
    response.set_cookie("access_token", access_token, max_age=timedelta(hours=1), httponly=True, secure=False)  # `secure=True` si vous utilisez HTTPS
    return response

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
