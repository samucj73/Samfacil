import random
from collections import Counter

# Universo de dezenas da Lotofácil
DEZENAS = list(range(1, 26))

def calcular_probabilidades(concursos):
    """
    Calcula a probabilidade de cada dezena com base na frequência de aparição
    nos concursos fornecidos.
    """
    todas_dezenas = [d for _, _, dezenas in concursos for d in dezenas]
    contagem = Counter(todas_dezenas)
    total = sum(contagem.values())
    probabilidades = {d: contagem.get(d, 0) / total for d in DEZENAS}
    return probabilidades

def gerar_cartao_probabilistico(probabilidades):
    """
    Gera um único cartão de 15 dezenas com base nas probabilidades calculadas.
    """
    dezenas_escolhidas = set()
    while len(dezenas_escolhidas) < 15:
        escolhida = random.choices(
            population=DEZENAS,
            weights=[probabilidades[d] for d in DEZENAS],
            k=1
        )[0]
        dezenas_escolhidas.add(escolhida)
    return sorted(dezenas_escolhidas)

def gerar_cartoes_mais_possiveis(concursos, quantidade=10):
    """
    Gera múltiplos cartões considerados mais possíveis, com base em distribuição
    estatística real dos últimos concursos.
    """
    probabilidades = calcular_probabilidades(concursos)
    cartoes_unicos = set()

    while len(cartoes_unicos) < quantidade:
        cartao = tuple(gerar_cartao_probabilistico(probabilidades))
        if cartao not in cartoes_unicos:
            cartoes_unicos.add(cartao)

    return [list(c) for c in cartoes_unicos]
