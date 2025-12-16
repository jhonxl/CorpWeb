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
    <title>CorpWeb API - Login</title>
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
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #555;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 15px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .hint {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            font-size: 13px;
            color: #555;
        }
        .hint strong {
            color: #667eea;
        }
        .message {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-size: 14px;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 CorpWeb API</h2>
        <p class="subtitle">JWT Authentication System</p>
        <form method="POST">
            <div class="input-group">
                <label>Email</label>
                <input type="email" name="email" placeholder="Digite seu email" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Digite sua senha" required>
            </div>
            <button type="submit">Entrar</button>
        </form>
        {% if error %}
        <div class="message error">
            {{ error }}
        </div>
        {% endif %}
        <div class="hint">
            <strong>💡 Dica:</strong> Apenas um usuário conhece a senha padrão
        </div>
    </div>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Realizado - CorpWeb API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .success-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 600px;
            text-align: center;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .check-icon {
            font-size: 64px;
            color: #28a745;
            margin-bottom: 20px;
            animation: bounce 0.6s ease-out;
        }
        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 28px;
        }
        .welcome-text {
            color: #666;
            font-size: 18px;
            margin-bottom: 30px;
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
            margin: 10px 0;
            font-size: 15px;
        }
        .user-info strong {
            color: #333;
        }
        .token-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }
        .token-section h3 {
            color: #333;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .token-box {
            background: #2d3748;
            color: #48bb78;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            word-break: break-all;
            max-height: 150px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .actions {
            margin-top: 30px;
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }
        .btn-success {
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
            color: white;
        }
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(33, 147, 176, 0.4);
        }
        .arrow-icon {
            margin-left: 5px;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="check-icon">✓</div>
        <h2>Login Realizado!</h2>
        <p class="welcome-text">Autenticação JWT bem-sucedida</p>
        
        <div class="user-info">
            <p><strong>👤 Nome:</strong> {{ name }}</p>
            <p><strong>📧 Email:</strong> {{ email }}</p>
            <p><strong>🔑 Role:</strong> {{ role }}</p>
        </div>

        <div class="token-section">
            <h3>🔐 JWT Token</h3>
            <div class="token-box">{{ token }}</div>
        </div>

        <div class="actions">
            <a href="/login" class="btn btn-secondary">← Voltar ao Login</a>
            <a href="http://127.0.0.1:5001/login" target="_blank" class="btn btn-success">
                Ir para Alvo 2 <span class="arrow-icon">→</span>
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
