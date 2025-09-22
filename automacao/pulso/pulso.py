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

# funções para baixar cada base e enviar para dentro de sua respectiva pagina
    def baixar_resolvido_por(self):
        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["resolvida_por"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["resolvida_por"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['resolvida_por']}")

    def baixar_dados_seller(self):
        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["dados_seller"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["dados_seller"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['dados_seller']}")

    def baixar_comentarios_bko(self):
        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["comentarios_bko"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["comentarios_bko"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['comentarios_bko']}")

    def baixar_criado_por(self):
        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["criado_por"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["criado_por"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['criado_por']}")

        
