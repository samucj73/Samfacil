import random

# Dezenas auxiliares
DEZENAS = list(range(1, 26))
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def eh_primo(n):
    return n in PRIMOS

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
    # Volante dividido em 4 quadrantes 5x5
    quadrantes = {
        1: set(range(1, 6)) | set(range(6, 11)),
        2: set(range(11, 16)),
        3: set(range(16, 21)),
        4: set(range(21, 26))
    }
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

def gerar_cartao_otimizado(anterior):
    for _ in range(5000):  # tenta até 5000 vezes encontrar um bom cartão
        repetidas = random.sample(anterior, random.choice([9, 10]))
        restantes = list(set(DEZENAS) - set(repetidas))
        complemento = random.sample(restantes, 15 - len(repetidas))
        cartao = repetidas + complemento
        random.shuffle(cartao)

        if (pares_impares_ok(cartao) and
            soma_ok(cartao) and
            primos_ok(cartao) and
            tem_sequencia(cartao, tamanho=3) and
            quadrantes_ok(cartao)):
            return sorted(cartao)
    return None  # caso não consiga

def gerar_cartoes_otimizados(anterior, quantidade=10):
    cartoes = []
    while len(cartoes) < quantidade:
        cartao = gerar_cartoes_otimizados(anterior)
        if cartao and cartao not in cartoes:
            cartoes.append(cartao)
    return cartoes
