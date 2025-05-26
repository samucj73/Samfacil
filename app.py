import streamlit as st
from datetime import datetime
from api_lotofacil import capturar_ultimos_resultados
from gerador_otimizado import gerar_cartoes_otimizados
from gerador_probabilistico import gerar_cartoes_mais_possiveis
from conferencia import conferir_cartoes

st.set_page_config(page_title="LotoFácil Inteligente", layout="centered")

st.markdown("<h1 style='text-align: center;'>🔮 LotoFácil Inteligente</h1>", unsafe_allow_html=True)

# 🔄 Atualização de concursos
if st.button("🔁 Atualizar concursos"):
    st.session_state.pop("concursos_25", None)
    st.session_state.pop("concursos_300", None)

if "concursos_25" not in st.session_state:
    with st.spinner("🔄 Buscando últimos 25 resultados da Lotofácil..."):
        concursos = capturar_ultimos_resultados(qtd=25)
        if not concursos:
            st.error("❌ Não foi possível obter os resultados.")
            st.stop()
        st.session_state.concursos_25 = concursos

if "concursos_300" not in st.session_state:
    with st.spinner("🔄 Buscando os 300 últimos concursos..."):
        concursos_300 = capturar_ultimos_resultados(qtd=300)
        st.session_state.concursos_300 = concursos_300

concursos = st.session_state.concursos_25
concursos_300 = st.session_state.concursos_300

numero, data, dezenas = concursos[0]
st.markdown(f"<h4 style='text-align: center;'>📅 Último concurso: {numero} ({data})</h4>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>**Dezenas sorteadas:** `{sorted(dezenas)}`</p>", unsafe_allow_html=True)
st.divider()

# 🗂️ Abas principais
abas = st.tabs(["📈 Otimizados", "🎲 Aleatórios", "📊 Probabilísticos", "✅ Conferência", "📅 Históricos"])

# 📈 Geração Otimizada
with abas[0]:
    st.markdown("### 🎰 Geração de Cartões Otimizados", unsafe_allow_html=True)
    qtde_cartoes = st.slider("📌 Quantidade de cartões a gerar:", 1, 2000, 450)

    if st.button("🚀 Gerar Cartões Otimizados"):
        with st.spinner("🔍 Gerando cartões com filtros avançados..."):
            cartoes = gerar_cartoes_otimizados(concursos, qtde_cartoes)
            st.session_state.cartoes_gerados = cartoes

        st.success(f"✅ {len(cartoes)} cartões gerados!")
        for i, c in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: `{c}`")
        st.divider()

# 🎲 Aleatórios base 300 concursos
with abas[1]:
    st.markdown("### 🎲 Geração Aleatória com Base nos 300 Últimos Concursos", unsafe_allow_html=True)

    if st.button("🎲 Gerar Aleatórios Base 300"):
        from gerador_otimizado import gerar_cartoes_aleatorios_base_300

        with st.spinner("🎲 Gerando cartões aleatórios..."):
            cartoes_aleatorios = gerar_cartoes_aleatorios_base_300(concursos_300, qtde_cartoes)
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
            cartoes_prob = gerar_cartoes_mais_possiveis(concursos_300, quantidade=qtde_prob)
            st.session_state.cartoes_probabilisticos = cartoes_prob

        st.success(f"✅ {len(cartoes_prob)} cartões gerados com base em frequência!")
        for i, c in enumerate(cartoes_prob, 1):
            st.write(f"Probabilístico {i:02d}: `{c}`")
        st.divider()

# ✅ Conferência
with abas[3]:
    st.markdown("### 📊 Conferência de Cartões", unsafe_allow_html=True)
    tipo_cartao = st.radio("Escolha quais cartões deseja conferir:",
                           ["Otimizados", "Aleatórios (300)", "Probabilísticos"],
                           horizontal=True)

    if tipo_cartao == "Otimizados" and "cartoes_gerados" in st.session_state:
        cartoes_para_conferir = st.session_state.cartoes_gerados
    elif tipo_cartao == "Aleatórios (300)" and "cartoes_gerados_aleatorios" in st.session_state:
        cartoes_para_conferir = st.session_state.cartoes_gerados_aleatorios
    elif tipo_cartao == "Probabilísticos" and "cartoes_probabilisticos" in st.session_state:
        cartoes_para_conferir = st.session_state.cartoes_probabilisticos
    else:
        cartoes_para_conferir = []

    if cartoes_para_conferir:
        min_concursos = st.slider("Mínimo de concursos com 13+ pontos para destacar cartão:", 1, 10, 3)

        if st.button("✅ Conferir Desempenho dos Cartões"):
            with st.spinner("🔍 Verificando desempenho..."):
                resultados, faixa_acertos, desempenho, bons_cartoes, destaques = conferir_cartoes(
                    cartoes_para_conferir,
                    concursos,
                    filtrar_excelentes=True,
                    min_acertos=min_concursos
                )

            st.markdown("#### 📈 Faixas de Acertos", unsafe_allow_html=True)
            for pontos in range(11, 16):
                st.write(f"✅ {pontos} pontos: `{faixa_acertos.get(pontos, 0)}`")

            st.markdown(f"#### 🏅 Cartões com pelo menos {min_concursos}x com 13+ pontos:", unsafe_allow_html=True)
            if bons_cartoes:
                for i, c in enumerate(bons_cartoes, 1):
                    st.write(f"{i:02d}) `{sorted(c)}`")
            else:
                st.info("Nenhum cartão teve desempenho destacado.")

            st.markdown("---")
            st.markdown("### 🏆 Detalhamento: Cartões com 14 ou 15 pontos + Histórico anterior", unsafe_allow_html=True)

            detalhes = []
            historico_anterior = {}

            for idx, cartao in enumerate(cartoes_para_conferir):
                for pos, concurso in enumerate(concursos):
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
                        for prev in concursos[pos+1:]:
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
                        st.markdown(f"🔄 Histórico anterior com 11 a 13 pontos:")
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
    st.markdown("### 📅 Ver os 300 últimos concursos", unsafe_allow_html=True)
    for item in concursos_300:
        numero = item[0]
        dezenas = ", ".join(str(d).zfill(2) for d in sorted(item[2]))
        st.write(f"Concurso {numero}: {dezenas}")

# 📌 Rodapé fixo
st.markdown("""
<hr style='border: 1px solid #ccc;'/>
<div style='text-align: center; font-size: 0.9em; color: #666;'>
    © 2025 LotoFácil Inteligente — Desenvolvido com ❤️ por SeuNome
</div>
""", unsafe_allow_html=True)
