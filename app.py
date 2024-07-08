import gradio as gr
from pdf2docx import Converter
from docx import Document
from fpdf import FPDF
import os

title_and_description = """
# Conversor de PDF para Word e Word para PDF
Criado por [@artificialguybr](https://artificialguy.com)
Faça o upload de um arquivo PDF para converter para Word ou um arquivo Word para converter para PDF.
## Características
- **Fácil de usar**: Interface simples para fazer upload de arquivos PDF ou Word e converter para o formato desejado.
- **Alta qualidade**: Converte mantendo a melhor qualidade possível.
- **Processamento eficiente**: Usa `pdf2docx`, `fpdf` e `docx` para conversões rápidas e confiáveis.
- **Uso ilimitado**: Sem limite de arquivos. Use à vontade!
Sinta-se à vontade para usar em seus próprios documentos!
"""

def pdf_to_word(pdf_file):
    docx_filename = pdf_file.name.replace('.pdf', '.docx')
    
    cv = Converter(pdf_file.name)
    cv.convert(docx_filename, multi_processing=True, start=0, end=None)
    cv.close()
    
    return docx_filename

def word_to_pdf(docx_file):
    pdf_filename = "output.pdf"
    
    doc = Document(docx_file)
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
    pdf.set_font('Arial', size=12)

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:  # Ignorar linhas vazias
            continue
        # Quebrar o texto em várias linhas se necessário
        words = text.split()
        line = ''
        for word in words:
            if pdf.get_string_width(line + word) < (pdf.w - 2 * pdf.l_margin):
                line += word + ' '
            else:
                pdf.cell(0, 10, line, ln=True)
                line = word + ' '
        if line:
            pdf.cell(0, 10, line, ln=True)

    pdf.output(pdf_filename)
    return pdf_filename

with gr.Blocks() as app:
    gr.Markdown(title_and_description)
    
    with gr.Row():
        with gr.Column():
            with gr.Accordion("PDF para Word"):
                pdf_input = gr.File(label="Faça upload do PDF")
                convert_pdf_to_word = gr.Button("Converter para Word")
                word_output = gr.File(label="Baixar arquivo Word", type="filepath")
                
                convert_pdf_to_word.click(pdf_to_word, inputs=[pdf_input], outputs=[word_output])
                
        with gr.Column():
            with gr.Accordion("Word para PDF"):
                word_input = gr.File(label="Faça upload do Word")
                convert_word_to_pdf = gr.Button("Converter para PDF")
                pdf_output = gr.File(label="Baixar arquivo PDF", type="filepath")
                
                convert_word_to_pdf.click(word_to_pdf, inputs=[word_input], outputs=[pdf_output])

app.launch()
