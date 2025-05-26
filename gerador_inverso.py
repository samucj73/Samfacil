from itertools import combinations
from collections import Counter
from random import sample

def gerar_cartoes_inversos(concursos_300, quantidade=100, excluir_qtd=10):
    # Garante que excluir_qtd esteja entre 1 e 20
    excluir_qtd = min(max(excluir_qtd, 1), 20)

    # 1. Conta frequência das dezenas
    contador = Counter()
    for _, _, dezenas in concursos_300:
        contador.update(dezenas)

    # 2. Seleciona as dezenas menos frequentes
    menos_frequentes = [dezena for dezena, _ in contador.most_common()][::-1][:excluir_qtd]

    # 3. Define dezenas válidas
    dezenas_possiveis = [d for d in range(1, 26) if d not in menos_frequentes]

    # 4. Verifica se é possível formar cartões
    if len(dezenas_possiveis) < 15:
        return [], menos_frequentes  # Não dá pra formar cartões

    # 5. Gera todas as combinações possíveis de 15 dezenas
    todas_combinacoes = list(combinations(dezenas_possiveis, 15))

    # 6. Limita à quantidade pedida
    selecionadas = sample(todas_combinacoes, min(quantidade, len(todas_combinacoes)))

    return selecionadas, menos_frequentes
