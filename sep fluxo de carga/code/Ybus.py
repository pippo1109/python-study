import pandas as pd
import numpy as np
from pathlib import Path

# 1. Leitura apenas dos dados das linhas de transmissão
arquivo_csv = (
    Path(__file__).resolve().parent.parent
    / 'Dados de entrada'
    / 'Dados das Linhas de Transmissão.csv'
)
df_linhas = pd.read_csv(
    arquivo_csv,
    encoding='cp1252',
    sep=';',
    decimal=',',
    usecols=[
        'Barra inicial',
        'Barra final',
        'Resistência',
        'Reatância',
        'Susceptância',
    ],
)

# 2. Identificação do número de barras
num_barras = int(max(df_linhas['Barra inicial'].max(), df_linhas['Barra final'].max()))

# 3. Inicialização da matriz Ybus com zeros complexos
Ybus = np.zeros((num_barras, num_barras), dtype=complex)

# 4. Preenchimento da matriz Ybus
for _, linha in df_linhas.iterrows():
    Barra_inicial = int(linha['Barra inicial']) - 1     # Conversão para índice 0
    Barra_final = int(linha['Barra final']) - 1 # Conversão para índice 0
    r, x, b = linha['Resistência'], linha['Reatância'], linha['Susceptância']

    # Impedância (Z), Admitância de série (y) e Susceptância shunt (y_sh)
    z = complex(r, x)
    y = 1 / z
    y_sh = complex(0, b / 2)
    
    # Elementos fora da diagonal (mutua): Y_ij = Y_ji = -y
    Ybus[Barra_inicial, Barra_final] -= y
    Ybus[Barra_final, Barra_inicial] -= y
    
    # Elementos da diagonal (própria): Y_ii = sum(y + y_sh)
    Ybus[Barra_inicial, Barra_inicial] += y + y_sh
    Ybus[Barra_final, Barra_final] += y + y_sh

# Exibir a matriz formatada
df_Ybus = pd.DataFrame(np.round(Ybus, 4), 
                       index=range(1, num_barras + 1), 
                       columns=range(1, num_barras + 1))
print(df_Ybus)

pasta_saida = Path(__file__).resolve().parent.parent / 'Dados de saída'
pasta_saida.mkdir(parents=True, exist_ok=True)
arquivo_saida = pasta_saida / 'Matriz Ybus.xlsx'
df_Ybus.to_excel(arquivo_saida, sheet_name='Ybus', index=False, header=False)