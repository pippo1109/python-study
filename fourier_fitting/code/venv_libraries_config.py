#!/usr/bin/env python3

import subprocess
import sys
import os

# ══════════════════════════════════════════════════════════════════════════════
# SETUP DO AMBIENTE VIRTUAL
# ══════════════════════════════════════════════════════════════════════════════

VENV_DIR = "venv_fourier"


def criar_venv():
    if not os.path.isdir(VENV_DIR):
        print(f"[setup] Criando ambiente virtual em '{VENV_DIR}'...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("[setup] Ambiente virtual criado.")
    else:
        print(f"[setup] Venv '{VENV_DIR}' ja existe. Pulando criacao.")


def python_venv():
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def instalar_dependencias():
    pv = python_venv()
    pacotes = ["numpy>=2.0", "matplotlib>=3.9", "scipy>=1.14"]
    print("[setup] Atualizando pip...")
    subprocess.check_call(
        [pv, "-m", "pip", "install", "--upgrade", "pip"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"[setup] Instalando: {', '.join(pacotes)}")
    subprocess.check_call(
        [pv, "-m", "pip", "install", "--upgrade"] + pacotes,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("[setup] Dependencias prontas.\n")


def reexecutar_no_venv():
    pv = os.path.abspath(python_venv())
    if os.path.abspath(sys.executable) != pv:
        print(f"[setup] Reiniciando com o Python do venv: {pv}\n")
        os.execv(pv, [pv] + sys.argv)


criar_venv()
instalar_dependencias()
reexecutar_no_venv()
