@echo off
echo Habilitando extensiones de Jupyter para Kepler.gl...

jupyter nbextension install --py --sys-prefix keplergl
jupyter nbextension enable --py --sys-prefix keplergl

echo Reinicia Jupyter Notebook y prueba de nuevo
pause