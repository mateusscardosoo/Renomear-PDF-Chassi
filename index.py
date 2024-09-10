import os
import re
import pdfplumber


def renomear_pdfs_em_massa(caminho_pasta):
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith('.pdf'):
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            
            try:
                with pdfplumber.open(caminho_completo) as pdf:
                    texto_completo = ""

                    for pagina in pdf.pages:
                        texto_completo += pagina.extract_text() or ''
                
                match = re.search(r'CHASSI:\s*([A-Z0-9]{17})', texto_completo.replace('\n', '').strip(), re.IGNORECASE)
                
                if match:
                    chassi = match.group(1)
                    novo_nome = f"{chassi}.pdf"
                    caminho_novo_arquivo = os.path.join(caminho_pasta, novo_nome)
                    print(caminho_novo_arquivo)

                    try:
                        os.rename(caminho_completo, caminho_novo_arquivo)
                        print(f"Arquivo {arquivo} renomeado para {novo_nome}.")
                    except OSError as e:
                        if e.errno == 32:  
                            print(f"Erro ao renomear {arquivo}: {e}")
                        else:
                            raise  
                else:
                    print(f"Chassi não encontrado no arquivo {arquivo}.")
            
            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo {arquivo}: {e}")

caminho_da_pasta = './NFs' 
renomear_pdfs_em_massa(caminho_da_pasta)
