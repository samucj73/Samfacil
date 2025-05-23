import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados, gerar_cartoes_otimizados

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")

st.title("🔮 LotoFácil Inteligente - Geração Otimizada")

# Capturar concursos
with st.spinner("🔄 Buscando últimos resultados da Lotofácil..."):
    concursos = capturar_ultimos_resultados(qtd=25)

if not concursos:
    st.error("❌ Não foi possível obter os resultados da Lotofácil.")
else:
    ultimo_concurso = concursos[0]
    numero, data, dezenas = ultimo_concurso

    st.subheader(f"📅 Último concurso: {numero} ({data})")
    st.markdown(f"**Dezenas sorteadas:** `{sorted(dezenas)}`")

    st.divider()

    qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", min_value=1, max_value=30, value=10)
    if st.button("🚀 Gerar Cartões Otimizados"):
        with st.spinner("🔍 Gerando cartões com filtros avançados..."):
            cartoes = gerar_cartoes_otimizados(dezenas, qtde_cartoes)

        st.success(f"✅ {len(cartoes)} cartões gerados com sucesso!")

        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: `{cartao}`")
