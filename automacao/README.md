# Automação de Bases CSV para Google Sheets

Este projeto automatiza o processo de carga de bases CSV para o Google Sheets, com renomeação automática de arquivos, processamento modular e inserção incremental de dados.

## Características

- ✅ **Caminho dinâmico da pasta Downloads** - Funciona em Windows, Mac e Linux
- ✅ **Renomeação automática** - Identifica e renomeia arquivos baixados automaticamente
- ✅ **Modular** - Classes separadas para cada base de dados
- ✅ **Inserção incremental** - Adiciona dados sem apagar conteúdo existente
- ✅ **Multi-projeto** - Suporte a múltiplas planilhas (boletim, csat, pulso)
- ✅ **Logging completo** - Rastreamento detalhado de todas as operações

## Estrutura do Projeto

```
bases/
├── main.py              # Orquestrador principal
├── config.py            # Configurações globais
├── renomear.py          # Renomeação automática de arquivos
├── google_sheets_base.py # Classe base para Google Sheets
├── voz.py               # Processador da base VOZ
├── texto.py             # Processador da base TEXTO
├── example_test.py      # Testes de conexão e validação
├── requirements.txt     # Dependências Python
├── processed/           # Pasta para arquivos processados
├── boletim.json        # Credenciais Google Cloud - Boletim
├── csat/
│   ├── csat.py         # Processador das bases CSAT
│   └── csat.json       # Credenciais Google Cloud - CSAT
└── pulso/
    ├── pulso.py        # Processador da base PULSO
    └── pulso.json      # Credenciais Google Cloud - Pulso
```

## Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar credenciais do Google Cloud:**
   - Coloque os arquivos JSON de credenciais nas pastas corretas:
     - `boletim.json` na pasta principal
     - `csat.json` na pasta `csat/`
     - `pulso.json` na pasta `pulso/`

## Uso

### Fluxo Completo (Recomendado)
```bash
python main.py
```
Executa todo o fluxo: renomeia arquivos → processa bases → envia para Google Sheets

### Testes Iniciais
```bash
python main.py --teste
```
Valida conexões com Google Sheets e testa funcionalidades básicas

### Apenas Renomeação
```bash
python main.py --renomear
```
Renomeia arquivos da pasta Downloads sem processar

### Projeto Específico
```bash
python main.py --projeto boletim
python main.py --projeto csat
```
Processa apenas um projeto específico

### Mover Arquivos Originais
```bash
python main.py --mover-originais
```
Move arquivos originais para backup após renomear

## Configuração

### Mapeamento de Arquivos (config.py)

O sistema identifica automaticamente os tipos de arquivo baseado nos nomes:

```python
ARQUIVO_PATTERNS = {
    "voz": ["export_", "voice_", "voz_"],
    "texto": ["text_", "texto_", "chat_"],
    "ge_fila": ["ge_fila", "gestao_fila"],
    "ge_colab": ["ge_colab", "gestao_colaborador"],
    "csat": ["csat", "satisfacao"],
    "pulso": ["pulso", "pulse"]
}
```

### Configuração de Planilhas

Cada projeto tem sua configuração no arquivo `config.py`:

```python
PLANILHAS_CONFIG = {
    "boletim": {
        "credenciais": "boletim.json",
        "id_planilha": "SEU_ID_PLANILHA",
        "abas": {
            "voz": "BASE VOZ",
            "texto": "BASE TEXTO",
            # ...
        }
    }
}
```

## Como Funciona

### 1. Renomeação Automática
- Busca arquivos CSV na pasta Downloads (últimas 24 horas)
- Identifica o tipo baseado no nome do arquivo
- Renomeia para padrão consistente (ex: `voz.csv`, `texto.csv`)
- Move para pasta `processed/`

### 2. Processamento Modular
- Cada base tem sua própria classe processadora
- Aplicação de transformações específicas (limpeza, formatação)
- Validação de dados antes do envio

### 3. Inserção Incremental
- Localiza primeira linha vazia na planilha Google Sheets
- Insere apenas novos dados, sem apagar existentes
- Ignora cabeçalhos em inserções subsequentes

## Estrutura de Classes

### GoogleSheetsBase
Classe base com funcionalidades comuns:
- Autenticação Google Sheets API
- Inserção incremental de dados
- Localização de linhas vazias
- Leitura e processamento de CSV

### Processadores Específicos
- **ProcessadorVoz**: VOZ e VOZ FILA
- **ProcessadorTexto**: TEXTO e TEXTO FILA  
- **ProcessadorCSAT**: Todas as bases CSAT

## Logs

O sistema gera logs detalhados em:
- Console (tempo real)
- Arquivo `automacao.log`

Exemplo de log:
```
2025-01-20 10:30:15 - INFO - Arquivo renomeado: export_voice_data.csv -> voz.csv
2025-01-20 10:30:16 - INFO - Dados inseridos na aba 'BASE VOZ' - Range: A15:F25 - 10 linhas
```

## Resolução de Problemas

### Erro de Autenticação
- Verificar se arquivos JSON de credenciais estão corretos
- Confirmar permissões das contas de serviço no Google Cloud
- Validar IDs das planilhas em `config.py`

### Arquivos Não Encontrados
- Verificar se arquivos estão na pasta Downloads
- Confirmar se nomes dos arquivos contêm os padrões esperados
- Executar `--renomear` primeiro se necessário

### Erro de Planilha
- Verificar se planilha existe e está acessível
- Confirmar nomes das abas na configuração
- Testar com `--teste` primeiro

## Customização

### Adicionar Nova Base
1. Criar classe processadora herdando de `GoogleSheetsBase`
2. Implementar método de processamento específico
3. Adicionar ao mapeamento em `main.py`
4. Configurar padrões de arquivo em `config.py`

### Modificar Transformações
Editar métodos `_transformar_dados_*` nas classes processadoras para aplicar regras específicas de limpeza e formatação.

## Suporte

Para dúvidas ou problemas:
1. Verificar logs em `automacao.log`
2. Executar `python main.py --teste` para validar configuração
3. Conferir arquivos de credenciais e configurações
