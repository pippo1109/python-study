#!/usr/bin/env python3
"""
Fourier Series Trend Fitting
Fita séries de Fourier sobre qualquer função definida pelo usuário.
"""
# ── Eixo X ───────────────────────────────────────────────────────────────────
X_EXPR = "np.linspace(0, 6*np.pi, N_PONTOS)"

# ── Função Y ──────────────────────────────────────────────────────────────────
# Defina y em termos de x. Use 'rng' para aleatoriedade reprodutível.
Y_EXPR = "np.sign(np.sin(x))"

# ── Harmônicos ────────────────────────────────────────────────────────────────
N_HARMONICOS = [1000]   # <- adicione ou remova valores à vontade

# ── Parâmetros gerais ─────────────────────────────────────────────────────────
N_PONTOS  = 500   # número de pontos amostrados (afeta X_EXPR via variável)
SEED      = 42    # semente para reprodutibilidade (afeta rng em Y_EXPR)

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

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm

# ══════════════════════════════════════════════════════════════════════════════
# AVALIAÇÃO DAS EXPRESSÕES DO USUÁRIO
# ══════════════════════════════════════════════════════════════════════════════

rng = np.random.default_rng(seed=SEED)

_ctx_x = {"np": np, "N_PONTOS": N_PONTOS}
try:
    # Permite multi-linha em X_EXPR (ex: "x = np.linspace(...)\nx = np.exp(x)")
    if "\n" in X_EXPR or ";" in X_EXPR:
        _ns = {"np": np, "N_PONTOS": N_PONTOS}
        exec(X_EXPR.replace(";", "\n"), _ns)
        x = _ns["x"]
    else:
        x = eval(X_EXPR, _ctx_x)
    x = np.asarray(x, dtype=float)
except Exception as e:
    raise ValueError(f"[erro] X_EXPR invalida: '{X_EXPR}'\n  → {e}") from e

if x.ndim != 1 or len(x) < 2:
    raise ValueError(
        f"[erro] X_EXPR deve gerar um array 1-D com pelo menos 2 pontos. "
        f"Resultado: shape={x.shape}"
    )

_ctx_y = {"np": np, "x": x, "rng": rng}
try:
    y = np.asarray(eval(Y_EXPR, _ctx_y), dtype=float)
except Exception as e:
    raise ValueError(f"[erro] Y_EXPR invalida: '{Y_EXPR}'\n  → {e}") from e

if y.shape != x.shape:
    raise ValueError(
        f"[erro] Y_EXPR gerou shape {y.shape}, mas x tem shape {x.shape}. "
        f"Certifique-se de que Y_EXPR retorna um array do mesmo tamanho que x."
    )

print(f"[info] x: {len(x)} pontos  |  x in [{x.min():.4g}, {x.max():.4g}]")
print(f"[info] y: min={y.min():.4g}  max={y.max():.4g}  std={y.std():.4g}")

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


print(f"[info] Calculando {len(N_HARMONICOS)} ajuste(s): N={N_HARMONICOS} ...")
fits = {}
for n in N_HARMONICOS:
    print(f"  → N={n} harmonicos...", end=" ", flush=True)
    fits[n] = ajustar_fourier(x, y, n)
    print(f"RMSE={fits[n][1]:.4f}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE CORES DINAMICA
# ══════════════════════════════════════════════════════════════════════════════

_palette = cm.get_cmap("plasma", len(N_HARMONICOS) + 2)
CORES = {n: _palette(i + 1) for i, n in enumerate(N_HARMONICOS)}

# ══════════════════════════════════════════════════════════════════════════════
# VISUALIZACAO
# ══════════════════════════════════════════════════════════════════════════════

N_CURVAS   = len(N_HARMONICOS)
N_COLS     = min(N_CURVAS, 3)
N_ROWS_SUB = (N_CURVAS + N_COLS - 1) // N_COLS

fig = plt.figure(figsize=(16, 5 + 3.5 * N_ROWS_SUB), facecolor="#0D1117")
gs  = gridspec.GridSpec(1 + N_ROWS_SUB, N_COLS, figure=fig,
                        hspace=0.55, wspace=0.35)

# Painel principal — visão geral
ax_main = fig.add_subplot(gs[0, :])
ax_main.set_facecolor("#161B22")
ax_main.plot(x, y, color="#C9D1D9", lw=0.9, alpha=0.5, label="Função original")

_titulo_y = Y_EXPR if len(Y_EXPR) <= 55 else Y_EXPR[:52] + "..."
ax_main.set_title(f"y = {_titulo_y}",
                  color="#8B949E", fontsize=10, pad=4)
ax_main.set_xlabel("x", color="#8B949E")
ax_main.set_ylabel("y", color="#8B949E")
ax_main.tick_params(colors="#8B949E")
for sp in ax_main.spines.values():
    sp.set_edgecolor("#30363D")
ax_main.legend(facecolor="#21262D", edgecolor="#30363D",
               labelcolor="#C9D1D9", fontsize=9,
               loc="upper right", ncols=max(1, N_CURVAS // 5))
ax_main.grid(True, color="#21262D", linewidth=0.7)

# Painéis individuais
for i, n in enumerate(N_HARMONICOS):
    ax = fig.add_subplot(gs[1 + i // N_COLS, i % N_COLS])
    ax.set_facecolor("#161B22")

    y_fit, rmse = fits[n]
    ax.plot(x, y, color="#C9D1D9", lw=0.8, alpha=0.35, label="Original")
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

fig.suptitle("Serie de Fourier como Tendencia de Curva",
             color="#E6EDF3", fontsize=16, fontweight="bold", y=1.01)

plt.savefig("fourier_fit.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("[plot] Grafico salvo em 'fourier_fit.png'")
plt.show()