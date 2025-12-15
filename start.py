import subprocess
import sys
import time
import os

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

def check_files():
    required_files = [
        "alvo1_jwt.py",
        "alvo2_senha_padrao.py"
    ]

    for file in required_files:
        if not os.path.isfile(file):
            print(f"[ERRO] Arquivo não encontrado: {file}")
            sys.exit(1)

def main():
    banner()
    check_files()

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
