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
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
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
        .error {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            text-align: center;
            border-left: 4px solid #c33;
        }
        .hint {
            text-align: center;
            color: #666;
            font-size: 13px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 CorpWeb API</h2>
        <form method="POST">
            <div class="input-group">
                <label>Email</label>
                <input name="email" type="email" placeholder="seu@email.com" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="••••••••" required>
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
            max-width: 500px;
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
        .user-info strong {
            color: #333;
        }
        .token-box {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            word-break: break-all;
            margin-top: 20px;
            text-align: left;
        }
        .token-label {
            color: #888;
            font-size: 12px;
            margin-bottom: 10px;
            text-align: left;
        }
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 15px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .copy-btn:hover {
            background: #5568d3;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="check-icon">✓</div>
        <h2>Login Realizado!</h2>
        <div class="user-info">
            <p><strong>Nome:</strong> {{ name }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Role:</strong> {{ role }}</p>
        </div>
        <div class="token-label">🔑 Seu JWT Token (Console do navegador):</div>
        <div class="token-box" id="token">{{ token }}</div>
        <button class="copy-btn" onclick="copyToken()">📋 Copiar Token</button>
        <br>
        <a href="/login" class="back-link">← Voltar ao Login</a>
    </div>
    <script>
        console.log("JWT Token:", "{{ token }}");
        function copyToken() {
            const token = document.getElementById('token').innerText;
            navigator.clipboard.writeText(token).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.innerText = '✓ Copiado!';
                setTimeout(() => btn.innerText = '📋 Copiar Token', 2000);
            });
        }
    </script>
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
        return render_template_string(SUCCESS_TEMPLATE, 
                                     token=token,
                                     name=user["name"],
                                     email=user["email"],
                                     role=user["role"])
    
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
    print(f"🎯 Alvo 1 (JWT) rodando em http://127.0.0.1:5000")
    print("=" * 60)
    app.run(port=5000, debug=True)
