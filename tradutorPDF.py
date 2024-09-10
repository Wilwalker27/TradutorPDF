import fitz  # PyMuPDF
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *

# Função para dividir o texto em partes menores
def dividir_texto(texto, tamanho_max):
    palavras = texto.split()
    partes = []
    parte_atual = []
    tamanho_atual = 0

    for palavra in palavras:
        if tamanho_atual + len(palavra) + 1 > tamanho_max:
            partes.append(' '.join(parte_atual))
            parte_atual = [palavra]
            tamanho_atual = len(palavra) + 1
        else:
            parte_atual.append(palavra)
            tamanho_atual += len(palavra) + 1

    if parte_atual:
        partes.append(' '.join(parte_atual))

    return partes

# Função para traduzir e gerar o PDF
def traduzir_e_gerar_pdf(pdf_path, output_pdf_path):
    # Abrir o PDF
    pdf_document = fitz.open(pdf_path)

    # Extrair texto de todas as páginas
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    # Inicializar o tradutor
    translator = Translator()

    # Dividir o texto em partes menores
    partes_texto = dividir_texto(text, 5000)

    # Traduzir cada parte individualmente
    partes_traduzidas = []
    for parte in partes_texto:
        traduzido = translator.translate(parte, src='en', dest='pt')
        partes_traduzidas.append(traduzido.text)

    # Combinar as partes traduzidas
    texto_traduzido = ' '.join(partes_traduzidas)

    # Gerar um novo PDF com o texto traduzido
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    # Adicionar o texto ao PDF
    y = height - 40  # Margem superior
    for linha in texto_traduzido.split('\n'):
        linhas = linha.split(' ')
        linha_atual = ""
        for palavra in linhas:
            if c.stringWidth(linha_atual + palavra) < width - 80:
                linha_atual += palavra + " "
            else:
                c.drawString(40, y, linha_atual.strip())
                y -= 15  # Espaçamento entre linhas
                linha_atual = palavra + " "
                if y < 40:  # Verificar se há espaço suficiente na página
                    c.showPage()
                    y = height - 40
        c.drawString(40, y, linha_atual.strip())
        y -= 15  # Espaçamento entre linhas
        if y < 40:  # Verificar se há espaço suficiente na página
            c.showPage()
            y = height - 40

    c.save()

# Função para selecionar o arquivo PDF
def selecionar_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entrada_arquivo.set(file_path)

# Função para iniciar a tradução e geração do PDF
def iniciar_traducao():
    pdf_path = entrada_arquivo.get()
    if not pdf_path:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
        return

    output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_pdf_path:
        return

    try:
        traduzir_e_gerar_pdf(pdf_path, output_pdf_path)
        messagebox.showinfo("Sucesso", "PDF traduzido e salvo com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao traduzir o PDF: {e}")

# Criar a interface gráfica
root = tk.Tk()
root.title("Tradutor de PDF")
style = Style(theme="darkly")

# Variável para armazenar o caminho do arquivo PDF
entrada_arquivo = tk.StringVar()

# Frame principal
frame_principal = ttk.Frame(root, padding="20")
frame_principal.pack(padx=10, pady=10)

# Botão para selecionar o arquivo PDF
btn_selecionar = ttk.Button(frame_principal, text="Selecionar PDF", command=selecionar_arquivo, bootstyle=PRIMARY)
btn_selecionar.pack(pady=10)

# Entrada para exibir o caminho do arquivo PDF selecionado
entrada_pdf = ttk.Entry(frame_principal, textvariable=entrada_arquivo, width=50, state="readonly")
entrada_pdf.pack(pady=10)

# Botão para iniciar a tradução e geração do PDF
btn_iniciar = ttk.Button(frame_principal, text="Iniciar Tradução", command=iniciar_traducao, bootstyle=SUCCESS)
btn_iniciar.pack(pady=10)

# Iniciar o loop principal da interface gráfica
root.mainloop()