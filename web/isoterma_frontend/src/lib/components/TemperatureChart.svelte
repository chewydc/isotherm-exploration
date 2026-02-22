<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	export let forecast: any;

	let chartCanvas: HTMLCanvasElement;
	let chart: any;

	onMount(async () => {
		if (!browser || !forecast) return;

		const { Chart, registerables } = await import('chart.js');
		const zoomPlugin = await import('chartjs-plugin-zoom');
		
		Chart.register(...registerables, zoomPlugin.default);

		const temps = forecast.hourly.temperature_2m.slice(0, 72);
		const times = forecast.hourly.time.slice(0, 72);

		chart = new Chart(chartCanvas, {
			type: 'line',
			data: {
				labels: times.map((t: string) => new Date(t)),
				datasets: [{
					label: 'Temperatura',
					data: temps,
					borderColor: '#3b82f6',
					backgroundColor: 'rgba(59, 130, 246, 0.1)',
					borderWidth: 2,
					fill: true,
					tension: 0.4,
					pointRadius: 0,
					pointHoverRadius: 6,
					pointHoverBackgroundColor: '#3b82f6',
					pointHoverBorderColor: '#fff',
					pointHoverBorderWidth: 2
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				interaction: {
					mode: 'index',
					intersect: false
				},
				plugins: {
					legend: {
						display: false
					},
					tooltip: {
						backgroundColor: 'rgba(0, 0, 0, 0.8)',
						padding: 12,
						titleFont: { size: 13 },
						bodyFont: { size: 14, weight: 'bold' },
						callbacks: {
							title: (context: any) => {
								const date = new Date(context[0].parsed.x);
								return date.toLocaleDateString('es-AR', { 
									weekday: 'short',
									day: '2-digit', 
									month: 'short',
									hour: '2-digit',
									minute: '2-digit'
								});
							},
							label: (context: any) => {
								return `${context.parsed.y.toFixed(1)}°C`;
							}
						}
					},
					zoom: {
						zoom: {
							wheel: {
								enabled: true,
								speed: 0.1
							},
							pinch: {
								enabled: true
							},
							mode: 'x'
						},
						pan: {
							enabled: true,
							mode: 'x'
						},
						limits: {
							x: { min: 'original', max: 'original' }
						}
					}
				},
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'hour',
							displayFormats: {
								hour: 'HH:mm',
								day: 'dd/MM'
							},
							tooltipFormat: 'dd/MM HH:mm'
						},
						grid: {
							color: 'rgba(0, 0, 0, 0.05)',
							drawBorder: false
						},
						ticks: {
							maxRotation: 0,
							autoSkipPadding: 20,
							font: { size: 11 }
						}
					},
					y: {
						beginAtZero: false,
						grid: {
							color: 'rgba(0, 0, 0, 0.05)',
							drawBorder: false
						},
						ticks: {
							callback: (value: any) => `${value}°C`,
							font: { size: 11 }
						}
					}
				}
			}
		});
	});

	onDestroy(() => {
		if (chart) {
			chart.destroy();
		}
	});

	export function resetZoom() {
		if (chart) {
			chart.resetZoom();
		}
	}
</script>

<div class="relative">
	<canvas bind:this={chartCanvas} class="w-full" style="height: 350px;"></canvas>
	<button
		on:click={resetZoom}
		class="absolute top-2 right-2 px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
	>
		Reset Zoom
	</button>
	<p class="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
		💡 Usa la rueda del mouse para hacer zoom, arrastra para desplazar
	</p>
</div>
