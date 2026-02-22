<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	export let data: any = null;
	export let config: any = null;

	let container: HTMLDivElement;
	let keplerInstance: any = null;

	onMount(async () => {
		if (!browser) return;

		try {
			// Importar dinámicamente Kepler.gl y dependencias
			const KeplerGl = (await import('kepler.gl/components')).default;
			const { createStore, combineReducers, applyMiddleware } = await import('redux');
			const { taskMiddleware } = await import('react-palm/tasks');
			const { Provider, useDispatch } = await import('react-redux');
			const React = await import('react');
			const ReactDOM = await import('react-dom/client');
			const keplerGlReducer = (await import('kepler.gl/reducers')).default;
			const { addDataToMap } = await import('kepler.gl/actions');

			// Crear store de Redux
			const reducers = combineReducers({
				keplerGl: keplerGlReducer
			});

			const store = createStore(reducers, {}, applyMiddleware(taskMiddleware));

			// Componente React wrapper
			const KeplerApp = () => {
				const dispatch = useDispatch();

				React.useEffect(() => {
					if (data && config) {
						dispatch(
							addDataToMap({
								datasets: {
									info: { label: 'Sensores', id: 'sensores' },
									data
								},
								config
							})
						);
					}
				}, [dispatch]);

				return React.createElement(KeplerGl, {
					id: 'map',
					mapboxApiAccessToken: undefined,
					width: window.innerWidth - 256,
					height: window.innerHeight
				});
			};

			// Renderizar con React 18
			const root = ReactDOM.createRoot(container);
			root.render(
				React.createElement(
					Provider,
					{ store },
					React.createElement(KeplerApp)
				)
			);

			keplerInstance = root;
		} catch (error) {
			console.error('Error loading Kepler.gl:', error);
		}
	});

	onDestroy(() => {
		if (keplerInstance) {
			keplerInstance.unmount();
		}
	});
</script>

<div bind:this={container} class="w-full h-full" />
