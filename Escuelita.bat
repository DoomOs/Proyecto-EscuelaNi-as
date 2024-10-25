@echo off
REM Cambia a la ruta del proyecto (en este caso, la carpeta actual)
cd /d .\

REM Activa el entorno virtual
call venv\Scripts\activate


REM Inicia el servidor de Django en segundo plano
start /B python manage.py runserver

REM Espera unos segundos para asegurarse de que el servidor haya iniciado
timeout /t 3 /nobreak >nul

REM Abre el navegador en http://127.0.0.1:8000/
start http://127.0.0.1:8000/

REM Mantén la ventana abierta después de ejecutar todo
pause
