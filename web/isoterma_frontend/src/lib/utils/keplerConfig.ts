export const createKeplerConfig = (dataId: string) => ({
	version: 'v1',
	config: {
		visState: {
			filters: [],
			layers: [
				{
					id: 'temp_1m',
					type: 'heatmap',
					config: {
						dataId,
						label: 'Temperatura 1m',
						color: [18, 147, 154],
						columns: {
							lat: 'latitude',
							lng: 'longitude'
						},
						isVisible: true,
						visConfig: {
							opacity: 0.8,
							colorRange: {
								name: 'Global Warming',
								type: 'sequential',
								category: 'Uber',
								colors: ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
							},
							radius: 150
						},
						hidden: false,
						textLabel: []
					},
					visualChannels: {
						weightField: {
							name: 'temp_1m',
							type: 'real'
						},
						weightScale: 'linear'
					}
				},
				{
					id: 'temp_2m',
					type: 'heatmap',
					config: {
						dataId,
						label: 'Temperatura 2m',
						color: [241, 92, 23],
						columns: {
							lat: 'latitude',
							lng: 'longitude'
						},
						isVisible: false,
						visConfig: {
							opacity: 0.8,
							colorRange: {
								name: 'Global Warming',
								type: 'sequential',
								category: 'Uber',
								colors: ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
							},
							radius: 150
						},
						hidden: false
					},
					visualChannels: {
						weightField: {
							name: 'temp_2m',
							type: 'real'
						},
						weightScale: 'linear'
					}
				},
				{
					id: 'temp_5m',
					type: 'heatmap',
					config: {
						dataId,
						label: 'Temperatura 5m',
						color: [23, 184, 190],
						columns: {
							lat: 'latitude',
							lng: 'longitude'
						},
						isVisible: false,
						visConfig: {
							opacity: 0.8,
							colorRange: {
								name: 'Global Warming',
								type: 'sequential',
								category: 'Uber',
								colors: ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
							},
							radius: 150
						},
						hidden: false
					},
					visualChannels: {
						weightField: {
							name: 'temp_5m',
							type: 'real'
						},
						weightScale: 'linear'
					}
				},
				{
					id: 'temp_10m',
					type: 'heatmap',
					config: {
						dataId,
						label: 'Temperatura 10m',
						color: [130, 154, 227],
						columns: {
							lat: 'latitude',
							lng: 'longitude'
						},
						isVisible: false,
						visConfig: {
							opacity: 0.8,
							colorRange: {
								name: 'Global Warming',
								type: 'sequential',
								category: 'Uber',
								colors: ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
							},
							radius: 150
						},
						hidden: false
					},
					visualChannels: {
						weightField: {
							name: 'temp_10m',
							type: 'real'
						},
						weightScale: 'linear'
					}
				}
			],
			interactionConfig: {
				tooltip: {
					fieldsToShow: {
						[dataId]: [
							{ name: 'sensor_id', format: null },
							{ name: 'temp_1m', format: null },
							{ name: 'temp_2m', format: null },
							{ name: 'temp_5m', format: null },
							{ name: 'temp_10m', format: null }
						]
					},
					compareMode: false,
					compareType: 'absolute',
					enabled: true
				},
				brush: { size: 0.5, enabled: false },
				geocoder: { enabled: false },
				coordinate: { enabled: false }
			},
			layerBlending: 'normal',
			splitMaps: [],
			animationConfig: { currentTime: null, speed: 1 }
		},
		mapState: {
			bearing: 0,
			dragRotate: false,
			latitude: -39.164,
			longitude: -67.035,
			pitch: 0,
			zoom: 14,
			isSplit: false
		},
		mapStyle: {
			styleType: 'satellite',
			topLayerGroups: {},
			visibleLayerGroups: {
				label: true,
				road: true,
				border: false,
				building: true,
				water: true,
				land: true,
				'3d building': false
			},
			threeDBuildingColor: [9.665468314072013, 17.18305478057247, 31.1442867897876],
			mapStyles: {}
		}
	}
});
