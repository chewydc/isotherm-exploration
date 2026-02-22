<script>
	import { page } from '$app/stores';
	import { api } from '$lib/api/client';
	import { onMount } from 'svelte';

	let farm = null;
	let settings = {
		temperature_threshold_min: 16.0,
		temperature_threshold_max: 25.0,
		alerts_enabled: true
	};
	let alerts = [];
	let loading = false;
	let saving = false;

	const farmId = $page.params.id;

	onMount(async () => {
		await loadFarm();
		await loadAlerts();
	});

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

	async function loadAlerts() {
		try {
			const response = await fetch(`/api/v1/farms/${farmId}/alerts`);
			const data = await response.json();
			alerts = data.data || [];
		} catch (error) {
			console.error('Error loading alerts:', error);
		}
	}

	async function saveSettings() {
		try {
			saving = true;
			const response = await fetch(`/api/v1/farms/${farmId}/settings`, {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(settings)
			});
			
			if (response.ok) {
				await loadAlerts();
				alert('Configuración guardada correctamente');
			}
		} catch (error) {
			console.error('Error saving settings:', error);
			alert('Error al guardar configuración');
		} finally {
			saving = false;
		}
	}
</script>

<div class="container mx-auto p-6">
	<div class="mb-6 flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-800 mb-2">Gestión de Finca</h1>
			{#if farm}
				<h2 class="text-xl text-gray-600">{farm.name}</h2>
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
		<div class="text-center">Cargando...</div>
	{:else if farm}

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<!-- Configuración de Umbrales -->
			<div class="bg-white rounded-lg shadow-md p-6">
				<h3 class="text-lg font-semibold mb-4">Configuración de Umbrales</h3>
				
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							Temperatura Mínima (°C)
						</label>
						<input
							type="number"
							step="0.1"
							bind:value={settings.temperature_threshold_min}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
						/>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							Temperatura Máxima (°C)
						</label>
						<input
							type="number"
							step="0.1"
							bind:value={settings.temperature_threshold_max}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
						/>
					</div>

					<div class="flex items-center">
						<input
							type="checkbox"
							bind:checked={settings.alerts_enabled}
							class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
						/>
						<label class="ml-2 block text-sm text-gray-700">
							Activar alertas automáticas
						</label>
					</div>

					<button
						on:click={saveSettings}
						disabled={saving}
						class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
					>
						{saving ? 'Guardando...' : 'Guardar Configuración'}
					</button>
				</div>
			</div>

			<!-- Alertas Activas -->
			<div class="bg-white rounded-lg shadow-md p-6">
				<h3 class="text-lg font-semibold mb-4">Alertas Activas</h3>
				
				{#if alerts.length === 0}
					<div class="text-center text-gray-500 py-8">
						<div class="text-4xl mb-2">✅</div>
						<p>No hay alertas activas</p>
						<p class="text-sm">Todos los sensores están dentro de los umbrales</p>
					</div>
				{:else}
					<div class="space-y-3">
						{#each alerts as alert}
							<div class="border-l-4 border-yellow-400 bg-yellow-50 p-4 rounded">
								<div class="flex items-center">
									<div class="text-yellow-600 mr-3">⚠️</div>
									<div class="flex-1">
										<p class="font-medium text-yellow-800">
											Sensor {alert.sensor_id}
										</p>
										<p class="text-sm text-yellow-700">
											{alert.message}
										</p>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/if}

				<button
					on:click={loadAlerts}
					class="mt-4 w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200"
				>
					🔄 Actualizar Alertas
				</button>
			</div>
		</div>
	{:else}
		<div class="text-center">Cargando...</div>
	{/if}
</div>