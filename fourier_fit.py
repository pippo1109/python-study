#!/usr/bin/env python3
"""
Fourier Series Trend Fitting
Gera uma curva aleatória e fita uma série de Fourier como reta de tendência.
"""

import subprocess
import sys
import os

# ─────────────────────────────────────────────
# 1. CRIAÇÃO E ATIVAÇÃO DO AMBIENTE VIRTUAL
# ─────────────────────────────────────────────

VENV_DIR = "venv_fourier"

def criar_venv():
    """Cria o ambiente virtual se ainda não existir."""
    if not os.path.isdir(VENV_DIR):
        print(f"[setup] Criando ambiente virtual em '{VENV_DIR}'...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("[setup] Ambiente virtual criado com sucesso.")
    else:
        print(f"[setup] Ambiente virtual '{VENV_DIR}' já existe. Pulando criação.")


def pip_executavel():
    """Retorna o caminho do pip dentro do venv."""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")


def python_executavel():
    """Retorna o caminho do python dentro do venv."""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def instalar_dependencias():
    """Instala / atualiza as bibliotecas necessárias no venv."""
    pip = pip_executavel()
    pacotes = [
        "numpy>=2.0",
        "matplotlib>=3.9",
        "scipy>=1.14",
    ]
    print("[setup] Atualizando pip...")
    subprocess.check_call([pip, "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
    print(f"[setup] Instalando pacotes: {', '.join(pacotes)}")
    subprocess.check_call([pip, "install", "--upgrade"] + pacotes, stdout=subprocess.DEVNULL)
    print("[setup] Dependências instaladas com sucesso.\n")


def reexecutar_no_venv():
    """
    Se o script não estiver rodando dentro do venv, reinicia usando
    o interpretador do venv para garantir acesso às bibliotecas.
    """
    python_venv = os.path.abspath(python_executavel())
    python_atual = os.path.abspath(sys.executable)

    if python_atual != python_venv:
        print(f"[setup] Reiniciando com o Python do venv: {python_venv}\n")
        os.execv(python_venv, [python_venv] + sys.argv)


# ─────────────────────────────────────────────
# SETUP: executa só quando necessário
# ─────────────────────────────────────────────
criar_venv()
instalar_dependencias()
reexecutar_no_venv()

# ─────────────────────────────────────────────
# 2. IMPORTS (após garantir que estamos no venv)
# ─────────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import CubicSpline

# ─────────────────────────────────────────────
# 3. GERAÇÃO DA CURVA ALEATÓRIA
# ─────────────────────────────────────────────

rng = np.random.default_rng(seed=42)

N = 500                          # pontos da curva
x = np.linspace(0, 4 * np.pi, N)

# Superposição de senoides com amplitudes/frequências/fases aleatórias + ruído
n_componentes = 8
y = np.zeros(N)
for _ in range(n_componentes):
    amp   = rng.uniform(0.5, 2.5)
    freq  = rng.uniform(0.3, 3.0)
    fase  = rng.uniform(0, 2 * np.pi)
    y    += amp * np.sin(freq * x + fase)

y += rng.normal(0, 0.4, N)      # ruído gaussiano

# ─────────────────────────────────────────────
# 4. AJUSTE POR SÉRIE DE FOURIER
# ─────────────────────────────────────────────

def ajustar_fourier(x: np.ndarray, y: np.ndarray, n_harmonicos: int) -> np.ndarray:
    """
    Fita uma série de Fourier truncada em n_harmonicos usando mínimos quadrados.

    A base é:
        f(x) = a0/2
             + Σ_{k=1}^{n} [ a_k * cos(2πkx/L) + b_k * sin(2πkx/L) ]

    Retorna os valores ajustados em x.
    """
    L = x[-1] - x[0]   # comprimento do domínio
    t = x - x[0]       # normaliza para começar em 0

    # Monta a matriz de design
    colunas = [np.ones(len(x))]        # termo a0/2
    for k in range(1, n_harmonicos + 1):
        colunas.append(np.cos(2 * np.pi * k * t / L))
        colunas.append(np.sin(2 * np.pi * k * t / L))

    A = np.column_stack(colunas)

    # Resolve por mínimos quadrados (lstsq é numericamente estável)
    coefs, *_ = np.linalg.lstsq(A, y, rcond=None)

    return A @ coefs, coefs, L, x[0]


N_HARMONICOS = [1, 3, 8, 20]   # diferentes graus de ajuste para comparação

fits = {}
for n in N_HARMONICOS:
    y_fit, coefs, L, x0 = ajustar_fourier(x, y, n)
    residuos = y - y_fit
    rmse = np.sqrt(np.mean(residuos**2))
    fits[n] = {"y_fit": y_fit, "rmse": rmse}

# ─────────────────────────────────────────────
# 5. VISUALIZAÇÃO
# ─────────────────────────────────────────────

CORES = {
    1:  "#FF6B6B",
    3:  "#FFD93D",
    8:  "#6BCB77",
    20: "#4D96FF",
}

fig = plt.figure(figsize=(16, 10), facecolor="#0D1117")
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# ── Painel principal (linha completa superior) ───────────────────────────────
ax_main = fig.add_subplot(gs[0, :])
ax_main.set_facecolor("#161B22")

ax_main.plot(x, y, color="#C9D1D9", lw=0.8, alpha=0.55, label="Curva aleatória")

for n, cor in CORES.items():
    ax_main.plot(x, fits[n]["y_fit"],
                 color=cor, lw=1.8, alpha=0.9,
                 label=f"Fourier N={n}  (RMSE={fits[n]['rmse']:.3f})")

ax_main.set_title("Ajuste por Série de Fourier — Visão Geral",
                   color="#E6EDF3", fontsize=14, fontweight="bold", pad=12)
ax_main.set_xlabel("x", color="#8B949E")
ax_main.set_ylabel("y", color="#8B949E")
ax_main.tick_params(colors="#8B949E")
for spine in ax_main.spines.values():
    spine.set_edgecolor("#30363D")
ax_main.legend(facecolor="#21262D", edgecolor="#30363D",
               labelcolor="#C9D1D9", fontsize=9, loc="upper right")
ax_main.grid(True, color="#21262D", linewidth=0.7)

# ── Painéis individuais (linha inferior) ─────────────────────────────────────
pares = [(0, 1), (0, 3), (1, 8), (1, 20)]
subplots = [
    fig.add_subplot(gs[1, 0]),
    fig.add_subplot(gs[1, 1]),
]

for idx, (col, n) in enumerate([(0, 3), (1, 20)]):
    ax = subplots[idx]
    ax.set_facecolor("#161B22")

    ax.plot(x, y, color="#C9D1D9", lw=0.8, alpha=0.4, label="Curva")
    ax.plot(x, fits[n]["y_fit"],
            color=CORES[n], lw=2.0,
            label=f"Fourier N={n}")

    # Área de erro
    ax.fill_between(x, y, fits[n]["y_fit"],
                    color=CORES[n], alpha=0.12, label="Resíduo")

    ax.set_title(f"N = {n} harmônicos  |  RMSE = {fits[n]['rmse']:.3f}",
                  color="#E6EDF3", fontsize=11, pad=8)
    ax.set_xlabel("x", color="#8B949E", fontsize=9)
    ax.set_ylabel("y", color="#8B949E", fontsize=9)
    ax.tick_params(colors="#8B949E", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363D")
    ax.legend(facecolor="#21262D", edgecolor="#30363D",
               labelcolor="#C9D1D9", fontsize=8)
    ax.grid(True, color="#21262D", linewidth=0.6)

# ── Título geral ─────────────────────────────────────────────────────────────
fig.suptitle("Série de Fourier como Tendência de Curva Aleatória",
             color="#E6EDF3", fontsize=16, fontweight="bold", y=1.01)

plt.savefig("fourier_fit.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("[plot] Gráfico salvo em 'fourier_fit.png'")
plt.show()