@echo off
echo A navegar para a pasta do projeto...
cd "C:\Users\Legion\code\Performance_N1"

echo A ativar o ambiente virtual (venv)...
call .\venv\Scripts\activate.bat

echo A executar o script principal (main.py)...
python main.py

echo.
echo Script concluido. Pressione qualquer tecla para sair.
pause > nul