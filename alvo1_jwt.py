# Arquivo: alvo1_jwt.py
from flask import Flask, request, jsonify, render_template_string
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# =============================
# CONFIGURAÇÕES INSEGURAS (LAB)
# =============================
SECRET_KEY = "super-secreta"  # JWT fraco (intencional)
GLOBAL_PASSWORD = "teste123"  # Senha global fraca (intencional)

app.config["SECRET_KEY"] = SECRET_KEY

# =============================
# BANCO DE DADOS FICTÍCIO
# =============================
USERS_DB = {
    1: {
        "id": 1,
        "email": "admin@corpweb.lab",
        "name": "Admin CorpWeb",
        "role": "admin"
    },
    2: {
        "id": 2,
        "email": "user1@corpweb.lab",
        "name": "Usuario Um",
        "role": "user"
    },
    3: {
        "id": 3,
        "email": "user2@corpweb.lab",
        "name": "Usuario Dois",
        "role": "user"
    }
}

# =============================
# TEMPLATE DE LOGIN
# =============================
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb - Login</title>
</head>
<body style="background:#0d1117;color:#f0f6fc;font-family:Arial;text-align:center;">
    <h2>🔐 CorpWeb Login</h2>
    <form action="/check_login" method="POST">
        <input type="text" name="username" placeholder="Email (user@corpweb.lab)" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    {% if message %}
        <p style="color:#ff7b72;">{{ message }}</p>
    {% endif %}
</body>
</html>
"""

# =============================
# DECORADOR JWT
# =============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"message": "Token ausente"}), 401

        token = auth.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = USERS_DB.get(payload["user_id"])
        except Exception:
            return jsonify({"message": "Token inválido"}), 401

        return f(user, *args, **kwargs)

    return decorated

# =============================
# HOME
# =============================
@app.route("/")
def home():
    return jsonify({
        "message": "Alvo 1 - JWT Vulnerable API",
        "hint": "Faça login em /login, capture o JWT no console e acesse /api/users/"
    })

# =============================
# LOGIN HTML
# =============================
@app.route("/login", methods=["GET"])
def login_page():
    return render_template_string(LOGIN_TEMPLATE)

# =============================
# PROCESSA LOGIN HTML
# =============================
@app.route("/check_login", methods=["POST"])
def check_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == username), None)

    if user and password == GLOBAL_PASSWORD:
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        print(f"[JWT GERADO] {token}")

        return f"""
        <h2>Login realizado com sucesso</h2>
        <p>Abra o console do navegador (F12) para ver o JWT.</p>
        <script>
            console.log("JWT Token:", "{token}");
        </script>
        """

    return render_template_string(LOGIN_TEMPLATE, message="Credenciais inválidas")

# =============================
# LOGIN API (JSON)
# =============================
@app.route("/login", methods=["POST"])
def login_api():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == email), None)

    if user and password == GLOBAL_PASSWORD:
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

# =============================
# ENDPOINT VULNERÁVEL
# =============================
@app.route("/api/users/", methods=["GET"])
@token_required
def list_users(current_user):
    return jsonify({
        "authenticated_as": current_user,
        "users": list(USERS_DB.values())
    })

# =============================
# MAIN
# =============================
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Alvo 1 (JWT API) rodando em http://127.0.0.1:5000")
    print("🔑 JWT FRACO + SENHA GLOBAL")
    print("=" * 60)
    app.run(debug=True, port=5000)
