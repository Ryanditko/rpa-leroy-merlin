"""
Configuraçõ    # Mapeamento de arquivos para renomeação
    ARQUIVO_PATTERNS = {
        "voz": ["export_", "voice_", "voz_", "voz ", "voz hc", "base voz"],
        "texto": ["text_", "texto_", "chat_", "base texto"],
        "ge_fila": ["ge_fila", "gestao_fila", "base ge fila"],
        "ge_colab": ["ge_colab", "gestao_colaborador", "base ge colaborador"],
        "csat": ["csat", "satisfacao"],
        "pulso": ["pulso", "pulse"]
    },s para automação de bases CSV para Google Sheets
"""
import os
from pathlib import Path

class Config:
    # Configurações de arquivos
    CREDENCIAIS_DIR = Path(__file__).parent
    
    # Pasta Downloads dinâmica (funciona em Windows, Mac e Linux)
    DOWNLOADS_DIR = Path.home() / "Downloads"
    
    # Pasta de destino para arquivos processados
    PROCESSED_DIR = Path(__file__).parent / "processed"
    
    # Mapeamento de arquivos para renomeação
    ARQUIVO_PATTERNS = {
        "voz": ["export_", "voice_", "voz_"],
        "texto": ["text_", "texto_", "chat_"],
        "ge_fila": ["ge_fila", "gestao_fila"],
        "ge_colab": ["ge_colab", "gestao_colaborador"],
        "csat": ["csat", "satisfacao"],
        "pulso": ["pulso", "pulse"]
    }
    
    # Configurações do Google Sheets por projeto
    PLANILHAS_CONFIG = {
        "boletim": {
            "credenciais": "boletim.json",
            "id_planilha": "1cHbKXMjJgnR_M3X2uGtDT3kPHTrlBd_g4kqxhrr6MOY",
            "abas": {
                "voz": "BASE VOZ",
                "voz_fila": "BASE VOZ FILA", 
                "texto": "BASE TEXTO",
                "texto_fila": "BASE TEXTO FILA",
                "ge_fila": "BASE GE FILA",
                "ge_colab": "BASE GE COLABORADOR"
            }
        },
        "csat": {
            "credenciais": "csat/csat.json",
            "id_planilha": "1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0",
            "abas": {
                "resolvida_por": "BASE ATUALIZADA CORRETA - RESOLVIDA",
                "dados_seller": "DADOS SELLER",
                "comentarios_bko": "COMENTARIO BKO", 
                "criado_por": "BASE ATUALIZADA CORRETA - CRIADO"
            }
        },
        "pulso": {
            "credenciais": "pulso.json",
            "id_planilha": "SEU_ID_PLANILHA_PULSO",
            "abas": {
                "pulso": "BASE PULSO"
            }
        }
    }
    
    @classmethod
    def criar_diretorios(cls):
        """Cria diretórios necessários se não existirem"""
        cls.PROCESSED_DIR.mkdir(exist_ok=True)
        
    @classmethod
    def get_downloads_path(cls):
        """Retorna o caminho da pasta Downloads"""
        return cls.DOWNLOADS_DIR
        
    @classmethod
    def get_credenciais_path(cls, arquivo_credencial):
        """Retorna caminho completo para arquivo de credenciais"""
        return cls.CREDENCIAIS_DIR / arquivo_credencial
