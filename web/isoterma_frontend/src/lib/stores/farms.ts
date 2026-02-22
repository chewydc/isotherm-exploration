import { writable } from 'svelte/store';

export const selectedFarm = writable<any>(null);
export const farms = writable<any[]>([]);
