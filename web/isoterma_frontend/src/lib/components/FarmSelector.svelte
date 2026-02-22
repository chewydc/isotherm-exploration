<script lang="ts">
	import { onMount } from 'svelte';
	import { selectedFarm, farms } from '$lib/stores/farms';
	import { api } from '$lib/api/client';

	onMount(async () => {
		try {
			const data = await api.getFarms();
			farms.set(data.farms || []);
			if (data.farms?.length > 0) {
				selectedFarm.set(data.farms[0]);
			}
		} catch (error) {
			console.error('Error loading farms:', error);
		}
	});

	function handleChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const farm = $farms.find((f) => f.id === target.value);
		selectedFarm.set(farm);
	}
</script>

<div class="flex items-center gap-3">
	<label for="farm-select" class="text-sm font-medium text-gray-700 dark:text-gray-300">
		Finca:
	</label>
	<select
		id="farm-select"
		on:change={handleChange}
		value={$selectedFarm?.id}
		class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
	>
		{#each $farms as farm}
			<option value={farm.id}>{farm.name}</option>
		{/each}
	</select>
</div>
