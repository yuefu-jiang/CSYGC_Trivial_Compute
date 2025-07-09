<script>
	import csygcLogo from "../assets/csygcLogo.png"
    import Chip, { Set, Text } from '@smui/chips';
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';

    let { closePage } = $props();

    let choices = [1, 2, 3, 4];
    let numberOfPlayers = $state(0);
    let valid_names = $state(false);
    let playerNames = $state([]);

    function validateNames() {
        for (let i = 0; i < numberOfPlayers; i++) {
            const name = playerNames[i];
            console.log(`name: ${name}`);
            if (name === '' || name === undefined) {
                valid_names = false;
                break;
            }
            valid_names = true;
        }
    }

    function allowOnlyLetters(event, index) {
        const cleaned = event.target.value.replace(/[^a-zA-Z\s]/g, '');
        playerNames[index] = cleaned;
        playerNames = [...playerNames];
        validateNames();        
    }

    function updateNumberOfPlayers(num) {
        numberOfPlayers = num;
        let size_diff = Math.abs(numberOfPlayers - playerNames.length);
        let AddMorePlayers = numberOfPlayers > playerNames.length;
        let oldPlayerNames = playerNames;
        for (let i = 0; i < size_diff; i++) {
            if (AddMorePlayers) {
                valid_names = false;
                oldPlayerNames.push('');
                continue;
            }
            oldPlayerNames.pop();
        }
        playerNames = oldPlayerNames;
        validateNames();
    }

</script>

<main class="min-h-screen bg-slate-900 text-white flex flex-col">
    <div>
        <!-- Choose Number of Players -->
        <section class="flex flex-col items-center justify-center mt-6">
            <h1 class="text-4xl font-bold">Trivial Compute!</h1>
            <h3 style="margin-top: 1em;">How many players?</h3>
            <div class="flex gap-4 mt-4">
                {#each choices as num}
                <Button
                    onclick={() => {
                        updateNumberOfPlayers(num);
                    }}
                    class={`p-4 border border-indigo-900 border-opacity-80 rounded-md transition-all duration-300
                    ${numberOfPlayers === num 
                        ? 'bg-slate-700 hover:bg-slate-600 border-indigo-500 text-white' 
                        : 'hover:bg-slate-800 bg-slate-900 text-white'}`}
                >
                    <Label>{num}</Label>
                </Button>
                {/each}
            </div>
        </section>

        <!-- Player Names -->
        {#if playerNames !== 0}
            <section class="flex flex-col items-center justify-center mt-6">
                {#each Array(numberOfPlayers) as _, num}
                    <div class="flex flex-col gap-4 w-full max-w-md m-2">
                        <input
                            bind:value={playerNames[num]}
                            oninput={(e) => allowOnlyLetters(e, num)}
                            placeholder="Player {num + 1}"
                            class="w-full p-3 text-white bg-slate-800 border border-indigo-900 border-opacity-70 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 transition-all duration-200"
                        />
                    </div>
                {/each}
            </section>
        {/if}
    

        <!-- Start Button -->
        {#if valid_names && numberOfPlayers !== 0}
            <section class="flex flex-col items-center justify-center mt-6">
                <div>
                    <button onclick={closePage} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Start Game</button>
                </div>
            </section>
        {/if}
    </div>
</main>
