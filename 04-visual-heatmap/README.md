# Heatmap 3D Multicapa - Visualización Térmica Continua

Visualización avanzada de isotermas usando heatmaps 3D con relieve del terreno real para análisis térmico agrícola en Río Negro, Argentina.

## 🔥 Características Principales

### Heatmap Continuo Multicapa
- **4 capas intercambiables**: Temperatura a 1m, 2m, 5m y 10m de altura
- **Superficie continua**: Interpolación suave entre 80 sensores
- **Relieve 3D**: Elevación real del terreno vía API Open-Elevation
- **Islas térmicas**: Zonas calientes y frías distribuidas realísticamente

### Visualización Adaptativa por Zoom
El heatmap se adapta dinámicamente al nivel de zoom, mostrando diferentes niveles de detalle:

#### Vista Aérea (Zoom Bajo)
![Corrida 00 - Vista Aérea](img/Corrida_00.png)
**Zoom bajo**: Superficie térmica continua y suave, ideal para análisis de patrones generales

#### Vista Intermedia 
![Corrida 01 - Vista Intermedia](img/Corrida_01.png)
**Zoom medio**: Mayor definición de islas térmicas, transiciones más marcadas

#### Vista Detallada (Zoom Alto)
![Corrida 02 - Vista Detallada](img/Corrida_02.png)
**Zoom alto**: Máximo detalle, se pueden distinguir sensores individuales y gradientes locales

## 🚀 Uso Rápido

1. **Instalar dependencias:**
   ```bash
   instalar_final.bat
   ```

2. **Activar entorno:**
   ```bash
   env\Scripts\activate
   ```

3. **Ejecutar:**
   ```bash
   python heatmap_3d_final.py
   ```

4. **Abrir mapa:**
   ```bash
   # Se genera: heatmap_3d_final.html
   ```

## 📊 Datos Generados

### Sensores
- **80 puntos** distribuidos en cuadrícula de ~88m
- **Coordenadas GPS** exactas de la finca
- **Altitud real** consultada vía API

### Temperaturas
- **4 niveles de altura**: 1m, 2m, 5m, 10m
- **Centros térmicos**: Zonas calientes y frías por nivel
- **Gradiente vertical**: Temperaturas decrecientes con altura
- **Variación realista**: 6-18°C con ruido natural

## 🎛️ Controles del Mapa

### Capas Intercambiables
- **Heatmap 1m altura**: Temperatura a nivel del suelo
- **Heatmap 2m altura**: Temperatura a altura de cultivos
- **Heatmap 5m altura**: Temperatura de dosel arbóreo
- **Heatmap 10m altura**: Temperatura atmosférica

### Vista 3D
- **Pitch 45°**: Vista oblicua para apreciar relieve
- **Relieve del terreno**: Elevación real escalada
- **Navegación 3D**: Rotación y zoom libre

## 🌡️ Análisis Térmico

### Patrones Identificables
- **Islas de calor**: Zonas de mayor temperatura
- **Corredores fríos**: Áreas de menor temperatura
- **Gradientes altitudinales**: Variación con la elevación
- **Microclimas**: Variaciones locales por topografía

### Aplicaciones Agrícolas
- **Zonificación térmica** para selección de cultivos
- **Identificación de microclimas** favorables
- **Planificación de riego** según demanda térmica
- **Monitoreo de estrés térmico** en cultivos

## 🔧 Configuración Técnica

### Heatmap
- **Radio**: 150px para cobertura continua
- **Interpolación**: Algoritmo de Kepler.gl nativo
- **Colores**: Espectro azul→rojo (frío→caliente)
- **Opacidad**: 80% para ver terreno subyacente

### Relieve 3D
- **Escala de elevación**: 0.1 (sutil pero visible)
- **Campo de altura**: `altitude_terrain`
- **Rango altitudinal**: 270-290m sobre nivel del mar

## 📁 Archivos Generados

- `heatmap_3d_final.html` - Mapa interactivo
- `heatmap_3d_final.csv` - Datos de sensores
- Logs de consulta API de altitud

---

**Caso 04 - Heatmap 3D Multicapa**  
*Visualización térmica continua con relieve real*