const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = {
	async getFarms() {
		const res = await fetch(`${API_BASE_URL}/farms`);
		if (!res.ok) throw new Error('Error fetching farms');
		return res.json();
	},

	async getFarm(id: string) {
		const res = await fetch(`${API_BASE_URL}/farms/${id}`);
		if (!res.ok) throw new Error('Error fetching farm');
		return res.json();
	},

	async getCurrentWeather(lat: number, lon: number) {
		const res = await fetch(`${API_BASE_URL}/weather/current?latitude=${lat}&longitude=${lon}`);
		if (!res.ok) throw new Error('Error fetching weather');
		return res.json();
	},

	async getForecast(lat: number, lon: number, days: number = 3) {
		const res = await fetch(`${API_BASE_URL}/weather/forecast?latitude=${lat}&longitude=${lon}&forecast_days=${days}`);
		if (!res.ok) throw new Error('Error fetching forecast');
		return res.json();
	}
};
