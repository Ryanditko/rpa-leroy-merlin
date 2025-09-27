#!/usr/bin/env python3
"""
🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN
Executa processamento completo das planilhas Genesys e Salesforce

Este script executa automaticamente:
1. Processamento de dados Genesys (VOZ, TEXTO, GESTÃO)
2. Processamento de dados Salesforce (CRIADO, RESOLVIDO, COMENTÁRIOS)
3. Relatório consolidado dos resultados

Uso:
    python main.py                # Executa tudo automaticamente
    python main.py --genesys      # Só Genesys
    python main.py --salesforce   # Só Salesforce
    python main.py --help         # Mostra ajuda
"""

import sys
import os
import argparse
from datetime import datetime

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase

# Configurações das planilhas
PLANILHAS_CONFIG = {
    "genesys": {
        "id": "14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc",  # Planilha oficial Genesys
        "nome": "📊 GENESYS",
        "deteccao": {
            # Função para detectar tipo do arquivo Genesys
            "voz_hc": ("BASE VOZ", "GENESYS VOZ HC"),
            "texto_hc": ("BASE TEXTO", "GENESYS TEXTO HC"), 
            "gestao_n1": ("BASE GE COLABORADOR", "GENESYS GESTÃO N1"),
            "gestao": ("BASE GE FILA", "GENESYS GESTÃO"),
            "fila": ("BASE VOZ FILA", "GENESYS FILA")
        }
    },
    "salesforce": {
        "id": "1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0",  # Planilha oficial Salesforce
        "nome": "💼 SALESFORCE", 
        "deteccao": {
            # Função para detectar tipo do arquivo Salesforce
            "criado": ("BASE ATUALIZADA CORRETA - CRIADO", "SALESFORCE CRIADO"),
            "resolvido": ("BASE ATUALIZADA CORRETA - RESOLVIDA", "SALESFORCE RESOLVIDO"),
            "comentario_bko": ("COMENTARIO BKO", "SALESFORCE COMENTÁRIOS"),
            "seller": ("DADOS SELLER", "SALESFORCE SELLER")
        }
    }
}

def detectar_tipo_arquivo(nome_arquivo, sistema):
    """Detecta o tipo do arquivo baseado no sistema (genesys ou salesforce)"""
    nome_lower = nome_arquivo.lower()
    
    if sistema == "genesys":
        if 'voz' in nome_lower and 'hc' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["voz_hc"]
        elif 'texto' in nome_lower and 'hc' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["texto_hc"]
        elif 'gestão' in nome_lower or 'gestao' in nome_lower:
            if 'n1' in nome_lower or 'entrega' in nome_lower:
                return PLANILHAS_CONFIG["genesys"]["deteccao"]["gestao_n1"]
            else:
                return PLANILHAS_CONFIG["genesys"]["deteccao"]["gestao"]
        elif 'fila' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["fila"]
    
    elif sistema == "salesforce":
        if 'criado' in nome_lower or 'created' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["criado"]
        elif 'resolvido' in nome_lower or 'resolved' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["resolvido"]
        elif 'comentario' in nome_lower or 'comment' in nome_lower or 'bko' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["comentario_bko"]
        elif 'seller' in nome_lower or 'vendedor' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["seller"]
    
    return None, None

def buscar_arquivos_csv():
    """Busca todos os arquivos CSV na pasta data"""
    data_dir = os.path.join(current_dir, 'data')
    arquivos_csv = []
    
    if os.path.exists(data_dir):
        for arquivo in os.listdir(data_dir):
            if arquivo.lower().endswith('.csv'):
                arquivos_csv.append(arquivo)
    
    return arquivos_csv, data_dir

