from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pypdf import PdfReader
from langchain_openai import ChatOpenAI

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Extração de dados estruturados de notas fiscais usando LLM
class DadosNotaFiscal(BaseModel):
    razao_social_prestador: str = Field(description="Nome da empresa que prestou o serviço ou emitiu a nota")
    cnpj_prestador: str = Field(description="CNPJ do prestador no formato XX.XXX.XXX/XXXX-XX")
    valor_total: float = Field(description="Valor total da nota fiscal em formato decimal")
    descricao_servico: str = Field(description="Resumo do serviço prestado detalhado em no máximo duas frases")

# Extrair as informações e retornar texto.
def extrair_texto_pdf(arquivo_pdf) -> str:

    leitor = PdfReader(arquivo_pdf) # Abre o arquivo PDF para leitura
    texto = ""
    for pagina in leitor.pages:
        texto_pagina = pagina.extract_text()
        if texto_pagina:
            texto += texto_pagina + "\n"
    return texto

def extrair_dados_llm(texto_documento: str) -> DadosNotaFiscal:
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Utiliza o modelo GPT-4o-mini para extração de dados estruturados
    extrator = llm.with_structured_output(DadosNotaFiscal)
    
    prompt = f"Extraia as informações fiscais do seguinte documento:\n\n{texto_documento}"
    return extrator.invoke(prompt)