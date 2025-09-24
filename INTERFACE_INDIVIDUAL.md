# 🎯 EXECUÇÃO INDIVIDUAL - INTERFACE LEROY MERLIN

## 📋 Visão Geral

A interface visual agora permite execução individual dos sistemas **Genesys** e **Salesforce**, além da execução completa. Isso resolve problemas de encoding e oferece controle granular sobre o processamento.

## 🔧 Novas Funcionalidades

### 1. **Botões de Execução Individual**
```
📊 GENESYS APENAS        💼 SALESFORCE APENAS
    [Botão Verde]           [Botão Verde]
    
🚀 EXECUTAR AUTOMAÇÃO COMPLETA
        [Botão Principal]
```

### 2. **Tratamento Robusto de Encoding**
- **UTF-8 com BOM**: Suporte completo para arquivos Excel exportados
- **Múltiplos Encodings**: Testa automaticamente 9 tipos diferentes
- **Detecção Inteligente**: Identifica separadores (`;`, `,`, `\t`, `|`, `:`)
- **Recuperação de Erros**: Pula linhas problemáticas automaticamente

### 3. **Logs Melhorados**
- **Numeração de Linhas**: `[001] Mensagem`
- **Stderr Separado**: `[ERR001] Erro específico`
- **Categorização**: Cores diferentes por tipo de mensagem
- **Traceback Detalhado**: Em caso de erros python

## 🚀 Como Usar

### **Execução Individual - Genesys**
1. Clique em **"📊 GENESYS APENAS"**
2. Confirme na janela de diálogo
3. Acompanhe o processamento no log
4. Resultado: Apenas dados Genesys processados

### **Execução Individual - Salesforce** 
1. Clique em **"💼 SALESFORCE APENAS"**
2. Confirme na janela de diálogo
3. Acompanhe o processamento no log
4. Resultado: Apenas dados Salesforce processados

### **Execução Completa**
1. Clique em **"🚀 EXECUTAR AUTOMAÇÃO COMPLETA"**
2. Processa Genesys + Salesforce juntos
3. Respeita os checkboxes selecionados

## ⚡ Vantagens da Execução Individual

### **🎯 Resolução de Problemas**
- **Isolamento de Erros**: Identificar se problema é Genesys ou Salesforce
- **Debugging Facilitado**: Logs mais limpos e específicos
- **Recuperação Rápida**: Processar só o que deu problema

### **📊 Eficiência Operacional**
- **Processamento Seletivo**: Só processar dados disponíveis
- **Tempo Otimizado**: Evitar esperas desnecessárias
- **Recursos Conservados**: Menor uso de CPU/memória

### **🔧 Flexibilidade**
- **Horários Diferentes**: Processar sistemas em momentos distintos
- **Priorização**: Processar primeiro o mais urgente
- **Teste Gradual**: Validar um sistema antes do outro

## 🛠️ Melhorias Técnicas Implementadas

### **1. Encoding Robusto**
```python
# Encodings testados automaticamente:
- utf-8-sig     # Excel com BOM
- utf-8         # Padrão
- latin-1       # Windows padrão
- cp1252        # Windows-1252
- iso-8859-1    # ISO Latin-1
- cp850         # DOS Latin-1
- utf-16*       # Unicode 16-bit
```

### **2. Separador Inteligente**
```python
# Detecta automaticamente:
separadores = [';', ',', '\t', '|', ':']
# Valida campos não vazios
# Evita falsos positivos
```

### **3. Recuperação de Erros**
```python
# Configurações robustas:
on_bad_lines='skip'      # Pula linhas problemáticas
engine='python'          # Engine mais tolerante  
errors='replace'         # Substitui caracteres inválidos
```

### **4. Interface Responsiva**
```python
# Durante execução:
- Desabilita todos os botões
- Mostra progresso visual
- Logs em tempo real
- Restaura estado final
```

## 🔍 Resolução do Erro UTF-8

### **Problema Original**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc7 in position 214
```

### **Solução Implementada**
1. **Detecção Automática**: Testa 9 encodings diferentes
2. **BOM Support**: Detecta Byte Order Mark do Excel
3. **Fallback Inteligente**: Converte problemas para UTF-8
4. **Logs Detalhados**: Mostra qual encoding foi usado

### **Como Funciona**
```python
# Processo automático:
1. Tenta utf-8-sig (Excel)
2. Se falhar, tenta utf-8 padrão  
3. Se falhar, tenta latin-1
4. Continue até encontrar compatível
5. Em último caso, usa chardet (se instalado)
```

## 📈 Resultados Esperados

### **✅ Sucesso Individual**
- Processamento isolado funcionando
- Logs limpos e específicos
- Identificação precisa de problemas
- Tempo de execução otimizado

### **🔧 Debugging Melhorado**
- Erros específicos por sistema
- Traceback detalhado quando necessário
- Encoding usado mostrado no log
- Separador detectado informado

### **💚 Experiência do Usuário**
- Interface mais intuitiva
- Controle granular sobre execução
- Feedback visual melhorado
- Recuperação de erros automatizada

## 🎯 Próximos Passos

1. **Teste a execução individual** com seus arquivos
2. **Compare os logs** entre execução individual e completa
3. **Identifique problemas específicos** usando isolamento
4. **Relate feedback** para melhorias adicionais

---

**💡 Dica**: Use execução individual para identificar problemas, depois use execução completa para operação normal.

**🔧 Troubleshooting**: Se ainda houver erros de encoding, verifique se o arquivo CSV não está corrompido ou use uma ferramenta para converter para UTF-8.