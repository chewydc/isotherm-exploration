<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	export let forecast: any;

	let chartCanvas: HTMLCanvasElement;
	let chart: any;
	let ChartJS: any;
	let selectedMetric = 'temperature';

	const metrics = [
		{ id: 'temperature', label: 'Temperatura', color: '#ef4444', unit: '°C' },
		{ id: 'humidity', label: 'Humedad', color: '#3b82f6', unit: '%' },
		{ id: 'precipitation', label: 'Precipitación', color: '#06b6d4', unit: 'mm' },
		{ id: 'wind', label: 'Viento', color: '#8b5cf6', unit: 'km/h' }
	];

	function changeMetric(metricId: string) {
		selectedMetric = metricId;
		updateChart();
	}

	onMount(async () => {
		if (!browser || !forecast) return;

		const { Chart, registerables } = await import('chart.js');
		const zoomPlugin = await import('chartjs-plugin-zoom');
		const annotationPlugin = await import('chartjs-plugin-annotation');
		await import('chartjs-adapter-date-fns');
		
		Chart.register(...registerables, zoomPlugin.default, annotationPlugin.default);
		ChartJS = Chart;

		createChart();
	});

	function createChart() {
		if (!ChartJS) return;
		
		const times = forecast.hourly.time.slice(0, 72).map((t: string) => new Date(t));
		
		chart = new ChartJS(chartCanvas, {
			type: 'line',
			data: {
				labels: times,
				datasets: getDatasets()
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
						display: true,
						position: 'top',
						labels: {
							usePointStyle: true,
							padding: 15,
							font: { size: 12, weight: '500' }
						}
					},
					tooltip: {
						backgroundColor: 'rgba(17, 24, 39, 0.95)',
						padding: 16,
						titleFont: { size: 13, weight: '600' },
						bodyFont: { size: 13 },
						bodySpacing: 8,
						cornerRadius: 8,
						displayColors: true,
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
								const metric = metrics.find(m => m.id === selectedMetric);
								return ` ${context.dataset.label}: ${context.parsed.y.toFixed(1)}${metric?.unit}`;
							}
						}
					},
					zoom: {
						zoom: {
							wheel: { enabled: true, speed: 0.1 },
							pinch: { enabled: true },
							mode: 'x'
						},
						pan: {
							enabled: true,
							mode: 'x'
						},
						limits: {
							x: { min: 'original', max: 'original' }
						}
					},
					annotation: {
						annotations: getDayAnnotations()
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
							}
						},
						grid: {
							color: 'rgba(156, 163, 175, 0.1)',
							drawBorder: false
						},
						ticks: {
							maxRotation: 0,
							autoSkipPadding: 30,
							font: { size: 11 }
						}
					},
					y: {
						beginAtZero: selectedMetric === 'precipitation',
						grid: {
							color: 'rgba(156, 163, 175, 0.1)',
							drawBorder: false
						},
						ticks: {
							callback: (value: any) => {
								const metric = metrics.find(m => m.id === selectedMetric);
								return `${value}${metric?.unit}`;
							},
							font: { size: 11 }
						}
					}
				}
			}
		});
	}

	function getDatasets() {
		const metric = metrics.find(m => m.id === selectedMetric);
		if (!metric) return [];

		let data: number[] = [];
		let label = metric.label;

		switch (selectedMetric) {
			case 'temperature':
				data = forecast.hourly.temperature_2m.slice(0, 72);
				break;
			case 'humidity':
				data = forecast.hourly.relative_humidity_2m.slice(0, 72);
				break;
			case 'precipitation':
				data = forecast.hourly.precipitation.slice(0, 72);
				return [{
					label,
					data,
					backgroundColor: metric.color,
					borderColor: metric.color,
					borderWidth: 0,
					type: 'bar',
					barPercentage: 0.9
				}];
			case 'wind':
				data = forecast.hourly.wind_speed_10m.slice(0, 72);
				break;
		}

		return [{
			label,
			data,
			borderColor: metric.color,
			backgroundColor: `${metric.color}20`,
			borderWidth: 3,
			fill: true,
			tension: 0.4,
			pointRadius: 0,
			pointHoverRadius: 7,
			pointHoverBackgroundColor: metric.color,
			pointHoverBorderColor: '#fff',
			pointHoverBorderWidth: 3
		}];
	}

	function getDayAnnotations() {
		const annotations: any = {};
		const times = forecast.hourly.time.slice(0, 72);
		
		let currentDay = new Date(times[0]).getDate();
		let dayCount = 1;

		times.forEach((time: string, i: number) => {
			const date = new Date(time);
			if (date.getDate() !== currentDay) {
				annotations[`day${dayCount}`] = {
					type: 'line',
					xMin: date,
					xMax: date,
					borderColor: 'rgba(156, 163, 175, 0.3)',
					borderWidth: 2,
					borderDash: [5, 5]
				};
				currentDay = date.getDate();
				dayCount++;
			}
		});

		return annotations;
	}

	function updateChart() {
		if (!chart) return;
		
		chart.data.datasets = getDatasets();
		chart.options.plugins.annotation.annotations = getDayAnnotations();
		chart.options.scales.y.beginAtZero = selectedMetric === 'precipitation';
		chart.update(); // Redibuja completamente el gráfico
	}

	function resetZoom() {
		if (chart) chart.resetZoom();
	}

	onDestroy(() => {
		if (chart) chart.destroy();
	});
