<script lang="ts">
	import { selectedFarm } from '$lib/stores/farms';
	import LeafletMap from '$lib/components/LeafletMap.svelte';
</script>

<svelte:head>
	<title>Mapa Isotermas - Isoterma</title>
</svelte:head>

<div class="h-full w-full p-4 bg-gray-100 dark:bg-gray-900">
	{#if $selectedFarm?.sensors && $selectedFarm?.location}
		<div class="h-full w-full rounded-xl overflow-hidden shadow-xl">
			<LeafletMap sensors={$selectedFarm.sensors} center={$selectedFarm.location} />
		</div>
	{:else}
		<div class="flex items-center justify-center h-full">
			<div class="text-center">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
				<p class="text-gray-600 dark:text-gray-400">Cargando mapa...</p>
			</div>
		</div>
	{/if}
</div>
