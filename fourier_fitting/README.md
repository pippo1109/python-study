# python-study
# First step: Run the libraries configuration file [venv_libraries_config] for update and download the needed packets
# Next: Run the [Fourier_fit.py] and edit when necessary.

#!/usr/bin/env python3
"""
Fourier Series Trend Fitting
Gera uma curva aleatória e fita séries de Fourier com N harmônicos configuráveis.
"""

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                  ★  CONFIGURAÇÕES — edite aqui  ★                       ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║                                                                          ║
# ║  X_EXPR : expressão Python que define o array de pontos x.               ║
# ║           Variáveis disponíveis: np, N_PONTOS                            ║
# ║                                                                          ║
# ║  Y_EXPR : expressão Python que define y em função de x.                  ║
# ║           Variáveis disponíveis: np, x, rng (gerador aleatório)          ║
# ║                                                                          ║
# ║  Exemplos de X_EXPR:                                                     ║
# ║    Linear         → "np.linspace(0, 4*np.pi, N_PONTOS)"                  ║
# ║    Exponencial    → "np.linspace(0, 3, N_PONTOS); x = np.exp(x)"         ║
# ║    Log            → "np.linspace(1, 100, N_PONTOS); x = np.log(x)"       ║
# ║                                                                          ║
# ║  Exemplos de Y_EXPR:                                                     ║
# ║    Polinômio      → "x**3 - 2*x**2 + x"                                  ║
# ║    Trigonométrica → "np.sin(x) + 0.5*np.cos(3*x)"                        ║
# ║    Mista          → "np.sin(x**2) + np.log(np.abs(x) + 1)"               ║
# ║    Com ruído      → "np.sin(x) + rng.normal(0, 0.3, len(x))"             ║
# ║    Aleatória      → use CURVA_ALEATORIA = True abaixo                    ║
# ║                                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

N_HARMONICOS = [1, 3, 8, 10000]   # <- MUDE AQUI

# Parâmetros da curva aleatória
SEED        = 42    # semente do gerador (mude para gerar outra curva)
N_PONTOS    = 500   # quantidade de pontos amostrados
X_MAX       = 4     # domínio: [0, X_MAX * pi]
N_SENOIDES  = 8     # componentes senoidais da curva base
RUIDO_STD   = 0.4   # desvio padrão do ruído gaussiano


# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm

# ══════════════════════════════════════════════════════════════════════════════
# GERACAO DA CURVA ALEATORIA
# ══════════════════════════════════════════════════════════════════════════════

rng = np.random.default_rng(seed=SEED)
x   = np.linspace(0, X_MAX * np.pi, N_PONTOS)
y   = np.zeros(N_PONTOS)

for _ in range(N_SENOIDES):
    y += rng.uniform(0.5, 2.5) * np.sin(
        rng.uniform(0.3, 3.0) * x + rng.uniform(0, 2 * np.pi)
    )
y += rng.normal(0, RUIDO_STD, N_PONTOS)

# ══════════════════════════════════════════════════════════════════════════════
# AJUSTE POR SERIE DE FOURIER
# ══════════════════════════════════════════════════════════════════════════════

def ajustar_fourier(x: np.ndarray, y: np.ndarray, n: int):
    """Retorna (y_ajustado, rmse) para n harmonicos via minimos quadrados."""
    L = x[-1] - x[0]
    t = x - x[0]
    cols = [np.ones(len(x))]
    for k in range(1, n + 1):
        cols.append(np.cos(2 * np.pi * k * t / L))
        cols.append(np.sin(2 * np.pi * k * t / L))
    A = np.column_stack(cols)
    coefs, *_ = np.linalg.lstsq(A, y, rcond=None)
    y_fit = A @ coefs
    rmse  = float(np.sqrt(np.mean((y - y_fit) ** 2)))
    return y_fit, rmse