def processar_sistema(sistema_nome, executar_sistema=True):
    """Processa um sistema específico (genesys ou salesforce)"""
    if not executar_sistema:
        return {"sucessos": 0, "falhas": 0, "processados": 0}
    
    print(f"\n{'='*70}")
    print(f"🎯 PROCESSANDO SISTEMA: {PLANILHAS_CONFIG[sistema_nome]['nome']}")
    print(f"{'='*70}")
    
    # Configurar para a planilha específica
    id_planilha = PLANILHAS_CONFIG[sistema_nome]["id"]
    sheets = GoogleSheetsBase(id_planilha=id_planilha)
    
    print(f"📊 ID da Planilha: {id_planilha}")
    print(f"🔗 Conectando...")
    
    try:
        client = sheets.client
        planilha = client.open_by_key(id_planilha)
        print(f"✅ Planilha: '{planilha.title}'")
        
        # Listar abas disponíveis
        abas_disponiveis = [aba.title for aba in planilha.worksheets()]
        print(f"📑 Abas disponíveis: {len(abas_disponiveis)} abas")
        
        # Buscar arquivos
        arquivos_csv, data_dir = buscar_arquivos_csv()
        
        # Filtrar arquivos para este sistema
        arquivos_sistema = []
        for arquivo in arquivos_csv:
            aba_destino, tipo_detectado = detectar_tipo_arquivo(arquivo, sistema_nome)
            if aba_destino and aba_destino in abas_disponiveis:
                arquivos_sistema.append((arquivo, aba_destino, tipo_detectado))
        
        print(f"📁 Arquivos {sistema_nome.upper()} encontrados: {len(arquivos_sistema)}")
        
        if not arquivos_sistema:
            print(f"⚠️  Nenhum arquivo {sistema_nome.upper()} encontrado")
            return {"sucessos": 0, "falhas": 0, "processados": 0}
        
        # Processar cada arquivo
        sucessos = 0
        falhas = 0
        
        for arquivo, aba_destino, tipo_detectado in arquivos_sistema:
            print(f"\n📤 Processando: {arquivo}")
            print(f"🎯 Tipo: {tipo_detectado}")
            print(f"📝 Destino: {aba_destino}")
            
            # Verificar dados existentes
            aba = planilha.worksheet(aba_destino)
            valores_existentes = aba.get_all_values()
            linhas_com_dados = sum(1 for linha in valores_existentes if any(cell.strip() for cell in linha))
            print(f"📊 Dados existentes: {linhas_com_dados:,} linhas")
            
            # Processar arquivo
            resultado = sheets.enviar_csv_para_planilha(arquivo, aba_destino)
            
            if resultado:
                print(f"✅ SUCESSO: {arquivo} → {aba_destino}")
                sucessos += 1
            else:
                print(f"❌ FALHA: {arquivo} → {aba_destino}")
                falhas += 1
            
            print("-" * 50)
        
        return {"sucessos": sucessos, "falhas": falhas, "processados": sucessos + falhas}
        
    except Exception as e:
        print(f"❌ ERRO no sistema {sistema_nome.upper()}: {e}")
        return {"sucessos": 0, "falhas": 1, "processados": 1}

