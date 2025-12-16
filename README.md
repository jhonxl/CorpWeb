
---
# 🧪 Lab de Pentest: Combo VAZAMENTO JWT + SENHA PADRÃO (Python/Flask)

Este repositório contém o código-fonte de duas aplicações Flask (Python) simulando um ambiente de **Pentest Fictício** chamado **CorpWeb Security Lab**.

O objetivo do lab é demonstrar uma metodologia que combina:

- **Enumeração de usuários via JWT**
- **Brute force direcionado** em um segundo alvo com **senha padrão**

---

## ⚠️ AVISO LEGAL E ÉTICO (IMPORTANTE)

Este código foi criado **EXCLUSIVAMENTE PARA FINS EDUCACIONAIS E DE ESTUDO**.

- Todo uso deve seguir princípios legais e éticos (*white hat*).

---

## 🛠️ Requisitos

- **Python 3.10+**
- Linux, Windows ou macOS

> ⚠️ **Não é necessário Docker**  
> ⚠️ **Ambiente virtual (`venv`) é opcional**

---

## 🚀 Instalação (Simples e Direto)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/jhonxl/CorpWeb
cd CorpWeb
````

---

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

> Se ocorrer erro de permissão:

```bash
pip install --user -r requirements.txt
```

---

## ▶️ Executar o Lab (UM comando)

### Linux / macOS

```bash
python start.py
```

### Windows

```bat
python start.py
```

ou simplesmente, após extrair os arquivos, dê dois cliques no:

```bat
start.bat
```

Ao executar, o navegador será aberto automaticamente com os alvos do lab.

---

## 🌐 Alvos Disponíveis

| Alvo   | Descrição              | Base URL                                       |
| ------ | ---------------------- | ---------------------------------------------- |
| Alvo 1 | API JWT vulnerável     | [http://127.0.0.1:5000](http://127.0.0.1:5000) |
| Alvo 2 | Login com senha padrão | [http://127.0.0.1:5001](http://127.0.0.1:5001) |

---

## ▶️ Como começar o Lab

---

## 🔹 Alvo 1 – JWT Vulnerable API

**Base URL:** `http://127.0.0.1:5000`

**Endpoints principais:**

* `GET /` → Página inicial com dica do lab
* `GET /login` → Formulário HTML de login
* `POST /login` → Login via API (JSON)
* `GET /api/users/` → Endpoint protegido (JWT)

---

### 🔑 Credenciais iniciais do Lab (Alvo 1)

**Login que você recebe: **

```
jsantos@corpweb.lab
teste123
```

**Usuários válidos:**

* `admin@corpweb.lab`
* `jsantos@corpweb.lab`
* `jsilva@corpweb.lab`

---

### ▶️ Fluxo sugerido (Alvo 1)

1. Acesse `http://127.0.0.1:5000/login`
2. Faça login com um dos emails válidos e a senha fixa
3. Após o login, abra o **Console do Navegador (F12)**
   → O token JWT será exibido **apenas no console**
4. Utilize o token para acessar endpoints
---

## 🔹 Alvo 2 – Senha Padrão

**Base URL:** `http://127.0.0.1:5001`

**Endpoints principais:**

* `GET /login` → Tela de login web
* `GET /default` → Exposição da senha padrão (**vulnerável**)
* `POST /check_login` → Validação de login (alvo de brute force)

---

### ▶️ Objetivo (Alvo 2)

Explorar a **senha padrão exposta** para realizar brute force direcionado
utilizando os usuários obtidos no **Alvo 1**.

As instruções completas e usuários disponíveis são exibidos no **console**
ao iniciar o alvo.

---

## 🧠 Observação Importante

A **facilidade de execução não reduz a dificuldade do lab**.

O atacante ainda precisa:

* Entender JWT
* Identificar onde o token é exposto
* Enumerar usuários
* Correlacionar dados entre dois sistemas
* Explorar falhas lógicas reais

---

## 🧪 Finalidade

Este lab é indicado para:

* Estudos de Pentest
* Treinamento ofensivo

