# Isoterma Backend API

Backend FastAPI para consultas meteorológicas, validación de sensores térmicos y análisis de isotermas para agricultura de precisión.

## 🎯 Propósito

Proveedor de datos meteorológicos en tiempo real y pronósticos para:
- Validación de sensores de temperatura en campo
- Análisis de isotermas para agricultura de precisión
- Monitoreo de condiciones climáticas en fincas
- Planificación de actividades agrícolas

## 📁 Estructura del Proyecto

```
isoterma_backend/
├── src/
│   ├── models/
│   │   └── weather_models.py      # Modelos Pydantic (request/response)
│   ├── routers/
│   │   ├── api.py                 # Router principal v1
│   │   ├── weather_routes.py      # Endpoints meteorológicos
│   │   └── health_routes.py       # Health checks (K8s ready)
│   ├── services/
│   │   └── weather_service.py     # Lógica de negocio y APIs externas
│   └── utils/
│       └── logging_config.py      # Configuración de logs
├── main.py                        # Aplicación FastAPI
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Containerización Docker
└── README.md                      # Este archivo
```

## 🚀 APIs Disponibles

### Base URL
```
Local: http://localhost:8000
Producción: https://api.isoterma.com (futuro)
```

### Endpoints Meteorológicos

#### 1. Clima Actual
```http
GET /api/v1/weather/current?latitude={lat}&longitude={lon}
```

**Parámetros Query:**
- `latitude` (float, required): Latitud (-90 a 90)
- `longitude` (float, required): Longitud (-180 a 180)

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "latitude": -39.164,
    "longitude": -67.035,
    "timezone": "America/Argentina/Buenos_Aires",
    "elevation": 200.0,
    "current": {
      "time": "2026-02-20T18:45",
      "temperature_2m": 32.9,
      "relative_humidity_2m": 19,
      "apparent_temperature": 30.4,
      "precipitation": 0.0,
      "rain": 0.0,
      "cloud_cover": 30,
      "pressure_msl": 1010.0,
      "wind_speed_10m": 10.5,
      "wind_direction_10m": 27,
      "wind_gusts_10m": 20.9
    }
  }
}
```

#### 2. Pronóstico Extendido
```http
GET /api/v1/weather/forecast?latitude={lat}&longitude={lon}&forecast_days={days}
```

**Parámetros Query:**
- `latitude` (float, required): Latitud
- `longitude` (float, required): Longitud
- `forecast_days` (int, optional): Días de pronóstico (1-7, default: 3)

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "current": { /* datos actuales */ },
    "hourly": {
      "time": ["2026-02-20T00:00", "2026-02-20T01:00", ...],  // 72 timestamps (3 días)
      "temperature_2m": [19.1, 18.5, 17.9, ...],                // 72 temperaturas
      "relative_humidity_2m": [57, 62, 64, ...],                // 72 humedades
      "precipitation_probability": [0, 0, 0, ...],              // 72 probabilidades
      "precipitation": [0.0, 0.0, 0.0, ...],                    // 72 precipitaciones
      "wind_speed_10m": [10.5, 11.2, 9.8, ...]                  // 72 velocidades viento
    }
  }
}
```

**Nota:** Con `forecast_days=3` se obtienen **72 valores horarios** (3 días × 24 horas)

#### 3. Validación de Sensor
```http
POST /api/v1/weather/validate
Content-Type: application/json
```

**Body:**
```json
{
  "latitude": -39.164,
  "longitude": -67.035,
  "measured_temperature": 18.5,
  "sensor_id": "S_001"
}
```

**Respuesta:**
```json
{
  "success": true,
  "sensor_id": "S_001",
  "validation": {
    "measured_temperature": 18.5,
    "api_temperature": 17.8,
    "difference": 0.7,
    "status": "OK",
    "message": "Sensor calibrated correctly"
  }
}
```

**Estados de Validación:**
- `OK`: Diferencia < 2°C (sensor calibrado)
- `WARNING`: Diferencia 2-5°C (revisar calibración)
- `ERROR`: Diferencia > 5°C (sensor descalibrado)

### Health Checks

#### Health Check
```http
GET /api/v1/health
```

#### Readiness Check
```http
GET /api/v1/health/ready
```

## 🌐 Fuentes de Datos

### Open-Meteo API (Principal)
- **URL**: https://api.open-meteo.com/v1/forecast
- **Licencia**: Gratuita, sin API key
- **Cobertura**: Global
- **Resolución**: 2-13km según región
- **Modelos**: GFS (NOAA), ICON (DWD), GEM (ECCC), ECMWF

**Precisión Típica:**
- 24 horas: ±1-2°C (muy confiable)
- 48 horas: ±2-3°C (confiable)
- 72 horas: ±3-5°C (menos confiable)
- 7+ días: ±5-10°C (tendencia general)

**Parámetros Disponibles:**
- Temperatura (aire, suelo a 4 profundidades)
- Humedad (aire, suelo a 5 profundidades)
- Precipitación y probabilidad
- Viento (velocidad, dirección, ráfagas)
- Presión atmosférica
- Evapotranspiración (ET0 FAO)
- Déficit de presión de vapor (VPD)
- Punto de rocío
- Cobertura de nubes
- Visibilidad

