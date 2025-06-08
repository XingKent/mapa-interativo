@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependências...
pip install -r requirements.txt

echo Rodando servidor Django...
python manage.py runserver
start "" http://127.0.0.1:8000/
pause
