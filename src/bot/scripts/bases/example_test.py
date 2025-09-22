"""
Teste inicial para validar autenticação e funcionamento básico
"""
import pandas as pd
from google_sheets_base import GoogleSheetsBase
from config import Config
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestePlataforma:
    def __init__(self):
        self.projetos = ["boletim", "csat"]  # Lista de projetos para testar
        
    def testar_conexoes(self):
        """Testa conexão com todos os projetos configurados"""
        resultados = {}
        
        for projeto in self.projetos:
            try:
                logger.info(f"Testando projeto: {projeto}")
                sheets = GoogleSheetsBase(projeto)
                
                # Testar conexão listando abas
                abas = sheets.listar_abas()
                resultados[projeto] = {
                    "sucesso": True,
                    "abas": abas,
                    "total_abas": len(abas)
                }
                
                logger.info(f"✓ Projeto {projeto}: {len(abas)} abas encontradas")
                
            except Exception as e:
                resultados[projeto] = {
                    "sucesso": False,
                    "erro": str(e),
                    "abas": [],
                    "total_abas": 0
                }
                logger.error(f"✗ Projeto {projeto}: {e}")
        
        return resultados
    
    def testar_insercao_simples(self, projeto="boletim"):
        """
        Testa inserção de dados simples em uma aba
        """
        try:
            logger.info(f"Testando inserção de dados no projeto: {projeto}")
            
            # Conectar ao projeto
            sheets = GoogleSheetsBase(projeto)
            
            # Criar dados de teste
            dados_teste = pd.DataFrame({
                'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'Teste': ['Dados de teste automático'],
                'Status': ['Sucesso'],
                'Versao': ['1.0']
            })
            
            # Obter primeira aba disponível
            abas = sheets.listar_abas()
            if not abas:
                logger.error("Nenhuma aba encontrada para teste")
                return False
            
            aba_teste = abas[0]  # Usar primeira aba disponível
            
            logger.info(f"Inserindo dados de teste na aba: {aba_teste}")
            
            # Inserir dados de forma incremental
            sheets.inserir_dados_incremental(aba_teste, dados_teste, incluir_cabecalho=True)
            
            logger.info("✓ Inserção de teste realizada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro no teste de inserção: {e}")
            return False
    
    def testar_localizacao_linha_vazia(self, projeto="boletim"):
        """
        Testa a funcionalidade de encontrar linha vazia
        """
        try:
            logger.info(f"Testando localização de linha vazia no projeto: {projeto}")
            
            sheets = GoogleSheetsBase(projeto)
            abas = sheets.listar_abas()
            
            if not abas:
                logger.error("Nenhuma aba encontrada")
                return False
            
            resultados = {}
            for aba in abas[:3]:  # Testar apenas primeiras 3 abas
                try:
                    linha_vazia = sheets.encontrar_primeira_linha_vazia(aba)
                    resultados[aba] = linha_vazia
                    logger.info(f"Aba '{aba}': primeira linha vazia = {linha_vazia}")
                except Exception as e:
                    logger.error(f"Erro ao verificar aba '{aba}': {e}")
                    resultados[aba] = None
            
            return resultados
            
        except Exception as e:
            logger.error(f"✗ Erro no teste de linha vazia: {e}")
            return False
    
    def executar_todos_testes(self):
        """
        Executa todos os testes disponíveis
        """
        logger.info("=== INICIANDO TESTES DA PLATAFORMA ===")
        
        # 1. Teste de conexões
        logger.info("\n1. Testando conexões...")
        resultados_conexao = self.testar_conexoes()
        
        # 2. Teste de localização de linha vazia
        logger.info("\n2. Testando localização de linha vazia...")
        for projeto in self.projetos:
            if resultados_conexao[projeto]["sucesso"]:
                self.testar_localizacao_linha_vazia(projeto)
        
        # 3. Teste de inserção (apenas se conexões funcionaram)
        logger.info("\n3. Testando inserção de dados...")
        for projeto in self.projetos:
            if resultados_conexao[projeto]["sucesso"]:
                self.testar_insercao_simples(projeto)
                break  # Fazer teste em apenas um projeto
        
        # Resumo final
        logger.info("\n=== RESUMO DOS TESTES ===")
        for projeto, resultado in resultados_conexao.items():
            status = "✓" if resultado["sucesso"] else "✗"
            logger.info(f"{status} {projeto}: {resultado['total_abas']} abas")
            if not resultado["sucesso"]:
                logger.error(f"    Erro: {resultado['erro']}")

def main():
    # Verificar se arquivos de configuração existem
    logger.info("Verificando arquivos de configuração...")
    
    for projeto, config in Config.PLANILHAS_CONFIG.items():
        credencial_path = Config.get_credenciais_path(config["credenciais"])
        if credencial_path.exists():
            logger.info(f"✓ Credencial encontrada: {config['credenciais']}")
        else:
            logger.warning(f"✗ Credencial não encontrada: {credencial_path}")
    
    # Executar testes
    teste = TestePlataforma()
    teste.executar_todos_testes()

if __name__ == "__main__":
    main()
