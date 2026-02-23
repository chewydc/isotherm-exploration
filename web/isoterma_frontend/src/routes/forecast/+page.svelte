<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { selectedFarm } from '$lib/stores/farms';
	import { api } from '$lib/api/client';
	import AdvancedForecastChart from '$lib/components/AdvancedForecastChart.svelte';

	let forecast: any = null;
	let loading = false;
	let farmData: any = null;

	$: if ($selectedFarm?.id) {
		loadFarmData();
		loadForecast();
	}

	afterNavigate(() => {
		if ($selectedFarm?.id) {
			loadFarmData();
			loadForecast();
		}
	});

	async function loadFarmData() {
		if (!$selectedFarm?.id) return;
		try {
			const response = await api.getFarm($selectedFarm.id);
			farmData = response.farm || response.data;
		} catch (error) {
			console.error('Error loading farm data:', error);
		}
	}

	async function loadForecast() {
		if (!$selectedFarm?.location) return;
		
		loading = true;
		try {
			const data = await api.getForecast(
				$selectedFarm.location.latitude,
				$selectedFarm.location.longitude,
				3
			);
			forecast = data.data;
		} catch (error) {
			console.error('Error loading forecast:', error);
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Pronóstico - Isoterma</title>
</svelte:head>

<div class="p-6">
	<h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Pronóstico 72 Horas</h2>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
		</div>
	{:else if forecast}
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Condiciones Actuales</h3>
				<div class="space-y-3">
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Temperatura:</span>
						<span class="font-semibold text-gray-900 dark:text-white">{forecast.current.temperature_2m}°C</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Humedad:</span>
						<span class="font-semibold text-gray-900 dark:text-white">{forecast.current.relative_humidity_2m}%</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Viento:</span>
						<span class="font-semibold text-gray-900 dark:text-white">{forecast.current.wind_speed_10m} km/h</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Precipitación:</span>
						<span class="font-semibold text-gray-900 dark:text-white">{forecast.current.precipitation} mm</span>
					</div>
				</div>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Resumen 72h</h3>
				<div class="space-y-3">
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Temp. Mínima:</span>
						<span class="font-semibold text-blue-600 dark:text-blue-400">
							{Math.min(...forecast.hourly.temperature_2m).toFixed(1)}°C
						</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Temp. Máxima:</span>
						<span class="font-semibold text-red-600 dark:text-red-400">
							{Math.max(...forecast.hourly.temperature_2m).toFixed(1)}°C
						</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-600 dark:text-gray-400">Precipitación Total:</span>
						<span class="font-semibold text-gray-900 dark:text-white">
							{forecast.hourly.precipitation.reduce((a, b) => a + b, 0).toFixed(1)} mm
						</span>
					</div>
				</div>
			</div>
		</div>

		<div class="mt-6">
			<h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">📊 Análisis Meteorológico 72 Horas</h3>
			<AdvancedForecastChart {forecast} thresholds={farmData?.settings} />
		</div>

		<div class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Próximas 24 Horas</h3>
			<div class="overflow-x-auto">
				<div class="flex gap-4 pb-4">
					{#each forecast.hourly.time.slice(0, 24) as time, i}
						<div class="flex-shrink-0 text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg min-w-[100px]">
							<p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
								{new Date(time).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}
							</p>
							<p class="text-2xl font-bold text-gray-900 dark:text-white mb-1">
								{forecast.hourly.temperature_2m[i].toFixed(0)}°
							</p>
							<p class="text-xs text-gray-600 dark:text-gray-400">
								{forecast.hourly.precipitation[i]} mm
							</p>
						</div>
					{/each}
				</div>
			</div>
		</div>
	{:else}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">No hay datos de pronóstico disponibles</p>
		</div>
	{/if}
</div>
