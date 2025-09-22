"""
Classe base para conexão e operações com Google Sheets
Com suporte a inserção incremental (sem apagar dados existentes)
"""
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleSheetsBase:
    def __init__(self, projeto):
        """
        Inicializa conexão com Google Sheets
        
        Args:
            projeto (str): Nome do projeto (boletim, csat, pulso)
        """
        self.projeto = projeto
        self.config = Config.PLANILHAS_CONFIG[projeto]
        
        # Caminho das credenciais
        self.caminho_credenciais = Config.get_credenciais_path(self.config["credenciais"])
        self.id_planilha = self.config["id_planilha"]
        self.nome_abas = self.config["abas"]
        
        # Autenticação
        self._autenticar()
    
    def _autenticar(self):
        """Autentica com Google Sheets API"""
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            creds = Credentials.from_service_account_file(
                str(self.caminho_credenciais), 
                scopes=scopes
            )
            self.client = gspread.authorize(creds)
            self.planilha = self.client.open_by_key(self.id_planilha)
            
            logger.info(f"Autenticação realizada com sucesso para projeto: {self.projeto}")
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {e}")
            raise
    
    def listar_abas(self):
        """Lista todas as abas da planilha"""
        try:
            abas = [sheet.title for sheet in self.planilha.worksheets()]
            logger.info(f"Abas encontradas: {abas}")
            return abas
        except Exception as e:
            logger.error(f"Erro ao listar abas: {e}")
            return []
    
    def encontrar_primeira_linha_vazia(self, nome_aba):
        """
        Encontra a primeira linha vazia em uma aba
        
        Args:
            nome_aba (str): Nome da aba
            
        Returns:
            int: Número da primeira linha vazia
        """
        try:
            aba = self.planilha.worksheet(nome_aba)
            valores = aba.get_all_values()
            
            # Se a aba estiver vazia, retorna linha 1
            if not valores:
                return 1
            
            # Encontrar primeira linha completamente vazia
            for i, linha in enumerate(valores, 1):
                if not any(linha):  # Se todos os valores da linha estão vazios
                    return i
            
            # Se não encontrou linha vazia, retorna a próxima após a última
            return len(valores) + 1
            
        except Exception as e:
            logger.error(f"Erro ao encontrar linha vazia na aba {nome_aba}: {e}")
            return 1
    
    def inserir_dados_incremental(self, nome_aba, dados_df, incluir_cabecalho=False):
        """
        Insere dados de forma incremental (sem apagar dados existentes)
        
        Args:
            nome_aba (str): Nome da aba
            dados_df (pd.DataFrame): DataFrame com os dados
            incluir_cabecalho (bool): Se deve incluir cabeçalho
        """
        try:
            aba = self.planilha.worksheet(nome_aba)
            
            # Encontrar primeira linha vazia
            primeira_linha_vazia = self.encontrar_primeira_linha_vazia(nome_aba)
            
            # Preparar dados
            if incluir_cabecalho and primeira_linha_vazia == 1:
                # Incluir cabeçalho apenas se for a primeira inserção
                dados = [dados_df.columns.tolist()] + dados_df.values.tolist()
            else:
                # Apenas dados, sem cabeçalho
                dados = dados_df.values.tolist()
            
            if not dados:
                logger.warning(f"Nenhum dado para inserir na aba {nome_aba}")
                return
            
            # Calcular range para inserção
            inicio_col = "A"
            fim_col = chr(ord('A') + len(dados_df.columns) - 1)
            inicio_linha = primeira_linha_vazia
            fim_linha = inicio_linha + len(dados) - 1
            
            range_insercao = f"{inicio_col}{inicio_linha}:{fim_col}{fim_linha}"
            
            # Inserir dados
            aba.update(range_insercao, dados)
            
            logger.info(f"Dados inseridos na aba '{nome_aba}' - Range: {range_insercao} - {len(dados)} linhas")
            
        except Exception as e:
            logger.error(f"Erro ao inserir dados na aba {nome_aba}: {e}")
            raise
    
    def limpar_aba(self, nome_aba):
        """Limpa completamente uma aba (método antigo, manter para compatibilidade)"""
        try:
            aba = self.planilha.worksheet(nome_aba)
            aba.clear()
            logger.info(f"Aba '{nome_aba}' limpa com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar aba {nome_aba}: {e}")
            raise
    
    def atualizar_aba_completa(self, nome_aba, dados_df):
        """
        Atualiza aba completa (limpa e insere tudo novamente)
        Método antigo, usar apenas quando necessário
        """
        try:
            aba = self.planilha.worksheet(nome_aba)
            
            # Limpar aba
            aba.clear()
            
            # Preparar dados com cabeçalho
            dados = [dados_df.columns.tolist()] + dados_df.values.tolist()
            
            # Atualizar
            aba.update(dados)
            
            logger.info(f"Aba '{nome_aba}' atualizada completamente - {len(dados_df)} linhas")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar aba completa {nome_aba}: {e}")
            raise
    
    def ler_csv_e_processar(self, caminho_csv, **kwargs):
        """
        Lê arquivo CSV e retorna DataFrame processado
        
        Args:
            caminho_csv (str): Caminho para o arquivo CSV
            **kwargs: Argumentos adicionais para pd.read_csv
        """
        try:
            # Parâmetros padrão para leitura
            params_padrao = {
                'sep': ',',
                'encoding': 'utf-8',
                'na_values': ['', 'NaN', 'null', 'NULL']
            }
            
            # Atualizar com parâmetros customizados
            params_padrao.update(kwargs)
            
            df = pd.read_csv(caminho_csv, **params_padrao)
            
            # Limpeza básica
            df = df.dropna(how='all')  # Remove linhas completamente vazias
            df = df.fillna('')  # Substitui NaN por string vazia
            
            logger.info(f"CSV lido com sucesso: {caminho_csv} - {len(df)} linhas")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV {caminho_csv}: {e}")
            raise

    def testar_conexao(self):
        """Testa a conexão listando as abas"""
        try:
            abas = self.listar_abas()
            logger.info(f"Teste de conexão bem-sucedido. Abas disponíveis: {len(abas)}")
            return True
        except Exception as e:
            logger.error(f"Teste de conexão falhou: {e}")
            return False
