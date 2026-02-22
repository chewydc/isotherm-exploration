<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { selectedFarm } from '$lib/stores/farms';
	import { api } from '$lib/api/client';

	let weatherData: any = null;
	let alerts: any[] = [];
	let loading = false;
	let loadingAlerts = false;
	let lastFarmId: string | null = null;

	$: if ($selectedFarm && $selectedFarm.id !== lastFarmId) {
		lastFarmId = $selectedFarm.id;
		loadWeatherData();
		loadAlerts();
	}

	afterNavigate(() => {
		if ($selectedFarm) {
			loadWeatherData();
			loadAlerts();
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

	async function loadAlerts() {
		if (!$selectedFarm) return;
		
		loadingAlerts = true;
		try {
			const response = await api.getFarmAlerts($selectedFarm.id);
			alerts = response.data || [];
		} catch (error) {
			console.error('Error loading alerts:', error);
			alerts = [];
		} finally {
			loadingAlerts = false;
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
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 relative">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Finca</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">{$selectedFarm.name}</p>
				<a 
					href="/farm/{$selectedFarm.id}/settings" 
					class="absolute bottom-4 right-4 bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-md text-sm font-medium transition-colors"
				>
					⚙️ Configurar
				</a>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Sensores</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
					{$selectedFarm.sensors?.length || 0}
				</p>
				<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
					{alerts.length} alertas activas
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Área</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
					{$selectedFarm.area_hectares} ha
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Umbrales</h3>
				{#if $selectedFarm.settings}
					<p class="text-lg font-bold text-gray-900 dark:text-white mt-2">
						{$selectedFarm.settings.temperature_threshold_min}°C - {$selectedFarm.settings.temperature_threshold_max}°C
					</p>
					<p class="text-xs {$selectedFarm.settings.alerts_enabled ? 'text-green-600' : 'text-red-600'} mt-1">
						{$selectedFarm.settings.alerts_enabled ? '✅ Alertas activas' : '❌ Alertas desactivadas'}
					</p>
				{:else}
					<p class="text-lg text-gray-500 dark:text-gray-400 mt-2">No configurado</p>
				{/if}
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
			<!-- Alertas Activas -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<div class="flex justify-between items-center mb-4">
					<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Alertas Activas</h3>
					<button
						on:click={loadAlerts}
						class="text-blue-600 hover:text-blue-800 text-sm"
						disabled={loadingAlerts}
					>
						{loadingAlerts ? '⏳' : '🔄'}
					</button>
				</div>
				
				{#if loadingAlerts}
					<div class="text-center py-4">
						<div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto"></div>
					</div>
				{:else if alerts.length === 0}
					<div class="text-center text-gray-500 py-4">
						<div class="text-3xl mb-2">✅</div>
						<p class="text-sm">Sin alertas</p>
					</div>
				{:else}
					<div class="space-y-2 max-h-48 overflow-y-auto">
						{#each alerts as alert}
							<div class="border-l-4 border-yellow-400 bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded">
								<div class="flex items-start">
									<div class="text-yellow-600 mr-2">⚠️</div>
									<div class="flex-1">
										<p class="font-medium text-yellow-800 dark:text-yellow-200 text-sm">
											{alert.sensor_id}
										</p>
										<p class="text-xs text-yellow-700 dark:text-yellow-300">
											{alert.temperature}°C
										</p>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<!-- Información de la Finca -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Información de la Finca</h3>
				<div class="space-y-2 text-gray-700 dark:text-gray-300">
					<p><strong>Ubicación:</strong> {$selectedFarm.location.address}</p>
					<p><strong>Región:</strong> {$selectedFarm.location.region}</p>
					<p><strong>Coordenadas:</strong> {$selectedFarm.location.latitude.toFixed(4)}, {$selectedFarm.location.longitude.toFixed(4)}</p>
					<p><strong>Cultivos:</strong> {$selectedFarm.crops?.join(', ') || 'N/A'}</p>
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
