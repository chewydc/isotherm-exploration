<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { selectedFarm } from '$lib/stores/farms';
	import { api } from '$lib/api/client';

	let weatherData: any = null;
	let loading = false;
	let lastFarmId: string | null = null;

	$: if ($selectedFarm && $selectedFarm.id !== lastFarmId) {
		lastFarmId = $selectedFarm.id;
		loadWeatherData();
	}

	afterNavigate(() => {
		if ($selectedFarm) {
			loadWeatherData();
		}
	});

	async function loadWeatherData() {
		if (!$selectedFarm) return;
		
		loading = true;
		try {
			const data = await api.getCurrentWeather(
				$selectedFarm.location.latitude,
				$selectedFarm.location.longitude
			);
			weatherData = data.data;
		} catch (error) {
			console.error('Error loading weather:', error);
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Dashboard - Isoterma</title>
</svelte:head>

<div class="p-6">
	<h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Dashboard</h2>

	{#if $selectedFarm}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Finca</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">{$selectedFarm.name}</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Sensores</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
					{$selectedFarm.sensors?.length || 0}
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Área</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
					{$selectedFarm.area_hectares} ha
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Cultivo</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
					{$selectedFarm.crops?.join(', ') || 'N/A'}
				</p>
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Información de la Finca</h3>
				<div class="space-y-2 text-gray-700 dark:text-gray-300">
					<p><strong>Ubicación:</strong> {$selectedFarm.location.address}</p>
					<p><strong>Región:</strong> {$selectedFarm.location.region}</p>
					<p><strong>Coordenadas:</strong> {$selectedFarm.location.latitude.toFixed(4)}, {$selectedFarm.location.longitude.toFixed(4)}</p>
					<p><strong>Propietario:</strong> {$selectedFarm.owner}</p>
					<p><strong>Fecha de creación:</strong> {new Date($selectedFarm.created_at).toLocaleDateString('es-AR')}</p>
				</div>
			</div>

			{#if loading}
				<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 flex items-center justify-center">
					<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
				</div>
			{:else if weatherData}
				<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
					<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Clima Actual</h3>
					<div class="space-y-3">
						<div class="flex justify-between items-center">
							<span class="text-gray-600 dark:text-gray-400">Temperatura:</span>
							<span class="text-3xl font-bold text-gray-900 dark:text-white">{weatherData.current.temperature_2m}°C</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-600 dark:text-gray-400">Sensación térmica:</span>
							<span class="font-semibold text-gray-900 dark:text-white">{weatherData.current.apparent_temperature}°C</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-600 dark:text-gray-400">Humedad:</span>
							<span class="font-semibold text-gray-900 dark:text-white">{weatherData.current.relative_humidity_2m}%</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-600 dark:text-gray-400">Viento:</span>
							<span class="font-semibold text-gray-900 dark:text-white">{weatherData.current.wind_speed_10m} km/h</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-600 dark:text-gray-400">Precipitación:</span>
							<span class="font-semibold text-gray-900 dark:text-white">{weatherData.current.precipitation} mm</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-600 dark:text-gray-400">Presión:</span>
							<span class="font-semibold text-gray-900 dark:text-white">{weatherData.current.pressure_msl} hPa</span>
						</div>
					</div>
				</div>
			{/if}
		</div>
	{:else}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">Cargando datos...</p>
		</div>
	{/if}
</div>
