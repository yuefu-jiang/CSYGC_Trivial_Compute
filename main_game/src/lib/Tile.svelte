<script>
    export let pieces = [];
    export let active = true;
    export let category; // Optional: for colored pieces by category
    export let tileColor;
    export let textColor = '#ffffff';
    export let text;

    // Define layouts for 1-4 pieces
    const pieceLayouts = {
        1: [{ x: 0, y: 0 }], // Center
        2: [{ x: -0.7, y: 0 }, { x: 0.7, y: 0 }], // Side by side
        3: [{ x: 0, y: -0.7 }, { x: -0.7, y: 0.7 }, { x: 0.7, y: 0.7 }], // Triangle
        4: [
            { x: -0.7, y: -0.7 }, // Top-left
            { x: 0.7, y: -0.7 },  // Top-right
            { x: -0.7, y: 0.7 },  // Bottom-left
            { x: 0.7, y: 0.7 }    // Bottom-right
        ]
    };

    // Color mapping for categories (optional)
    const pieceColors = ['bg-blue-500', 'bg-yellow-500', 'bg-red-500', 'bg-green-500'];
    // Calculate current layout based on piece count
    $: currentLayout = pieceLayouts[Math.min(pieces.length, 4)] || [];
</script>

<div class="relative aspect-square  border-1 {!active ? 'opacity-0' : ''}" style="background-color: {tileColor};  border-style: solid; border-color: rgba(255, 255, 255, 1); /* red */">
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 ">
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

</style>