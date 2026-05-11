#!/usr/bin/env bash

set -e

PYTHON=python3
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 não foi encontrado. Instale o Python 3 e tente novamente."
  exit 1
fi

echo "Verificando o ambiente Python..."

if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual..."
  "$PYTHON" -m venv .venv
fi

echo "Ativando ambiente virtual e instalando dependências..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Iniciando o aplicativo..."
python main.py