<script>
	import csygcLogo from "./assets/csygcLogo.png"
	import Counter from "./lib/Counter.svelte"
	import { writable } from 'svelte/store';
	import { activeqID } from './session_store.js'
	import { activeSession } from './session_store.js'
	import GameSession from './lib/GameSession.svelte';
	import { onMount } from 'svelte';

	let currentRoute = window.location.hash || '#/';
	let queryParams = new URLSearchParams();

	const updateRoute = () => {
		const [path, query] = window.location.hash.split('?');
		currentRoute = path || '#/';
		queryParams = new URLSearchParams(query);
	};

	onMount(() => {
		updateRoute();
		window.addEventListener('hashchange', updateRoute);
		return () => window.removeEventListener('hashchange', updateRoute);
	});

	// Generate a random ID (customizable length and characters)
	function generateRandomID() {
		const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
		const length = 6;
		return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
	}

	// Main function: returns a unique ID not in dict keys
	export function generateUniqueID(dict) {
		let id;
		do {
			id = generateRandomID();
		} while (dict.hasOwnProperty(id));
		
		return id;
	};

    async function newGameSession() {

		const backendPort = window.api.getBackendPort()
        const response = await fetch(`http://127.0.0.1:${backendPort}/init_questions`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': 'new session' }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();
		const initData = result.data;
		console.log(initData)
		const newSessionID = generateUniqueID(activeSession);
		sessionID = newSessionID;

		activeSession.update(store => {
		const updated = {
				...store,
				[newSessionID]: initData
			};
			console.log('Updating session store:', updated);
			return updated;
		});
		console.log(currentRoute)
		window.electronAPI.openGameSession(newSessionID);

	}
	let sessionID = '';
	$: sessionID = queryParams.get('id');
 
</script>
{#if currentRoute === '#/'}
	<main class="min-h-screen bg-slate-900 text-white flex flex-col">
		<!-- Top Part -->
		<section class="flex justify-center items-center h-96">
			<div class="flex items-center space-x-4 gap-4 md:gap-16 flex-wrap">
				<a href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/" target="_blank" rel="noreferrer">
					<img
						class="h-80  hover:drop-shadow-[0_0_2rem_#ac00ac] transition-all duration-300"
						src={csygcLogo}
						alt="Vite logo"
					/>
				</a>
			</div>
		</section>

		
		<!-- Middle Part -->
		<section class="flex flex-col items-center justify-center mt-6">
			<h1 class="text-4xl font-bold">Trivial Compute!</h1>
			<p class="mt-6">
				Welcome! Click button below to start a new game.
			</p>
			<div>
				<button on:click={newGameSession} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">New game</button>
			</div>

		</section>

		<!-- Footer -->
		<footer class="bg-gray-950 fixed bottom-0 left-0 w-full py-2">
			<div class="flex justify-between items-center mx-6">
				<p class="flex-auto text-xs font-light">
					Trivial Compute is a FREE software made by CYSGC.
				</p>
			</div>
		</footer>
	</main>
{:else if currentRoute === '#/game-session'}
	<GameSession  sessionID={sessionID} />

{:else}
	<p>404 - Page not found</p>
{/if}
