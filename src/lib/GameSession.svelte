<script>
	import csygcLogo from "../assets/csygcLogo.png"
	import Counter from "./Counter.svelte"
	import { writable } from 'svelte/store';
	import { activeqID } from '../session_store.js'
	import { activeSession } from '../session_store.js'

	import { onMount } from 'svelte';

	export let sessionID;

	onMount(async () => {
		const hash = window.location.hash;
		const params = new URLSearchParams(hash.split('?')[1]);
		sessionID = params.get('id');
		console.log(params);
		console.log("Backend port:", window.api.getBackendPort(), sessionID);


		const backendPort = window.api.getBackendPort()
        const response = await fetch(`http://127.0.0.1:${backendPort}/init_questions`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': 'new session' }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();
        console.log(result.data)
        const initData = result.data

		activeSession.update(store => {
		const updated = {
				...store,
				...initData
			};
			console.log('Updating session store:', updated);
			return updated;
		});
	});


	//console.log("Backend port:", window.api.getBackendPort(), sessionID);

	let displayResultTest;
	let displayMsgTest;
	let displayMsgQ;
	let displayMsgA;
	let displayAnswerTest;
	
	let category ='science'; // fix at science for now
	let qid;
	let question;


	function getRandomItem(list) {
		if (!Array.isArray(list) || list.length === 0) return null;
		const index = Math.floor(Math.random() * list.length);
		return list[index];
	}
	// function for fetching question from backend
	async function fetchQuestion() {
		const currCatQlist = [...$activeSession[category]]
		qid = getRandomItem(currCatQlist)

		const backendPort = window.api.getBackendPort()
		const response = await fetch(`http://127.0.0.1:${backendPort}/question?category=${category}&qid=${qid}`, {
			headers: { 'Content-Type': 'application/json' },
            method: 'GET',
		});
		const result = await response.json();
		console.log(result.data)
        displayResultTest = true;
        displayMsgQ = result.data.question;
        displayMsgA = result.data.answer;
        // print out the response
        console.log(result.data)

        displayAnswerTest = false;

	}


    function hideTestDiv () {
    	displayResultTest = false;
    }

    function showAnswerDiv() {
		displayAnswerTest = true;
    }

</script>

<main class="min-h-screen bg-slate-900 text-white flex flex-col">
	<!-- header -->
	<section class="flex justify-center items-center h-16">
		<div class="flex items-center space-x-4 gap-4 md:gap-16 flex-wrap">
			<a href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/" target="_blank" rel="noreferrer">
				<img
					class="h-8 hover:drop-shadow-[0_0_2rem_#ac00ac] transition-all duration-300"
					src={csygcLogo}
					alt="Vite logo"
				/>
			</a>
		</div>
	</section>

	
	<!-- Middle Part -->
	<section class="flex flex-col items-center justify-center mt-6">
		<section class="flex flex-col items-center justify-center mt-6">
			<h1 class="text-4xl font-bold">Trivial Compute!</h1>
			<p class="mt-6 ml-10 mr-10">
				Game board not implemented yet. Example function that fetches random question/answer from JSON database through python backend:
			</p>
			<div>
				<button on:click={fetchQuestion} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Fetch Question &#x1F607</button>
			</div>
			<div class="flex-col items-center justify-center" style="display: {displayResultTest ? 'block' : 'none'};">
				<div>
				&#128013 Question: {displayMsgQ} &#128013
				<button on:click={showAnswerDiv} class="p-4 mt-2 ml-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Show Answer</button>
				</div>
				<div id="answerDiv Test" style="display: {displayAnswerTest ? 'block' : 'none'};">
				&#128013 Answer: {displayMsgA} &#128013
				</div>
			</div>
			<button on:click={hideTestDiv} class="p-4 mt-2 ml-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300" style="display: {displayResultTest ? 'block' : 'none'};">Hide it &#x1fae0</button>
		</section>
	</section>

	<!-- Footer -->
	<footer class="bg-gray-950 fixed bottom-0 left-0 w-full py-2">
		<div class="flex justify-between items-center mx-6">
			<p class="flex-auto text-xs font-light">
				Session ID: {sessionID}
			</p>
		</div>
	</footer>
</main>