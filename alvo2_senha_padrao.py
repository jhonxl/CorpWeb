# Arquivo: alvo2_senha_padrao.py
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de Dados Fictícia
# 2 usuários com senha padrão, 1 com senha diferente
USERS_DB = {
    'admin': {'username': 'admin', 'password': 'CorpWeb123!', 'name': 'Administrador'},
    'manager': {'username': 'manager', 'password': 'CorpWeb123!', 'name': 'Gerente TI'},
    'jsilva': {'username': 'jsilva', 'password': 'Senhas3gur4!', 'name': 'João Silva'}
}

# Template HTML simples para a tela de login
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            margin-top: 15px;
            padding: 10px;
            border-radius: 4px;
            text-align: center;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 CorpWeb Login</h2>
        <form action="/check_login" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
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

# 1. Endpoint da tela de login
@app.route('/login', methods=['GET'])
def login():
    return render_template_string(LOGIN_TEMPLATE)

# 2. Endpoint VULNERÁVEL - Expõe a senha padrão (Vulnerabilidade 2 - Principal Ponto)
# TOTALMENTE DESPROTEGIDO - Qualquer pessoa pode acessar
@app.route('/default', methods=['GET'])
def default_password():
    # VULNERABILIDADE CRÍTICA: Configuração sensível exposta publicamente
    # Este endpoint não deveria existir ou deveria estar protegido
    return jsonify({
        'default_password': 'CorpWeb123!',
        'message': 'Default password for new accounts',
        'users_with_default': ['admin', 'manager'],
        'warning': 'This endpoint should not be publicly accessible!'
    }), 200

# 3. Endpoint para verificar login (para uso com Hydra)
@app.route('/check_login', methods=['POST'])
def check_login():
    # Aceita tanto form-data quanto JSON
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if not username or not password:
        if request.is_json:
            return jsonify({'message': 'Username and password are required'}), 400
        return render_template_string(LOGIN_TEMPLATE, 
                                     message='Username and password are required',
                                     message_type='error')
    
    # Verifica se o usuário existe e a senha está correta
    user = USERS_DB.get(username)
    
    if user and user['password'] == password:
        if request.is_json:
            return jsonify({
                'message': 'Login Successful',
                'username': username,
                'name': user['name']
            }), 200
        return render_template_string(LOGIN_TEMPLATE,
                                     message=f'Login Successful! Welcome {user["name"]}',
                                     message_type='success')
    
    # Credenciais inválidas
    if request.is_json:
        return jsonify({'message': 'Invalid Credentials'}), 401
    return render_template_string(LOGIN_TEMPLATE,
                                 message='Invalid Credentials',
                                 message_type='error')

# Endpoint adicional para informações
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Alvo 2 - Senha Padrão e Configuração Exposta',
        'endpoints': {
            '/login': 'GET - Tela de login',
            '/check_login': 'POST - Verificar credenciais (form-data ou JSON)',
            '/default': 'GET - ⚠️ VULNERÁVEL - Expõe senha padrão'
        },
        'users': list(USERS_DB.keys()),
        'hint': 'Tente acessar /default para descobrir a senha padrão'
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print(f"🎯 Alvo 2 (Senha Padrão) rodando em http://127.0.0.1:5001")
    print("=" * 60)
    print("\n📋 INSTRUÇÕES DE USO:")
    print("1. Acesse /login para ver a tela de login")
    print("2. Acesse /default para descobrir a senha padrão (VULNERÁVEL!)")
    print("3. Use Hydra para testar brute force em /check_login")
    print("\n👥 USUÁRIOS NO SISTEMA:")
    for user, info in USERS_DB.items():
        uses_default = "✓ (usa senha padrão)" if info['password'] == 'CorpWeb123!' else "✗ (senha diferente)"
        print(f"   - {user}: {info['name']} {uses_default}")
    print("\n⚠️  VULNERABILIDADES:")
    print("- Endpoint /default expõe a senha padrão (sem autenticação)")
    print("- Múltiplos usuários usando senha padrão")
    print("- Informações sobre usuários expostas publicamente")
    print("\n🔨 COMANDO HYDRA DE EXEMPLO:")
    print("hydra -L users.txt -p CorpWeb123! 127.0.0.1 -s 5001 http-post-form")
    print('"/check_login:username=^USER^&password=^PASS^:Invalid Credentials"')
    print("=" * 60)
    app.run(port=5001, debug=True, use_reloader=False)

