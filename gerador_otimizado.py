import random
from collections import Counter

# Dezenas auxiliares
DEZENAS = list(range(1, 26))
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def tem_sequencia(dezenas, tamanho=3):
    dezenas_ordenadas = sorted(dezenas)
    for i in range(len(dezenas_ordenadas) - tamanho + 1):
        if all(dezenas_ordenadas[i + j] == dezenas_ordenadas[i] + j for j in range(tamanho)):
            return True
    return False

def pares_impares_ok(dezenas):
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = 15 - pares
    return (pares == 7 and impares == 8) or (pares == 8 and impares == 7)

def soma_ok(dezenas):
    soma = sum(dezenas)
    return 185 <= soma <= 200

def primos_ok(dezenas):
    qnt_primos = sum(1 for d in dezenas if d in PRIMOS)
    return 5 <= qnt_primos <= 6

def quadrantes_ok(dezenas):
    contagem = [0, 0, 0, 0]
    for d in dezenas:
        if d <= 10:
            contagem[0] += 1
        elif d <= 15:
            contagem[1] += 1
        elif d <= 20:
            contagem[2] += 1
        else:
            contagem[3] += 1
    return all(3 <= c <= 4 for c in contagem)

def calcular_frequencia(concursos):
    todas = [d for _, _, dz in concursos for d in dz]
    contagem = Counter(todas)
    return contagem

def analisar_dezenas_estrategicas(concursos):
    freq = calcular_frequencia(concursos)
    mais_frequentes = {d for d, _ in freq.most_common(12)}
    menos_frequentes = {d for d, _ in freq.most_common()[-8:]}
    return mais_frequentes, menos_frequentes

def gerar_cartao_estrategico(mais_freq, menos_freq, tentativas=50000):
    for _ in range(tentativas):
        base = random.sample(list(mais_freq), 8)
        extra_pool = list(set(DEZENAS) - set(base) - set(menos_freq))
        if len(extra_pool) < 7:
            continue
        complemento = random.sample(extra_pool, 7)
        cartao = base + complemento
        random.shuffle(cartao)

        if (
            soma_ok(cartao) and
            pares_impares_ok(cartao) and
            tem_sequencia(cartao, tamanho=3)
           # quadrantes_ok(cartao) and
           #  primos_ok(cartao)
        ):
            return sorted(cartao)
    return None

def gerar_cartoes_otimizados(concursos_25, quantidade=10):
    mais_frequentes, menos_frequentes = analisar_dezenas_estrategicas(concursos_25)
    cartoes = []
    set_cartoes = set()
    falhas = 0
    max_falhas = 1000

    while len(cartoes) < quantidade and falhas < max_falhas:
        cartao = gerar_cartao_estrategico(mais_frequentes, menos_frequentes)
        if cartao:
            cartao_tuple = tuple(cartao)
            if cartao_tuple not in set_cartoes:
                cartoes.append(cartao)
                set_cartoes.add(cartao_tuple)
            else:
                falhas += 1
        else:
            falhas += 1

    return cartoes

def gerar_cartoes_aleatorios_base_300(concursos_300, quantidade=10):
    mais_frequentes, menos_frequentes = analisar_dezenas_estrategicas(concursos_300)
    cartoes = []
    set_cartoes = set()
    tentativas = 0
    max_tentativas = 10000

    while len(cartoes) < quantidade and tentativas < max_tentativas:
        base = random.sample(list(mais_frequentes), 6)
        restante = list(set(DEZENAS) - set(base) - menos_frequentes)
        if len(restante) < 9:
            tentativas += 1
            continue
        complemento = random.sample(restante, 9)
        cartao = sorted(base + complemento)
        cartao_tuple = tuple(cartao)

        if cartao_tuple not in set_cartoes:
            cartoes.append(cartao)
            set_cartoes.add(cartao_tuple)

        tentativas += 1

    return cartoes
