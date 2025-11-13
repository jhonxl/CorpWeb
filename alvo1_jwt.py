# Arquivo: alvo1_jwt_api.py
from flask import Flask, request, jsonify
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

# Decorador para validar o JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Espera: 'Bearer <token>'
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Tenta decodificar o token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Aqui você obteria o usuário logado se fosse um sistema real
            current_user = USERS_DB.get(data['user_id']) 
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# 1. Endpoint de Registro (Vulnerabilidade 1A)
@app.route('/register', methods=['POST'])
def register():
    global NEXT_ID
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    new_user = {
        "id": NEXT_ID,
        "email": data.get('email'),
        "password_hash": "mocked_hash_for_" + data.get('password'),  # Mocked hash
        "name": data.get('name', 'Novo Usuario'),
        "role": "user"
    }
    USERS_DB[NEXT_ID] = new_user
    NEXT_ID += 1
    return jsonify({'message': 'User registered successfully!', 'user_id': new_user['id']}), 201

# 2. Endpoint de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  # Senha fictícia para login
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    # Simula a checagem de credenciais (apenas para fins de lab)
    user_match = next((u for u in USERS_DB.values() if u['email'] == email), None)

    # Se o usuário existir e a senha for 'teste123' (fictício)
    if user_match and password == 'teste123': 
        # Payload do JWT - O que o atacante verá
        token_payload = {
            'user_id': user_match['id'],
            'email': user_match['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'message': 'Login successful!', 'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# 3. Endpoint Vulnerável (Vulnerabilidade 1B - Principal Ponto)
# BROKEN ACCESS CONTROL: A função é protegida por token, mas retorna TODOS os usuários
# Não verifica se o usuário tem permissão de admin para listar todos os usuários
@app.route('/api/users/', methods=['GET'])
@token_required
def list_all_users(current_user):
    # VULNERABILIDADE: Um usuário comum (current_user) consegue listar todos.
    # Não há verificação de role/permissão (ex: if current_user['role'] != 'admin')
    user_list = list(USERS_DB.values())
    
    # Retorna todos os dados, simulando a enumeração e vazamento
    # Inclui hashes de senha, emails, roles, etc.
    return jsonify({
        'users': user_list,
        'total': len(user_list),
        'message': 'All users retrieved successfully'
    }), 200

# Endpoint adicional para teste
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Alvo 1 - JWT API Vulnerable',
        'endpoints': {
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
    print("1. Faça login em /login com email e password='teste123'")
    print("2. Use o token JWT recebido no header Authorization")
    print("3. Acesse /api/users/ com o token para ver TODOS os usuários")
    print("\n⚠️  VULNERABILIDADES:")
    print("- SECRET_KEY fraca e exposta")
    print("- Broken Access Control: qualquer usuário autenticado pode listar todos")
    print("- Exposição de dados sensíveis (password_hash)")
    print("=" * 60)
    app.run(debug=True, port=5000)
