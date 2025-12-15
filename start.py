import subprocess
import sys
import time
import os

REQUIREMENTS = "requirements.txt"

def banner():
    print("""
==============================================
 🧪 CorpWeb Security Lab
==============================================

Alvo 1 - JWT Fraco (API):
  http://127.0.0.1:5000

Alvo 2 - Senha Padrão (Login Web):
  http://127.0.0.1:5001

CTRL+C para encerrar os alvos
==============================================
""")

def check_requirements():
    if not os.path.isfile(REQUIREMENTS):
        print("[ERRO] requirements.txt não encontrado.")
        sys.exit(1)

    try:
        import flask
        import jwt
    except ImportError:
        print("[INFO] Dependências não encontradas. Instalando automaticamente...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS]
        )

def check_files():
    files = ["alvo1_jwt.py", "alvo2_senha_padrao.py"]
    for f in files:
        if not os.path.isfile(f):
            print(f"[ERRO] Arquivo ausente: {f}")
            sys.exit(1)

def main():
    banner()
    check_files()
    check_requirements()

    try:
        subprocess.Popen([sys.executable, "alvo1_jwt.py"])
        subprocess.Popen([sys.executable, "alvo2_senha_padrao.py"])

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Encerrando o lab...")
        sys.exit(0)

    except Exception as e:
        print("[ERRO] Falha ao iniciar os alvos:", e)

if __name__ == "__main__":
    main()
