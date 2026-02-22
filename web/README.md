# Isoterma Web Application

Sistema completo de monitoreo de isotermas para agricultura de precisión.

## 🏗️ Arquitectura

```
┌─────────────────┐      ┌──────────────────┐
│  Frontend       │─────▶│  Backend         │
│  SvelteKit      │      │  FastAPI         │
│  Kepler.gl      │      │  Open-Meteo API  │
│  Port: 3000     │      │  Port: 8000      │
└─────────────────┘      └──────────────────┘
```

## 📦 Componentes

- **isoterma_backend/** - API FastAPI para datos meteorológicos
- **isoterma_frontend/** - Dashboard SvelteKit con Kepler.gl
- **docker-compose.yml** - Orquestación de servicios

## ✨ Funcionalidades

### 🌡️ Monitoreo de Temperatura
- Dashboard con datos de sensores en tiempo real
- Visualización de isotermas con Kepler.gl
- Pronóstico meteorológico 72h (Open-Meteo API)
- Validación automática de sensores

### 🚨 Sistema de Alertas
- **Configuración de umbrales** por finca
- **Alertas automáticas** cuando sensores salen de rango
- **Panel de gestión** para cada finca
- **Notificaciones visuales** en tiempo real

### 🏭 Gestión de Fincas
- **30 sensores** en Chacra 143 (Río Negro)
- **Configuración personalizable** de umbrales
- **Estados de sensores:** active, warning, error
- **Datos persistentes** en JSON

## 🚀 Inicio Rápido

### Con Docker (Recomendado)

```bash
# Iniciar todo el stack
docker-start.bat

# Ver logs
docker-logs.bat

# Detener
docker-stop.bat
```

### Sin Docker

**Backend:**
```bash
cd isoterma_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd isoterma_frontend
npm install
npm run dev
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Gestión de Finca**: http://localhost:3000/farm/finca_001/settings

## 🔧 API Endpoints

### Fincas
- `GET /api/v1/farms` - Listar todas las fincas
- `GET /api/v1/farms/{id}` - Obtener detalles de finca
- `PUT /api/v1/farms/{id}/settings` - Actualizar umbrales
- `GET /api/v1/farms/{id}/alerts` - Obtener alertas activas

### Clima
- `GET /api/v1/weather/current` - Clima actual
- `GET /api/v1/weather/forecast` - Pronóstico 72h
- `POST /api/v1/weather/validate` - Validar sensor

## 📁 Estructura

```
web/
├── isoterma_backend/       # Backend FastAPI
├── isoterma_frontend/      # Frontend SvelteKit
├── docker-compose.yml      # Orquestación Docker
├── docker-start.bat        # Script inicio
├── docker-stop.bat         # Script detener
├── docker-logs.bat         # Script logs
└── README.md              # Este archivo
```

## 🔧 Desarrollo

Ver documentación específica en cada componente:
- [Backend README](./isoterma_backend/README.md)
- [Frontend README](./isoterma_frontend/README.md)
