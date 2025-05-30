import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados
from gerador_otimizado import gerar_cartoes_otimizados
from gerador_probabilistico import gerar_cartoes_mais_possiveis
from conferencia import conferir_cartoes
from gerador_inverso import gerar_cartoes_inversos

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")

st.markdown("<h1 style='text-align: center;'>🔮 LotoFácil Inteligente</h1>", unsafe_allow_html=True)

# 🔧 Configuração global na barra lateral
st.sidebar.markdown("### ⚙️ Configuração Global")
qtd_concursos_global = st.sidebar.slider(
    "📊 Quantidade de concursos a considerar (para geração e análise):",
    min_value=15, max_value=2500, value=10, step=15
)

# Botão para recarregar os concursos
if st.sidebar.button("🔄 Recarregar Concursos"):
    st.session_state.pop("concursos_dinamico", None)

# Carregamento dos concursos conforme a quantidade global escolhida
if "concursos_dinamico" not in st.session_state:
    with st.spinner(f"🔍 Carregando os últimos {qtd_concursos_global} concursos..."):
        concursos_dinamico = capturar_ultimos_resultados(qtd=qtd_concursos_global)
        if not concursos_dinamico:
            st.error("❌ Não foi possível obter os resultados.")
            st.stop()
        st.session_state.concursos_dinamico = concursos_dinamico

concursos_dinamico = st.session_state.concursos_dinamico
numero, data, dezenas = concursos_dinamico[0]
st.markdown(f"<h4 style='text-align: center;'>📅 Último concurso: {numero} ({data})</h4>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>**Dezenas sorteadas:** `{sorted(dezenas)}`</p>", unsafe_allow_html=True)
st.divider()

# 🗂️ Abas principais
abas = st.tabs(["📈 Otimizados", "🎲 Aleatórios", "📊 Probabilísticos", "✅ Conferência", "📅 Históricos", "🚫 Inverso"])

# 📈 Geração Otimizada
with abas[0]:
    st.markdown("### 🎰 Geração de Cartões Otimizados", unsafe_allow_html=True)
    qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", 1, 2000, 450)

    if st.button("🚀 Gerar Cartões Otimizados"):
        with st.spinner("🔍 Gerando cartões com filtros avançados..."):
            cartoes = gerar_cartoes_otimizados(concursos_dinamico, qtde_cartoes)
            st.session_state.cartoes_gerados = cartoes

        st.success(f"✅ {len(cartoes)} cartões gerados!")
        for i, c in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: `{c}`")
        st.divider()

# 🎲 Aleatórios base
with abas[1]:
    st.markdown("### 🎲 Geração Aleatória com Base nos Últimos Concursos", unsafe_allow_html=True)

    if st.button("🎲 Gerar Aleatórios Base"):
        from gerador_otimizado import gerar_cartoes_aleatorios_base_300

        with st.spinner("🎲 Gerando cartões aleatórios..."):
            cartoes_aleatorios = gerar_cartoes_aleatorios_base_300(concursos_dinamico, qtde_cartoes)
            st.session_state.cartoes_gerados_aleatorios = cartoes_aleatorios

        st.success(f"✅ {len(cartoes_aleatorios)} cartões gerados!")
        for i, c in enumerate(cartoes_aleatorios, 1):
            st.write(f"Aleatório {i}: `{c}`")
        st.divider()

# 📊 Probabilísticos
with abas[2]:
    st.markdown("### 📈 Geração de Cartões Probabilísticos", unsafe_allow_html=True)
    qtde_prob = st.slider("📌 Quantidade de cartões probabilísticos:", 1, 10000, 5000)

    if st.button("📈 Gerar Cartões Probabilísticos"):
        with st.spinner("🎯 Gerando com base em frequência..."):
            cartoes_prob = gerar_cartoes_mais_possiveis(concursos_dinamico, quantidade=qtde_prob)
            st.session_state.cartoes_probabilisticos = cartoes_prob

        st.success(f"✅ {len(cartoes_prob)} cartões gerados com base em frequência!")
        for i, c in enumerate(cartoes_prob, 1):
            st.write(f"Probabilístico {i:02d}: `{c}`")
        st.divider()

