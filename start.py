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

    # Inicia Alvo 1
    subprocess.Popen(
        [sys.executable, "alvo1_jwt.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Pequena pausa para garantir que a porta 5000 suba primeiro
    time.sleep(2)

    # Inicia Alvo 2
    subprocess.Popen(
        [sys.executable, "alvo2_senha_padrao.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Aguarda e abre o navegador no ALVO 1
    time.sleep(2)
    print("[INFO] Abrindo navegador no Alvo 1 (JWT)...")
    webbrowser.open("http://127.0.0.1:5000/login")

    # Mantém o script vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Encerrando CorpWeb Security Lab.")

if __name__ == "__main__":
    main()
