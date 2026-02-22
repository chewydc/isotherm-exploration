<script lang="ts">
	import { selectedFarm } from '$lib/stores/farms';

	function getStatusColor(status: string) {
		switch (status) {
			case 'active':
				return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
			case 'warning':
				return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
			case 'error':
				return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
			default:
				return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
		}
	}
</script>

<svelte:head>
	<title>Sensores - Isoterma</title>
</svelte:head>

<div class="p-6">
	<h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Sensores</h2>

	{#if $selectedFarm?.sensors}
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
			<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
				<thead class="bg-gray-50 dark:bg-gray-900">
					<tr>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
							ID Sensor
						</th>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
							Ubicación
						</th>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
							Temperatura
						</th>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
							Estado
						</th>
					</tr>
				</thead>
				<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
					{#each $selectedFarm.sensors as sensor}
						<tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
							<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
								{sensor.id}
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
								{sensor.latitude.toFixed(4)}, {sensor.longitude.toFixed(4)}
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold">
								{#if sensor.temperature}
									<span class="text-gray-900 dark:text-white">{sensor.temperature.toFixed(1)}°C</span>
								{:else}
									<span class="text-gray-400">N/A</span>
								{/if}
							</td>
							<td class="px-6 py-4 whitespace-nowrap">
								<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {getStatusColor(sensor.status)}">
									{sensor.status}
								</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{:else}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">No hay sensores disponibles</p>
		</div>
	{/if}
</div>
