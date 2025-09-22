@echo off
echo ========================================
echo   RPA LEROY MERLIN - EXECUTAR
echo ========================================
echo.

cd /d "%~dp0\..\automacao"

if "%1"=="" (
    echo Escolha uma opção:
    echo.
    echo [1] Executar projeto BOLETIM
    echo [2] Executar projeto CSAT  
    echo [3] Executar apenas renomeação
    echo [4] Executar todos os testes
    echo [5] Ver logs
    echo.
    set /p opcao="Digite sua opção (1-5): "
    
    if "!opcao!"=="1" (
        echo.
        echo 🚀 Executando projeto BOLETIM...
        python main.py --projeto boletim
    ) else if "!opcao!"=="2" (
        echo.
        echo 🚀 Executando projeto CSAT...
        python main.py --projeto csat
    ) else if "!opcao!"=="3" (
        echo.
        echo 📝 Executando apenas renomeação...
        python main.py --renomear
    ) else if "!opcao!"=="4" (
        echo.
        echo 🧪 Executando testes...
        python main.py --teste
    ) else if "!opcao!"=="5" (
        echo.
        echo 📋 Últimas 20 linhas do log:
        if exist logs\automacao.log (
            type logs\automacao.log | more +20
        ) else (
            echo Nenhum log encontrado.
        )
    ) else (
        echo Opção inválida!
    )
) else (
    echo 🚀 Executando com parâmetros: %*
    python main.py %*
)

echo.
pause
