import pandas as pd 
import openpyxl as px
import gspread
from google.oauth2.service_account import Credentials
import os

class GoogleCloud:
    def __init__(self):
        self.CAMINHO_CREDENCIAIS = "boletim.json"
        self.ID_PLANILHA = "1cHbKXMjJgnR_M3X2uGtDT3kPHTrlBd_g4kqxhrr6MOY"   
        self.NOME_ABAS = {
            "voz": "BASE VOZ",
            "voz_fila": "BASE VOZ FILA",
            "texto": "BASE TEXTO",
            "texto_fila": "BASE TEXTO FILA",
            "ge_fila": "BASE GE FILA",
            "ge_colab": "BASE GE COLABORADOR" 
        }

        # Autenticação
        scopes = ["https://www.googleapis.com/auth/spreadsheets", 
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(self.CAMINHO_CREDENCIAIS, scopes=scopes)
        self.client = gspread.authorize(creds)

    # funções para baixar cada base e enviar para dentro de sua respectiva pagina
    def baixar_base_voz(self):
        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["voz"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["voz"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['voz']}")

    def baixar_base_voz_fila(self):

        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["voz_fila"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["voz_fila"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['voz_fila']}")

    def baixar_base_texto(self):

        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["texto"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["texto"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['texto']}")

    def baixar_base_texto_fila(self):

        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["texto_fila"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["texto_fila"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['texto_fila']}")

    def baixar_base_ge_fila(self):

        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["ge_fila"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["ge_fila"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['ge_fila']}")

    def baixar_ge_colab(self):

        # Lê o CSV
        caminho_csv = self.ARQUIVOS_CSV["ge_colab"]
        df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")

        # Abre a planilha e aba correta
        planilha = self.client.open_by_key(self.ID_PLANILHA)
        aba = planilha.worksheet(self.NOME_ABAS["ge_colab"])

        # Limpa a aba antes de atualizar
        aba.clear()

        # Converte DataFrame para lista
        dados = [df.columns.values.tolist()] + df.values.tolist()

        # Atualiza os valores no Google Sheets
        aba.update(dados)
        print(f"Dados enviados para aba: {self.NOME_ABAS['ge_colab']}")