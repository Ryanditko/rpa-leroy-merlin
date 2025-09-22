@echo off
echo ========================================
echo Instalacao da Automacao de Bases CSV
echo ========================================

echo.
echo 1. Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado. Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo.
echo 2. Instalando dependencias...
pip install -r requirements.txt

echo.
echo 3. Criando diretorios necessarios...
if not exist "processed" mkdir processed
if not exist "processed\originais" mkdir processed\originais

echo.
echo 4. Verificando arquivos de credenciais...
if not exist "boletim.json" (
    echo AVISO: boletim.json nao encontrado
    echo        Configure as credenciais do Google Cloud para o projeto boletim
)

if not exist "csat\csat.json" (
    echo AVISO: csat\csat.json nao encontrado
    echo        Use csat\csat.json.template como modelo
)

echo.
echo 5. Testando instalacao...
python main.py --teste

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Para usar:
echo   python main.py              # Fluxo completo
echo   python main.py --teste       # Apenas testes
echo   python main.py --renomear    # Apenas renomear arquivos
echo.
pause
