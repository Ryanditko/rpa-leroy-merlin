# RPA Leroy Merlin - Automação CSV para Google Sheets

> **Automação completa para processar arquivos CSV baixados e enviar para planilhas Google Sheets de forma incremental**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Produção-green.svg)
![Plataforma](https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

---

## 📋 **Funcionalidades**

- ✅ **Detecção automática** da pasta Downloads em qualquer sistema
- ✅ **Renomeação inteligente** de arquivos com padrões customizáveis
- ✅ **Processamento incremental** - nunca sobrescreve dados existentes
- ✅ **Múltiplos projetos** - suporte para diferentes planilhas
- ✅ **Logs detalhados** para auditoria e debugging
- ✅ **Interface simples** via linha de comando

---

## 📁 **Estrutura do Projeto**

```
rpa-leroy-merlin/
├── 📂 automacao/           # Código principal da automação
│   ├── 📂 core/           # Módulos principais
│   │   ├── config.py      # Configurações centralizadas
│   │   ├── renomear.py    # Renomeação de arquivos
│   │   └── google_sheets_base.py  # Base Google Sheets API
│   ├── 📂 processadores/  # Processadores específicos
│   │   ├── voz.py         # Processador dados VOZ
│   │   └── texto.py       # Processador dados TEXTO
│   ├── 📂 projetos/       # Credenciais por projeto
│   │   ├── boletim/       # Projeto boletim
│   │   └── csat/          # Projeto CSAT
│   ├── 📂 tests/          # Testes automatizados
│   ├── 📂 logs/           # Logs de execução
│   ├── 📂 processed/      # Arquivos processados
│   ├── main.py            # 🚀 ARQUIVO PRINCIPAL
│   └── requirements.txt   # Dependências Python
├── 📂 scripts/            # Scripts de instalação/execução
│   ├── instalar.bat       # Instalador Windows
│   └── executar.bat       # Executor Windows
├── 📂 docs/              # Documentação
└── README.md             # Este arquivo
```

---

## 🚀 **Instalação Rápida**

### **Windows** 
```batch
# 1. Clone ou baixe o projeto
# 2. Execute o instalador
scripts\instalar.bat
```

### **Linux/macOS**
```bash
# 1. Clone o repositório
cd automacao

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute teste
python main.py --teste
```

---

## ⚙️ **Configuração**

### **1. Ativar APIs do Google Cloud**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Ative as APIs:
   - **Google Sheets API**
   - **Google Drive API**

### **2. Configurar Service Account**
1. Crie um Service Account
2. Baixe o arquivo JSON de credenciais
3. Salve como:
   - `automacao/projetos/boletim/credentials.json` (projeto boletim)
   - `automacao/projetos/csat/csat.json` (projeto CSAT)

### **3. Compartilhar Planilhas**
Compartilhe suas planilhas Google Sheets com o email do Service Account:
```
nomedoservico@nomeproject.iam.gserviceaccount.com
```

### **4. Configurar IDs das Planilhas**
Edite `automacao/core/config.py` e atualize:
```python
PLANILHAS_CONFIG = {
    "boletim": {
        "id_planilha": "SEU_ID_DA_PLANILHA_AQUI",
        # ...
    }
}
```

---

## 📖 **Como Usar**

### **Execução Simples**
```bash
cd automacao

# Processar projeto específico
python main.py --projeto boletim

# Executar todos os projetos
python main.py

# Apenas renomear arquivos
python main.py --renomear

# Executar testes
python main.py --teste
```

### **Windows - Interface Gráfica**
```batch
# Executor com menu interativo
scripts\executar.bat
```

---

## 🧪 **Testes**

```bash
# Executar todos os testes
python main.py --teste

# Testes específicos (dentro da pasta tests/)
python -m pytest tests/
```

---

## 📊 **Logs e Monitoramento**

### **Localização dos Logs**
- **Arquivo**: `automacao/logs/automacao.log`
- **Console**: Saída em tempo real

### **Tipos de Log**
- ✅ **INFO**: Operações normais
- ⚠️ **WARNING**: Avisos (arquivos não encontrados)
- ❌ **ERROR**: Erros que impedem execução

### **Exemplo de Log**
```
2025-09-20 10:30:15,123 - INFO - Arquivo renomeado: Voz HC.csv -> voz.csv
2025-09-20 10:30:16,456 - INFO - CSV lido com sucesso: 486 linhas
2025-09-20 10:30:20,789 - INFO - Dados inseridos na aba 'BASE VOZ' - Range: A2958:O3443
```

---

## 🛠️ **Solução de Problemas**

### **Erro: "FileNotFoundError: credentials.json"**
```bash
# Verifique se o arquivo existe
ls automacao/projetos/boletim/credentials.json

# Se não existe, baixe do Google Cloud Console
```

### **Erro: "Permission denied Google Sheets"**
```bash
# Verifique se a planilha foi compartilhada com o Service Account
# Email deve estar em: credenciais JSON -> client_email
```

### **Erro: "No module named 'gspread'"**
```bash
# Reinstale dependências
pip install -r requirements.txt
```

### **Arquivos não sendo detectados**
```bash
# Verifique padrões em core/config.py
# Adicione novos padrões se necessário
```

---

## 📞 **Suporte**

- **📧 Email**: [seu-email@empresa.com]
- **📱 Slack**: #rpa-suporte
- **📋 Issues**: Use o sistema de issues do repositório

---

## 🏆 **Desenvolvido por**

**Equipe RPA - Leroy Merlin Brasil** 🇧🇷

*Automatizando processos, liberando pessoas para criar valor.*

---

<div align="center">

**⭐ Deu certo? Compartilhe com a equipe! ⭐**

</div>

Sistema de automação RPA para processos da Leroy Merlin, incluindo atualização de bases de dados e relatórios.

## 📁 Estrutura do Projeto

```
src/
└── bot/
    └── scripts/
        └── bases/
            ├── boletim-agosto-setembro/    # Scripts para boletim mensal
            ├── csat/                       # Scripts CSAT
            └── pulso/                      # Scripts Pulso
```

## 🚀 Como Configurar

### 1. Credenciais do Google Cloud

Para cada script que usa Google Sheets, você precisa configurar as credenciais:

1. Copie o arquivo de exemplo:
   ```bash
   cp src/bot/scripts/bases/pulso/pulso.json.example src/bot/scripts/bases/pulso/pulso.json
   ```

2. Edite o arquivo `pulso.json` com suas credenciais reais do Google Cloud Service Account

3. Repita o processo para outros scripts conforme necessário

### 2. Instalação de Dependências

```bash
pip install pandas openpyxl gspread google-auth
```

## 📊 Scripts Disponíveis

### Pulso
- **Arquivo**: `src/bot/scripts/bases/pulso/pulso-atualizada.py`
- **Função**: Atualiza diferentes abas da planilha Pulso com bases específicas
- **Documentação**: Ver `src/bot/scripts/bases/pulso/README.md`

### Boletim
- **Arquivo**: `src/bot/scripts/bases/boletim-agosto-setembro/boletim.py`
- **Função**: Gera relatórios de boletim mensal

### CSAT
- **Arquivo**: `src/bot/scripts/bases/csat/csat.py`
- **Função**: Processa dados de satisfação do cliente

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- Nunca commite arquivos `.json` com credenciais reais
- Use apenas os arquivos `.json.example` como modelo
- Mantenha suas credenciais locais e seguras

## 📝 Como Usar

1. Configure suas credenciais (veja seção "Como Configurar")
2. Prepare seus arquivos CSV de dados
3. Execute o script desejado
4. Verifique os resultados na planilha Google Sheets

## 🛠️ Desenvolvimento

Para contribuir com o projeto:

1. Clone o repositório
2. Configure suas credenciais locais
3. Teste suas alterações
4. Faça commit (sem arquivos sensíveis)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação específica de cada script ou entre em contato com a equipe.