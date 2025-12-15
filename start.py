import subprocess
import sys
import time
import webbrowser
import os

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("=" * 46)
    print(" 🧪 CorpWeb Security Lab")
    print("=" * 46)
    print()
    print("Alvo 1 - JWT Fraco (API)")
    print(" 👉 http://127.0.0.1:5000/login")
    print(" 👉 http://127.0.0.1:5000/api/users")
    print()
    print("Alvo 2 - Senha Padrão (Login Web)")
    print(" 👉 http://127.0.0.1:5001/login")
    print()
    print("CTRL+C para encerrar os alvos")
    print("=" * 46)
    print()

def main():
    clear_terminal()
    banner()

    subprocess.Popen([sys.executable, "alvo1_jwt.py"])
    subprocess.Popen([sys.executable, "alvo2_senha_padrao.py"])

    print("[INFO] Iniciando serviços...")
    time.sleep(3)

    print("[INFO] Abrindo navegador no Alvo 1 (JWT)...")
    webbrowser.open("http://127.0.0.1:5000/login")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Encerrando CorpWeb Security Lab.")

if __name__ == "__main__":
    main()
