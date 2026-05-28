@echo off
echo ===================================================
echo   INICIANDO SISTEMA CLINICO FUNDACREDESA
echo ===================================================
echo.
echo Verificando dependencias...
pip install -r requirements.txt

echo.
echo Arrancando el servidor web...
echo Por favor, no cierres esta ventana negra.
echo Para acceder al sistema abre tu navegador web en: http://localhost:5000
echo.

python run.py
pause
