#!/bin/bash

# Encerra o script se qualquer comando falhar
set -e

echo "Verificando o ambiente Python..."

# Verifica se há um ambiente virtual .venv e cria um caso não exista
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

echo "Ativando ambiente virtual e instalando dependencias..."
source .venv/bin/activate
pip install -r requirements.txt

echo "Iniciando o aplicativo..."
python3 main.py