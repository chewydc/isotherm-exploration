<script lang="ts">
	import { page } from '$app/stores';
	import { onMount, onDestroy } from 'svelte';

	const navItems = [
		{ href: '/', label: 'Dashboard', icon: '📊' },
		{ href: '/mapa', label: 'Mapa Isotermas', icon: '🗺️' },
		{ href: '/sensores', label: 'Sensores', icon: '🌡️' },
		{ href: '/forecast', label: 'Pronóstico', icon: '🌤️' }
	];

	let currentDateTime = new Date();
	let timeInterval: any;

	onMount(() => {
		timeInterval = setInterval(() => {
			currentDateTime = new Date();
		}, 60000);
	});

	onDestroy(() => {
		if (timeInterval) clearInterval(timeInterval);
	});
</script>

<aside class="w-64 bg-gray-100 dark:bg-gray-800 h-screen p-4 border-r border-gray-300 dark:border-gray-700 flex flex-col">
	<div class="mb-8">
		<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Isoterma</h1>
		<p class="text-sm text-gray-600 dark:text-gray-400">Monitoreo Agrícola</p>
	</div>

	<nav class="space-y-2 flex-1">
		{#each navItems as item}
			<a
				href={item.href}
				class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors {$page.url
					.pathname === item.href
					? 'bg-blue-500 text-white'
					: 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'}"
			>
				<span class="text-xl">{item.icon}</span>
				<span class="font-medium">{item.label}</span>
			</a>
		{/each}
	</nav>

	<div class="mt-auto pt-4 border-t border-gray-300 dark:border-gray-600">
		<div class="text-center">
			<p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Ahora</p>
			<p class="text-sm font-semibold text-gray-800 dark:text-white">
				{currentDateTime.toLocaleDateString('es-AR', { weekday: 'short', day: '2-digit', month: 'short' })}
			</p>
			<p class="text-xs text-gray-600 dark:text-gray-400">
				{currentDateTime.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit', hour12: false })}
			</p>
		</div>
	</div>
</aside>