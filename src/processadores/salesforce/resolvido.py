"""
Processador para base RESOLVIDO do Salesforce
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from google_sheets_base import GoogleSheetsBase

class ProcessadorResolvido(GoogleSheetsBase):
    """Processador para base RESOLVIDO"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            super().__init__(id_planilha="1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0")
        self.NOME_ABA = "BASE ATUALIZADA CORRETA - RESOLVIDA"
        self.PADRAO_ARQUIVO = "BASE-BOLETIM-RESOLVIDO"
    
    def processar(self, caminho_csv=None):
        """Processa base RESOLVIDO"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADRAO_ARQUIVO}.csv"
        
        return self.enviar_csv_para_planilha(caminho_csv, self.NOME_ABA)