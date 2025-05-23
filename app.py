import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados, gerar_cartoes_otimizados
from conferencia import conferir_cartoes  # <- Novo módulo

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")

st.title("🔮 LotoFácil Inteligente")

# Captura de concursos
with st.spinner("🔄 Buscando últimos resultados da Lotofácil..."):
    concursos = capturar_ultimos_resultados(qtd=25)

if not concursos:
    st.error("❌ Não foi possível obter os resultados.")
else:
    numero, data, dezenas = concursos[0]
    st.subheader(f"📅 Último concurso: {numero} ({data})")
    st.markdown(f"**Dezenas sorteadas:** `{sorted(dezenas)}`")
    st.divider()

    # Geração de cartões
    qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", 1, 30, 10)
    if st.button("🚀 Gerar Cartões Otimizados"):
        with st.spinner("🔍 Gerando cartões com filtros avançados..."):
            cartoes = gerar_cartoes_otimizados(dezenas, qtde_cartoes)
        st.success(f"✅ {len(cartoes)} cartões gerados!")
        
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: `{cartao}`")

        st.divider()

        # Conferência
        st.subheader("📊 Conferência com últimos 25 concursos")
        min_concursos = st.slider("Mínimo de concursos com 12+ pontos para destacar cartão:", 1, 10, 3)
        if st.button("✅ Conferir Desempenho dos Cartões"):
            with st.spinner("Analisando desempenho..."):
                resultados, faixas, desempenho, bons = conferir_cartoes(
                    cartoes, concursos, filtrar_excelentes=True, min_acertos=min_concursos
                )

            st.write("### 🎯 Faixas de Acertos (total em todos concursos):")
            for pontos in range(11, 16):
                st.write(f"✅ {pontos} pontos: `{faixas.get(pontos, 0)}`")

            st.write("---")
            st.write(f"🏅 Cartões que acertaram **12+ pontos em pelo menos {min_concursos} concursos**:")
            if bons:
                for i, c in enumerate(bons, 1):
                    st.write(f"{i:02d}) `{sorted(c)}`")
            else:
                st.info("Nenhum cartão teve bom desempenho com esse critério.")
                # 🔽 Exibição dos concursos detalhados
    with st.expander("📅 Ver os 25 últimos concursos detalhados"):
        for numero, data, dezenas in concursos:
            dezenas_str = ", ".join(str(d).zfill(2) for d in dezenas)
            st.write(f"Concurso {numero} ({data}): {dezenas_str}")
