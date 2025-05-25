import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados
from gerador_otimizado import gerar_cartoes_otimizados
from conferencia import conferir_cartoes  # <- Módulo de conferência

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")
st.title("🔮 LotoFácil Inteligente")

# 🔄 Captura dos 25 últimos concursos com cache por sessão
st.subheader("📥 Resultados dos últimos concursos")

if st.button("🔁 Atualizar concursos"):
    st.session_state.pop("concursos_25", None)

if "concursos_25" not in st.session_state:
    with st.spinner("🔄 Buscando últimos 25 resultados da Lotofácil..."):
        concursos = capturar_ultimos_resultados(qtd=150)
        if not concursos:
            st.error("❌ Não foi possível obter os resultados.")
            st.stop()
        st.session_state.concursos_25 = concursos

concursos = st.session_state.concursos_25

# 🟢 Exibir último concurso
numero, data, dezenas = concursos[0]
st.subheader(f"📅 Último concurso: {numero} ({data})")
st.markdown(f"**Dezenas sorteadas:** `{sorted(dezenas)}`")
st.divider()

# 🔧 Inicializa dezenas no session_state
if 'dezenas' not in st.session_state:
    st.session_state.dezenas = sorted(dezenas)

# 🎰 Geração de cartões otimizados
qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", 1, 100, 50)

if st.button("🚀 Gerar Cartões Otimizados"):
    with st.spinner("🔍 Gerando cartões com filtros avançados..."):
        cartoes = gerar_cartoes_otimizados(st.session_state.concursos_25, qtde_cartoes)
        st.session_state.cartoes_gerados = cartoes

    st.success(f"✅ {len(cartoes)} cartões gerados!")
    for i, c in enumerate(cartoes, 1):
        st.write(f"Cartão {i}: `{c}`")

    st.divider()

# 🎲 Geração de cartões aleatórios com base nos 300 concursos
st.markdown("### 🎲 Geração com lógica mais aleatória (300 concursos)")

if st.button("📊 Gerar com base nos últimos 300 concursos (Aleatório)"):
    from gerador_otimizado import gerar_cartoes_aleatorios_base_300

    with st.spinner("🎲 Gerando cartões com lógica menos restrita..."):
        cartoes_aleatorios = gerar_cartoes_aleatorios_base_300(
            st.session_state.concursos_300, qtde_cartoes
        )
        st.session_state.cartoes_gerados_aleatorios = cartoes_aleatorios

    st.success(f"✅ {len(cartoes_aleatorios)} cartões gerados com lógica aleatória baseada nos 300 concursos!")
    for i, c in enumerate(cartoes_aleatorios, 1):
        st.write(f"[Aleatório 300] Cartão {i}: `{c}`")

    st.divider()

# 📊 Conferência de desempenho
if "cartoes_gerados" in st.session_state:
    st.subheader("📊 Conferência com últimos 25 concursos")
    min_concursos = st.slider("Mínimo de concursos com 13+ pontos para destacar cartão:", 1, 10, 3)

    if st.button("✅ Conferir Desempenho dos Cartões"):
        with st.spinner("🔎 Analisando desempenho..."):
            resultados, faixa_acertos, desempenho, bons_cartoes, destaques = conferir_cartoes(
                st.session_state.cartoes_gerados,
                concursos,
                filtrar_excelentes=True,
                min_acertos=min_concursos
            )

        st.write("### 🎯 Faixas de Acertos (total em todos concursos):")
        for pontos in range(11, 16):
            st.write(f"✅ {pontos} pontos: `{faixa_acertos.get(pontos, 0)}`")

        st.write("---")
        st.write(f"🏅 Cartões que acertaram **12+ pontos em pelo menos {min_concursos} concursos**:")
        if bons_cartoes:
            for i, c in enumerate(bons_cartoes, 1):
                st.write(f"{i:02d}) `{sorted(c)}`")
        else:
            st.info("Nenhum cartão teve bom desempenho com esse critério.")

        # 🎯 Destaque especial: cartões com 14 pontos
        if destaques[14]:
            st.write("---")
            st.subheader("🌟 Destaques: Cartões com 14 pontos")
            for cartao, concurso, idx in destaques[14]:
                st.markdown(f"✅ Cartão #{idx + 1} acertou 14 pontos no concurso **{concurso}**:")
                st.code(sorted(cartao), language="python")
        else:
            st.info("Nenhum cartão acertou 14 pontos nos últimos concursos.")

# 📅 Expansor com os 300 últimos concursos
with st.expander("📅 Ver os 300 últimos concursos"):
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("🔁 Atualizar 300"):
            st.session_state.pop("concursos_300", None)

    if 'concursos_300' not in st.session_state:
        with st.spinner("🔄 Buscando os 300 últimos concursos..."):
            st.session_state.concursos_300 = capturar_ultimos_resultados(qtd=300)

    todos = st.session_state.concursos_300
    for item in todos:
        numero = item[0]
        dezenas = ", ".join(str(d).zfill(2) for d in sorted(item[2]))
        st.write(f"Concurso {numero}: {dezenas}")
