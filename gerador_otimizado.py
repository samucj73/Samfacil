import random
from collections import Counter

# Dezenas auxiliares
DEZENAS = list(range(1, 26))
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

# Verifica se há sequência de tamanho especificado
def tem_sequencia(dezenas, tamanho=3):
    dezenas_ordenadas = sorted(dezenas)
    for i in range(len(dezenas_ordenadas) - tamanho + 1):
        if all(dezenas_ordenadas[i + j] == dezenas_ordenadas[i] + j for j in range(tamanho)):
            return True
    return False

# Filtro de pares e ímpares equilibrado
def pares_impares_ok(dezenas):
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = 15 - pares
    return (pares == 7 and impares == 8) or (pares == 8 and impares == 7)

# Filtro por soma total
def soma_ok(dezenas):
    soma = sum(dezenas)
    return 185 <= soma <= 200

# Filtro por quantidade de primos
def primos_ok(dezenas):
    qnt_primos = sum(1 for d in dezenas if d in PRIMOS)
    return 5 <= qnt_primos <= 6

# Filtro por quadrantes (1-10, 11-15, 16-20, 21-25)
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

# Frequência das dezenas nos concursos fornecidos
def calcular_frequencia(concursos):
    todas = [d for _, _, dz in concursos for d in dz]
    contagem = Counter(todas)
    return contagem

# Identifica dezenas mais e menos frequentes
def analisar_dezenas_estrategicas(concursos):
    freq = calcular_frequencia(concursos)

    mais_frequentes = {d for d, _ in freq.most_common(12)}
    menos_frequentes = {d for d, _ in freq.most_common()[-8:]}

    return mais_frequentes, menos_frequentes

# Geração de cartão único aplicando todos os filtros
def gerar_cartao_estrategico(mais_freq, menos_freq, tentativas=300):
    for _ in range(tentativas):
        base = random.sample(list(mais_freq), 10)  # Corrigido aqui
        extra_pool = list(set(DEZENAS) - set(base) - set(menos_freq))
        if len(extra_pool) < 5:
            continue
        complemento = random.sample(extra_pool, 5)
        cartao = base + complemento
        random.shuffle(cartao)

        if (
            soma_ok(cartao) and
            pares_impares_ok(cartao) and
            quadrantes_ok(cartao) and
            primos_ok(cartao) and
            not tem_sequencia(cartao, tamanho=3)  # Agora rejeita cartões com sequência
        ):
            return sorted(cartao)

    return None

# Geração de múltiplos cartões otimizados
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
                falhas += 1  # Cartão duplicado
        else:
            falhas += 1  # Nenhum cartão gerado

    return cartoes
