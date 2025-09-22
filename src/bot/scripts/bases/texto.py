"""
Processamento da base TEXTO
"""
import pandas as pd
from google_sheets_base import GoogleSheetsBase
from config import Config
import logging

logger = logging.getLogger(__name__)

class ProcessadorTexto(GoogleSheetsBase):
    def __init__(self):
        super().__init__("boletim")  # Usa configuração do projeto boletim
        
    def processar_texto(self, caminho_csv=None):
        """
        Processa base TEXTO e envia para Google Sheets
        
        Args:
            caminho_csv (str): Caminho para o arquivo CSV. Se None, busca na pasta processada
        """
        try:
            # Se não foi especificado caminho, buscar na pasta processada
            if not caminho_csv:
                processed_files = Config.PROCESSED_DIR / "texto.csv"
                if not processed_files.exists():
                    logger.error("Arquivo texto.csv não encontrado na pasta processada")
                    return False
                caminho_csv = processed_files
            
            # Ler e processar CSV
            df = self.ler_csv_e_processar(caminho_csv)
            
            if df.empty:
                logger.warning("DataFrame vazio para base TEXTO")
                return False
            
            # Aplicar transformações específicas para TEXTO
            df = self._transformar_dados_texto(df)
            
            # Inserir dados de forma incremental
            self.inserir_dados_incremental("BASE TEXTO", df, incluir_cabecalho=False)
            
            logger.info(f"Base TEXTO processada com sucesso - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar base TEXTO: {e}")
            return False
    
    def processar_texto_fila(self, caminho_csv=None):
        """
        Processa base TEXTO FILA e envia para Google Sheets
        """
        try:
            # Se não foi especificado caminho, buscar na pasta processada
            if not caminho_csv:
                processed_files = Config.PROCESSED_DIR / "texto_fila.csv"
                if not processed_files.exists():
                    logger.error("Arquivo texto_fila.csv não encontrado na pasta processada")
                    return False
                caminho_csv = processed_files
            
            # Ler e processar CSV
            df = self.ler_csv_e_processar(caminho_csv)
            
            if df.empty:
                logger.warning("DataFrame vazio para base TEXTO FILA")
                return False
            
            # Aplicar transformações específicas para TEXTO FILA
            df = self._transformar_dados_texto_fila(df)
            
            # Inserir dados de forma incremental
            self.inserir_dados_incremental("BASE TEXTO FILA", df, incluir_cabecalho=False)
            
            logger.info(f"Base TEXTO FILA processada com sucesso - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar base TEXTO FILA: {e}")
            return False
    
    def _transformar_dados_texto(self, df):
        """
        Aplica transformações específicas para dados TEXTO
        
        Args:
            df (pd.DataFrame): DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame transformado
        """
        try:
            # Transformações específicas para TEXTO
            
            # Converter datas
            date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar textos (remover quebras de linha, espaços extras)
            text_columns = [col for col in df.select_dtypes(include=['object']).columns]
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace('\n', ' ').str.replace('\r', ' ').str.strip()
                    # Remover espaços duplos
                    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            
            # Remover linhas duplicadas
            df = df.drop_duplicates()
            
            logger.info("Transformações aplicadas aos dados TEXTO")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados TEXTO: {e}")
            return df
    
    def _transformar_dados_texto_fila(self, df):
        """
        Aplica transformações específicas para dados TEXTO FILA
        """
        try:
            # Transformações específicas para TEXTO FILA
            
            # Converter datas
            date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar textos
            text_columns = [col for col in df.select_dtypes(include=['object']).columns]
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace('\n', ' ').str.replace('\r', ' ').str.strip()
                    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            
            df = df.drop_duplicates()
            
            logger.info("Transformações aplicadas aos dados TEXTO FILA")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados TEXTO FILA: {e}")
            return df

if __name__ == "__main__":
    # Teste da classe
    processador = ProcessadorTexto()
    
    # Testar conexão
    if processador.testar_conexao():
        print("Conexão teste bem-sucedida!")
        
        # Processar bases se arquivos existirem
        processador.processar_texto()
        processador.processar_texto_fila()
    else:
        print("Erro na conexão!")
