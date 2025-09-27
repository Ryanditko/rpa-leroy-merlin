# 🚀 Automação Leroy Merlin - RPA Boletins

Sistema automatizado para processamento de boletins e relatórios das plataformas Genesys e Salesforce em planilhas Google Sheets.

## ✨ Funcionalidades

### 🎯 **NOVIDADES v2.2 - EXECUÇÃO INDIVIDUAL**

**✨ Agora você pode executar Genesys e Salesforce separadamente!**

- **📊 Botão "GENESYS APENAS"**: Processa só dados Genesys
- **💼 Botão "SALESFORCE APENAS"**: Processa só dados Salesforce  
- **🚀 Botão "EXECUÇÃO COMPLETA"**: Ambos sistemas juntos
- **🔧 Encoding Robusto**: Resolve erros UTF-8 automaticamente (testa 9 encodings)
- **📝 Logs Melhorados**: Numeração, stderr separado, traceback detalhado

**💡 Vantagens da Execução Individual:**
- 🎯 **Isolamento de Problemas**: Identifica exatamente onde está o erro
- ⚡ **Maior Eficiência**: Processa só o que tem dados
- 🔍 **Debugging Fácil**: Logs limpos e específicos
- 🕒 **Flexibilidade**: Execute sistemas em horários diferentes

### 🎯 Automação Completa
- **Genesys**: Processamento de dados de VOZ HC, TEXTO HC, GESTÃO (incluindo N1) e FILA
- **Salesforce**: Processamento de CRIADO, RESOLVIDO, COMENTÁRIOS BKO e DADOS SELLER
- **Detecção Automática**: Identificação inteligente do tipo de arquivo baseado no nome
- **Múltiplos Encodings**: Suporte automático para UTF-8, Latin-1, CP1252, ISO-8859-1
- **Separadores Flexíveis**: Detecção automática de separadores (';', ',', '\t')

