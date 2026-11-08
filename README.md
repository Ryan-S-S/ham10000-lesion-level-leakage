# HAM10000 — Análise de vazamento de dados por lesão

Repositório de scripts, workflow e resultados experimentais utilizados no estudo **“Vazamento de dados entre imagens da mesma lesão no HAM10000: impacto sobre o desempenho de classificadores e o papel dos dados clínicos”**.

O projeto investiga como a estratégia de particionamento das imagens — individualmente ou agrupadas por `lesion_id` — influencia a avaliação de classificadores para as sete categorias diagnósticas do HAM10000. Também examina a contribuição adicional de sexo, idade e localização anatômica.

## Resultados

O relatório completo está disponível em [`results/relatorio_resultados.html`](results/relatorio_resultados.html).

O documento reúne:

- resultados da rede neural nas quatro condições experimentais;
- cinco sementes aleatórias (7, 12, 42, 99 e 100);
- médias e desvios-padrão descritivos das cinco execuções;
- comparação complementar com regressão logística e floresta aleatória (semente 42);
- resultados da rede neural utilizando somente dados clínicos (semente 42);
- seis matrizes de confusão exportadas pelo Orange.

O HTML é autocontido e pode ser aberto diretamente em um navegador. Não requer servidor, instalação de bibliotecas ou conexão com a internet.

## Perguntas de pesquisa

1. Quanto o desempenho estimado se altera quando imagens associadas ao mesmo identificador de lesão são mantidas no mesmo fold?
2. A inclusão de dados clínicos contribui para o desempenho nos protocolos por imagem e agrupado por lesão?

## Dataset

O estudo utiliza o **HAM10000**, composto por 10.015 imagens dermatoscópicas distribuídas em sete categorias diagnósticas e associadas a 7.470 identificadores de lesão.

| Sigla | Categoria |
|---|---|
| AKIEC | Ceratose actínica e carcinoma intraepitelial |
| BCC | Carcinoma basocelular |
| BKL | Lesões benignas semelhantes à ceratose |
| DF | Dermatofibroma |
| MEL | Melanoma |
| NV | Nevo melanocítico |
| VASC | Lesões vasculares |

O dataset original não é redistribuído neste repositório. Consulte a publicação original: [Tschandl et al. (2018), *The HAM10000 Dataset*](https://doi.org/10.1038/sdata.2018.161).

## Metodologia resumida

### Representação das imagens

As imagens foram representadas por vetores de 2.048 atributos extraídos pelo embedder **Painters**, disponível no complemento Image Analytics do Orange Data Mining.

### Dados clínicos

Foram comparadas duas configurações: (1) atributos de imagem; e (2) atributos de imagem combinados com sexo, idade e localização anatômica.

### Protocolos de validação

- **Por imagem (intra):** `StratifiedKFold`, com estratificação pelo diagnóstico (`dx`) e sem agrupamento por `lesion_id`. Imagens da mesma lesão podem aparecer em folds diferentes.
- **Agrupado por lesão (inter):** `StratifiedGroupKFold`, com estratificação aproximada pelo diagnóstico e agrupamento por `lesion_id`. Todas as imagens com o mesmo identificador permanecem no mesmo fold.

> **Limitação importante:** `lesion_id` identifica lesões, não pacientes. Portanto, a validação agrupada por lesão não garante que imagens de um mesmo paciente estejam exclusivamente em um único fold. Também há limitações conhecidas nos metadados de identificação de lesões do HAM10000; consulte Abhishek et al. (2025).

### Classificadores

A rede neural é o modelo principal. O relatório também apresenta uma comparação complementar com regressão logística e floresta aleatória, além de uma execução da rede neural utilizando somente dados clínicos. Os hiperparâmetros completos devem ser consultados no manuscrito e no workflow do Orange publicado junto aos scripts.

## Estrutura recomendada do repositório

Para manter códigos, workflow e resultados separados, recomenda-se organizar o repositório desta forma:

```text
.
├── README.md
├── scripts/
│   ├── kfold_image_level.py
│   └── kfold_lesion_grouped.py
├── workflows/
│   └── ham10000_experiments.ows
└── results/
    ├── README.md
    └── relatorio_resultados.html
```

O repositório publicado atualmente contém um arquivo Python com os dois procedimentos (`Código.py.txt`) e o workflow do Orange (`Exeperimentos.ows`). Ao aplicar a organização sugerida, separe os dois blocos do arquivo Python em `scripts/kfold_image_level.py` e `scripts/kfold_lesion_grouped.py`, mova o workflow para `workflows/` e corrija seu nome para `ham10000_experiments.ows`.

- `scripts/kfold_image_level.py`: script de criação dos folds por imagem, executado no widget **Python Script** do Orange.
- `scripts/kfold_lesion_grouped.py`: script de criação dos folds agrupados por `lesion_id`, executado no widget **Python Script** do Orange.
- `workflows/ham10000_experiments.ows`: workflow do Orange utilizado nos experimentos.
- `results/relatorio_resultados.html`: relatório organizado dos resultados exportados.

Os scripts do Orange usam as variáveis `in_data` e `out_data` fornecidas pelo próprio widget; não são programas independentes para execução direta pelo terminal.

## Como consultar os resultados

1. Abra `results/relatorio_resultados.html` em um navegador.
2. Consulte primeiro o resumo das cinco sementes.
3. Utilize a seção de resultados por semente para conferir as execuções individuais.
4. Consulte as comparações complementares e as matrizes de confusão, lembrando que estas foram exportadas para a semente 42.

As médias e os desvios-padrão apresentados no HTML foram recalculados a partir dos valores individuais exportados com três casas decimais. Pequenas diferenças de arredondamento podem ocorrer em relação a cálculos feitos com a precisão interna completa do Orange.

## Requisitos para reprodução

- Orange Data Mining;
- complemento Orange3 Image Analytics;
- scikit-learn compatível com os métodos `StratifiedKFold` e `StratifiedGroupKFold`;
- NumPy;
- dataset HAM10000 obtido da fonte original.

Registre as versões efetivamente utilizadas de Orange, Orange3 Image Analytics, Python, NumPy e scikit-learn ao reproduzir os experimentos. Os caminhos dos arquivos de imagem devem ser ajustados ao ambiente local.

## Referências principais

- Tschandl, P. et al. (2018). [The HAM10000 Dataset, a Large Collection of Multi-Source Dermatoscopic Images of Common Pigmented Skin Lesions](https://doi.org/10.1038/sdata.2018.161). *Scientific Data*, 5, 180161.
- Kapoor, S.; Narayanan, A. (2023). [Leakage and the Reproducibility Crisis in Machine-Learning-Based Science](https://doi.org/10.1016/j.patter.2023.100804). *Patterns*, 4(9), 100804.
- Abhishek, K. et al. (2025). [Investigating the Quality of DermaMNIST and Fitzpatrick17k Dermatological Image Datasets](https://doi.org/10.1038/s41597-025-04382-5). *Scientific Data*, 12, 196.
- Godec, P. et al. (2019). [Democratized Image Analytics by Visual Programming through Integration of Deep Models and Small-Scale Machine Learning](https://doi.org/10.1038/s41467-019-12397-x). *Nature Communications*, 10, 4551.
- Demšar, J. et al. (2013). [Orange: Data Mining Toolbox in Python](https://jmlr.org/papers/v14/demsar13a.html). *Journal of Machine Learning Research*, 14, 2349–2353.

## Aviso de escopo

Este repositório documenta experimentos de pesquisa em aprendizado de máquina. Os modelos avaliados não foram validados como ferramentas clínicas e não devem ser utilizados para diagnóstico ou decisão médica.
