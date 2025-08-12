<script>
	import { onMount } from "svelte";
	import MainPage from "./lib/MainPage.svelte";
	import QuestionsGrid from "./lib/QuestionsGrid.svelte";

	let currentRoute = window.location.hash || "#/";
	let queryParams = new URLSearchParams();

	let currentPage = 'main';

	function goTo(page) {
		currentPage = page;
	}
	
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
</script>

<!-- {#if currentRoute === "#/"}
	<MainPage />
{:else}
	<p>404 - Page not found</p>
{/if} -->

{#if currentPage === 'main'}
	<MainPage on:navigate={() => goTo('second')} />
{:else if currentPage === 'second'}
	<QuestionsGrid onBack={() => goTo('main')} />
{/if}