fits = {n: ajustar_fourier(x, y, n) for n in N_HARMONICOS}

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE CORES — gerada dinamicamente para qualquer quantidade de curvas
# ══════════════════════════════════════════════════════════════════════════════

_palette = cm.get_cmap("plasma", len(N_HARMONICOS) + 2)
CORES = {n: _palette(i + 1) for i, n in enumerate(N_HARMONICOS)}

# ══════════════════════════════════════════════════════════════════════════════
# VISUALIZACAO DINAMICA
# ══════════════════════════════════════════════════════════════════════════════
# Layout:
#   Linha 0 (painel largo) : todas as curvas sobrepostas
#   Linhas seguintes       : paineis individuais em grade de ate 3 colunas

N_CURVAS   = len(N_HARMONICOS)
N_COLS     = min(N_CURVAS, 3)
N_ROWS_SUB = (N_CURVAS + N_COLS - 1) // N_COLS

fig_height = 5 + 3.5 * N_ROWS_SUB
fig = plt.figure(figsize=(16, fig_height), facecolor="#0D1117")

gs = gridspec.GridSpec(
    1 + N_ROWS_SUB, N_COLS,
    figure=fig,
    hspace=0.55, wspace=0.35,
)

# Painel principal
ax_main = fig.add_subplot(gs[0, :])
ax_main.set_facecolor("#161B22")
ax_main.plot(x, y, color="#C9D1D9", lw=0.9, alpha=0.5, label="Curva aleatoria")

for n in N_HARMONICOS:
    y_fit, rmse = fits[n]
    ax_main.plot(x, y_fit, color=CORES[n], lw=1.8, alpha=0.95,
                 label=f"N={n}  (RMSE={rmse:.3f})")

ax_main.set_title("Ajuste por Serie de Fourier — Visao Geral",
                  color="#E6EDF3", fontsize=14, fontweight="bold", pad=12)
ax_main.set_xlabel("x", color="#8B949E")
ax_main.set_ylabel("y", color="#8B949E")
ax_main.tick_params(colors="#8B949E")
for sp in ax_main.spines.values():
    sp.set_edgecolor("#30363D")
ax_main.legend(facecolor="#21262D", edgecolor="#30363D",
               labelcolor="#C9D1D9", fontsize=9,
               loc="upper right", ncols=max(1, N_CURVAS // 5))
ax_main.grid(True, color="#21262D", linewidth=0.7)

# Paineis individuais
for i, n in enumerate(N_HARMONICOS):
    row = 1 + i // N_COLS
    col = i % N_COLS
    ax  = fig.add_subplot(gs[row, col])
    ax.set_facecolor("#161B22")

    y_fit, rmse = fits[n]

    ax.plot(x, y, color="#C9D1D9", lw=0.8, alpha=0.35, label="Curva")
    ax.plot(x, y_fit, color=CORES[n], lw=2.0, label=f"Fourier N={n}")
    ax.fill_between(x, y, y_fit, color=CORES[n], alpha=0.12, label="Residuo")

    ax.set_title(f"N = {n} harmonicos  |  RMSE = {rmse:.3f}",
                 color="#E6EDF3", fontsize=10, pad=7)
    ax.set_xlabel("x", color="#8B949E", fontsize=8)
    ax.set_ylabel("y", color="#8B949E", fontsize=8)
    ax.tick_params(colors="#8B949E", labelsize=7)
    for sp in ax.spines.values():
        sp.set_edgecolor("#30363D")
    ax.legend(facecolor="#21262D", edgecolor="#30363D",
              labelcolor="#C9D1D9", fontsize=7)
    ax.grid(True, color="#21262D", linewidth=0.6)

fig.suptitle("Serie de Fourier como Tendencia de Curva Aleatoria",
             color="#E6EDF3", fontsize=16, fontweight="bold", y=1.01)

plt.savefig("fourier_fit.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("[plot] Grafico salvo em 'fourier_fit.png'")
plt.show()