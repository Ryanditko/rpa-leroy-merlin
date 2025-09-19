import pandas as pd 
import openpyxl as px
import gspread
from google.oauth2.service_account import Credentials
import os

class GoogleCloud:
    def __init__(self):
        self.CAMINHO_CREDENCIAIS = "pulso.json"
        self.ID_PLANILHA = "1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0"   
        self.NOME_ABAS = {
            "resolvida_por": "BASE ATUALIZADA CORRETA - RESOLVIDA",
            "dados_seller": "DADOS SELLER",
            "comentarios_bko": "COMENTARIO BKO",
            "criado_por": "BASE ATUALIZADA CORRETA - CRIADO"
        }
        
        # Configuração dos arquivos CSV para cada base
        self.ARQUIVOS_CSV = {
            "resolvida_por": "dados_resolvidos.csv",
            "dados_seller": "dados_seller.csv", 
            "comentarios_bko": "comentarios_bko.csv",
            "criado_por": "dados_criados.csv"
        }

        # Autenticação
        scopes = ["https://www.googleapis.com/auth/spreadsheets", 
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(self.CAMINHO_CREDENCIAIS, scopes=scopes)
        self.client = gspread.authorize(creds)

    #TODO funções para baixar cada base e enviar para dentro de sua respectiva pagina