def main():
    """Função principal"""
    
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description='🚀 Automação Principal Leroy Merlin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py                    # Executa Genesys + Salesforce
  python main.py --genesys          # Só Genesys
  python main.py --salesforce       # Só Salesforce
  python main.py --dados ./csvs     # Especifica pasta de dados
        """
    )
    
    parser.add_argument('--genesys', action='store_true', 
                       help='Processar apenas sistema Genesys')
    parser.add_argument('--salesforce', action='store_true',
                       help='Processar apenas sistema Salesforce')
    parser.add_argument('--dados', type=str, 
                       help='Pasta onde estão os arquivos CSV')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo detalhado')
    
    args = parser.parse_args()
    
    # Header principal
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN")
    print("=" * 80)
    print(f"⏰ Iniciado em: {timestamp}")
    print("🔧 Modo: COMPLEMENTAR (preserva dados existentes)")
    print("🎨 Primeira linha: VERDE LEROY MERLIN")
    print("📋 Cabeçalho: REMOVIDO automaticamente")
    
    # Determinar quais sistemas executar
    executar_genesys = True
    executar_salesforce = True
    
    if args.genesys and not args.salesforce:
        executar_salesforce = False
        print("🎯 Executando apenas: GENESYS")
    elif args.salesforce and not args.genesys:
        executar_genesys = False
        print("🎯 Executando apenas: SALESFORCE")
    else:
        print("🎯 Executando: GENESYS + SALESFORCE")
    
    # Verificar arquivos disponíveis
    arquivos_csv, data_dir = buscar_arquivos_csv()
    print(f"📁 Pasta de dados: {data_dir}")
    print(f"📄 Arquivos CSV encontrados: {len(arquivos_csv)}")
    
    if not arquivos_csv:
        print(f"❌ Nenhum arquivo CSV encontrado em: {data_dir}")
        print("💡 Adicione arquivos CSV na pasta data/ e execute novamente")
        return
    
    # Executar processamentos
    inicio_processamento = datetime.now()
    
    resultado_genesys = processar_sistema("genesys", executar_genesys)
    resultado_salesforce = processar_sistema("salesforce", executar_salesforce)
    
    fim_processamento = datetime.now()
    duracao = fim_processamento - inicio_processamento
    
    # Relatório final consolidado
    print(f"\n{'='*80}")
    print("🎉 RELATÓRIO FINAL CONSOLIDADO")
    print(f"{'='*80}")
    print(f"⏱️  Tempo total: {duracao}")
    print(f"📊 Processamento iniciado: {inicio_processamento.strftime('%H:%M:%S')}")
    print(f"🏁 Processamento concluído: {fim_processamento.strftime('%H:%M:%S')}")
    print()
    
    # Estatísticas por sistema
    total_sucessos = resultado_genesys["sucessos"] + resultado_salesforce["sucessos"]
    total_falhas = resultado_genesys["falhas"] + resultado_salesforce["falhas"]
    total_processados = resultado_genesys["processados"] + resultado_salesforce["processados"]
    
    if executar_genesys:
        print(f"📊 GENESYS:")
        print(f"   ✅ Sucessos: {resultado_genesys['sucessos']}")
        print(f"   ❌ Falhas: {resultado_genesys['falhas']}")
        print(f"   📊 Total: {resultado_genesys['processados']}")
    
    if executar_salesforce:
        print(f"💼 SALESFORCE:")
        print(f"   ✅ Sucessos: {resultado_salesforce['sucessos']}")
        print(f"   ❌ Falhas: {resultado_salesforce['falhas']}")
        print(f"   📊 Total: {resultado_salesforce['processados']}")
    
    print(f"\n🎯 TOTAIS GERAIS:")
    print(f"   ✅ Total de sucessos: {total_sucessos}")
    print(f"   ❌ Total de falhas: {total_falhas}")
    print(f"   📊 Total processado: {total_processados}")
    
    # Taxa de sucesso
    if total_processados > 0:
        taxa_sucesso = (total_sucessos / total_processados) * 100
        print(f"   📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
    
    # Links para as planilhas
    if total_sucessos > 0:
        print(f"\n🔗 ACESSE AS PLANILHAS ATUALIZADAS:")
        if executar_genesys and resultado_genesys["sucessos"] > 0:
            print(f"   📊 Genesys: https://docs.google.com/spreadsheets/d/{PLANILHAS_CONFIG['genesys']['id']}")
        if executar_salesforce and resultado_salesforce["sucessos"] > 0:
            print(f"   💼 Salesforce: https://docs.google.com/spreadsheets/d/{PLANILHAS_CONFIG['salesforce']['id']}")
    
    print(f"\n✨ Automação concluída! Primeira linha de cada inserção está pintada de VERDE LEROY MERLIN 🟢")
    print("=" * 80)

if __name__ == "__main__":
    main()