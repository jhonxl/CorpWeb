from flask import Flask, request, jsonify, render_template_string
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

SECRET_KEY = "super-secreta"
app.config["SECRET_KEY"] = SECRET_KEY

USERS_DB = {
    1: {"id": 1, "email": "admin@corpweb.lab", "name": "Admin CorpWeb", "role": "admin"},
    2: {"id": 2, "email": "user1@corpweb.lab", "name": "Usuario Um", "role": "user"},
    3: {"id": 3, "email": "user2@corpweb.lab", "name": "Usuario Dois", "role": "user"}
}

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb API Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        h2 { text-align: center; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; }
        input {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .error {
            margin-top: 15px;
            color: #c33;
            text-align: center;
        }
        .hint {
            margin-top: 20px;
            font-size: 13px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 CorpWeb API</h2>
        <form method="POST">
            <div class="input-group">
                <label>Email</label>
                <input name="email" type="email" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Entrar</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <div class="hint">💡 Dica: Senha padrão é "teste123"</div>
    </div>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Realizado - CorpWeb</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .success-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            width: 100%;
            max-width: 520px;
            text-align: center;
        }
        .user-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: left;
            margin: 20px 0;
        }
        .token-box {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
        }
        .service-card {
            margin-top: 25px;
            padding: 20px;
            border-radius: 12px;
            background: #eef1ff;
        }
        .service-card a {
            display: inline-block;
            margin-top: 10px;
            padding: 12px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
        }
        .service-card a:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <h2>✅ Login Realizado</h2>

        <div class="user-info">
            <p><strong>Nome:</strong> {{ name }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Role:</strong> {{ role }}</p>
        </div>

        <p><strong>JWT Token:</strong></p>
        <div class="token-box">{{ token }}</div>

        <!-- 🔗 LINK PARA O ALVO 2 -->
        <div class="service-card">
            <h3>🌐 Outro Serviço Corporativo</h3>
            <p>Acesse nosso sistema interno de autenticação</p>
            <a href="http://127.0.0.1:5001/login" target="_blank">
                Acessar Serviço
            </a>
        </div>
    </div>
</body>
</html>
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

    if user and password == "teste123":
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

    if user and password == "teste123":
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        return jsonify({"token": jwt.encode(payload, SECRET_KEY, algorithm="HS256")})

    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/users")
@token_required
def list_users(current_user):
    return jsonify(list(USERS_DB.values()))

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
    print("🎯 Alvo 1 (JWT) rodando em http://127.0.0.1:5000/login")
    print("=" * 60)
    app.run(port=5000, debug=True)
