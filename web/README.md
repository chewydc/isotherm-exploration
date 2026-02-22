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