</script>

<div class="space-y-4">
	<!-- Selector de métricas -->
	<div class="flex flex-wrap gap-2">
		{#each metrics as metric}
			<button
				on:click={() => changeMetric(metric.id)}
				class="px-4 py-2 rounded-lg font-medium transition-all duration-200 {selectedMetric === metric.id 
					? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg scale-105' 
					: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}"
			>
				<span class="inline-block w-3 h-3 rounded-full mr-2" style="background-color: {metric.color}"></span>
				{metric.label}
			</button>
		{/each}
	</div>

	<!-- Gráfico -->
	<div class="relative bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
		<canvas bind:this={chartCanvas} class="w-full" style="height: 400px;"></canvas>
		<button
			on:click={resetZoom}
			class="absolute top-8 right-8 px-3 py-1.5 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors shadow-sm"
		>
			🔄 Reset
		</button>
	</div>

	<!-- Estadísticas -->
	<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
		{#each metrics as metric}
			{@const data = metric.id === 'temperature' ? forecast.hourly.temperature_2m.slice(0, 72)
				: metric.id === 'humidity' ? forecast.hourly.relative_humidity_2m.slice(0, 72)
				: metric.id === 'precipitation' ? forecast.hourly.precipitation.slice(0, 72)
				: forecast.hourly.wind_speed_10m.slice(0, 72)}
			{@const min = Math.min(...data)}
			{@const max = Math.max(...data)}
			{@const avg = data.reduce((a, b) => a + b, 0) / data.length}
			
			<div class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
				<div class="flex items-center gap-2 mb-2">
					<span class="w-2 h-2 rounded-full" style="background-color: {metric.color}"></span>
					<span class="text-xs font-medium text-gray-600 dark:text-gray-400">{metric.label}</span>
				</div>
				<div class="space-y-1">
					<div class="flex justify-between text-xs">
						<span class="text-gray-500 dark:text-gray-400">Mín:</span>
						<span class="font-semibold text-blue-600 dark:text-blue-400">{min.toFixed(1)}{metric.unit}</span>
					</div>
					<div class="flex justify-between text-xs">
						<span class="text-gray-500 dark:text-gray-400">Máx:</span>
						<span class="font-semibold text-red-600 dark:text-red-400">{max.toFixed(1)}{metric.unit}</span>
					</div>
					<div class="flex justify-between text-xs">
						<span class="text-gray-500 dark:text-gray-400">Prom:</span>
						<span class="font-semibold text-gray-700 dark:text-gray-300">{avg.toFixed(1)}{metric.unit}</span>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<p class="text-xs text-center text-gray-500 dark:text-gray-400">
		💡 Usa la rueda del mouse para zoom • Arrastra para desplazar • Click en las métricas para cambiar
	</p>
</div>
