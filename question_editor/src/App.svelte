<script>
	import csygcLogo from "./assets/csygcLogo.png";
	import { onMount } from "svelte";
	import ImportJsonModal from "./lib/ImportJsonModal.svelte";

	let currentRoute = window.location.hash || "#/";
	let queryParams = new URLSearchParams();
	let openAddByJsonModal = false;

	const updateRoute = () => {
		const [path, query] = window.location.hash.split("?");
		currentRoute = path || "#/";
		queryParams = new URLSearchParams(query);
	};

	onMount(() => {
		updateRoute();
		window.addEventListener("hashchange", updateRoute);
		return () => window.removeEventListener("hashchange", updateRoute);
	});

	function showJsonModalClick() {
		openAddByJsonModal = true;
	}
</script>

{#if currentRoute === "#/"}
	<main class="min-h-screen bg-slate-900 text-white flex flex-col">
		<!-- Top Part -->
		<section class="flex justify-center items-center h-96">
			<div class="flex items-center space-x-4 gap-4 md:gap-16 flex-wrap">
				<a
					href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/"
					target="_blank"
					rel="noreferrer"
				>
					<img
						class="h-80 hover:drop-shadow-[0_0_2rem_#ac00ac] transition-all duration-300"
						src={csygcLogo}
						alt="Logo"
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
				<button
					on:click={showJsonModalClick}
					class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300"
				>
					Import From JSON
				</button>
			</div>
			<!-- <div>
				<button
					on:click={() => alert("Not yet implemented")}
					class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300"
				>
					View/Edit Current Questions (Under Development...)
				</button>
			</div> -->
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

	<!-- Modal Component -->
	<ImportJsonModal bind:open={openAddByJsonModal} />
{:else}
	<p>404 - Page not found</p>
{/if}
