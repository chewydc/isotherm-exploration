@echo off
echo ========================================
echo Isoterma Stack - Docker Compose
echo ========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no esta instalado
    echo Descarga desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
docker --version
echo.

echo Verificando Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose no esta instalado
    pause
    exit /b 1
)
docker-compose --version
echo.

echo ========================================
echo Construyendo imagenes...
echo ========================================
docker-compose build

if errorlevel 1 (
    echo ERROR: Fallo la construccion de imagenes
    pause
    exit /b 1
)

echo.
echo ========================================
echo Iniciando servicios...
echo ========================================
docker-compose up -d

if errorlevel 1 (
    echo ERROR: Fallo al iniciar servicios
    pause
    exit /b 1
)

echo.
echo ========================================
echo Stack iniciado correctamente!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs:     http://localhost:8000/docs
echo.
echo Para ver logs:
echo   docker-compose logs -f
echo.
echo Para detener:
echo   docker-compose down
echo ========================================
pause
