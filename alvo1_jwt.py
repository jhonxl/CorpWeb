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

LOGIN_TEMPLATE = """ ... (SEM ALTERAÇÕES) ... """

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Realizado - CorpWeb</title>
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
        .success-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 520px;
            text-align: center;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .check-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 28px;
        }
        .user-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }
        .user-info p {
            color: #555;
            margin: 8px 0;
            font-size: 14px;
        }
        .token-box {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
            margin-top: 15px;
            text-align: left;
        }

        /* 🔗 CARD DO OUTRO SERVIÇO */
        .service-card {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2193b0, #6dd5ed);
            color: white;
        }
        .service-card h3 {
            margin-bottom: 10px;
        }
        .service-card p {
            font-size: 14px;
            margin-bottom: 15px;
        }
        .service-card a {
            display: inline-block;
            padding: 10px 20px;
            background: white;
            color: #2193b0;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .service-card a:hover {
            transform: translateY(-2px);
        }

        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="check-icon">✅</div>
        <h2>Login Realizado!</h2>

        <div class="user-info">
            <p><strong>Nome:</strong> {{ name }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Role:</strong> {{ role }}</p>
        </div>

        <div class="token-box">{{ token }}</div>

        <!-- 🔗 OUTRO SERVIÇO -->
        <div class="service-card">
            <h3>🌐 Outro Serviço Corporativo</h3>
            <p>Detectamos que você possui acesso a outro sistema interno da CorpWeb.</p>
            <a href="http://127.0.0.1:5001/login" target="_blank">
                Acessar Portal Corporativo
            </a>
        </div>

        <a href="/login" class="back-link">← Voltar ao Login</a>
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

@app.route("/api/users")
@token_required
def list_users(current_user):
    return jsonify(list(USERS_DB.values()))

if __name__ == "__main__":
    print("🎯 Alvo 1 rodando em http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
