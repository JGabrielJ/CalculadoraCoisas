@echo off
setlocal
title Calculadora de Coisas

echo Verificando o ambiente Python...

IF NOT EXIST .venv (
    echo Criando ambiente virtual...
    py -3 -m venv .venv 2>nul || python -m venv .venv
)

echo Ativando ambiente virtual e instalando dependências...
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Iniciando o aplicativo...
python main.py

endlocal
