"""
Processamento da base VOZ
"""
import pandas as pd
import sys
from pathlib import Path

# Adicionar path para importar a classe base
sys.path.append(str(Path(__file__).parent.parent / "core"))

from google_sheets_base import GoogleSheetsBase
from config import CONFIG
import logging

logger = logging.getLogger(__name__)

class ProcessadorVoz(GoogleSheetsBase):
    def __init__(self):
        super().__init__("boletim")  # Usa configuração do projeto boletim
        
    def processar_voz(self, caminho_csv=None):
        """
        Processa base VOZ e envia para Google Sheets
        
        Args:
            caminho_csv (str): Caminho para o arquivo CSV. Se None, busca na pasta processada
        """
        try:
            # Se não foi especificado caminho, buscar na pasta processada
            if not caminho_csv:
                processed_files = Path("processed") / "voz.csv"
                if not processed_files.exists():
                    logger.error("Arquivo voz.csv não encontrado na pasta processada")
                    return False
                caminho_csv = processed_files
            
            # Ler e processar CSV (usar ponto e vírgula como separador para arquivos do Genesys)
            df = self.ler_csv_e_processar(caminho_csv, sep=';')
            
            if df.empty:
                logger.warning("DataFrame vazio para base VOZ")
                return False
            
            # Aplicar transformações específicas para VOZ
            df = self._transformar_dados_voz(df)
            
            # Inserir dados de forma incremental
            self.inserir_dados_incremental("BASE VOZ", df, incluir_cabecalho=False)
            
            logger.info(f"Base VOZ processada com sucesso - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar base VOZ: {e}")
            return False
    
    def processar_voz_fila(self, caminho_csv=None):
        """
        Processa base VOZ FILA e envia para Google Sheets
        """
        try:
            # Se não foi especificado caminho, buscar na pasta processada
            if not caminho_csv:
                processed_files = Path("processed") / "voz_fila.csv"
                if not processed_files.exists():
                    logger.error("Arquivo voz_fila.csv não encontrado na pasta processada")
                    return False
                caminho_csv = processed_files
            
            # Ler e processar CSV
            df = self.ler_csv_e_processar(caminho_csv)
            
            if df.empty:
                logger.warning("DataFrame vazio para base VOZ FILA")
                return False
            
            # Aplicar transformações específicas para VOZ FILA
            df = self._transformar_dados_voz_fila(df)
            
            # Inserir dados de forma incremental
            self.inserir_dados_incremental("BASE VOZ FILA", df, incluir_cabecalho=False)
            
            logger.info(f"Base VOZ FILA processada com sucesso - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar base VOZ FILA: {e}")
            return False
    
    def _transformar_dados_voz(self, df):
        """
        Aplica transformações específicas para dados VOZ
        
        Args:
            df (pd.DataFrame): DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame transformado
        """
        try:
            # Exemplo de transformações (ajustar conforme necessário)
            
            # Converter datas se houver colunas de data
            date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar espaços em branco
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            # Remover linhas duplicadas se houver
            df = df.drop_duplicates()
            
            logger.info("Transformações aplicadas aos dados VOZ")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados VOZ: {e}")
            return df
    
    def _transformar_dados_voz_fila(self, df):
        """
        Aplica transformações específicas para dados VOZ FILA
        """
        try:
            # Transformações específicas para VOZ FILA
            
            # Converter datas
            date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar dados
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            df = df.drop_duplicates()
            
            logger.info("Transformações aplicadas aos dados VOZ FILA")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados VOZ FILA: {e}")
            return df

if __name__ == "__main__":
    # Teste da classe
    processador = ProcessadorVoz()
    
    # Testar conexão
    if processador.testar_conexao():
        print("Conexão teste bem-sucedida!")
        
        # Processar bases se arquivos existirem
        processador.processar_voz()
        processador.processar_voz_fila()
    else:
        print("Erro na conexão!")
