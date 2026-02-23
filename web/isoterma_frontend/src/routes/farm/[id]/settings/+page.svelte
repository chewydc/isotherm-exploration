<script>
	import { page } from '$app/stores';
	import { api } from '$lib/api/client';
	import { onMount } from 'svelte';

	let farm = null;
	let settings = {
		temperature_threshold_min: 16.0,
		temperature_threshold_max: 25.0,
		alerts_enabled: true,
		forecast_alert_hours: 24
	};
	let loading = false;
	let saving = false;
	let saveMessage = '';

	$: farmId = $page.params.id;
	$: if (farmId) {
		loadFarm();
	}

	async function loadFarm() {
		try {
			loading = true;
			const response = await api.getFarm(farmId);
			farm = response.farm;
			if (farm.settings) {
				settings = { ...settings, ...farm.settings };
			}
		} catch (error) {
			console.error('Error loading farm:', error);
		} finally {
			loading = false;
		}
	}

	async function saveSettings() {
		try {
			saving = true;
			saveMessage = '';
			const response = await api.updateFarmSettings(farmId, settings);
			
			if (response.success) {
				saveMessage = '✅ Configuración guardada correctamente';
				setTimeout(() => saveMessage = '', 3000);
			} else {
				saveMessage = '❌ Error al guardar configuración';
			}
		} catch (error) {
			console.error('Error saving settings:', error);
			saveMessage = '❌ Error al guardar configuración';
		} finally {
			saving = false;
		}
	}
</script>

<div class="container mx-auto p-6">
	<div class="mb-6 flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-2">Gestión de Finca</h1>
			{#if farm}
				<h2 class="text-xl text-gray-600 dark:text-gray-300">{farm.name}</h2>
			{/if}
		</div>
		<a 
			href="/" 
			class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
		>
			← Volver al Dashboard
		</a>
	</div>

	{#if loading}
		<div class="text-center text-gray-900 dark:text-white">Cargando...</div>
	{:else if farm}
		<!-- Configuración de Umbrales -->
		<div class="max-w-2xl mx-auto">
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
				<h3 class="text-lg font-semibold mb-6 text-gray-900 dark:text-white">Configuración de Umbrales de Temperatura</h3>
				
				{#if saveMessage}
					<div class="mb-4 p-3 rounded-md {saveMessage.includes('✅') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
						{saveMessage}
					</div>
				{/if}

				<div class="space-y-6">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
								Temperatura Mínima (°C)
							</label>
							<input
								type="number"
								step="0.1"
								bind:value={settings.temperature_threshold_min}
								class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
							/>
						</div>

						<div>
							<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
								Temperatura Máxima (°C)
							</label>
							<input
								type="number"
								step="0.1"
								bind:value={settings.temperature_threshold_max}
								class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
							/>
						</div>
					</div>

					<div class="flex items-center">
						<input
							type="checkbox"
							bind:checked={settings.alerts_enabled}
							class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
						/>
						<label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
							Activar alertas automáticas
						</label>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
							Pronóstico de Alertas
						</label>
						<select
							bind:value={settings.forecast_alert_hours}
							class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
						>
							<option value={24}>24 horas</option>
							<option value={48}>48 horas</option>
							<option value={72}>72 horas</option>
						</select>
						<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
							Tiempo de anticipación para alertas de pronóstico
						</p>
					</div>

					<div class="pt-4">
						<button
							on:click={saveSettings}
							disabled={saving}
							class="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 disabled:opacity-50 font-medium transition-colors"
						>
							{saving ? 'Guardando...' : 'Guardar Configuración'}
						</button>
					</div>
				</div>
			</div>
		</div>
	{:else}
		<div class="text-center text-gray-900 dark:text-white">Cargando...</div>
	{/if}
</div>