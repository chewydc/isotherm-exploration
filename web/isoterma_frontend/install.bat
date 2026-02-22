@echo off
echo ========================================
echo Isoterma Frontend - Instalacion
echo ========================================
echo.

echo [1/3] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Descarga desde: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo.

echo [2/3] Instalando dependencias...
call npm install
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo.

echo [3/3] Instalacion completada!
echo.
echo ========================================
echo Para ejecutar el proyecto:
echo   npm run dev
echo.
echo Luego abre: http://localhost:3000
echo ========================================
pause
