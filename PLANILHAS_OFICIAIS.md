# 📊 Planilhas Oficiais - Leroy Merlin

## 🎯 **Configuração Final das Planilhas**

### **Planilhas Atualizadas para Versão Oficial:**

#### 📈 **Genesys (Oficial)**
- **ID:** `14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc`
- **URL:** https://docs.google.com/spreadsheets/d/14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc/edit?gid=282816795#gid=282816795
- **Abas processadas:**
  - BASE VOZ (Voz HC)
  - BASE TEXTO (Texto HC)
  - BASE GE COLABORADOR (Gestão N1)
  - BASE GE FILA (Gestão/Fila)

#### 💼 **Salesforce (Oficial)**
- **ID:** `1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0`
- **URL:** https://docs.google.com/spreadsheets/d/1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0/edit?gid=571976706#gid=571976706
- **Abas processadas:**
  - BASE ATUALIZADA CORRETA - CRIADO
  - BASE ATUALIZADA CORRETA - RESOLVIDA
  - BASE COMENTÁRIO BKO
  - BASE SELLER

---

## ✅ **Arquivos Atualizados:**

### **Arquivos Principais:**
- ✅ `main.py` - IDs atualizados no `PLANILHAS_CONFIG`
- ✅ `interface_visual.py` - Links dos botões atualizados
- ✅ `src/core/google_sheets_base.py` - ID padrão removido para flexibilidade

### **Arquivos de Teste:**
- ✅ `tests/teste-genesys.py` - ID oficial Genesys
- ✅ `tests/teste-salesforce.py` - ID oficial Salesforce  
- ✅ `tests/teste-voz.py` - ID oficial Genesys
- ✅ `tests/processar-todos-csvs.py` - ID oficial Genesys

---

## 🚀 **Status da Migração:**

**✅ CONCLUÍDA** - Todos os arquivos foram atualizados para usar as planilhas oficiais da Leroy Merlin.

### **Funcionalidades Mantidas:**
- ⚡ Execução individual (Genesys/Salesforce/Ambos)
- 🎨 Interface visual moderna com scroll
- 🔗 Links diretos para as planilhas oficiais
- 🎯 Detecção automática de tipo de arquivo
- 🌈 Coloração completa das linhas nas planilhas
- 🛡️ Encoding robusto (9 formatos suportados)
- 📝 Logs em tempo real compactos

### **Como usar:**
```bash
# Automação completa
python main.py

# Interface visual
python interface_visual.py

# Execução individual
python main.py --genesys      # Só Genesys
python main.py --salesforce   # Só Salesforce
```

---

**Data de Atualização:** 24/09/2025  
**Versão:** 2.2 - Oficializada ✨