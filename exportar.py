from fpdf import FPDF

def exportar_txt(cartoes):
    linhas = [f"Cartão {i}: {' - '.join(f'{n:02}' for n in sorted(cartao))}" for i, cartao in enumerate(cartoes, 1)]
    return "\n".join(linhas)

def exportar_pdf(cartoes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, cartao in enumerate(cartoes, 1):
        linha = f"Cartão {i}: {' - '.join(f'{n:02}' for n in sorted(cartao))}"
        pdf.cell(0, 10, linha, ln=True)
    return pdf.output(dest='S').encode('latin1')
