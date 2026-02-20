@echo off
echo === INSTALACION FINCA RIO NEGRO ALTITUDE ===

echo 1. Creando entorno virtual...
python -m venv env

echo 2. Activando entorno...
call env\Scripts\activate

echo 3. Instalando dependencias...
pip install pandas numpy requests keplergl==0.2.2 matplotlib scipy

echo === INSTALACION COMPLETADA ===
echo.
echo Para usar:
echo 1. call env\Scripts\activate
echo 2. python finca_altitude.py
echo 3. Abrir finca_altitude_mapa.html
echo.
pause