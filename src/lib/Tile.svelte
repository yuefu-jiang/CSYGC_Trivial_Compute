<script>
    export let pieces = [];
    export let active = true;
    export let category;
    export let tileColor;
    export let textColor = '#ffffff';
    export let text;
    export let key;
    export let possibleDest = false;

    // Define layouts for 1-4 pieces
    const pieceLayouts = {
        1: [{ x: 0, y: 0 }],
        2: [{ x: -0.7, y: 0 }, { x: 0.7, y: 0 }],
        3: [{ x: 0, y: -0.7 }, { x: -0.7, y: 0.7 }, { x: 0.7, y: 0.7 }],
        4: [
            { x: -0.7, y: -0.7 },
            { x: 0.7, y: -0.7 },
            { x: -0.7, y: 0.7 },
            { x: 0.7, y: 0.7 }
        ]
    };

    const pieceColors = ['bg-blue-500', 'bg-yellow-500', 'bg-red-500', 'bg-green-500'];
    
    $: currentLayout = pieceLayouts[Math.min(pieces.length, 4)] || [];

    // Dispatch event when tile is clicked
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    function handleClick() {
        if (possibleDest) {
            dispatch('tileClick', { key });
            //console.log(key)
        }
    }
</script>

<div 
    class="relative aspect-square border-1 {!active ? 'opacity-0' : ''} transition-all duration-300 ease-in-out"
    class:possible-destination={possibleDest}
    class:clickable={possibleDest}
    style="background-color: {tileColor}; border-style: solid; border-color: rgba(255, 255, 255, 1);"
    on:click={handleClick}
>
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <h3 class="text-xl" style="color: {textColor}">{text}</h3>
    </div>
    {#each pieces.slice(0, 4) as piece, index}
        <div
            class="absolute w-[35%] h-[35%] rounded-full shadow-md border-2 border-black outline-3 outline-yellow-300 outline-dotted
                   {pieceColors[piece]}"
            style="
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%) 
                          translate({currentLayout[index].x * 100}%, {currentLayout[index].y * 100}%);
            "
        />
    {/each}
</div>

<style>
    .possible-destination {
        box-shadow: 0 0 20px 5px rgba(255, 255, 0, 0.7);
        transform: scale(1.05);
        z-index: 10;
    }

    .clickable {
        cursor: pointer;
    }

    .clickable:hover {
        filter: brightness(1.1);
    }
</style>