from flask import Flask, request, jsonify, render_template_string
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# =============================
# CONFIGURAÇÕES
# =============================
SECRET_KEY = "super-secreta"
app.config["SECRET_KEY"] = SECRET_KEY

# =============================
# BANCO FICTÍCIO
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
# TEMPLATE LOGIN
# =============================
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb API Login</title>
</head>
<body style="background:#0d1117;color:#f0f6fc;font-family:Arial;text-align:center;padding-top:80px;">
    <h2>🔐 CorpWeb API Login</h2>
    <form method="POST">
        <input name="email" placeholder="Email" required><br><br>
        <input type="password" name="password" placeholder="Password (teste123)" required><br><br>
        <button type="submit">Login</button>
    </form>
    {% if error %}
        <p style="color:#ff7b72;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# =============================
# JWT DECORATOR
# =============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"message": "Token ausente"}), 401

        token = auth.split(" ")[1]

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = USERS_DB.get(data["user_id"])
        except Exception:
            return jsonify({"message": "Token inválido"}), 401

        return f(user, *args, **kwargs)
    return decorated

# =============================
# LOGIN HTML (GET + POST)
# =============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_TEMPLATE)

    email = request.form.get("email")
    password = request.form.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == email), None)

    if user and password == "teste123":
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        print(f"[JWT GERADO] {token}")

        return f"""
        <h2>Login realizado</h2>
        <p>Abra o console do navegador (F12).</p>
        <script>
            console.log("JWT:", "{token}");
        </script>
        """

    return render_template_string(LOGIN_TEMPLATE, error="Credenciais inválidas")

# =============================
# LOGIN API (JSON)
# =============================
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == email), None)

    if user and password == "teste123":
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

# =============================
# ENDPOINT VULNERÁVEL
# =============================
@app.route("/api/users", methods=["GET"])
@token_required
def list_users(current_user):
    return jsonify(list(USERS_DB.values()))

# =============================
# HOME
# =============================
@app.route("/")
def home():
    return jsonify({
        "message": "Alvo 1 - JWT Vulnerable API",
        "login_html": "/login",
        "login_api": "/api/login",
        "enum": "/api/users"
    })

# =============================
# MAIN
# =============================
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Alvo 1 (JWT API)")
    print("👉 http://127.0.0.1:5000/login")
    print("👉 http://127.0.0.1:5000/api/users")
    print("=" * 60)
    app.run(port=5000, debug=True, use_reloader=False)

