<script>
    import { createEventDispatcher } from 'svelte';
    const dispatcher = createEventDispatcher();

    export let autoClose = false;
    let rolling = false;
    let face = 1;

    // Animation state
    let interval;


    async function rollDice() {
        if (rolling) return;
        rolling = true;
        // Animate dice roll
        let ticks = 0;
        interval = setInterval(() => {
            face = Math.floor(Math.random() * 6) + 1;
            ticks++;
            if (ticks > 15) {
                clearInterval(interval);
            }
        }, 50);

        // Call backend
        const backendPort = window.api.getBackendPort();
        const response = await fetch(`http://127.0.0.1:${backendPort}/roll`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const result = await response.json();

        // Finish animation
        setTimeout(() => {
            face = result.roll;
            rolling = false;
            dispatcher('rolled', result);
        }, 900);
        setTimeout(() => dispatcher('close'), 3000);
    }
</script>

<button class="dice-btn" on:click={rollDice} disabled={rolling}>
    <div class="dice-face dice-face-{face}">
        {#if face === 1}
            <span class="dot center"></span>
        {:else if face === 2}
            <span class="dot top-left"></span>
            <span class="dot bottom-right"></span>
        {:else if face === 3}
            <span class="dot top-left"></span>
            <span class="dot center"></span>
            <span class="dot bottom-right"></span>
        {:else if face === 4}
            <span class="dot top-left"></span>
            <span class="dot top-right"></span>
            <span class="dot bottom-left"></span>
            <span class="dot bottom-right"></span>
        {:else if face === 5}
            <span class="dot top-left"></span>
            <span class="dot top-right"></span>
            <span class="dot center"></span>
            <span class="dot bottom-left"></span>
            <span class="dot bottom-right"></span>
        {:else if face === 6}
            <span class="dot top-left"></span>
            <span class="dot top-right"></span>
            <span class="dot middle-left"></span>
            <span class="dot middle-right"></span>
            <span class="dot bottom-left"></span>
            <span class="dot bottom-right"></span>
        {/if}
    </div>
    <span>{rolling ? 'Rolling...' : 'Roll Dice'}</span>
</button>

<style>
.dice-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: #222;
    border-radius: 1rem;
    border: 2px solid #444;
    cursor: pointer;
    min-width: 100px;
    min-height: 100px;
    margin: 1rem;
    transition: background 0.2s;
}
.dice-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
.dice-face {
    width: 48px;
    height: 48px;
    background: #fff;
    border-radius: 8px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 2px;
    margin-bottom: 0.5rem;
    position: relative;
}
.dot {
    width: 10px;
    height: 10px;
    background: #222;
    border-radius: 50%;
    position: absolute;
}
.center { top: 50%; left: 50%; transform: translate(-50%, -50%); }
.top-left { top: 8px; left: 8px; }
.top-right { top: 8px; right: 8px; }
.bottom-left { bottom: 8px; left: 8px; }
.bottom-right { bottom: 8px; right: 8px; }
.middle-left { top: 50%; left: 8px; transform: translateY(-50%); }
.middle-right { top: 50%; right: 8px; transform: translateY(-50%); }
</style> 