# ✅ Conferência
with abas[3]:
    st.subheader("📊 Conferência com últimos concursos")
    tipo_cartao = st.radio("Escolha quais cartões deseja conferir:",
                           ["Otimizados", "Aleatórios (300)", "Probabilísticos", "Inversos"],
                           horizontal=True)

    cartoes_para_conferir = []

    if tipo_cartao == "Otimizados":
        cartoes_para_conferir = st.session_state.get("cartoes_gerados", [])
    elif tipo_cartao == "Aleatórios (300)":
        cartoes_para_conferir = st.session_state.get("cartoes_gerados_aleatorios", [])
    elif tipo_cartao == "Probabilísticos":
        cartoes_para_conferir = st.session_state.get("cartoes_probabilisticos", [])
    elif tipo_cartao == "Inversos":
        cartoes_para_conferir = st.session_state.get("cartoes_inversos", [])

    if cartoes_para_conferir:
        min_concursos = st.slider("Mínimo de concursos com 13+ pontos para destacar cartão:", 1, 10, 3)

        if st.button("✅ Conferir Desempenho dos Cartões"):
            with st.spinner("🔍 Verificando desempenho..."):
                resultados, faixa_acertos, desempenho, bons_cartoes, destaques = conferir_cartoes(
                    cartoes_para_conferir,
                    concursos_dinamico,
                    filtrar_excelentes=True,
                    min_acertos=min_concursos
                )

            st.subheader("📈 Faixas de Acertos")
            for pontos in range(11, 16):
                st.write(f"✅ {pontos} pontos: `{faixa_acertos.get(pontos, 0)}`")

            st.subheader(f"🏅 Cartões com pelo menos {min_concursos}x com 13+ pontos:")
            if bons_cartoes:
                for i, c in enumerate(bons_cartoes, 1):
                    st.write(f"{i:02d}) `{sorted(c)}`")
            else:
                st.info("Nenhum cartão teve desempenho destacado.")

            st.markdown("---")
            st.subheader("🏆 Detalhamento: Cartões com 14 ou 15 pontos + Histórico anterior")

            detalhes = []
            historico_anterior = {}

            for idx, cartao in enumerate(cartoes_para_conferir):
                for pos, concurso in enumerate(concursos_dinamico):
                    num, _, dezenas_sorteadas = concurso
                    acertos = len(set(cartao) & set(dezenas_sorteadas))

                    if acertos in [14, 15]:
                        detalhes.append({
                            "cartao_idx": idx + 1,
                            "cartao": sorted(cartao),
                            "concurso": num,
                            "acertos": acertos,
                            "sorteadas": sorted(dezenas_sorteadas)
                        })

                        historico = []
                        for prev in concursos_dinamico[pos+1:]:
                            num_ant, _, dezenas_ant = prev
                            acertos_ant = len(set(cartao) & set(dezenas_ant))
                            if acertos_ant in [11, 12, 13]:
                                historico.append((num_ant, acertos_ant, sorted(dezenas_ant)))
                        historico_anterior[(idx + 1, num)] = historico

            if detalhes:
                for item in detalhes:
                    st.markdown(f"""
                    🎯 **{item['acertos']} pontos** no concurso **{item['concurso']}**  
                    - 🪪 Cartão **{item['cartao_idx']}**: `{item['cartao']}`  
                    - 🎱 Sorteio: `{item['sorteadas']}`
                    """)
                    chave = (item['cartao_idx'], item['concurso'])
                    historico = historico_anterior.get(chave, [])
                    if historico:
                        st.markdown("🔄 Histórico anterior com 11 a 13 pontos:")
                        for num, acertos, dezenas in historico:
                            st.write(f"• Concurso {num}: {acertos} pontos — `{dezenas}`")
                    else:
                        st.info("Nenhum desempenho anterior relevante.")
            else:
                st.info("Nenhum cartão fez 14 ou 15 pontos.")
    else:
        st.warning("Gere os cartões primeiro para poder conferi-los.")

# 📅 Histórico
with abas[4]:
    st.markdown("### 📅 Ver os últimos concursos", unsafe_allow_html=True)
    for item in concursos_dinamico:
        numero = item[0]
        dezenas = ", ".join(str(d).zfill(2) for d in sorted(item[2]))
        st.write(f"Concurso {numero}: {dezenas}")

# 🚫 Inverso
with abas[5]:
    st.markdown("### 🚫 Gerar Cartões Inversos (excluindo dezenas menos prováveis)")
    qtde_inversos = st.slider("📌 Quantidade de cartões inversos:", 1, 1000, 200)
    qtd_excluir = st.slider("❌ Quantas dezenas deseja excluir (menos frequentes):", 5, 10, 10)

    if st.button("🚫 Gerar Cartões Inversos"):
        with st.spinner("🔍 Analisando concursos..."):
            cartoes_inversos, excluidas = gerar_cartoes_inversos(
                concursos_dinamico,
                quantidade=qtde_inversos,
                excluir_qtd=qtd_excluir
            )

        if not cartoes_inversos:
            st.error("⚠️ Não foi possível gerar cartões com os critérios definidos.")
        else:
            st.success(f"✅ {len(cartoes_inversos)} cartões gerados excluindo as {qtd_excluir} menos frequentes.")
            st.markdown(f"**🔻 Dezenas excluídas:** `{sorted(excluidas)}`")
            st.session_state.cartoes_inversos = cartoes_inversos
            st.markdown("---")
            for i, c in enumerate(cartoes_inversos, 1):
                st.write(f"Cartão Inverso {i:02d}: `{sorted(c)}`")

# 📌 Rodapé fixo
st.markdown("""
<hr style='border: 1px solid #ccc;'/>
<div style='text-align: center; font-size: 0.9em; color: #666;'>
© 2025  Desenvolvido por SAMUCJ TECHNOLOGY
</div>
""", unsafe_allow_html=True)
