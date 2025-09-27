"""
Processador para bases do Genesys
Handles: Gestão da entrega, Texto HC, Voz HC
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from core.google_sheets_base import GoogleSheetsBase

class ProcessadorGenesys(GoogleSheetsBase):
    """Processador especializado para arquivos do Genesys"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão do Genesys
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            # ID da planilha oficial do Genesys
            super().__init__(id_planilha="14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc")
        self.NOME_ABAS = {
            "gestao_entrega": "BASE GE COLABORADOR",
            "texto": "BASE TEXTO", 
            "voz": "BASE VOZ"
        }
        
        # Padrões de arquivos Genesys
        self.PADROES_ARQUIVOS = {
            "gestao_entrega": "Gestão da entrega N1 HC",
            "texto": "Texto HC", 
            "voz": "VOZ HC"  # Corrigido para VOZ HC
        }
    
    def processar_gestao_entrega(self, caminho_csv=None):
        """Processa base Gestão da Entrega"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['gestao_entrega']}.csv"
        
        return self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["gestao_entrega"]
        )
    
    def processar_texto_hc(self, caminho_csv=None):
        """Processa base Texto HC"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['texto']}.csv"
        
        return self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["texto"]
        )
    
    def processar_voz_hc(self, caminho_csv=None):
        """Processa base Voz HC"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['voz']}.csv"
        
        return self.enviar_csv_para_planilha(
            caminho_csv,
            self.NOME_ABAS["voz"]
        )
    
    def processar_todos(self):
        """Processa todos os arquivos Genesys disponíveis"""
        resultados = {}
        
        print("🔄 Processando bases Genesys...")
        
        processadores = {
            "Gestão da Entrega": self.processar_gestao_entrega,
            "Texto HC": self.processar_texto_hc,
            "Voz HC": self.processar_voz_hc
        }
        
        for nome, funcao in processadores.items():
            try:
                resultado = funcao()
                resultados[nome] = resultado
                if resultado:
                    print(f"✅ {nome} processado")
                else:
                    print(f"⚠️  {nome} não encontrado")
            except Exception as e:
                print(f"❌ Erro ao processar {nome}: {str(e)}")
                resultados[nome] = False
        
        return resultados