### 🔧 Recursos Avançados
- **Preservação de Dados**: Modo complementar que preserva dados existentes
- **Expansão Automática**: Solução para limite de linhas do Google Sheets
- **Formatação Visual**: Primeira linha pintada em verde Leroy Merlin (#00A859)
- **Logs Detalhados**: Sistema completo de logs com emojis e cores
- **Detecção de Duplicatas**: Identifica e processa arquivos duplicados automaticamente
- **Interface Gráfica**: Interface visual moderna com cores Leroy Merlin
- **🆕 Renomeação Inteligente**: Sistema automático de padronização de nomes de arquivos

## 🏗️ Estrutura do Projeto

```
rpa-leroy-merlin/
├── src/                          # Código fonte principal
│   ├── core/                     # Núcleo do sistema
│   │   ├── __init__.py
│   │   └── google_sheets_base.py # Classe base para Google Sheets
│   └── processadores/            # Processadores específicos
│       ├── __init__.py
│       └── genesys/              # Processador Genesys
│           ├── __init__.py
│           └── processador_genesys.py
├── tests/                        # Scripts de teste
│   ├── teste-genesys.py          # Testes específicos Genesys
│   ├── teste-salesforce.py       # Testes específicos Salesforce
│   └── processar-todos-csvs.py   # Processamento em lote
├── config/                       # Configurações
│   ├── boletim.json              # Credenciais Google (não versionado)
│   ├── requirements.txt          # Dependências Python
│   └── README.md                 # Instruções de configuração
├── data/                         # Dados de entrada
│   └── README.md                 # Instruções sobre dados
├── docs/                         # Documentação
│   └── README.md                 # Documentação técnica
├── main.py                       # Script principal de automação (linha de comando)
├── interface_visual.py           # Interface gráfica moderna v2.2 🎨
├── renomeador_inteligente.py     # Sistema de renomeação automática 
├── INTERFACE_INDIVIDUAL.md      # 📋 Documentação execução individual
├── MELHORIAS_VISUAIS.md         # 🎨 Documentação melhorias visuais v2.2
├── RENOMEADOR.md                # 📝 Documentação sistema renomeação
├── renomeador_inteligente.py     # Sistema de renomeação automática (NOVO)
├── executar.bat                  # Execução rápida CLI (Batch)
├── executar.ps1                  # Execução rápida CLI (PowerShell)
├── interface.bat                 # Interface visual (Batch)
├── interface.ps1                 # Interface visual (PowerShell)
├── .gitignore                    # Arquivos ignorados pelo Git
├── README.md                     # Esta documentação
└── RENOMEADOR.md                 # Documentação do renomeador (NOVO)
```

## ⚡ Como Usar

### 🎨 Interface Visual (MAIS FÁCIL - RECOMENDADO!)

A forma mais fácil e intuitiva de usar o sistema:

**Windows - Duplo clique:**
```cmd
interface.bat  # OU
interface.ps1
```

**Linha de comando:**
```bash
python interface_visual.py
```

**Recursos da Interface:**
- 🎨 Design moderno com cores Leroy Merlin (verde #00A859, laranja #FF6B35)
- ✅ Checkboxes para selecionar Genesys/Salesforce
- 📊 Logs em tempo real com cores
- � **NOVO**: Botão "Renomear Arquivos" para padronização automática
- �📁 Botões para verificar arquivos e abrir pastas
- 🔗 Links diretos para as planilhas
- 📈 Barra de progresso e status
- 🧹 Limpeza de logs
- 🔍 Modo detalhado opcional

### 🚀 Linha de Comando (Avançado)

```bash
# Executar tudo automaticamente
python main.py

# Apenas Genesys
python main.py --genesys

# Apenas Salesforce  
python main.py --salesforce

# Com logs detalhados
python main.py --verbose

# Ver todas as opções
python main.py --help
```

### �️ Execução Rápida CLI no Windows

**Batch (.bat):**
```cmd
# Duplo clique ou execute:
executar.bat
```

**PowerShell (.ps1):**
```powershell
# Execute no PowerShell:
.\executar.ps1
```

### 🧪 Testes Específicos

```bash
# Testar apenas Genesys
python tests/teste-genesys.py

# Testar apenas Salesforce
python tests/teste-salesforce.py

# Processar todos os CSVs encontrados
python tests/processar-todos-csvs.py
```

## 🔧 Configuração Inicial

### 1️⃣ Instalar Dependências
```bash
pip install -r config/requirements.txt
```

### 2️⃣ Configurar Credenciais Google
1. Baixe o arquivo `boletim.json` das credenciais da Service Account
2. Coloque na pasta `config/` ou na raiz do projeto
3. O sistema encontra automaticamente o arquivo

### 3️⃣ Preparar Dados
1. Adicione os arquivos CSV na pasta `data/`
2. **🆕 RECOMENDADO**: Use o botão "📝 Renomear Arquivos" na interface para padronizar nomes
3. O sistema detecta automaticamente o tipo baseado no nome do arquivo
4. Na interface visual, use o botão "📁 Verificar Arquivos" para conferir

## 📊 Planilhas de Destino

### Genesys
- **ID**: `1cHbKXMjJgnR_M3X2uGtDT3kPHTrlBd_g4kqxhrr6MOY`
- **Abas**: BASE VOZ, BASE TEXTO, BASE GE COLABORADOR, BASE GE FILA

### Salesforce  
- **ID**: `1vrOSg1zIYYinSt5A4FNK2403IpecH_06aKSTnMhmCl0`
- **Abas**: BASE ATUALIZADA CORRETA - CRIADO, BASE ATUALIZADA CORRETA - RESOLVIDA, COMENTARIO BKO

## 🎨 Interface Visual - Recursos

### 🖥️ Tela Principal
- **Header Verde**: Título com cores oficiais Leroy Merlin e efeito sombra
- **Layout em Colunas**: Opções de Execução + Gestão de Arquivos
- **Checkboxes**: Escolha entre Genesys, Salesforce ou ambos
- **Botões Funcionais**:
  - 🚀 **EXECUTAR AUTOMAÇÃO COMPLETA**: Botão principal verde (centralizado)
  - 📝 **🆕 Renomear Arquivos**: Padronização inteligente de nomes
  - 📁 **Verificar Arquivos**: Lista arquivos CSV encontrados
  - 📂 **Abrir Pasta Dados**: Abre a pasta data/ no explorer
  - 🧹 **Limpar Logs**: Limpa a área de logs

### 📊 Área de Logs
- **Cores Inteligentes**: 
  - 🟢 Verde: Sucessos
  - 🟠 Laranja: Erros
  - 🔵 Azul: Informações
  - 🟡 Amarelo: Avisos
- **Auto-scroll**: Logs mais recentes sempre visíveis
- **Timestamps**: Cada mensagem com horário

### 🔗 Footer Interativo
- **Links Clicáveis**: Acesso direto às planilhas Genesys e Salesforce
- **Informações do Sistema**: Versão, data/hora
- **Design Responsivo**: Cores Leroy Merlin em todo footer

## 📝 Renomeação Inteligente (NOVO!)

### � Problema Resolvido
Arquivos CSV baixados das plataformas vêm com nomes variáveis:
- `BASE - BOLETIM - CRIADO-2025-09-23-07-00-06.csv`
- `Cópia de BASE - BOLETIM - COMENTARIO BKO-2025-09-23.csv`
- `Gestão da entrega N1 HC.csv`

### ✅ Solução Automática
O sistema **renomeia automaticamente** para nomes padronizados:
- `BASE_SALESFORCE_CRIADO.csv`
- `BASE_SALESFORCE_COMENTARIO_BKO.csv` 
- `BASE_GENESYS_GESTAO_N1_HC.csv`

### 🚀 Como Usar
1. Na interface visual, clique **"📝 Renomear Arquivos"**
2. Veja o **preview** das renomeações planejadas
3. **Confirme** para executar
4. Arquivos ficam prontos para automação!

### 📊 Recursos do Renomeador
- **Preview**: Vê mudanças antes de executar
- **Histórico**: Mantém registro das renomeações
- **Conflitos**: Resolve nomes duplicados automaticamente
- **Backup**: Permite reverter mudanças
- **Tipos**: Identifica automaticamente Genesys vs Salesforce

👉 **Documentação completa**: [RENOMEADOR.md](RENOMEADOR.md)

### Genesys
- `voz` + `hc` → BASE VOZ
- `texto` + `hc` → BASE TEXTO  
- `gestão`/`gestao` + `n1` → BASE GE COLABORADOR
- `gestão`/`gestao` → BASE GE FILA
- `fila` → BASE GE FILA

### Salesforce
- `criado`/`created` → BASE ATUALIZADA CORRETA - CRIADO
- `resolvido`/`resolved` → BASE ATUALIZADA CORRETA - RESOLVIDA
- `comentario`/`comment`/`bko` → COMENTARIO BKO

## 🔍 Resolução de Problemas

### ❌ Erro de Credenciais
```bash
python diagnostico-credenciais.py
```

### ❌ Erro de Encoding
- O sistema tenta automaticamente múltiplos encodings
- Suporte para arquivos em UTF-8, Latin-1, CP1252, ISO-8859-1

### ❌ Limite de Linhas Google Sheets
- Sistema possui solução automática de expansão
- Usa técnica de inserção de linha em branco para expandir

### ❌ Arquivos Não Encontrados
- Verificar se estão na pasta `data/`
- Na interface visual: usar botão "📁 Verificar Arquivos"
- Sistema busca arquivos duplicados automaticamente
- Aceita padrões como `arquivo.csv`, `arquivo (1).csv`, etc.

## 📋 Exemplos de Uso

### Exemplo 1: Interface Visual (Recomendado)
1. Execute `interface.bat` (duplo clique)
2. **🆕 Clique "📝 Renomear Arquivos"** (se necessário)
3. Marque as opções desejadas (Genesys/Salesforce)
4. Clique em "🚀 EXECUTAR AUTOMAÇÃO COMPLETA"
5. Acompanhe os logs em tempo real
6. Clique nos links do footer para ver as planilhas

### Exemplo 2: Linha de Comando Completa
```bash
# Processa todos os CSVs encontrados em ambos os sistemas
python main.py
```

### Exemplo 3: Apenas um Sistema
```bash
# Só Genesys (linha de comando)
python main.py --genesys

# Só Salesforce (linha de comando)
python main.py --salesforce
```

## 🚨 Características Importantes

- **Modo Complementar**: Preserva dados existentes, adiciona novos
- **Remove Cabeçalhos**: Remove automaticamente a primeira linha dos CSVs
- **Formatação Verde**: Primeira linha de cada inserção fica verde Leroy Merlin
- **🆕 Renomeação Inteligente**: Padroniza nomes de arquivos automaticamente
- **Interface Intuitiva**: Design moderno com cores e ícones oficiais
- **Logs Visuais**: Sistema completo de feedback com cores e emojis
- **Detecção Inteligente**: Encontra arquivos automaticamente
- **Robustez**: Múltiplas tentativas de conexão e tratamento de erros
- **Multi-plataforma**: Funciona em Windows com interface nativa

## 🎨 Cores Oficiais Leroy Merlin

A interface usa as cores oficiais da marca:
- **Verde Principal**: `#00A859` - Botões principais, sucessos
- **Verde Escuro**: `#008A47` - Headers, footer
- **Laranja**: `#FF6B35` - Botões secundários, erros
- **Azul Info**: `#17A2B8` - Informações, links
- **Cinza Escuro**: `#333333` - Textos, área de logs
- **Cinza Claro**: `#F5F5F5` - Background

## 🔗 Links das Planilhas

- [📊 Planilha Genesys](https://docs.google.com/spreadsheets/d/1cHbKXMjJgnR_M3X2uGtDT3kPHTrlBd_g4kqxhrr6MOY)
- [💼 Planilha Salesforce](https://docs.google.com/spreadsheets/d/1vrOSg1zIYYinSt5A4FNK2403IpecH_06aKSTnMhmCl0)

---

**🎯 Sistema desenvolvido para automatizar completamente o processo de envio de boletins para planilhas Google, com interface visual intuitiva, renomeação inteligente, detecção automática e tratamento robusto de erros.**

**🎨 Use a interface visual para uma experiência mais amigável e fácil!**

**🆕 NOVIDADE v2.1: Sistema de renomeação inteligente integrado - nunca mais se preocupe com nomes de arquivos!**

### Execução Principal

```bash
# Executar sistema completo
python src/main.py

# Processar apenas Genesys
python src/main.py --genesys

# Processar apenas Salesforce  
python src/main.py --salesforce

# Especificar pasta de dados
python src/main.py --dados ./meus_dados
```

### Teste Rápido

```bash
# Testar envio de dados VOZ para Google Sheets
python tests/teste-voz-melhorado.py
```

## 🔧 Funcionalidades

### ✅ Processamento Automático
- Detecta arquivos CSV na pasta `data/`
- Identifica automaticamente o tipo de dados
- Processa e envia para Google Sheets
- Preserva dados existentes (modo complementar)

### ✅ Suporte a Múltiplas Fontes
- **Genesys**: Dados de VOZ, TEXTO, FILA
- **Salesforce**: Comentários, Criados, Resolvidos

### ✅ Recursos Avançados
- Detecção automática de separadores CSV (`,` ou `;`)
- Remoção automática de cabeçalhos duplicados
- Modo incremental (não sobrescreve dados existentes)
- Logs detalhados de execução

## 🛠️ Solução de Problemas

### Erro: "FileNotFoundError: config/boletim.json"
- Verifique se o arquivo de credenciais existe
- Confirme se está no formato JSON correto

### Erro: "Permission denied Google Sheets"
- Verifique se a planilha foi compartilhada com o Service Account
- Confirme se o Service Account tem permissão de "Editor"

### Arquivos não sendo detectados
- Verifique se os arquivos estão na pasta `data/`
- Confirme se os nomes dos arquivos seguem os padrões esperados

## 📊 IDs das Planilhas Configuradas

- **Planilha Principal**: `1cHbKXMjJgnR_M3X2uGtDT3kPHTrlBd_g4kqxhrr6MOY`
- **Aba VOZ**: BASE VOZ
- **Aba TEXTO**: BASE TEXTO
- **Aba SALESFORCE**: BASE SALESFORCE

## 🧪 Estrutura de Testes

```bash
# Executar teste principal
python tests/teste-voz-melhorado.py

# Resultado esperado:
# ✅ Conecta com Google Sheets
# ✅ Processa arquivo Voz HC.csv
# ✅ Envia dados para aba BASE VOZ
# ✅ Preserva dados existentes
```

## 🤝 Contribuindo

1. Mantenha a estrutura de pastas organizada
2. Adicione testes para novas funcionalidades
3. Documente mudanças importantes
4. Use logs informativos

## 📄 Licença

Projeto interno Leroy Merlin - Uso restrito.

---

**Desenvolvido para automatizar o processamento de boletins e relatórios da Leroy Merlin** 🏪