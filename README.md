# RPA Leroy Merlin

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