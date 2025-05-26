from itertools import combinations
from collections import Counter
from random import sample

def gerar_cartoes_inversos(concursos_300, quantidade=100):
    # 1. Conta frequência das dezenas
    contador = Counter()
    for _, _, dezenas in concursos_300:
        contador.update(dezenas)

    # 2. Seleciona as 10 dezenas menos frequentes
    menos_frequentes = [dezena for dezena, _ in contador.most_common()][::-1][:10]

    # 3. Define o conjunto de dezenas válidas (excluindo as 10 menos frequentes)
    dezenas_possiveis = [d for d in range(1, 26) if d not in menos_frequentes]

    # 4. Gera todas as combinações possíveis de 15 dezenas
    todas_combinacoes = list(combinations(dezenas_possiveis, 15))

    # 5. Evita repetições: sorteia combinações únicas aleatórias
    quantidade_maxima = min(quantidade, len(todas_combinacoes))
    combinacoes_unicas = sample(todas_combinacoes, quantidade_maxima)

    return combinacoes_unicas, menos_frequentes
