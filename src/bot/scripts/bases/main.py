"""
Arquivo principal para orquestração da automação de bases CSV para Google Sheets

Este script:
1. Renomeia arquivos baixados automaticamente
2. Processa cada base de dados através dos módulos específicos
3. Envia dados para Google Sheets de forma incremental
4. Gera relatório de execução

Uso:
    python main.py                    # Executa fluxo completo
    python main.py --teste            # Executa apenas testes
    python main.py --renomear         # Executa apenas renomeação
    python main.py --projeto boletim  # Executa apenas projeto específico
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Importar módulos da automação
from renomear import RenomeadorArquivos
from config import Config
from example_test import TestePlataforma

# Importar processadores específicos
from voz import ProcessadorVoz
from texto import ProcessadorTexto

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automacao.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OrquestradorPrincipal:
    def __init__(self):
        self.renomeador = RenomeadorArquivos()
        self.teste_plataforma = TestePlataforma()
        
        # Mapeamento de processadores por projeto
        self.processadores = {
            "boletim": {
                "voz": ProcessadorVoz(),
                "texto": ProcessadorTexto()
            }
        }
        
        # Tentar importar processador CSAT dinamicamente
        try:
            sys.path.append(str(Path(__file__).parent / "csat"))
            from csat import ProcessadorCSAT
            self.processadores["csat"] = {
                "csat": ProcessadorCSAT()
            }
            logger.info("Processador CSAT carregado com sucesso")
        except (ImportError, FileNotFoundError) as e:
            logger.warning(f"Processador CSAT não disponível: {e}")
            # Continua sem o processador CSAT
    
    def executar_testes(self):
        """Executa bateria completa de testes"""
        logger.info("=== EXECUTANDO TESTES DA PLATAFORMA ===")
        self.teste_plataforma.executar_todos_testes()
        return True
    
    def executar_renomeacao(self, mover_originais=False):
        """
        Executa renomeação de arquivos
        
        Args:
            mover_originais (bool): Se deve mover arquivos originais para backup
        """
        logger.info("=== INICIANDO RENOMEAÇÃO DE ARQUIVOS ===")
        
        arquivos_processados = self.renomeador.processar_todos_arquivos(mover_originais)
        
        if not arquivos_processados:
            logger.warning("Nenhum arquivo encontrado para renomear")
            return False
        
        logger.info("Arquivos renomeados:")
        for tipo, caminho in arquivos_processados.items():
            logger.info(f"  ✓ {tipo}: {caminho.name}")
        
        return arquivos_processados
    
    def executar_projeto_boletim(self):
        """Executa processamento do projeto boletim"""
        logger.info("=== PROCESSANDO PROJETO BOLETIM ===")
        
        resultados = {}
        
        # Processar VOZ
        try:
            processador_voz = self.processadores["boletim"]["voz"]
            resultados["voz"] = processador_voz.processar_voz()
            resultados["voz_fila"] = processador_voz.processar_voz_fila()
        except Exception as e:
            logger.error(f"Erro ao processar VOZ: {e}")
            resultados["voz"] = False
            resultados["voz_fila"] = False
        
        # Processar TEXTO
        try:
            processador_texto = self.processadores["boletim"]["texto"]
            resultados["texto"] = processador_texto.processar_texto()
            resultados["texto_fila"] = processador_texto.processar_texto_fila()
        except Exception as e:
            logger.error(f"Erro ao processar TEXTO: {e}")
            resultados["texto"] = False
            resultados["texto_fila"] = False
        
        return resultados
    
    def executar_projeto_csat(self):
        """Executa processamento do projeto CSAT"""
        logger.info("=== PROCESSANDO PROJETO CSAT ===")
        
        if "csat" not in self.processadores:
            logger.error("Processador CSAT não disponível")
            return {}
        
        try:
            processador_csat = self.processadores["csat"]["csat"]
            resultados = processador_csat.processar_todas_bases()
            return resultados
        except Exception as e:
            logger.error(f"Erro ao processar CSAT: {e}")
            return {}
    
    def executar_projeto_especifico(self, projeto):
        """
        Executa processamento de projeto específico
        
        Args:
            projeto (str): Nome do projeto (boletim, csat)
        """
        if projeto == "boletim":
            return self.executar_projeto_boletim()
        elif projeto == "csat":
            return self.executar_projeto_csat()
        else:
            logger.error(f"Projeto desconhecido: {projeto}")
            return {}
    
    def executar_fluxo_completo(self, mover_originais=False):
        """
        Executa fluxo completo da automação
        
        Args:
            mover_originais (bool): Se deve mover arquivos originais para backup
        """
        logger.info("=== INICIANDO FLUXO COMPLETO DE AUTOMAÇÃO ===")
        
        relatorio = {
            "inicio": datetime.now(),
            "arquivos_renomeados": {},
            "resultados_processamento": {},
            "erros": []
        }
        
        try:
            # 1. Renomear arquivos
            logger.info("\n1. Renomeando arquivos...")
            arquivos_renomeados = self.executar_renomeacao(mover_originais)
            relatorio["arquivos_renomeados"] = arquivos_renomeados
            
            if not arquivos_renomeados:
                logger.warning("Sem arquivos para processar. Verificando arquivos já processados...")
                arquivos_renomeados = self.renomeador.listar_arquivos_processados()
            
            # 2. Determinar quais projetos processar baseado nos arquivos disponíveis
            projetos_para_processar = set()
            
            for tipo_arquivo in arquivos_renomeados.keys():
                if tipo_arquivo in ["voz", "texto", "voz_fila", "texto_fila", "ge_fila", "ge_colab"]:
                    projetos_para_processar.add("boletim")
                elif tipo_arquivo in ["resolvida_por", "dados_seller", "comentarios_bko", "criado_por"]:
                    projetos_para_processar.add("csat")
            
            # 3. Processar cada projeto
            for projeto in projetos_para_processar:
                logger.info(f"\n2. Processando projeto: {projeto}")
                resultados = self.executar_projeto_especifico(projeto)
                relatorio["resultados_processamento"][projeto] = resultados
            
            if not projetos_para_processar:
                logger.warning("Nenhum projeto identificado para processamento")
            
        except Exception as e:
            logger.error(f"Erro no fluxo completo: {e}")
            relatorio["erros"].append(str(e))
        
        # 4. Gerar relatório final
        relatorio["fim"] = datetime.now()
        relatorio["duracao"] = relatorio["fim"] - relatorio["inicio"]
        
        self._gerar_relatorio_final(relatorio)
        
        return relatorio
    
    def _gerar_relatorio_final(self, relatorio):
        """Gera relatório final da execução"""
        logger.info("\n=== RELATÓRIO FINAL ===")
        logger.info(f"Duração total: {relatorio['duracao']}")
        
        # Relatório de arquivos
        if relatorio["arquivos_renomeados"]:
            logger.info("\nArquivos processados:")
            for tipo, caminho in relatorio["arquivos_renomeados"].items():
                if isinstance(caminho, Path):
                    logger.info(f"  ✓ {tipo}: {caminho.name}")
                else:
                    logger.info(f"  ✓ {tipo}: {caminho}")
        else:
            logger.info("\nNenhum arquivo novo processado")
        
        # Relatório de processamento
        if relatorio["resultados_processamento"]:
            logger.info("\nResultados do processamento:")
            for projeto, resultados in relatorio["resultados_processamento"].items():
                logger.info(f"\n  Projeto {projeto}:")
                for base, sucesso in resultados.items():
                    status = "✓" if sucesso else "✗"
                    logger.info(f"    {status} {base}")
        
        # Relatório de erros
        if relatorio["erros"]:
            logger.error("\nErros encontrados:")
            for erro in relatorio["erros"]:
                logger.error(f"  • {erro}")

def main():
    """Função principal com argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description="Automação de bases CSV para Google Sheets")
    
    parser.add_argument("--teste", action="store_true", 
                       help="Executa apenas testes de conexão")
    parser.add_argument("--renomear", action="store_true",
                       help="Executa apenas renomeação de arquivos")
    parser.add_argument("--projeto", choices=["boletim", "csat"],
                       help="Executa apenas projeto específico")
    parser.add_argument("--mover-originais", action="store_true",
                       help="Move arquivos originais para backup após renomear")
    
    args = parser.parse_args()
    
    # Criar diretórios necessários
    Config.criar_diretorios()
    
    # Inicializar orquestrador
    orquestrador = OrquestradorPrincipal()
    
    # Executar ação solicitada
    if args.teste:
        orquestrador.executar_testes()
    elif args.renomear:
        orquestrador.executar_renomeacao(args.mover_originais)
    elif args.projeto:
        # Primeiro renomear, depois processar projeto específico
        arquivos = orquestrador.executar_renomeacao(args.mover_originais)
        resultados = orquestrador.executar_projeto_especifico(args.projeto)
        
        logger.info(f"\nResultados do projeto {args.projeto}:")
        for base, sucesso in resultados.items():
            status = "✓" if sucesso else "✗"
            logger.info(f"  {status} {base}")
    else:
        # Fluxo completo
        orquestrador.executar_fluxo_completo(args.mover_originais)

if __name__ == "__main__":
    main()