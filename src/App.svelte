<script>
	import csygcLogo from "./assets/csygcLogo.png"
	import Counter from "./lib/Counter.svelte"

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
			Counter app is imported below with js from lib. Py backend is pending implementation.
		</p>
		<div>
			<Counter />
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
