<script>
	import csygcLogo from "./assets/csygcLogo.png"
	import Counter from "./lib/Counter.svelte"
	import {writable} from 'svelte/store';

	let displayResultTest;
	let displayMsgTest;


	// Sample function for sending a message to backend
	// Async function enables the await keyword. That means that it will wait for the response rather than moving on to next line immediatly.
    async function messageFromBackEnd () {
	   	//call backend method
        const messageDiagogue = window.confirm(
            `This is an example method to send message to py backend. \nTry it now?`,
        );
        // break if cancelled from dialog box
        if (!messageDiagogue) return;
        // equivalent to print statement
	   	console.log("Backend port:", window.api.getBackendPort());

	   	// defined in electron/preload.js. This is the port where python is running.
	   	const backendPort = window.api.getBackendPort()

	   	// demand a response from py server.
	   	// works with Flask; it invoke the sample rule function in server.py
	   	// send a json to backend with header, body and method
	   	// usually the actual content passed will be in body as stringfied json
        const response = await fetch(`http://127.0.0.1:${backendPort}/rule`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': 'yo' }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();

        // this controls the message display down below
        displayResultTest = result.action;
        displayMsgTest = result.data;
        // print out the response
        console.log(result.data)
    };

    function hideTestDiv () {
    	displayResultTest = false;
    }
</script>

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
			This is a paragraph! 
		</p>
		<p class="mt-2">
			This is a template adapted from <a href="https://github.com/feernandobraga/vitesvelctron" target="_blank" style="color:green">vitesvelectron</a>.
		</p>
		<p class="mt-2">
			Counter app is imported below with js from lib. This is an example of a PURE js solution.
		</p>
		<div>
			<Counter />
		</div>
		<p class="mt-2">
			Message button below is executed in te backend by Python. This is an example of a FLASK server solution.
		</p>
		<div>
			<button on:click={messageFromBackEnd} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Send a Bottle to Backend</button>
		</div>
		<div style="display: {displayResultTest ? 'block' : 'none'};">
			{displayMsgTest} &#128013
			<button on:click={hideTestDiv} class="p-4 mt-2 ml-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Hide it &#x1fae0</button>
		</div>
	</section>

	<!-- Footer -->
	<footer class="bg-gray-950 fixed bottom-0 left-0 w-full py-2">
		<div class="flex justify-between items-center mx-6">
			<p class="flex-auto text-xs font-light">
				This is a footer
			</p>
		</div>
	</footer>
</main>
