from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

USERS_DB = {
    'admin': {'username': 'admin', 'password': 'CorpWeb123!', 'name': 'Administrador'},
    'manager': {'username': 'manager', 'password': 'CorpWeb123!', 'name': 'Gerente TI'},
    'jsilva': {'username': 'jsilva', 'password': 'Senhas3gur4!', 'name': 'João Silva'}
}

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CorpWeb - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
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
            border-color: #2193b0;
            box-shadow: 0 0 0 3px rgba(33, 147, 176, 0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
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
            box-shadow: 0 10px 20px rgba(33, 147, 176, 0.4);
        }
        button:active {
            transform: translateY(0);
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
        .success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
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
        <h2>🔐 CorpWeb Login</h2>
        <form action="/check_login" method="POST">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Digite seu username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Digite sua senha" required>
            </div>
            <button type="submit">Entrar</button>
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

SUCCESS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Realizado - CorpWeb</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
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
        .actions {
            margin-top: 30px;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 5px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(33, 147, 176, 0.4);
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="check-icon">✓</div>
        <h2>Login Realizado!</h2>
        <p class="welcome-text">Bem-vindo(a) ao sistema</p>
        <div class="user-info">
            <p><strong>👤 Nome:</strong> {{ name }}</p>
            <p><strong>🔑 Username:</strong> {{ username }}</p>
        </div>
        <div class="actions">
            <a href="/login" class="btn btn-secondary">← Voltar ao Login</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/login', methods=['GET'])
def login():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/default', methods=['GET'])
def default_password():
    return jsonify({
        'default_password': 'CorpWeb123!',
        'message': 'Default password for new accounts',
        'users_with_default': ['admin', 'manager'],
        'warning': 'This endpoint should not be publicly accessible!'
    }), 200

@app.route('/check_login', methods=['POST'])
def check_login():
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
                                     message='Username e password são obrigatórios',
                                     message_type='error')
    
    user = USERS_DB.get(username)
    
    if user and user['password'] == password:
        if request.is_json:
            return jsonify({
                'message': 'Login Successful',
                'username': username,
                'name': user['name']
            }), 200
        return render_template_string(SUCCESS_TEMPLATE,
                                     username=username,
                                     name=user['name'])
    
    if request.is_json:
        return jsonify({'message': 'Invalid Credentials'}), 401
    return render_template_string(LOGIN_TEMPLATE,
                                 message='Credenciais inválidas',
                                 message_type='error')

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
    app.run(port=5001, debug=False)
