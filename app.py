
import streamlit as st
from gerador_otimizado import gerar_cartoes_otimizados
from exportar import exportar_pdf, exportar_txt
from api_lotofacil import obter_ultimos_concursos
from estatisticas import calcular_frequencia

st.set_page_config(page_title="Lotofácil Inteligente", layout="wide")

st.title("💡 Lotofácil Inteligente")

abas = st.tabs(["🏠 Início", "📈 Estatísticas", "📊 Conferência", "🎯 Cartões Otimizados"])

# Aba de Cartões Otimizados
with abas[3]:
    st.header("🎯 Gerador de Cartões Otimizados")

    concursos = obter_ultimos_concursos()
    freq_dict = calcular_frequencia(concursos)
    dezenas_ordenadas = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    dezenas_mais_freq = [d[0] for d in dezenas_ordenadas[:15]]
    dezenas_menos_freq = [d[0] for d in dezenas_ordenadas[-5:]]

    qtd_cartoes = st.number_input("Quantidade de cartões otimizados a gerar", min_value=1, max_value=100, value=10, step=1)

    if st.button("Gerar Cartões Otimizados"):
        cartoes_otimizados = gerar_cartoes_otimizados(qtd_cartoes, dezenas_mais_freq, dezenas_menos_freq)
        for i, c in enumerate(cartoes_otimizados, 1):
            st.write(f"Cartão {i}: {c}")

        nome_arquivo = "cartoes_otimizados"
        st.download_button("📄 Exportar PDF", data=exportar_pdf(cartoes_otimizados), file_name=f"{nome_arquivo}.pdf")
        st.download_button("📄 Exportar TXT", data=exportar_txt(cartoes_otimizados), file_name=f"{nome_arquivo}.txt")
