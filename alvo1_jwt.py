from flask import Flask, request, jsonify, render_template_string
import jwt
import datetime
from functools import wraps
import hashlib

app = Flask(__name__)

SECRET_KEY = "super-secreta"
app.config["SECRET_KEY"] = SECRET_KEY

# 🔐 Função de hash fraco (intencional)
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

# 🗄️ "Banco de dados"
USERS_DB = {
    1: {
        "id": 1,
        "email": "admin@corpweb.lab",
        "name": "Admin CorpWeb",
        "role": "admin",
        "password_hash": weak_hash("love")
    },
    2: {
        "id": 2,
        "email": "jsantos@corpweb.lab",
        "name": "João Santos",
        "role": "user",
        "password_plain": "teste123"  # 👈 único usuário com senha conhecida
    },
    3: {
        "id": 3,
        "email": "jsilva@corpweb.lab",
        "name": "João Silva",
        "role": "user",
        "password_hash": weak_hash("welcome")
    }
}

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb API Login</title>
</head>
<body style="font-family: Arial; background:#f2f2f2;">
    <h2>🔐 CorpWeb API</h2>
    <form method="POST">
        <input name="email" placeholder="email" required><br><br>
        <input type="password" name="password" placeholder="password" required><br><br>
        <button type="submit">Entrar</button>
    </form>
    {% if error %}
        <p style="color:red">{{ error }}</p>
    {% endif %}
    <p><small>Dica: apenas um usuário conhece a senha padrão</small></p>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<h2>Login realizado</h2>
<p><strong>Nome:</strong> {{ name }}</p>
<p><strong>Email:</strong> {{ email }}</p>
<p><strong>Role:</strong> {{ role }}</p>

<p><strong>JWT:</strong></p>
<pre>{{ token }}</pre>

<hr>
<p>➡️ Acesse outro sistema corporativo:</p>
<a href="http://127.0.0.1:5001/login" target="_blank">Ir para Alvo 2</a>
"""

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"message": "Token ausente"}), 401
        try:
            token = auth.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = USERS_DB.get(data["user_id"])
        except Exception:
            return jsonify({"message": "Token inválido"}), 401
        return f(user, *args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_TEMPLATE)

    email = request.form.get("email")
    password = request.form.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == email), None)

    # ✅ apenas jsantos conhece a senha
    if user and user.get("password_plain") == password:
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return render_template_string(
            SUCCESS_TEMPLATE,
            token=token,
            name=user["name"],
            email=user["email"],
            role=user["role"]
        )

    return render_template_string(LOGIN_TEMPLATE, error="Credenciais inválidas")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == email), None)

    if user and user.get("password_plain") == password:
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        return jsonify({"token": jwt.encode(payload, SECRET_KEY, algorithm="HS256")})

    return jsonify({"message": "Invalid credentials"}), 401

# 🚨 ENDPOINT VULNERÁVEL
@app.route("/api/users")
@token_required
def list_users(current_user):
    leaked_users = []

    for u in USERS_DB.values():
        leaked_users.append({
            "id": u["id"],
            "email": u["email"],
            "role": u["role"],
            "password_hash": u.get("password_hash", "NOT STORED")
        })

    return jsonify(leaked_users)

@app.route("/")
def home():
    return jsonify({
        "message": "Alvo 1 - JWT Vulnerable API",
        "login_html": "/login",
        "login_api": "/api/login",
        "enum": "/api/users"
    })

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Alvo 1 (JWT Vulnerável)")
    print("👉 http://127.0.0.1:5000/login")
    print("=" * 60)
    app.run(port=5000, debug=True)
