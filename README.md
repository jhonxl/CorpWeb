
````md
# 🧪 Lab de Pentest: Combo VAZAMENTO JWT + SENHA PADRÃO (Python/Flask)

Este repositório contém o código-fonte de duas aplicações Flask (Python) simulando um ambiente de **Pentest Fictício** chamado **CorpWeb Security Lab**.

O objetivo do lab é demonstrar uma metodologia que combina:
- **Enumeração de usuários via JWT**
- **Brute force direcionado** em um segundo alvo com **senha padrão**

---

## ⚠️ AVISO LEGAL E ÉTICO (IMPORTANTE)

Este código foi criado **EXCLUSIVAMENTE PARA FINS EDUCACIONAIS E DE ESTUDO**.

- **Não utilize este código** para atacar sistemas reais sem autorização.
- Todo uso deve seguir princípios legais e éticos (*white hat*).

---

## 🛠️ Requisitos

- **Python 3.10+**
- Linux, Windows ou macOS

> ⚠️ Não é necessário Docker  
> ⚠️ Ambiente virtual (`venv`) é opcional

---

## 🚀 Instalação (Simples e Direto)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/jhonxl/CorpWeb
cd CorpWeb
````

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

> Se ocorrer erro de permissão, use:

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

ou simplesmente:

```bat
start.bat
```

---

## 🌐 Alvos Disponíveis

| Alvo   | Descrição              | URL                                            |
| ------ | ---------------------- | ---------------------------------------------- |
| Alvo 1 | API JWT vulnerável     | [http://127.0.0.1:5000](http://127.0.0.1:5000) |
| Alvo 2 | Login com senha padrão | [http://127.0.0.1:5001](http://127.0.0.1:5001) |

---

## 🎯 Alvo 1: MyCorpWeb – JWT Fraco

**Base URL:** `http://127.0.0.1:5000`

Este alvo simula uma API REST vulnerável.
Todas as interações são feitas via requisições HTTP (não há formulário web).

### Login (POST `/login`)

```bash
# Credenciais padrão do lab
user1@corpweb.lab : teste123
```


---

## 🧠 Observação Importante

A **facilidade de execução não reduz a dificuldade do lab**.

O atacante ainda precisa:

* Entender JWT
* Enumerar usuários
* Criar um brute force inteligente
* Explorar falhas lógicas reais

---

## 🧪 Finalidade

Este lab é ideal para:

* Estudos de Pentest
* Treinamento ofensivo

```

