<script lang="ts">
	import { page } from '$app/stores';

	const navItems = [
		{ href: '/', label: 'Dashboard', icon: '📊' },
		{ href: '/mapa', label: 'Mapa Isotermas', icon: '🗺️' },
		{ href: '/sensores', label: 'Sensores', icon: '🌡️' },
		{ href: '/forecast', label: 'Pronóstico', icon: '🌤️' }
	];
</script>

<aside class="w-64 bg-gray-100 dark:bg-gray-800 h-screen p-4 border-r border-gray-300 dark:border-gray-700">
	<div class="mb-8">
		<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Isoterma</h1>
		<p class="text-sm text-gray-600 dark:text-gray-400">Monitoreo Agrícola</p>
	</div>

	<nav class="space-y-2">
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
</aside>
