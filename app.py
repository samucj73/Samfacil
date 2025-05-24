import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados
from gerador_otimizado import gerar_cartoes_otimizados
from conferencia import conferir_cartoes

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")
st.title("🔮 LotoFácil Inteligente")
st.markdown("Otimize suas apostas com estatísticas e inteligência baseada nos últimos concursos.")
st.divider()

# 🔧 Utilitário de exportação
def exportar_cartoes_txt(cartoes):
    conteudo = "\n".join(", ".join(str(d).zfill(2) for d in sorted(c)) for c in cartoes)
    return conteudo.encode("utf-8")

# 🔄 Captura dos concursos
with st.spinner("🔄 Buscando últimos resultados da Lotofácil..."):
    concursos = capturar_ultimos_resultados(qtd=250)

if not concursos:
    st.error("❌ Não foi possível obter os resultados.")
    st.stop()

# Último concurso (usado para análises e repetições)
numero, data, dezenas = concursos[]
if 'dezenas' not in st.session_state:
    st.session_state.dezenas = sorted(dezenas)

# 🔁 Abas principais
aba1, aba2, aba3 = st.tabs(["🎰 Gerar Cartões", "📊 Conferência", "📅 Últimos Concursos"])

# 🎰 Geração de Cartões
with aba1:
    st.subheader("🎰 Geração de Cartões Otimizados")
    st.markdown("Com base nas dezenas do último concurso e filtros avançados.")

    qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", 1, 30, 10)

    if st.button("🚀 Gerar Cartões"):
        with st.spinner("🔍 Gerando cartões com filtros avançados..."):
            cartoes = gerar_cartoes_otimizados(st.session_state.dezenas, qtde_cartoes)
            st.session_state.cartoes_gerados = cartoes

        st.success(f"✅ {len(cartoes)} cartões gerados!")
        for i, c in enumerate(cartoes, 1):
            st.write(f"Cartão {i:02d}: `{sorted(c)}`")

        st.download_button("📥 Baixar Cartões (.txt)", exportar_cartoes_txt(cartoes), file_name="cartoes_lotofacil.txt")

# 📊 Conferência de Desempenho
with aba2:
    st.subheader("📊 Conferência com últimos 25 concursos")

    if "cartoes_gerados" not in st.session_state:
        st.info("Gere cartões na aba anterior para conferi-los.")
    else:
        min_concursos = st.slider("Mínimo de concursos com 12+ pontos para destacar cartão:", 1, 10, 3)

        if st.button("✅ Conferir Desempenho"):
            with st.spinner("🔎 Analisando desempenho..."):
                _, faixas, _, bons = conferir_cartoes(
                    st.session_state.cartoes_gerados,
                    concursos,
                    filtrar_excelentes=True,
                    min_acertos=min_concursos
                )

            st.write("### 🎯 Faixas de Acertos (total em todos concursos):")
            for pontos in range(11, 16):
                st.write(f"✅ {pontos} pontos: `{faixas.get(pontos, 0)}`")

            st.write("---")
            st.write(f"🏅 Cartões com **12+ pontos em ≥ {min_concursos} concursos**:")
            if bons:
                for i, c in enumerate(bons, 1):
                    st.write(f"{i:02d}) `{sorted(c)}`")
            else:
                st.info("Nenhum cartão teve bom desempenho com esse critério.")

# 📅 Últimos concursos
with aba3:
    st.subheader("📅 Últimos 300 Concursos")
    with st.spinner("🔄 Carregando concursos..."):
        todos = capturar_ultimos_resultados(qtd=300)

    for item in todos:
        numero = item[0]
        dezenas = ", ".join(str(d).zfill(2) for d in sorted(item[2]))
        st.write(f"Concurso {numero}: {dezenas}")
