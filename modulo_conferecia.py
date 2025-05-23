from collections import Counter, defaultdict

def conferir_cartoes(cartoes, ultimos_resultados, filtrar_excelentes=True, min_acertos=3):
    """
    Compara os cartões gerados com os últimos 25 concursos.

    Parâmetros:
    - cartoes: lista de listas (cada cartão com 15 dezenas)
    - ultimos_resultados: lista de tuplas (concurso, data, dezenas sorteadas)
    - filtrar_excelentes: se True, retorna cartões com 12+ acertos em >= min_acertos concursos
    - min_acertos: mínimo de vezes que o cartão deve acertar 12+ dezenas

    Retorna:
    - lista de tuplas: (concurso, acertos_por_cartao)
    - contagem de acertos por faixa (Counter)
    - desempenho dos cartões (dict): {cartao: contagem_12+}
    - bons_cartoes: lista de cartões com bom desempenho
    """
    resultados = []
    faixa_acertos = Counter()
    desempenho = defaultdict(int)
    bons_cartoes = []

    for concurso, data, dezenas_sorteadas in ultimos_resultados:
        acertos_por_cartao = []
        sorteio = set(dezenas_sorteadas)
        for cartao in cartoes:
            acertos = len(set(cartao) & sorteio)
            acertos_por_cartao.append(acertos)
            if 11 <= acertos <= 15:
                faixa_acertos[acertos] += 1
            if acertos >= 12:
                desempenho[tuple(cartao)] += 1
        resultados.append((concurso, acertos_por_cartao))

    if filtrar_excelentes:
        bons_cartoes = [list(c) for c, v in desempenho.items() if v >= min_acertos]

    return resultados, faixa_acertos, desempenho, bons_cartoes


# -------------------------
# ✅ USO DIRETO COM SEUS DADOS REAIS
# -------------------------
if __name__ == "__main__":
    from meus_dados import cartoes, ultimos_resultados  # <- ajuste para seu projeto

    resultados, faixa_acertos, desempenho, bons_cartoes = conferir_cartoes(
        cartoes,
        ultimos_resultados,
        filtrar_excelentes=True,
        min_acertos=3
    )

    print("📊 Faixas de Acertos (11 a 15 pontos):")
    for pontos in range(11, 16):
        print(f"{pontos} pontos: {faixa_acertos.get(pontos, 0)}")

    print("\n🏅 Cartões com 12+ pontos em 3 ou mais concursos:")
    if bons_cartoes:
        for i, cartao in enumerate(bons_cartoes, 1):
            print(f"{i:02d}) {cartao}")
    else:
        print("Nenhum cartão atingiu o critério.")
