# Isoterma - Monitoreo Agrícola de Precisión

Sistema completo de monitoreo de isotermas para agricultura de precisión con visualización Kepler.gl.

## 🏗️ Arquitectura

```
┌─────────────────┐      ┌──────────────────┐
│                 │      │                  │
│  Frontend       │─────▶│  Backend         │
│  SvelteKit      │      │  FastAPI         │
│  Kepler.gl      │      │  Open-Meteo API  │
│  Port: 3000     │      │  Port: 8000      │
│                 │      │                  │
└─────────────────┘      └──────────────────┘
```

## 📦 Componentes

### Backend (FastAPI)
- API REST para datos meteorológicos
- Integración con Open-Meteo API
- Gestión de fincas y sensores
- Validación de sensores térmicos

### Frontend (SvelteKit + Kepler.gl)
- Dashboard interactivo
- Mapa de isotermas con Kepler.gl
- 4 capas de temperatura (1m, 2m, 5m, 10m)
- Pronóstico meteorológico 72h
- Tema dark/light

## 🚀 Inicio Rápido con Docker

### Requisitos
- Docker Desktop instalado
- Docker Compose

### Scripts Automáticos

```bash
cd web

# Iniciar todo el stack
docker-start.bat

# Ver logs
docker-logs.bat

# Detener
docker-stop.bat
```

## 🌐 URLs

Una vez iniciado:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
kepler/
├── web/                       # Aplicación Web
│   ├── isoterma_backend/      # Backend FastAPI
│   ├── isoterma_frontend/     # Frontend SvelteKit
│   ├── docker-compose.yml     # Orquestación
│   ├── docker-start.bat       # Script inicio
│   ├── docker-stop.bat        # Script detener
│   ├── docker-logs.bat        # Script logs
│   └── README.md
│
├── 01-tiny-example/           # Ejemplos básicos Kepler.gl
├── 02-finca-rio-negro/        # Ejemplo finca simple
├── 03-finca-rio-negro-altitude/  # Ejemplo con altitud
├── 04-visual-heatmap/         # Ejemplos heatmap avanzados
├── 05-API Integration Temperature/  # Ejemplos integración API
└── README.md                  # Este archivo
```

## 🗺️ Características Kepler.gl

✅ **Heatmaps** de temperatura en 4 alturas  
✅ **Vista 3D** con elevaciones del terreno  
✅ **Capas intercambiables** para análisis  
✅ **Vista satelital** de alta resolución  
✅ **Tooltips** con datos de sensores  
✅ **Exportar** configuraciones  

## 🔧 Desarrollo Local (Sin Docker)

### Backend

```bash
cd web/isoterma_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd web/isoterma_frontend
npm install
npm run dev
```

## 📊 Datos de Ejemplo

El proyecto incluye 2 fincas de ejemplo:

1. **Chacra 143** (Río Negro)
   - 80 sensores en cuadrícula
   - 143 hectáreas
   - Cultivo: Manzanas

2. **Quinta Los Álamos** (Río Negro)
   - 60 sensores
   - 95 hectáreas
   - Cultivo: Peras

## 🐛 Troubleshooting

### Puerto ocupado

```bash
# Ver qué usa el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Cambiar puerto en docker-compose.yml
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
```

### Rebuild completo

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Ver logs de un servicio específico

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Entrar al contenedor

```bash
docker exec -it isoterma-backend bash
docker exec -it isoterma-frontend sh
```

## 🔄 Actualizar Código

```bash
# Detener
docker-compose down

# Rebuild
docker-compose build

# Reiniciar
docker-compose up -d
```

## 📝 Variables de Entorno

### Backend
- `LOG_LEVEL`: Nivel de logs (info, debug, warning)
- `PYTHONUNBUFFERED`: Output inmediato de logs

### Frontend
- `NODE_ENV`: production/development
- `PUBLIC_API_URL`: URL del backend API

## 🚢 Producción

Para producción, considera:

1. **Usar nginx** como reverse proxy
2. **HTTPS** con certificados SSL
3. **Variables de entorno** desde archivos .env
4. **Volúmenes** para persistencia de datos
5. **Health checks** configurados
6. **Logging** centralizado
7. **Monitoring** (Prometheus/Grafana)

### docker-compose.prod.yml (ejemplo)

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - backend
      - frontend

  backend:
    build: ./isoterma_backend
    environment:
      - LOG_LEVEL=warning
    restart: always

  frontend:
    build: ./isoterma_frontend
    environment:
      - NODE_ENV=production
    restart: always
```

## 📚 Documentación

- [Web Application](./web/README.md)
- [Backend README](./web/isoterma_backend/README.md)
- [Frontend README](./web/isoterma_frontend/README.md)
- [API Docs](http://localhost:8000/docs) (cuando esté corriendo)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

MIT License

---

**Desarrollado para agricultura de precisión en Argentina** 🌾🇦🇷
