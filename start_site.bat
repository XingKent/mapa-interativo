@echo off
echo Criando ambiente virtual, se necessario...
if not exist venv\ (
    python -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo --- INICIANDO O SERVIDOR DJANGO EM UMA NOVA JANELA ---
start "" python manage.py runserver

echo.
echo Aguardando 5 segundos para o servidor iniciar completamente...
timeout /t 5 /nobreak >nul

echo Abrindo o site no seu navegador...
start http://127.0.0.1:8000/

echo.
echo O servidor Django esta rodando na outra janela.
echo Pressione Ctrl+C naquela janela para parar o servidor.
echo.
pause
