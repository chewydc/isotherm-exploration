# Isoterma Frontend - SvelteKit + Kepler.gl

Frontend web para visualización de isotermas agrícolas con Kepler.gl embebido.

## 🎯 Stack Tecnológico

- **SvelteKit** - Framework web moderno
- **TypeScript** - Type-safety
- **TailwindCSS** - Styling
- **Kepler.gl** - Visualización geoespacial (embebido vía React)
- **React/Redux** - Requerido por Kepler.gl

## 🚀 Instalación

### Requisitos
- Node.js 18+
- npm o pnpm

### Pasos

```bash
# 1. Instalar dependencias
npm install

# 2. Ejecutar en desarrollo
npm run dev

# 3. Abrir navegador
# http://localhost:3000
```

## 📁 Estructura

```
src/
├── routes/
│   ├── +layout.svelte          # Layout con sidebar
│   ├── +page.svelte            # Dashboard principal
│   ├── mapa/+page.svelte       # Mapa Kepler.gl con isotermas
│   ├── sensores/+page.svelte   # Lista de sensores
│   └── forecast/+page.svelte   # Pronóstico meteorológico
├── lib/
│   ├── components/
│   │   ├── KeplerMap.svelte    # ⭐ Wrapper de Kepler.gl
│   │   ├── Sidebar.svelte
│   │   ├── FarmSelector.svelte
│   │   └── ThemeToggle.svelte
│   ├── stores/
│   │   ├── theme.ts            # Store de tema dark/light
│   │   └── farms.ts            # Store de fincas
│   ├── api/
│   │   └── client.ts           # Cliente API backend
│   └── utils/
│       └── keplerConfig.ts     # Configuración Kepler.gl
└── app.css                     # Estilos globales
```

## 🗺️ Kepler.gl Integration

### Características

✅ **4 Capas de Temperatura** (1m, 2m, 5m, 10m)  
✅ **Heatmaps** con colores personalizados  
✅ **Vista Satelital** de alta resolución  
✅ **Capas Intercambiables** para análisis  
✅ **Tooltips** con información de sensores  
✅ **Zoom y Navegación** fluida  

### Componente KeplerMap.svelte

El componente `KeplerMap.svelte` es el wrapper que permite usar Kepler.gl (React) dentro de Svelte:

```svelte
<script>
  import KeplerMap from '$lib/components/KeplerMap.svelte';
  import { createKeplerConfig } from '$lib/utils/keplerConfig';

  const data = {
    fields: [
      { name: 'latitude', type: 'real' },
      { name: 'longitude', type: 'real' },
      { name: 'temp_1m', type: 'real' }
    ],
    rows: [
      [-39.164, -67.035, 18.5],
      [-39.165, -67.036, 19.2]
    ]
  };

  const config = createKeplerConfig('sensores');
</script>

<KeplerMap {data} {config} />
```

## 🎨 Temas

La aplicación soporta tema claro y oscuro:

- Toggle en esquina superior derecha
- Persistencia en localStorage
- CSS variables para personalización

## 🔌 API Backend

El frontend consume el backend FastAPI:

```typescript
// src/lib/api/client.ts
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Endpoints disponibles:
- GET /farms              // Lista de fincas
- GET /farms/{id}         // Detalle de finca
- GET /weather/current    // Clima actual
- GET /weather/forecast   // Pronóstico 72h
```

## 📊 Páginas

### 1. Dashboard (/)
- Resumen de finca seleccionada
- Métricas principales (sensores, área, cultivo)
- Información general

### 2. Mapa Isotermas (/mapa)
- **Kepler.gl embebido** con datos de sensores
- 4 capas de temperatura intercambiables
- Heatmaps con gradientes de color
- Vista satelital

### 3. Sensores (/sensores)
- Tabla con todos los sensores
- Estado (active, warning, error)
- Ubicación GPS
- Última lectura

### 4. Pronóstico (/forecast)
- Condiciones actuales
- Pronóstico 72 horas
- Gráfico de próximas 24 horas
- Temperaturas min/max

## 🛠️ Desarrollo

### Comandos

```bash
# Desarrollo
npm run dev

# Build producción
npm run build

# Preview build
npm run preview

# Type checking
npm run check
```

### Hot Reload

SvelteKit tiene HMR (Hot Module Replacement) automático. Los cambios se reflejan instantáneamente.

## 🚢 Producción

### Build

```bash
npm run build
```

Genera carpeta `build/` con archivos estáticos.

### Deploy

Compatible con:
- **Vercel** (recomendado para SvelteKit)
- **Netlify**
- **AWS S3 + CloudFront**
- **Docker** (nginx)

### Variables de Entorno

Crear `.env`:

```bash
PUBLIC_API_URL=https://api.isoterma.com/api/v1
```

## 🔧 Configuración Kepler.gl

Archivo `src/lib/utils/keplerConfig.ts` contiene la configuración de capas:

```typescript
export const createKeplerConfig = (dataId: string) => ({
  config: {
    visState: {
      layers: [
        {
          type: 'heatmap',
          config: {
            dataId,
            label: 'Temperatura 1m',
            visConfig: {
              radius: 150,
              colorRange: { /* colores */ }
            }
          }
        }
      ]
    }
  }
});
```

## 📝 Notas Técnicas

### Kepler.gl + Svelte

Kepler.gl es un componente React, pero funciona en Svelte mediante:

1. Importación dinámica (`await import()`)
2. Renderizado con `ReactDOM.createRoot()`
3. Store de Redux para estado
4. Wrapper Svelte que maneja lifecycle

### Performance

- Kepler.gl maneja miles de puntos eficientemente
- Heatmaps se recalculan en GPU (WebGL)
- SvelteKit hace code-splitting automático

## 🐛 Troubleshooting

### Error: "Cannot find module 'kepler.gl'"

```bash
npm install kepler.gl react react-dom react-redux redux
```

### Mapa no se renderiza

Verificar que el backend esté corriendo en `http://localhost:8000`

### Tema no persiste

Limpiar localStorage:

```javascript
localStorage.clear();
```

## 📚 Recursos

- [SvelteKit Docs](https://kit.svelte.dev/)
- [Kepler.gl Docs](https://docs.kepler.gl/)
- [TailwindCSS Docs](https://tailwindcss.com/)

---

**Desarrollado para monitoreo agrícola de precisión** 🌾🇦🇷
