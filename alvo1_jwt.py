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
            box-shadow: 0 2px 15px rgba(0,0,0,0.4);
            width: 300px;
            border: 1px solid #30363d;
        }
        h2 {
            text-align: center;
            color: #58a6ff;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #30363d;
            background: #0d1117;
            color: #f0f6fc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input:focus {
            border-color: #58a6ff;
            outline: none;
            box-shadow: 0 0 5px #58a6ff;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #238636;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2ea043;
        }
        .message {
            margin-top: 15px;
            padding: 10px;
            border-radius: 4px;
            text-align: center;
        }
        .success {
            background-color: #1b4721;
            color: #3fb950;
            border: 1px solid #2ea043;
        }
        .error {
            background-color: #3b0a0a;
            color: #ff7b72;
            border: 1px solid #ff7b72;
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
        <div class="message {{ message_type }}">
            {{ message }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# =============================
# DECORADOR DE TOKEN
# =============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = USERS_DB.get(data['user_id']) 
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# =============================
# ROTA DE LOGIN HTML (NOVA)
# =============================
@app.route('/login', methods=['GET'])
def login():
    return render_template_string(LOGIN_TEMPLATE)

# =============================
# ROTA QUE PROCESSA LOGIN HTML (NOVA)
# =============================
@app.route('/check_login', methods=['POST'])
def check_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_match = next((u for u in USERS_DB.values() if u["email"] == username), None)

    if user_match and password == "teste123":
        # gera o token para mostrar ao usuário
        token_payload = {
            'user_id': user_match['id'],
            'email': user_match['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        # Exibe o token diretamente na página
        return render_template_string(
            LOGIN_TEMPLATE,
            message=f"Login OK! Use este token:<br><br><textarea style='width:100%;height:80px;'>{token}</textarea>",
            message_type="success"
        )

    return render_template_string(
        LOGIN_TEMPLATE,
        message="Credenciais inválidas",
        message_type="error"
    )

# =============================
# ENDPOINT ORIGINAL DE REGISTRO
# =============================
@app.route('/register', methods=['POST'])
def register():
    global NEXT_ID
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    new_user = {
        "id": NEXT_ID,
        "email": data.get('email'),
        "password_hash": "mocked_hash_for_" + data.get('password'),
        "name": data.get('name', 'Novo Usuario'),
        "role": "user"
    }
    USERS_DB[NEXT_ID] = new_user
    NEXT_ID += 1
    return jsonify({'message': 'User registered successfully!', 'user_id': new_user['id']}), 201

# =============================
# ENDPOINT DE LOGIN API ORIGINAL
# =============================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    user_match = next((u for u in USERS_DB.values() if u['email'] == email), None)

    if user_match and password == 'teste123':
        token_payload = {
            'user_id': user_match['id'],
            'email': user_match['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'message': 'Login successful!', 'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# =============================
# ENDPOINT VULNERÁVEL (LISTA TUDO)
# =============================
@app.route('/api/users/', methods=['GET'])
@token_required
def list_all_users(current_user):
    user_list = list(USERS_DB.values())
    return jsonify({
        'users': user_list,
        'total': len(user_list),
        'message': 'All users retrieved successfully'
    }), 200

# =============================
# HOME
# =============================
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Alvo 1 - JWT API Vulnerable',
        'endpoints': {
            '/login': 'GET - Tela de login HTML',
            '/check_login': 'POST - Verificação de login HTML',
            '/register': 'POST - Registrar novo usuário',
            '/login': 'POST - Fazer login e receber JWT',
            '/api/users/': 'GET - Listar todos os usuários (requer JWT)'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print(f"🎯 Alvo 1 (JWT API) rodando em http://127.0.0.1:5000")
    print(f"🔑 SECRET KEY: {SECRET_KEY}")
    print("=" * 60)
    print("\n📋 INSTRUÇÕES DE USO:")
    print("1. Use /login para acessar a tela de login HTML")
    print("2. Faça login com qualquer email válido e password='teste123'")
    print("3. Copie o token exibido e use no header Authorization")
    print("4. Acesse /api/users/ com o token para ver TODOS os usuários")
    print("=" * 60)
    app.run(debug=True, port=5000)
