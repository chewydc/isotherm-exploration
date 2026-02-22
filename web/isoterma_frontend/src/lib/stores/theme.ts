import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const stored = browser ? localStorage.getItem('theme') : null;
export const theme = writable<'light' | 'dark'>(stored === 'dark' ? 'dark' : 'light');

theme.subscribe((value) => {
	if (browser) {
		localStorage.setItem('theme', value);
		if (value === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	}
});
