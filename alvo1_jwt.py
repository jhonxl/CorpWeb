# Arquivo: alvo1_jwt_api.py
from flask import Flask, request, jsonify, render_template_string, redirect
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# --- Configurações Fictícias ---
SECRET_KEY = 'super-secreta'  # Chave secreta fraca para o JWT
app.config['SECRET_KEY'] = SECRET_KEY

# Base de Dados Fictícia
USERS_DB = {
    1: {"id": 1, "email": "admin@corpweb.lab", "password_hash": "hash_admin_$2b$12$xyz", "name": "Admin CorpWeb", "role": "admin"},
    2: {"id": 2, "email": "user1@corpweb.lab", "password_hash": "hash_user1_$2b$12$abc", "name": "Usuario Um", "role": "user"},
    3: {"id": 3, "email": "user2@corpweb.lab", "password_hash": "hash_user2_$2b$12$def", "name": "Usuario Dois", "role": "user"}
}
NEXT_ID = 4  # Próximo ID para registro

# =============================
# TEMPLATE DE LOGIN
# =============================
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #0d1117;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: #f0f6fc;
        }
        .login-container {
            background: #161b22;
            padding: 30px;
            border-radius: 8px;
            width: 300px;
            border: 1px solid #30363d;
        }
        h2 {
            text-align: center;
            color: #58a6ff;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            background: #0d1117;
            color: #f0f6fc;
            border: 1px solid #30363d;
            border-radius: 4px;
        }
        button {
            background-color: #238636;
            cursor: pointer;
        }
        button:hover {
            background-color: #2ea043;
        }
        .message {
            margin-top: 15px;
            padding: 10px;
            text-align: center;
        }
        .error {
            color: #ff7b72;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 CorpWeb Login</h2>
        <form action="/check_login" method="POST">
            <input type="text" name="username" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password (teste123)" required>
            <button type="submit">Login</button>
        </form>
        {% if message %}
            <div class="message error">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

# =============================
# DECORADOR JWT
# =============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = USERS_DB.get(data["user_id"])
        except Exception:
            return jsonify({'message': 'Invalid or expired token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# =============================
# LOGIN HTML
# =============================
@app.route('/login', methods=['GET'])
def login_html():
    return render_template_string(LOGIN_TEMPLATE)

# =============================
# PROCESSA LOGIN HTML
# JWT APENAS NO CONSOLE
# =============================
@app.route('/check_login', methods=['POST'])
def check_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = next((u for u in USERS_DB.values() if u["email"] == username), None)

    if user and password == "teste123":
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb - Dashboard</title>
    <script>
        console.log("JWT Token:", "{token}");
    </script>
</head>
<body style="background:#0d1117;color:#f0f6fc;font-family:Arial;text-align:center;padding-top:50px;">
    <h2>Login realizado com sucesso</h2>
    <p>Bem-vindo ao sistema.</p>
    <p style="color:#8b949e;font-size:14px;">
        Nenhuma informação sensível é exibida na interface.
    </p>
</body>
</html>
        ''')

    return render_template_string(LOGIN_TEMPLATE, message="Credenciais inválidas")

# =============================
# LOGIN API (JSON)
# =============================
@app.route('/login', methods=['POST'])
def login_api():
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
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# =============================
# ENDPOINT VULNERÁVEL
# =============================
@app.route('/api/users/', methods=['GET'])
@token_required
def list_users(current_user):
    return jsonify({
        "users": list(USERS_DB.values()),
        "total": len(USERS_DB)
    })

# =============================
# HOME
# =============================
@app.route('/')
def home():
    return jsonify({
        "message": "Alvo 1 - JWT Vulnerable API",
        "hint": "Faça login via HTML, encontre o token no console e enumere /api/users/"
    })

# =============================
# MAIN
# =============================
if __name__ == '__main__':
    print("=" * 60)
    print("🎯 Alvo 1 (JWT API) rodando em http://127.0.0.1:5000")
    print("🔑 JWT NÃO É EXIBIDO NA TELA — APENAS NO CONSOLE")
    print("=" * 60)
    app.run(debug=True, port=5000)
