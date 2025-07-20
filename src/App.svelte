<script>
	import csygcLogo from "./assets/csygcLogo.png"
	import Counter from "./lib/Counter.svelte"
	import {writable} from 'svelte/store';
	import NewGameSignInPage from "./lib/NewGameSignInPage.svelte";

	import { activeqID } from './session_store.js'
	import { activeSession } from './session_store.js'
	import GameSession from './lib/GameSession.svelte';
	import { onMount } from 'svelte';
	import { sessionID } from './session_store.js';

	let displayResultTest;
	let displayMsgTest;
	let displayNewGamePage = false;

	function openNewGamePage() {
		displayNewGamePage = true;
	};

	function closeNewGamePage() {
		displayNewGamePage = false;
	}

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


</script>

{#if currentRoute === '#/'}
	
	{#if displayNewGamePage}
	<NewGameSignInPage closePage={closeNewGamePage}/>
	{:else}
		<main class="min-h-screen bg-slate-900 text-white flex flex-col">
			<!-- Top Part -->
			<section class="flex justify-center items-center h-72">
				<div class="flex items-center space-x-4 gap-4 md:gap-16 flex-wrap">
					<a href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/" target="_blank" rel="noreferrer">
						<img
							class="h-60  hover:drop-shadow-[0_0_2rem_#ac00ac] transition-all duration-300"
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
					<button on:click={openNewGamePage} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Start New Game</button>
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
	{/if}
{:else if currentRoute === '#/game-session'}
	<GameSession  sessionID={$sessionID} />

{:else}
	<p>404 - Page not found</p>
{/if}
