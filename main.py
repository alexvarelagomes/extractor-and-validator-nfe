import streamlit as st
from llm import extrair_texto_pdf, extrair_dados_llm

st.set_page_config(page_title="Extrator Fiscal IA", layout="centered")
st.title("Extrator de Documentos Fiscais")
st.write("Faça o upload de uma nota fiscal em PDF para extrair os dados estruturados via IA.")

arquivo_upload = st.file_uploader("Selecione o documento (PDF)", type=["pdf"])

if arquivo_upload is not None:
    if st.button("Processar Documento"):
        with st.spinner("Lendo e analisando o documento..."):
            # Leitura do arquivo e extração do texto
            texto_extraido = extrair_texto_pdf(arquivo_upload)
            
            if not texto_extraido.strip():
                st.error("O PDF parece estar vazio ou é uma imagem escaneada. OCR é necessário.")
            else:
                # Extrair dados estruturados usando LLM
                dados_estruturados = extrair_dados_llm(texto_extraido)
                
                # Exibe os dados extraídos em formato JSON
                st.success("Extração concluída!")
                st.json(dados_estruturados.model_dump())