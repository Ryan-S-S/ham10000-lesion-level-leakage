# Resultados experimentais

Este diretório contém o relatório HTML com os resultados organizados do Orange Data Mining.

- `relatorio_resultados.html`: resumo das cinco sementes da rede neural, resultados individuais, análises complementares, matrizes de confusão e teste preliminar de encoders.

## Sobre os dados do relatório

As quatro condições da rede neural foram executadas com as sementes 7, 12, 42, 99 e 100. As comparações de regressão logística, floresta aleatória e rede neural somente com dados clínicos, assim como as matrizes de confusão, correspondem à semente 42.

As matrizes de confusão apresentam percentuais por classe real (normalização por linha) e o suporte de cada classe. As médias e os desvios-padrão do resumo foram calculados a partir dos valores de três casas decimais exportados pelo Orange.

O teste de encoders (Painters, SqueezeNet, Inception, VGG19, DeepLoc e OpenFace) foi feito com redes neurais reduzidas, com 50 neurônios na camada interna, por se tratar de uma etapa inicial e pouco decisiva no projeto. Usou Stratified Shuffle split (5 amostras aleatórias, 80% dos dados), uma única execução por encoder, e seus valores não são comparáveis aos dos experimentos principais.
