import subprocess
import sys
import time
import webbrowser
import os
import socket

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

def wait_for_port(host, port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def main():
    clear_terminal()
    banner()

    # Inicia Alvo 1
    subprocess.Popen(
        [sys.executable, "alvo1_jwt.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Inicia Alvo 2
    subprocess.Popen(
        [sys.executable, "alvo2_senha_padrao.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 🔑 Tempo para o Flask inicializar corretamente (especialmente no Windows)
    time.sleep(2)

    print("[INFO] Aguardando Alvo 1 ficar disponível...")

    if wait_for_port("127.0.0.1", 5000, timeout=30):
        print("[INFO] Abrindo navegador no Alvo 1 (JWT)...")
        webbrowser.open("http://127.0.0.1:5000/login")
    else:
        print("[ERRO] Alvo 1 não respondeu a tempo.")
        return

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Encerrando CorpWeb Security Lab.")

if __name__ == "__main__":
    main()
