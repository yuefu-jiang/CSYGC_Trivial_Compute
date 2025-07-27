import {writable} from 'svelte/store';

export const playerResponse = writable(false);
export const selectedCat = writable('');
export const activeqID = writable([]);
export const activeSession = writable({});
export const sessionID = writable('');