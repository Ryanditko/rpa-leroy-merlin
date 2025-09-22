#!/bin/bash

echo "========================================"
echo "Instalação da Automação de Bases CSV"
echo "========================================"

echo ""
echo "1. Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERRO: Python não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

echo ""
echo "2. Instalando dependências..."
pip3 install -r requirements.txt

echo ""
echo "3. Criando diretórios necessários..."
mkdir -p processed/originais

echo ""
echo "4. Verificando arquivos de credenciais..."
if [ ! -f "boletim.json" ]; then
    echo "AVISO: boletim.json não encontrado"
    echo "       Configure as credenciais do Google Cloud para o projeto boletim"
fi

if [ ! -f "csat/csat.json" ]; then
    echo "AVISO: csat/csat.json não encontrado"
    echo "       Use csat/csat.json.template como modelo"
fi

echo ""
echo "5. Testando instalação..."
python3 main.py --teste

echo ""
echo "========================================"
echo "Instalação concluída!"
echo "========================================"
echo ""
echo "Para usar:"
echo "  python3 main.py              # Fluxo completo"
echo "  python3 main.py --teste       # Apenas testes"
echo "  python3 main.py --renomear    # Apenas renomear arquivos"
echo ""
