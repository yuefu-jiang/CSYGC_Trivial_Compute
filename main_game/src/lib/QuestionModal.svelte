<script>
	import { Modal, Button } from 'flowbite-svelte';
	import { createEventDispatcher } from 'svelte';

	export let open;
	export let question = "";
	export let answer = "";

	let showAnswer = false;
	let isTiming = false;
	let timerId = null;
	let countdown = 10;
	let countdownInterval = null;

	const dispatch = createEventDispatcher();

	function onaction({ action }) {
        if (action === "reveal") {
            reveal()
            return false;
        }
        if (action === "timedReveal") {
            timedReveal()
            return false;
        }
		if (action === "correct" || action === "incorrect") {
			dispatch("answered", { wasCorrect: action === "correct"});
			open = false;
		}
        return true
	}

	function reveal() {
		clearTimers();
		showAnswer = true;
	}

	function timedReveal() {
		if (isTiming) {
			// Cancel
			clearTimers();
		} else {
			// Start
			isTiming = true;
			countdown = 10;

			// Countdown every second
			countdownInterval = setInterval(() => {
				countdown -= 1;
				if (countdown <= 0) {
					reveal();
				}
			}, 1000);

			// Final timeout safety net
			timerId = setTimeout(reveal, 10000);
		}
	}

	function clearTimers() {
		clearTimeout(timerId);
		clearInterval(countdownInterval);
		isTiming = false;
		countdown = 10;
	}

	$: if (!open) {
		showAnswer = false;
		clearTimers();
	}
</script>

<Modal title="Trivia Question" form bind:open={open} size="lg" {onaction}>
	<p class="mb-4">{question}</p>

	{#if showAnswer}
		<p class="font-semibold text-green-300">Answer: {answer}</p>
	{:else}
		<div class="flex flex-col gap-2">
			<!-- <button class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300" on:click={reveal}>Reveal</button>
            <button class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300" on:click={timedReveal}>
                {isTiming ? `Cancel Timed Reveal (${countdown}s)` : "Timed Reveal (10s)"}
            </button> -->
            <Button type="submit" value="reveal" color="dark">Reveal</Button>
			<Button type="submit" value="timedReveal" color="blue">
				{isTiming ? `Cancel Timed Reveal (${countdown}s)` : "Timed Reveal (10s)"}
			</Button>
		</div>
	{/if}

    {#snippet footer()}
    {#if showAnswer}
        <Button type="submit" value="correct" color="green">Correct</Button>
        <Button type="submit" value="incorrect" color="red">Incorrect</Button>
    {/if}   
    {/snippet}
</Modal>
