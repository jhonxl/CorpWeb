from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

USERS_DB = {
    'admin': {'username': 'admin', 'password': 'CorpWeb123!', 'name': 'Administrador'},
    'manager': {'username': 'manager', 'password': 'CorpWeb123!', 'name': 'Gerente TI'},
    'jsilva': {'username': 'jsilva', 'password': 'Senhas3gur4!', 'name': 'João Silva'}
}

# Configurações que o admin pode alterar
SYSTEM_CONFIG = {
    'theme_color1': '#2193b0',
    'theme_color2': '#6dd5ed',
    'system_message': 'Sistema operando normalmente',
    'message_active': False
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
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        {% if show_message %}
        .system-banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff9800;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: 600;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideDown 0.5s ease-out;
        }
        @keyframes slideDown {
            from { transform: translateY(-100%); }
            to { transform: translateY(0); }
        }
        {% endif %}
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
            border-color: {{ color1 }};
            box-shadow: 0 0 0 3px rgba(33, 147, 176, 0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
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
    {% if show_message %}
    <div class="system-banner">
         {{ system_message }}
    </div>
    {% endif %}
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
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
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
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
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
        .btn-admin {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-admin:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(240, 147, 251, 0.4);
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
            {% if is_admin %}
            <a href="/admin/panel" class="btn btn-admin"> Painel Admin</a>
            {% endif %}
            <a href="/login" class="btn btn-secondary">← Voltar ao Login</a>
        </div>
    </div>
</body>
</html>
'''

ADMIN_PANEL_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Painel Admin - CorpWeb</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            animation: slideDown 0.5s ease-out;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .congratulations {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .congratulations h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .congratulations p {
            font-size: 16px;
            opacity: 0.9;
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .card h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            color: #555;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 14px;
        }
        input[type="text"], input[type="color"] {
            width: 100%;
            padding: 10px 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }
        input[type="color"] {
            height: 45px;
            cursor: pointer;
        }
        input:focus {
            outline: none;
            border-color: {{ color1 }};
            box-shadow: 0 0 0 3px rgba(33, 147, 176, 0.1);
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, {{ color1 }} 0%, {{ color2 }} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(33, 147, 176, 0.4);
        }
        .user-list {
            list-style: none;
        }
        .user-item {
            background: #f8f9fa;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }
        .user-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .user-item strong {
            color: #333;
        }
        .user-item span {
            color: #666;
            font-size: 13px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-box h4 {
            font-size: 32px;
            margin-bottom: 5px;
        }
        .stat-box p {
            font-size: 13px;
            opacity: 0.9;
        }
        .back-btn {
            display: inline-block;
            padding: 12px 30px;
            background: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .back-btn:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #28a745;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="congratulations">
                <h1> PARABÉNS, ADMINISTRADOR!</h1>
                <p>Você conseguiu explorar o Alvo 2 e acessar a conta admin com sucesso!</p>
                <p><strong>Vulnerabilidade explorada:</strong> Senha padrão exposta no endpoint e usuário admin com senha padrão /default</p>
            </div>
            <h2> Painel Administrativo</h2>
            <p style="color: #666;">Gerencie as configurações do sistema CorpWeb</p>
        </div>

        <div class="grid">
            <!-- Card de Tema -->
            <div class="card">
                <h3> Personalização de Tema</h3>
                {% if success_theme %}
                <div class="success-message">✓ Tema atualizado com sucesso!</div>
                {% endif %}
                <form action="/admin/update_theme" method="POST">
                    <div class="form-group">
                        <label>Cor do Gradiente 1</label>
                        <input type="color" name="color1" value="{{ color1 }}" required>
                    </div>
                    <div class="form-group">
                        <label>Cor do Gradiente 2</label>
                        <input type="color" name="color2" value="{{ color2 }}" required>
                    </div>
                    <button type="submit">Aplicar Tema</button>
                </form>
            </div>

            <!-- Card de Mensagem do Sistema -->
            <div class="card">
                <h3> Mensagem do Sistema</h3>
                {% if success_message %}
                <div class="success-message">✓ Mensagem atualizada!</div>
                {% endif %}
                <form action="/admin/update_message" method="POST">
                    <div class="form-group">
                        <label>Mensagem de Aviso</label>
                        <input type="text" name="message" value="{{ system_message }}" placeholder="Digite a mensagem" required>
                    </div>
                    <div class="checkbox-group">
                        <input type="checkbox" name="active" id="active" {{ 'checked' if message_active else '' }}>
                        <label for="active" style="margin: 0;">Exibir banner na página de login</label>
                    </div>
                    <button type="submit">Atualizar Mensagem</button>
                </form>
            </div>

            <!-- Card de Estatísticas -->
            <div class="card">
                <h3> Estatísticas do Sistema</h3>
                <div class="stats">
                    <div class="stat-box">
                        <h4>3</h4>
                        <p>Usuários Ativos</p>
                    </div>
                    <div class="stat-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <h4>2</h4>
                        <p>Senhas Padrão</p>
                    </div>
                    <div class="stat-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <h4>100%</h4>
                        <p>Vulnerável</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Card de Lista de Usuários -->
        <div class="card">
            <h3> Usuários Cadastrados</h3>
            <ul class="user-list">
                {% for user in users %}
                <li class="user-item">
                    <div>
                        <strong>{{ user.name }}</strong><br>
                        <span>@{{ user.username }}</span>
                    </div>
                    <span style="{% if user.has_default %}color: #dc3545; font-weight: 600;{% else %}color: #28a745; font-weight: 600;{% endif %}">
                        {% if user.has_default %} Senha Padrão{% else %}✓ Senha Forte{% endif %}
                    </span>
                </li>
                {% endfor %}
            </ul>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/logout" class="back-btn">← Sair do Painel</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/login', methods=['GET'])
def login():
    return render_template_string(LOGIN_TEMPLATE,
                                 color1=SYSTEM_CONFIG['theme_color1'],
                                 color2=SYSTEM_CONFIG['theme_color2'],
                                 show_message=SYSTEM_CONFIG['message_active'],
                                 system_message=SYSTEM_CONFIG['system_message'])

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
                                     message_type='error',
                                     color1=SYSTEM_CONFIG['theme_color1'],
                                     color2=SYSTEM_CONFIG['theme_color2'],
                                     show_message=SYSTEM_CONFIG['message_active'],
                                     system_message=SYSTEM_CONFIG['system_message'])
    
    user = USERS_DB.get(username)
    
    if user and user['password'] == password:
        # Criar sessão
        session['username'] = username
        session['name'] = user['name']
        session['is_admin'] = (username == 'admin')
        
        if request.is_json:
            return jsonify({
                'message': 'Login Successful',
                'username': username,
                'name': user['name']
            }), 200
        return render_template_string(SUCCESS_TEMPLATE,
                                     username=username,
                                     name=user['name'],
                                     is_admin=(username == 'admin'),
                                     color1=SYSTEM_CONFIG['theme_color1'],
                                     color2=SYSTEM_CONFIG['theme_color2'])
    
    if request.is_json:
        return jsonify({'message': 'Invalid Credentials'}), 401
    return render_template_string(LOGIN_TEMPLATE,
                                 message='Credenciais inválidas',
                                 message_type='error',
                                 color1=SYSTEM_CONFIG['theme_color1'],
                                 color2=SYSTEM_CONFIG['theme_color2'],
                                 show_message=SYSTEM_CONFIG['message_active'],
                                 system_message=SYSTEM_CONFIG['system_message'])

@app.route('/admin/panel')
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users_list = []
    for username, user in USERS_DB.items():
        users_list.append({
            'username': username,
            'name': user['name'],
            'has_default': user['password'] == 'CorpWeb123!'
        })
    
    return render_template_string(ADMIN_PANEL_TEMPLATE,
                                 color1=SYSTEM_CONFIG['theme_color1'],
                                 color2=SYSTEM_CONFIG['theme_color2'],
                                 system_message=SYSTEM_CONFIG['system_message'],
                                 message_active=SYSTEM_CONFIG['message_active'],
                                 users=users_list,
                                 success_theme=request.args.get('theme') == 'success',
                                 success_message=request.args.get('msg') == 'success')

@app.route('/admin/update_theme', methods=['POST'])
def update_theme():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    SYSTEM_CONFIG['theme_color1'] = request.form.get('color1', '#2193b0')
    SYSTEM_CONFIG['theme_color2'] = request.form.get('color2', '#6dd5ed')
    
    return redirect(url_for('admin_panel', theme='success'))

@app.route('/admin/update_message', methods=['POST'])
def update_message():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    SYSTEM_CONFIG['system_message'] = request.form.get('message', 'Sistema operando normalmente')
    SYSTEM_CONFIG['message_active'] = 'active' in request.form
    
    return redirect(url_for('admin_panel', msg='success'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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
    print("\n🎉 BONUS:")
    print("- Logue como 'admin' para acessar o painel administrativo!")
    print("=" * 60)
    app.run(port=5001, debug=False)
