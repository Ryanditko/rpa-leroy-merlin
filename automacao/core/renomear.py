"""
Script para         self.downloads_dir = CONFIG.get_downloads_path()
        self.processed_dir = CONFIG.PROCESSED_DIR
        self.patterns = CONFIG.ARQUIVO_PATTERNS
        
        # Criar diretórios necessários
        CONFIG.criar_diretorios()ar arquivos baixados automaticamente
"""
import os
import glob
from pathlib import Path
import shutil
from datetime import datetime, timedelta
from config import CONFIG
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RenomeadorArquivos:
    def __init__(self):
        self.downloads_dir = Config.get_downloads_path()
        self.processed_dir = Config.PROCESSED_DIR
        self.patterns = Config.ARQUIVO_PATTERNS
        
        # Criar diretórios se necessário
        Config.criar_diretorios()
        
    def encontrar_arquivos_recentes(self, horas=24):
        """
        Encontra arquivos CSV baixados nas últimas X horas
        """
        arquivos_recentes = []
        limite_tempo = datetime.now() - timedelta(hours=horas)
        
        # Procurar por arquivos .csv na pasta Downloads
        csv_files = list(self.downloads_dir.glob("*.csv"))
        
        for arquivo in csv_files:
            # Verificar se foi modificado recentemente
            mod_time = datetime.fromtimestamp(arquivo.stat().st_mtime)
            if mod_time > limite_tempo:
                arquivos_recentes.append(arquivo)
                logger.info(f"Arquivo recente encontrado: {arquivo.name}")
        
        return arquivos_recentes
    
    def identificar_tipo_arquivo(self, nome_arquivo):
        """
        Identifica o tipo de base baseado no nome do arquivo
        """
        nome_lower = nome_arquivo.lower()
        
        for tipo, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.lower() in nome_lower:
                    return tipo
        
        # Verificação adicional para casos específicos
        if "voz" in nome_lower and "hc" in nome_lower:
            return "voz"
        if "texto" in nome_lower and ("hc" in nome_lower or "chat" in nome_lower):
            return "texto"
        
        return None
    
    def renomear_arquivo(self, arquivo_origem, novo_nome):
        """
        Renomeia e move arquivo para pasta processada
        """
        try:
            # Caminho de destino
            destino = self.processed_dir / f"{novo_nome}.csv"
            
            # Se já existe, adicionar timestamp
            if destino.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destino = self.processed_dir / f"{novo_nome}_{timestamp}.csv"
            
            # Copiar arquivo
            shutil.copy2(arquivo_origem, destino)
            logger.info(f"Arquivo renomeado: {arquivo_origem.name} -> {destino.name}")
            
            return destino
            
        except Exception as e:
            logger.error(f"Erro ao renomear arquivo {arquivo_origem}: {e}")
            return None
    
    def processar_todos_arquivos(self, mover_originais=False):
        """
        Processa todos os arquivos recentes na pasta Downloads
        """
        arquivos_processados = {}
        arquivos_recentes = self.encontrar_arquivos_recentes()
        
        if not arquivos_recentes:
            logger.info("Nenhum arquivo CSV recente encontrado na pasta Downloads")
            return arquivos_processados
        
        for arquivo in arquivos_recentes:
            tipo = self.identificar_tipo_arquivo(arquivo.name)
            
            if tipo:
                novo_arquivo = self.renomear_arquivo(arquivo, tipo)
                if novo_arquivo:
                    arquivos_processados[tipo] = novo_arquivo
                    
                    # Mover arquivo original se solicitado
                    if mover_originais:
                        try:
                            backup_dir = self.processed_dir / "originais"
                            backup_dir.mkdir(exist_ok=True)
                            shutil.move(str(arquivo), str(backup_dir / arquivo.name))
                            logger.info(f"Arquivo original movido para backup: {arquivo.name}")
                        except Exception as e:
                            logger.error(f"Erro ao mover arquivo original: {e}")
            else:
                logger.warning(f"Tipo não identificado para arquivo: {arquivo.name}")
        
        return arquivos_processados
    
    def listar_arquivos_processados(self):
        """
        Lista todos os arquivos na pasta processada
        """
        if not self.processed_dir.exists():
            return {}
        
        arquivos = {}
        for arquivo in self.processed_dir.glob("*.csv"):
            # Tentar identificar o tipo pelo nome
            nome_base = arquivo.stem.split('_')[0]  # Remove timestamp se houver
            if nome_base in self.patterns.keys():
                arquivos[nome_base] = arquivo
        
        return arquivos

if __name__ == "__main__":
    renomeador = RenomeadorArquivos()
    arquivos = renomeador.processar_todos_arquivos()
    
    print("Arquivos processados:")
    for tipo, caminho in arquivos.items():
        print(f"  {tipo}: {caminho}")