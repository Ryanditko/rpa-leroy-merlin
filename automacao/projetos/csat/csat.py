"""
Processamento das bases CSAT
"""
import pandas as pd
import sys
import os

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google_sheets_base import GoogleSheetsBase
from config import Config
import logging

logger = logging.getLogger(__name__)

class ProcessadorCSAT(GoogleSheetsBase):
    def __init__(self):
        super().__init__("csat")  # Usa configuração do projeto csat
        
        # Mapeamento de arquivos para métodos
        self.processadores = {
            "resolvida_por": self.processar_resolvida_por,
            "dados_seller": self.processar_dados_seller,
            "comentarios_bko": self.processar_comentarios_bko,
            "criado_por": self.processar_criado_por
        }
    
    def processar_todas_bases(self):
        """Processa todas as bases CSAT disponíveis"""
        resultados = {}
        
        for tipo, metodo in self.processadores.items():
            try:
                resultado = metodo()
                resultados[tipo] = resultado
            except Exception as e:
                logger.error(f"Erro ao processar {tipo}: {e}")
                resultados[tipo] = False
        
        return resultados
    
    def processar_resolvida_por(self, caminho_csv=None):
        """Processa base de dados resolvidos"""
        try:
            if not caminho_csv:
                caminho_csv = Config.PROCESSED_DIR / "resolvida_por.csv"
                if not caminho_csv.exists():
                    logger.error("Arquivo resolvida_por.csv não encontrado")
                    return False
            
            df = self.ler_csv_e_processar(caminho_csv)
            if df.empty:
                logger.warning("DataFrame vazio para resolvida_por")
                return False
            
            df = self._transformar_dados_resolvida_por(df)
            self.inserir_dados_incremental("BASE ATUALIZADA CORRETA - RESOLVIDA", df)
            
            logger.info(f"Base resolvida_por processada - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar resolvida_por: {e}")
            return False
    
    def processar_dados_seller(self, caminho_csv=None):
        """Processa base de dados seller"""
        try:
            if not caminho_csv:
                caminho_csv = Config.PROCESSED_DIR / "dados_seller.csv"
                if not caminho_csv.exists():
                    logger.error("Arquivo dados_seller.csv não encontrado")
                    return False
            
            df = self.ler_csv_e_processar(caminho_csv)
            if df.empty:
                logger.warning("DataFrame vazio para dados_seller")
                return False
            
            df = self._transformar_dados_seller(df)
            self.inserir_dados_incremental("DADOS SELLER", df)
            
            logger.info(f"Base dados_seller processada - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar dados_seller: {e}")
            return False
    
    def processar_comentarios_bko(self, caminho_csv=None):
        """Processa base de comentários BKO"""
        try:
            if not caminho_csv:
                caminho_csv = Config.PROCESSED_DIR / "comentarios_bko.csv"
                if not caminho_csv.exists():
                    logger.error("Arquivo comentarios_bko.csv não encontrado")
                    return False
            
            df = self.ler_csv_e_processar(caminho_csv)
            if df.empty:
                logger.warning("DataFrame vazio para comentarios_bko")
                return False
            
            df = self._transformar_dados_comentarios_bko(df)
            self.inserir_dados_incremental("COMENTARIO BKO", df)
            
            logger.info(f"Base comentarios_bko processada - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar comentarios_bko: {e}")
            return False
    
    def processar_criado_por(self, caminho_csv=None):
        """Processa base de dados criados"""
        try:
            if not caminho_csv:
                caminho_csv = Config.PROCESSED_DIR / "criado_por.csv"
                if not caminho_csv.exists():
                    logger.error("Arquivo criado_por.csv não encontrado")
                    return False
            
            df = self.ler_csv_e_processar(caminho_csv)
            if df.empty:
                logger.warning("DataFrame vazio para criado_por")
                return False
            
            df = self._transformar_dados_criado_por(df)
            self.inserir_dados_incremental("BASE ATUALIZADA CORRETA - CRIADO", df)
            
            logger.info(f"Base criado_por processada - {len(df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar criado_por: {e}")
            return False
    
    def _transformar_dados_resolvida_por(self, df):
        """Transformações específicas para dados resolvidos"""
        try:
            # Converter datas
            date_columns = [col for col in df.columns if 'data' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar dados
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            df = df.drop_duplicates()
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados resolvida_por: {e}")
            return df
    
    def _transformar_dados_seller(self, df):
        """Transformações específicas para dados seller"""
        try:
            # Limpeza específica para dados de seller
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            df = df.drop_duplicates()
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados seller: {e}")
            return df
    
    def _transformar_dados_comentarios_bko(self, df):
        """Transformações específicas para comentários BKO"""
        try:
            # Limpar textos de comentários
            text_columns = [col for col in df.columns if 'comentario' in col.lower() or 'texto' in col.lower()]
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace('\n', ' ').str.strip()
            
            df = df.drop_duplicates()
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar comentários BKO: {e}")
            return df
    
    def _transformar_dados_criado_por(self, df):
        """Transformações específicas para dados criados"""
        try:
            # Converter datas
            date_columns = [col for col in df.columns if 'data' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpar dados
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            df = df.drop_duplicates()
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados criado_por: {e}")
            return df

if __name__ == "__main__":
    # Teste da classe
    processador = ProcessadorCSAT()
    
    # Testar conexão
    if processador.testar_conexao():
        print("Conexão teste bem-sucedida!")
        
        # Processar todas as bases
        resultados = processador.processar_todas_bases()
        print("Resultados do processamento:")
        for base, sucesso in resultados.items():
            status = "✓" if sucesso else "✗"
            print(f"  {status} {base}")
    else:
        print("Erro na conexão!")