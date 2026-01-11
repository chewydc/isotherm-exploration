# Isotherm Exploration - Kepler.gl Examples

Exploración de isotermas y visualización de datos geoespaciales usando Kepler.gl para análisis agrícola en Argentina.

## 📁 Casos de Estudio

### [01-tiny-example](01-tiny-example/)
**Ejemplo básico de Kepler.gl**
- 20 puntos de temperatura en Madrid
- Introducción a Kepler.gl
- Configuración simple
- Ideal para aprender los conceptos básicos

### [02-finca-rio-negro](02-finca-rio-negro/)
**Chacra 143 - Cuadrícula básica**
- Finca real en Río Negro, Argentina
- Cuadrícula cada 100m dentro de polígono
- 4 esquinas exactas + sensores internos
- Datos de temperatura simulados

### [03-finca-rio-negro-altitude](03-finca-rio-negro-altitude/)
**Sensores multinivel con altitud real** ⭐
- Misma finca que caso 02
- **5 capas intercambiables:**
  - Temperatura a 1m, 2m, 5m, 10m
  - Altitud del terreno
- **Altitud real** vía API Open-Elevation
- **Vista 3D** con elevaciones proporcionales
- Cuadrícula cada ~88m

## 🛠️ Tecnologías

- **Kepler.gl** - Visualización geoespacial interactiva
- **Python** - Procesamiento de datos
- **Pandas** - Manipulación de datos
- **Open-Elevation API** - Altitudes reales
- **Jupyter** - Desarrollo interactivo

## 🚀 Inicio Rápido

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/chewydc/isotherm-exploration.git
   cd isotherm-exploration
   ```

2. **Elegir caso de estudio:**
   ```bash
   cd 03-finca-rio-negro-altitude  # Recomendado
   ```

3. **Instalar dependencias:**
   ```bash
   instalar_final.bat
   ```

4. **Ejecutar:**
   ```bash
   env\Scripts\activate
   python finca_altitude.py
   ```

5. **Abrir mapa:**
   ```bash
   # Abrir archivo HTML generado en navegador
   ```

## 📊 Características Principales

### Visualización Interactiva
- **Mapas de calor** por temperatura
- **Vista satelital** de alta resolución
- **Capas intercambiables** para análisis comparativo
- **Zoom y navegación** fluida

### Datos Geoespaciales
- **Coordenadas GPS** exactas
- **Altitudes reales** sobre nivel del mar
- **Cuadrículas precisas** cada 50-100m
- **Polígonos irregulares** respetados

### Análisis Multinivel
- **Temperaturas estratificadas** (1m, 2m, 5m, 10m)
- **Visualización 3D** con elevaciones
- **Comparación entre capas** atmosféricas
- **Datos exportables** en CSV

## 🌍 Casos de Uso

- **Agricultura de precisión**
- **Monitoreo ambiental**
- **Análisis climático**
- **Investigación agronómica**
- **Planificación de cultivos**

## 📈 Progresión de Complejidad

1. **Básico** → Puntos simples en mapa
2. **Intermedio** → Cuadrícula en polígono real
3. **Avanzado** → Múltiples capas con altitud 3D

## 🔧 Requisitos

- Python 3.8+
- Conexión a internet (para API de altitud)
- Navegador web moderno
- ~2GB espacio libre

## 📝 Licencia

MIT License - Ver cada carpeta para detalles específicos.

---

**Desarrollado para exploración de isotermas en fincas argentinas** 🇦🇷