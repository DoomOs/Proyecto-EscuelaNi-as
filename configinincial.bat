@echo off
REM Cambia a la ruta del proyecto (en este caso, la carpeta actual)
cd /d .\

start /B pip install -r requirements.txt

REM Activa el entorno virtual
call venv\Scripts\activate

timeout /t 3 /nobreak >nul



REM Inicia el servidor de Django en segundo plano
start /B python manage.py makemigrations
REM Espera unos segundos para asegurarse de que el servidor haya iniciado
timeout /t 3 /nobreak >nul
REM Inicia el servidor de Django en segundo plano
start /B python manage.py migrate

REM Creacion de tu usuario

start python manage.py createsuperuser