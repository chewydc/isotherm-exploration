# Finca Río Negro Altitude - Sensores Multinivel

## Descripción
Visualización de sensores cada ~88m en finca de Río Negro con datos de temperatura a múltiples alturas (1m, 2m, 5m, 10m) y altitud real del terreno.

![Ejemplo de salida](img/corrida_01.png)

## Instalación (RECOMENDADA)
```bash
instalar_final.bat
```

## Instalación Manual
```bash
# 1. Crear entorno virtual
python -m venv env

# 2. Activar entorno
env\Scripts\activate

# 3. Instalar dependencias
pip install pandas numpy keplergl==0.2.2 requests
```

## Uso
```bash
# 1. Ejecutar instalador
instalar_final.bat

# 2. Activar entorno
env\Scripts\activate

# 3. Ejecutar script
python finca_altitude.py

# 4. Abrir archivo HTML generado
finca_altitude_mapa.html
```

## Archivos Generados
- `finca_altitude_mapa.html` - Mapa interactivo con 5 capas
- `finca_altitude_datos.csv` - Datos completos de sensores

## Características del Mapa
- **5 capas intercambiables:**
  - Temperatura a 1m (visible por defecto)
  - Temperatura a 2m, 5m, 10m (ocultas)
  - Altitud del terreno (oculta)
- **Cuadrícula uniforme** cada ~88m dentro del polígono
- **Vista satelital** con escala de colores térmica
- **Panel de capas** para alternar entre niveles

## API de Altitud
**Open-Elevation API** (https://api.open-elevation.com)
- ✅ **Completamente gratuita** - Sin API key
- ✅ **Sin límites oficiales** de rate limit
- ✅ **Código abierto** - Datos SRTM/ASTER
- ✅ **Altitud real** sobre nivel del mar (msnm)
- ⚠️ **Servidor compartido** - Puede ser lento
- ⚠️ **Sin garantías uptime** - Servicio comunitario

**Fallback:** Si la API falla, usa 280m (altitud típica de Río Negro)

## Datos por Sensor
- Coordenadas GPS exactas
- Altitud real del terreno (msnm)
- Temperatura simulada a 1m, 2m, 5m y 10m
- Temperatura promedio de los 4 niveles
- ID único por sensor

## Coordenadas de la Finca
- NOROESTE: -39.163552, -67.037345
- NORESTE: -39.164707, -67.028948  
- SURESTE: -39.169029, -67.030009
- SUROESTE: -39.167885, -67.038406

## Tiempo de Ejecución
~2 segundos por sensor (consulta API + pausa)
Total estimado mostrado al inicio del script