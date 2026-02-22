<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import FarmSelector from '$lib/components/FarmSelector.svelte';
	import { theme } from '$lib/stores/theme';
</script>

<div class="flex h-screen bg-white dark:bg-gray-900">
	<Sidebar />
	
	<div class="flex-1 flex flex-col overflow-hidden">
		<header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-between items-center">
			<div class="flex-1">
				<FarmSelector />
			</div>
			<ThemeToggle />
		</header>

		<main class="flex-1 overflow-auto">
			<slot />
		</main>
	</div>
</div>
