<script>
	import csygcLogo from "../assets/csygcLogo.png"
    import Chip, { Text } from '@smui/chips';
    import Button, { Label } from '@smui/button';
    import Select, { Option } from '@smui/select';
    import Textfield from '@smui/textfield';

    import { activeqID } from '../session_store.js'
    import { activeSession } from '../session_store.js'
    import { sessionID } from '../session_store.js';

    let { closePage } = $props();
    
    const NUMBER_OF_CATEGORIES = 4;

    //let sessionID;
    //$: sessionID = queryParams.get('id');

    let choices = [2, 3, 4];
    let numberOfPlayers = $state(0);
    let validNames = $state(false);
    let playerNames = $state([]);

    let validCategories = $state(false);
    let categoryOptions = new Set([
        "Geography",
        "History",
        "Math",
        "Computer Science",
        "Spanish",
        "English",
        "Physics",
    ]);
    // let selectedCategories = new Set([]);
    let selectedCategoriesList = $state(Array(NUMBER_OF_CATEGORIES).fill(''));

    let currentRoute = window.location.hash || '#/';
    let queryParams = new URLSearchParams();


    function validateNames() {
        for (let i = 0; i < numberOfPlayers; i++) {
            const name = playerNames[i];
            console.log(`name: ${name}`);
            if (name === '' || name === undefined) {
                validNames = false;
                break;
            }
            validNames = true;
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
        let sizeDiff = Math.abs(numberOfPlayers - playerNames.length);
        let AddMorePlayers = numberOfPlayers > playerNames.length;
        let oldPlayerNames = playerNames;
        for (let i = 0; i < sizeDiff; i++) {
            if (AddMorePlayers) {
                validNames = false;
                oldPlayerNames.push('');
                continue;
            }
            oldPlayerNames.pop();
        }
        playerNames = oldPlayerNames;
        validateNames();
    }

    function validateCategorySelection() {
        for (let i = 0; i < NUMBER_OF_CATEGORIES; i++) {
            if (selectedCategoriesList[i] === "") {
                validCategories = false;
                return;
            }
        }

        validCategories = true;
        return;
    }

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
        //console.log(initData)
        const newSessionID = generateUniqueID(activeSession);
        sessionID.set(newSessionID);

        activeSession.update(store => {
        const updated = {
                ...store,
                [newSessionID]: initData
            };
            //console.log('Updating session store:', updated);
            return updated;

        });
        console.log('Started new session: ', newSessionID)
        window.electronAPI.openGameSession(newSessionID);
        closePage()

    }

</script>
{#if currentRoute === '#/'}
    <main class="min-h-screen bg-slate-900 text-white flex flex-col">
        <div>
            <!-- Choose Number of Players -->
            <section class="flex flex-col items-center justify-center mt-6">
                <h1 class="text-4xl font-bold">Trivial Compute!</h1>
                <h2 style="margin-top: 1em;">How many players?</h2>
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
            {#if numberOfPlayers !== 0}
                <section class="flex flex-col items-center justify-center mt-6">
                    <h2 style="margin-top: 1em;">Enter your names!</h2>
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

            <!-- Choose Categories -->
            {#if validNames && numberOfPlayers !== 0}
            <section class="flex flex-col items-center gap-6 mt-6 px-4">
                <h2 style="margin-top: 1em;">Pick your game categories!</h2>
                {#each Array(NUMBER_OF_CATEGORIES) as _, num}
                    {#if num === 0 || selectedCategoriesList[num - 1] !== "" }
                        <div class="w-full max-w-md">
                            <select
                                class="w-full p-3 text-white bg-slate-800 border border-indigo-900 border-opacity-70 rounded-md
                                    focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 transition-all duration-200"
                                bind:value={selectedCategoriesList[num]}
                                onchange={() => { validateCategorySelection(); } }
                                >
                                <!-- <Option value={undefined}>Select category</Option> -->
                                {#each categoryOptions as category}
                                    <option
                                    value={category}
                                    disabled={selectedCategoriesList.includes(category) && selectedCategoriesList[num] !== category}
                                    >
                                    {category}
                                    </option>
                                {/each}
                            </select>
                        </div>
                    {/if}
                {/each}
              </section>
            {/if}


            <!-- Start Button -->
            {#if validCategories}
                <section class="flex flex-col items-center justify-center mt-6">
                    <div>
                        <button onclick={newGameSession} class="p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Start Game</button>
                    </div>
                </section>
            {/if}
        </div>
    </main>
{:else if currentRoute === '#/game-session'}
    <GameSession  sessionID={$sessionID} />

{:else}
    <p>404 - Page not found</p>
{/if}

<style>
    select, input {
      background-color: #1E293B;
      border: 2px solid #3B82F6;
      color: white;
      padding: 0.5rem 0.75rem;
      border-radius: 0.4rem;
      width: 100%;
      font-size: 0.95rem;
      transition: border-color 0.3s ease;
    }
  
    input:focus, select:focus {
      outline: none;
      border-color: #FBBF24;
    }
  
    button {
      cursor: pointer;
      border-radius: 0.6rem;
      font-weight: 600;
      transition: background 0.3s ease, box-shadow 0.3s ease;
      font-size: 0.95rem;
    }
  
    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-8px); }
    }
  </style>
  