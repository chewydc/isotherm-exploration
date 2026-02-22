<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	export let sensors: any[] = [];
	export let center: { latitude: number; longitude: number };

	$: if (map && center) {
		map.setView([center.latitude, center.longitude], 14);
	}

	$: if (map && sensors && L) {
		updateSensorsAndHeatmap();
	}

	let mapContainer: HTMLDivElement;
	let map: any;
	let L: any;
	let heatLayer: any;
	let markersLayer: any;
	let showHeatmap = true;
	let streetMap: any;
	let satellite: any;
	let currentLayer: 'street' | 'satellite' = 'satellite';
	let tileErrorCount = 0;
	let lastZoomCheck = 0;

	onMount(async () => {
		if (!browser) return;

		L = await import('leaflet');
		
		// Cargar leaflet.heat desde CDN y esperar a que esté disponible
		await new Promise((resolve, reject) => {
			const script = document.createElement('script');
			script.src = 'https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js';
			script.onload = () => {
				setTimeout(() => {
					if ((window as any).L && (window as any).L.heatLayer) {
						// Parchear leaflet-heat para usar willReadFrequently
						const originalHeatLayer = (window as any).L.heatLayer;
						(window as any).L.heatLayer = function(...args: any[]) {
							const layer = originalHeatLayer.apply(this, args);
							if (layer._canvas) {
								const ctx = layer._canvas.getContext('2d', { willReadFrequently: true });
							}
							return layer;
						};
						resolve(true);
					} else {
						reject(new Error('heatLayer not available'));
					}
				}, 100);
			};
			script.onerror = reject;
			document.head.appendChild(script);
		});
		
		map = L.map(mapContainer).setView([center.latitude, center.longitude], 14);

		// Definir capas base
		streetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '© OpenStreetMap',
			minZoom: 1,
			maxZoom: 19
		});

		// Usar Google Satellite como fallback - mejor cobertura global
		satellite = L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
			attribution: '© Google',
			minZoom: 1,
			maxZoom: 20,
			subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
		});

		// Agregar capa por defecto (satélite)
		satellite.addTo(map);
		currentLayer = 'satellite';

		// Control de capas
		const baseMaps = {
			'🗺️ Calles': streetMap,
			'🛰️ Satélite': satellite
		};

		L.control.layers(baseMaps, null, { position: 'topright' }).addTo(map);

		// Listener para cambios manuales de capa
		map.on('baselayerchange', (e: any) => {
			if (e.name === '🗺️ Calles') {
				currentLayer = 'street';
			} else if (e.name === '🛰️ Satélite') {
				currentLayer = 'satellite';
			}
		});

		// Crear capa de marcadores
		markersLayer = L.layerGroup();
		sensors.forEach((sensor) => {
			const color = sensor.status === 'active' ? 'green' : sensor.status === 'warning' ? 'orange' : 'red';
			
			L.circleMarker([sensor.latitude, sensor.longitude], {
				radius: 6,
				fillColor: color,
				color: '#fff',
				weight: 2,
				opacity: 1,
				fillOpacity: 0.8
			})
			.bindPopup(`<b>Sensor ${sensor.id}</b><br>Estado: ${sensor.status}<br>Temp: ${sensor.temperature?.toFixed(1) || 'N/A'}°C`)
			.addTo(markersLayer);
		});

		// Crear capa de heatmap con temperaturas reales
		// Normalizar temperaturas para el heatmap (0-1)
		const temps = sensors.map(s => s.temperature || 18).filter(t => t);
		const minTemp = Math.min(...temps);
		const maxTemp = Math.max(...temps);
		const tempRange = maxTemp - minTemp || 1;

		const heatData = sensors.map((sensor) => [
			sensor.latitude,
			sensor.longitude,
			(sensor.temperature - minTemp) / tempRange // Normalizar entre 0 y 1
		]);

		// Usar window.L para acceder a heatLayer
		const WindowL = window as any;
		if (WindowL.L && WindowL.L.heatLayer) {
			heatLayer = WindowL.L.heatLayer(heatData, {
				radius: 80,
				blur: 60,
				max: 1.0,
				maxZoom: 18,
				minOpacity: 0.6,
				gradient: {
					0.0: '#0000ff',
					0.25: '#00ffff',
					0.5: '#00ff00',
					0.75: '#ffff00',
					1.0: '#ff0000'
				}
			});
		}

		updateLayers();
	});

	function updateSensorsAndHeatmap() {
		if (!map || !sensors || !L) return;
		
		// Limpiar capas existentes
		if (markersLayer) map.removeLayer(markersLayer);
		if (heatLayer) map.removeLayer(heatLayer);

		// Recrear marcadores
		markersLayer = L.layerGroup();
		sensors.forEach((sensor) => {
			const color = sensor.status === 'active' ? 'green' : sensor.status === 'warning' ? 'orange' : 'red';
			L.circleMarker([sensor.latitude, sensor.longitude], {
				radius: 6,
				fillColor: color,
				color: '#fff',
				weight: 2,
				opacity: 1,
				fillOpacity: 0.8
			})
			.bindPopup(`<b>Sensor ${sensor.id}</b><br>Estado: ${sensor.status}<br>Temp: ${sensor.temperature?.toFixed(1) || 'N/A'}°C`)
			.addTo(markersLayer);
		});

		// Recrear heatmap
		const temps = sensors.map(s => s.temperature || 18).filter(t => t);
		const minTemp = Math.min(...temps);
		const maxTemp = Math.max(...temps);
		const tempRange = maxTemp - minTemp || 1;
		const heatData = sensors.map((sensor) => [
			sensor.latitude,
			sensor.longitude,
			(sensor.temperature - minTemp) / tempRange
		]);

		const WindowL = window as any;
		if (WindowL.L && WindowL.L.heatLayer) {
			heatLayer = WindowL.L.heatLayer(heatData, {
				radius: 80,
				blur: 60,
				max: 1.0,
				maxZoom: 18,
				minOpacity: 0.6,
				gradient: {
					0.0: '#0000ff',
					0.25: '#00ffff',
					0.5: '#00ff00',
					0.75: '#ffff00',
					1.0: '#ff0000'
				}
			});
		}

		updateLayers();
	}

	function updateLayers() {
		if (!map) return;
		
		if (showHeatmap) {
			if (heatLayer && !map.hasLayer(heatLayer)) {
				heatLayer.addTo(map);
			}
			if (markersLayer && map.hasLayer(markersLayer)) {
				map.removeLayer(markersLayer);
			}
		} else {
			if (heatLayer && map.hasLayer(heatLayer)) {
				map.removeLayer(heatLayer);
			}
			if (markersLayer && !map.hasLayer(markersLayer)) {
				markersLayer.addTo(map);
			}
		}
	}

	function toggleView() {
		showHeatmap = !showHeatmap;
		updateLayers();
	}

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
</svelte:head>

<div class="relative w-full h-full">
	<div bind:this={mapContainer} class="w-full h-full" />
	
	<button
		on:click={toggleView}
		class="absolute bottom-6 left-6 z-[1000] px-4 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg shadow-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-medium"
	>
		{showHeatmap ? '📍 Ver Sensores' : '🔥 Ver Mapa de Calor'}
	</button>
</div>

<style>
	:global(.leaflet-container) {
		height: 100%;
		width: 100%;
	}
	/* Suprimir warning de canvas en consola - es solo informativo */
</style>

<svelte:options immutable={false} />
