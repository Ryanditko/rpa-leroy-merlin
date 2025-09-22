"""
Teste da automação completa em modo simulação
"""
import sys
import os
from pathlib import Path
import pandas as pd
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TesteModoSimulacao:
    def __init__(self):
        self.processed_dir = Path("processed")
        
    def simular_processamento_voz(self):
        """Simula o processamento da base VOZ"""
        try:
            caminho_csv = self.processed_dir / "voz.csv"
            
            if not caminho_csv.exists():
                logger.error(f"Arquivo não encontrado: {caminho_csv}")
                return False
                
            logger.info("=== SIMULANDO PROCESSAMENTO VOZ ===")
            
            # Ler CSV
            df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')
            logger.info(f"✓ Arquivo carregado: {len(df)} registros")
            
            # Aplicar transformações
            df_original_size = len(df)
            
            # Limpar dados
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            # Remover duplicatas
            df = df.drop_duplicates()
            df = df.dropna(how='all')
            
            logger.info(f"✓ Transformações aplicadas: {len(df)} registros após limpeza")
            
            # Simular inserção no Google Sheets
            logger.info("✓ SIMULAÇÃO: Conectando ao Google Sheets...")
            logger.info("✓ SIMULAÇÃO: Abrindo planilha do projeto Boletim...")
            logger.info("✓ SIMULAÇÃO: Acessando aba 'BASE VOZ'...")
            logger.info("✓ SIMULAÇÃO: Localizando primeira linha vazia...")
            
            # Simular linha vazia (exemplo: linha 2958 se já houver dados)
            linha_vazia_simulada = 2958
            logger.info(f"✓ SIMULAÇÃO: Primeira linha vazia encontrada: {linha_vazia_simulada}")
            
            # Simular range de inserção
            inicio_col = "A"
            fim_col = chr(ord('A') + len(df.columns) - 1)  # Calcular última coluna
            fim_linha = linha_vazia_simulada + len(df) - 1
            range_insercao = f"{inicio_col}{linha_vazia_simulada}:{fim_col}{fim_linha}"
            
            logger.info(f"✓ SIMULAÇÃO: Inserindo {len(df)} registros no range {range_insercao}")
            logger.info("✓ SIMULAÇÃO: Dados inseridos com sucesso!")
            
            # Mostrar resumo
            print(f"\n=== RESUMO DA OPERAÇÃO ===")
            print(f"Arquivo origem: {caminho_csv.name}")
            print(f"Registros processados: {len(df)}")
            print(f"Planilha destino: Google Sheets - Projeto Boletim")
            print(f"Aba destino: BASE VOZ")
            print(f"Range de inserção: {range_insercao}")
            print(f"Modo: Inserção incremental (sem apagar dados existentes)")
            
            # Mostrar exemplos de dados que seriam inseridos
            print(f"\n=== EXEMPLOS DE DADOS INSERIDOS ===")
            registros_com_metricas = df[df['Atendidas'].notna() & (df['Atendidas'] != '')]
            
            if not registros_com_metricas.empty:
                print(f"Agentes com métricas de atendimento:")
                for idx, row in registros_com_metricas.head(5).iterrows():
                    nome = str(row['Nome do agente'])[:50]
                    print(f"  • {nome}: {row['Atendidas']} atendidas")
            
            registros_sem_metricas = df[df['Atendidas'].isna() | (df['Atendidas'] == '')]
            print(f"\nAgentes cadastrados sem métricas: {len(registros_sem_metricas)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na simulação: {e}")
            return False
    
    def executar_fluxo_completo_simulado(self):
        """Executa simulação do fluxo completo"""
        logger.info("=== INICIANDO SIMULAÇÃO DA AUTOMAÇÃO COMPLETA ===")
        
        # 1. Verificar arquivos processados
        logger.info("\n1. Verificando arquivos processados...")
        voz_existe = (self.processed_dir / "voz.csv").exists()
        
        if voz_existe:
            logger.info("✓ Arquivo voz.csv encontrado")
        else:
            logger.error("✗ Arquivo voz.csv não encontrado")
            return False
        
        # 2. Simular processamento
        logger.info("\n2. Processando base VOZ...")
        sucesso_voz = self.simular_processamento_voz()
        
        # 3. Relatório final
        logger.info("\n=== RELATÓRIO FINAL ===")
        if sucesso_voz:
            logger.info("✓ Automação executada com sucesso!")
            print("\nEm produção, este processo:")
            print("1. Conectaria ao Google Sheets usando as credenciais")
            print("2. Localizaria a primeira linha vazia na aba 'BASE VOZ'")
            print("3. Inseriria os dados sem apagar conteúdo existente")
            print("4. Registraria a operação em logs")
            
            print(f"\nPara ativar em produção:")
            print("1. Configure as credenciais do Google Cloud")
            print("2. Habilite a API do Google Sheets")
            print("3. Adicione a conta de serviço como editor na planilha")
            print("4. Execute: python main.py")
            
        else:
            logger.error("✗ Erro na automação!")
        
        return sucesso_voz

if __name__ == "__main__":
    teste = TesteModoSimulacao()
    teste.executar_fluxo_completo_simulado()
