README - PASSOS DO PROJETO DE FLUXO DE POTENCIA 2026.2
SEP I - Sistemas Eletricos de Potencia - Prof. Artur Passos Dias Lima
Centro Universitario SENAI CIMATEC

PRAZOS
- Entrega do PDF escrito no Canvas, com assinatura de todos os integrantes, ate 21/10/2026 as 23h59. Entrega fora do prazo nao tem efeito.
- Apresentacao em sala em 23 ou 26/10/2026, das 18h30 as 20h20.

ARQUIVOS DE DADOS
- dados_barras.xlsx (aba Barras) com as colunas Barra, Tipo, Pg, Qg, Pd, Qd, V e Delta.
- Celulas vazias correspondem a "-" no enunciado.
- Ler em Python com pd.read_excel('dados_barras.xlsx').
- Todos os valores estao em p.u. na base de 100 MVA.





--------------------------------------------------------------
ETAPA 1 - IDEIA CENTRAL (item a, 0,1 ponto)
--------------------------------------------------------------
1. Escrever o objetivo. Calcular tensoes e fluxos de potencia ativa e reativa em todas as barras e linhas e comparar Gauss-Jacobi, Gauss-Seidel e Newton-Raphson.
2. Definir a sequencia do trabalho. Dados, Ybus, metodos iterativos, resultados, fluxos nas linhas, comparacao e conclusao.






--------------------------------------------------------------
ETAPA 2 - MATRIZ Ybus (itens b e d, 1a a 7a questoes)
--------------------------------------------------------------
3. Para cada uma das 10 linhas, calcular a impedancia Z = R + jX. Como R = 0, Z = jX.
4. Calcular a admitancia de cada linha, y = 1/Z = -j/X.
5. Elementos fora da diagonal. Yij = -yij. Se nao existe linha entre as barras, o elemento e zero. A matriz e simetrica.
6. Elementos da diagonal. Yii = soma das admitancias das linhas ligadas a barra i, mais metade do Bsh de cada linha ligada a barra i.
7. Montar a matriz 8x8 completa e mostrar o passo a passo de algumas linhas.






--------------------------------------------------------------
ETAPA 3 - DADOS DE ENTRADA E VARIAVEIS (item c, 0,5 ponto)
--------------------------------------------------------------
8. Classificar as barras.
   Slack: barra 1 (V = 1,05 e angulo 0).
   PV: barras 2 (V = 1,05) e 7 (V = 1,04).
   PQ: barras 3, 4, 5, 6 e 8.
9. Calcular as potencias liquidas especificadas, P = Pg - Pd e Q = Qg - Qd.
10. Listar as incognitas. Barras PQ tem V e delta, barras PV tem Q e delta, e a barra Slack tem P e Q.
11. Definir os chutes iniciais das barras 3, 4, 5, 6 e 8 (partida plana, V = 1,0 e delta = 0). Nas barras PV, manter o V especificado e iniciar delta em 0.
12. Definir a tolerancia de convergencia e o numero maximo de iteracoes.
13. Explicar cada variavel usada (V, delta, P, Q, Y, G, B).






--------------------------------------------------------------
ETAPA 4 - GAUSS-JACOBI (item e, 0,5 ponto)
--------------------------------------------------------------
14. Escrever a equacao de tensao das barras PQ.
    Vi = (1/Yii) * [ (Pi - jQi)/conj(Vi) - soma de Yij*Vj para j diferente de i ]
15. Explicar que, no Jacobi, todas as tensoes da iteracao k+1 usam apenas valores da iteracao k.
16. Tratar as barras PV. Calcular Qi com as tensoes atuais, atualizar a tensao e reajustar o modulo para o valor especificado, mantendo o angulo novo.
17. Fazer as primeiras iteracoes a mao e registrar o erro maximo de cada uma.






--------------------------------------------------------------
ETAPA 5 - GAUSS-SEIDEL (item f, 0,5 ponto)
--------------------------------------------------------------
18. Usar a mesma equacao, aproveitando imediatamente os valores ja atualizados na iteracao corrente.
19. Aplicar o mesmo tratamento das barras PV. Comentar o fator de aceleracao, se for usado.
20. Mostrar as primeiras iteracoes detalhadas e a evolucao do erro.






--------------------------------------------------------------
ETAPA 6 - NEWTON-RAPHSON (item g, 0,5 ponto)
--------------------------------------------------------------
21. Escrever as equacoes de potencia.
    Pi = soma de |Vi||Vj| (Gij cos(dij) + Bij sen(dij))
    Qi = soma de |Vi||Vj| (Gij sen(dij) - Bij cos(dij))
22. Montar o vetor de incognitas. Sao 7 angulos (barras 2 a 8) e 5 modulos de tensao (barras 3, 4, 5, 6 e 8), totalizando 12 variaveis.
23. Calcular os residuos dP (barras 2 a 8) e dQ (barras PQ).
24. Montar o Jacobiano em blocos [H N; M L] (12x12) e resolver o sistema linear a cada iteracao.
25. Atualizar as variaveis e repetir ate o maior residuo ficar abaixo da tolerancia. Mostrar a primeira iteracao detalhada.






--------------------------------------------------------------
ETAPA 7 - RESULTADOS FINAIS
--------------------------------------------------------------
26. Apresentar as tensoes (modulo e angulo) de todas as barras, para cada metodo.
27. Calcular P e Q da barra Slack e Q das barras PV.
28. Calcular os fluxos Sij e Sji de cada linha, incluindo a contribuicao de Bsh/2, e as perdas por linha. Como R = 0, as perdas ativas devem ser nulas, o que serve de verificacao.
29. Fazer o balanco de potencia do sistema (geracao = carga + perdas).






--------------------------------------------------------------
ETAPA 8 - CONVERGENCIA (item h, 0,3 ponto)
--------------------------------------------------------------
30. Comparar numero de iteracoes, tempo de execucao e curva de erro dos tres metodos.
31. Gerar grafico do erro (escala logaritmica) por iteracao para cada metodo.
32. Concluir sobre a velocidade de convergencia. Newton-Raphson tem convergencia quadratica e precisa de poucas iteracoes. Gauss-Seidel precisa de mais, e Gauss-Jacobi em geral de ainda mais.






--------------------------------------------------------------
ETAPA 9 - ALGORITMOS (item i, 1,0 ponto)
--------------------------------------------------------------
33. Implementar em Python, Matlab, Octave ou JavaScript. Montagem da Ybus, os tres metodos, calculo dos fluxos e graficos.
34. Comentar o codigo e explicar a logica de cada bloco no relatorio, com fluxogramas se possivel.
35. Conferir se os tres metodos chegam as mesmas tensoes finais.






--------------------------------------------------------------
ETAPA 10 - RELATORIO E APRESENTACAO
--------------------------------------------------------------
36. Formatar o relatorio com capa, introducao, desenvolvimento, resultados, conclusao e referencias. A formatacao vale 1 ponto.
37. Coletar as assinaturas de todos os integrantes e enviar o PDF pelo Canvas ate 21/10/2026 as 23h59.
38. Preparar a apresentacao para 23 ou 26/10/2026. A apresentacao vale 4 pontos e a falta faz a pontuacao ir para a prova.

