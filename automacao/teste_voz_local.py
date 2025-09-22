"""
Teste simulado da automação VOZ sem conexão com Google Sheets
Mostra como os dados seriam processados e inseridos
"""
import pandas as pd
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_processamento_voz_local():
    """
    Testa o processamento do arquivo VOZ localmente
    """
    try:
        # Caminho do arquivo processado
        caminho_csv = Path("processed/voz.csv")
        
        if not caminho_csv.exists():
            logger.error(f"Arquivo não encontrado: {caminho_csv}")
            return False
        
        logger.info(f"Lendo arquivo: {caminho_csv}")
        
        # Ler CSV com separador ponto e vírgula
        df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')
        
        logger.info(f"Arquivo carregado com sucesso!")
        logger.info(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Mostrar informações do DataFrame
        print("\n=== INFORMAÇÕES DO ARQUIVO ===")
        print(f"Total de registros: {len(df)}")
        print(f"Colunas: {list(df.columns)}")
        
        # Mostrar primeiras 5 linhas
        print("\n=== PRIMEIRAS 5 LINHAS ===")
        print(df.head())
        
        # Aplicar transformações básicas
        logger.info("Aplicando transformações...")
        
        # Remover linhas completamente vazias
        df_limpo = df.dropna(how='all')
        
        # Converter colunas de texto para string e limpar espaços
        for col in df_limpo.select_dtypes(include=['object']).columns:
            df_limpo[col] = df_limpo[col].astype(str).str.strip()
        
        # Substituir 'nan' strings por string vazia
        df_limpo = df_limpo.replace('nan', '')
        
        # Remover duplicatas
        df_limpo = df_limpo.drop_duplicates()
        
        print(f"\n=== APÓS LIMPEZA ===")
        print(f"Registros após limpeza: {len(df_limpo)}")
        print(f"Registros removidos: {len(df) - len(df_limpo)}")
        
        # Simular inserção no Google Sheets
        print(f"\n=== SIMULAÇÃO DE INSERÇÃO ===")
        print(f"Planilha: Google Sheets - Projeto Boletim")
        print(f"Aba de destino: BASE VOZ")
        print(f"Modo: Inserção incremental (primeira linha vazia)")
        print(f"Dados a inserir: {len(df_limpo)} registros")
        print(f"Incluir cabeçalho: Não (apenas dados)")
        
        # Mostrar estrutura dos dados que seriam enviados
        print(f"\n=== ESTRUTURA DOS DADOS ===")
        for i, col in enumerate(df_limpo.columns, 1):
            valores_nao_vazios = df_limpo[col].replace('', pd.NA).notna().sum()
            print(f"Coluna {i:2d}: {col:30s} - {valores_nao_vazios:3d} valores preenchidos")
        
        # Mostrar alguns registros com dados preenchidos
        print(f"\n=== EXEMPLOS DE REGISTROS COM DADOS ===")
        # Filtrar registros que têm dados além das primeiras colunas básicas
        registros_com_dados = df_limpo[df_limpo['Atendidas'].notna() & (df_limpo['Atendidas'] != '')]
        
        if not registros_com_dados.empty:
            print(f"Encontrados {len(registros_com_dados)} registros com dados de atendimento:")
            for idx, row in registros_com_dados.head(3).iterrows():
                nome = row['Nome do agente'][:40] + "..." if len(str(row['Nome do agente'])) > 40 else row['Nome do agente']
                print(f"  - {nome}: {row['Atendidas']} atendidas, TM: {row['Tratamento médio']}")
        else:
            print("Todos os registros parecem estar com campos de métricas vazios.")
        
        print(f"\n=== RESUMO ===")
        print("✓ Arquivo CSV carregado com sucesso")
        print("✓ Dados processados e limpos")
        print("✓ Pronto para inserção no Google Sheets")
        print("\nPara funcionar completamente, é necessário:")
        print("1. Habilitar Google Sheets API no Google Cloud Console")
        print("2. Configurar permissões da conta de serviço na planilha")
        print("3. Verificar ID da planilha na configuração")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro no teste: {e}")
        return False

if __name__ == "__main__":
    testar_processamento_voz_local()
