<script>
	import csygcLogo from "./assets/csygcLogo.png"
	import { writable } from 'svelte/store';
	import { onMount } from 'svelte';
	import JsonModal from './lib/components/JsonModal.svelte';
	import { Button, Modal, P, Fileupload, Label, Helper, Checkbox } from "flowbite-svelte";

	let currentRoute = window.location.hash || '#/';
	let queryParams = new URLSearchParams();
	let openAddByJsonModal = $state(false);
	let error = $state("");

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

	function showJsonModalClick() {
		console.log("add", openAddByJsonModal)
		openAddByJsonModal = true
		console.log("add", openAddByJsonModal)
	}

function onaction({ action, data }) {
	error = "";

	if (action === "cancel") return;

	// Step 1: Get file and checkbox from FormData
	const file = data.get("file");
	const replace = data.get("replace") === "on"; // "on" means checkbox is checked

	// Step 2: Validate the file
	if (!file || !(file instanceof File) || !file.name) {
		error = "Must choose a file";
		console.log("Must choose a file");
		return false;
	}
	if (file.type !== "application/json") {
		error = "File must be of type JSON";
		console.log("Not a JSON file");
		return false;
	}

	// Step 3: Read the file contents
	const reader = new FileReader();
	reader.readAsText(file);
	reader.onload = () => {
		try {
			const json = JSON.parse(String(reader.result));

			// Step 4: Choose endpoint
			const backendPort = window.api?.getBackendPort?.() || 5000;
			const endpoint = replace
				? `http://127.0.0.1:${backendPort}/replace_questions_file`
				: `http://127.0.0.1:${backendPort}/add_to_questions_file`;

			// Step 5: Send to backend
			fetch(endpoint, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(json)
			})
			.then(async (res) => {
				const result = await res.json();
				if (!res.ok) throw result;
				alert('✅ Questions file successfully updated!');
			})
			.catch((err) => {
				console.error('Failed to update questions file:', err);
				alert(`❌ Error: ${err?.error || 'Unknown error'}`);
			});
		} catch (e) {
			alert("❌ Invalid JSON content.");
			console.error("JSON parse error:", e);
		}
	};
}


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
			<h1 class="text-4xl font-bold">Question Editor</h1>
			<p class="mt-6">
				Import questions using a JSON file or edit existing questions.
			</p>
			<div>
				<button on:click={showJsonModalClick} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Import From JSON</button>
				
			</div>
			<div>
				<button on:click={() => alert("Not yet implemented")} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">View/Edit Current Questions (Under Development...)</button>
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

	
	<Modal title="Add questions using JSON file" form bind:open={openAddByJsonModal} size="lg"{onaction}>
		<Fileupload id="with_helper" name ="file" class="mb-2" />
		{#if error}
			<Label color="red">{error}</Label>
		{/if}
		<Helper>JSON</Helper>
		<Checkbox name='replace'>Replace Current Question Bank</Checkbox>
		{#snippet footer()}
			<Button type="submit" value="submit" color="dark">Accept</Button>
			<Button type="submit" value="cancel" color="alternative">Cancel</Button>
		{/snippet}
	</Modal>
	
{:else}
	<p>404 - Page not found</p>
{/if}