### APIs Futuras (Extensibles)
- WeatherAPI.com (1M llamadas/mes gratis)
- OpenWeatherMap (1000 llamadas/día gratis)
- INTA Argentina (datos agrometeorológicos)
- SMN Argentina (Servicio Meteorológico Nacional)

## 🛠️ Instalación y Ejecución

### Requisitos
- Python 3.11+
- pip
- Docker (opcional)

### Instalación Local

```bash
# Clonar repositorio
cd isoterma_backend

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python main.py
```

**Servidor corriendo en:**
- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

### Docker

```bash
# Build imagen
docker build -t isoterma-backend:latest .

# Run contenedor
docker run -d -p 8000:8000 --name isoterma-backend isoterma-backend:latest

# Ver logs
docker logs -f isoterma-backend

# Detener
docker stop isoterma-backend
```

### Docker Compose (Futuro)

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=info
    restart: unless-stopped
```

## ☸️ Kubernetes (Preparado)

El backend está preparado para despliegue en Kubernetes:

**Características K8s-ready:**
- Health checks configurados (`/api/v1/health`)
- Readiness probe (`/api/v1/health/ready`)
- Logs estructurados a stdout
- Variables de entorno
- Stateless (escalabilidad horizontal)
- Graceful shutdown

**Deployment ejemplo:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: isoterma-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: isoterma-backend
  template:
    metadata:
      labels:
        app: isoterma-backend
    spec:
      containers:
      - name: backend
        image: isoterma-backend:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/v1/health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

## 📊 Ejemplos de Uso

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Obtener clima actual
response = requests.get(
    f"{BASE_URL}/weather/current",
    params={
        "latitude": -39.164,
        "longitude": -67.035
    }
)
data = response.json()
print(f"Temperatura actual: {data['data']['current']['temperature_2m']}°C")

# 2. Obtener pronóstico 3 días
response = requests.get(
    f"{BASE_URL}/weather/forecast",
    params={
        "latitude": -39.164,
        "longitude": -67.035,
        "forecast_days": 3
    }
)
data = response.json()
temps = data['data']['hourly']['temperature_2m']
print(f"Pronóstico 72 horas: {len(temps)} valores")
print(f"Temp mín: {min(temps)}°C, máx: {max(temps)}°C")

# 3. Validar sensor
response = requests.post(
    f"{BASE_URL}/weather/validate",
    json={
        "latitude": -39.164,
        "longitude": -67.035,
        "measured_temperature": 18.5,
        "sensor_id": "S_001"
    }
)
data = response.json()
validation = data['validation']
print(f"Estado: {validation['status']}")
print(f"Diferencia: {validation['difference']}°C")
```

### cURL

```bash
# Clima actual
curl "http://localhost:8000/api/v1/weather/current?latitude=-39.164&longitude=-67.035"

# Pronóstico 5 días
curl "http://localhost:8000/api/v1/weather/forecast?latitude=-39.164&longitude=-67.035&forecast_days=5"

# Validar sensor
curl -X POST "http://localhost:8000/api/v1/weather/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -39.164,
    "longitude": -67.035,
    "measured_temperature": 18.5,
    "sensor_id": "S_001"
  }'
```

### JavaScript/Fetch

```javascript
// Clima actual
const response = await fetch(
  'http://localhost:8000/api/v1/weather/current?latitude=-39.164&longitude=-67.035'
);
const data = await response.json();
console.log('Temperatura:', data.data.current.temperature_2m);

// Validar sensor
const response = await fetch(
  'http://localhost:8000/api/v1/weather/validate',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      latitude: -39.164,
      longitude: -67.035,
      measured_temperature: 18.5,
      sensor_id: 'S_001'
    })
  }
);
const data = await response.json();
console.log('Validación:', data.validation.status);
```

## 🔧 Configuración

### Variables de Entorno (Futuro)

```bash
# .env
LOG_LEVEL=info
API_TIMEOUT=15
CORS_ORIGINS=*
OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast
```

## 📝 Dependencias

```txt
fastapi==0.104.1          # Framework web
uvicorn[standard]==0.24.0 # Servidor ASGI
pydantic==2.5.0           # Validación de datos
requests==2.31.0          # Cliente HTTP
python-dotenv==1.0.0      # Variables de entorno
```

## 🚦 Roadmap

### v1.0 (Actual)
- ✅ API clima actual
- ✅ API pronóstico extendido
- ✅ Validación de sensores
- ✅ Health checks
- ✅ Dockerización

### v1.1 (Próximo)
- ⏳ Múltiples fuentes de datos (WeatherAPI, OpenWeatherMap)
- ⏳ Cache de respuestas (Redis)
- ⏳ Rate limiting
- ⏳ Autenticación JWT

### v2.0 (Futuro)
- ⏳ Base de datos histórica (PostgreSQL)
- ⏳ Análisis de tendencias
- ⏳ Alertas automáticas
- ⏳ WebSockets para datos en tiempo real
- ⏳ Integración con sensores IoT

## 📄 Licencia

MIT License

## 👥 Contacto

Proyecto: Isoterma - Análisis térmico para agricultura de precisión  
Repositorio: https://github.com/chewydc/isotherm-exploration