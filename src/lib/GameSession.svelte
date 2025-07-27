<script>
	import csygcLogo from "../assets/csygcLogo.png"
	import Counter from "./Counter.svelte"
	import { writable } from 'svelte/store';
	import { activeqID } from '../session_store.js'
	import { activeSession } from '../session_store.js'
 	import Tile from './Tile.svelte';
	import { onMount } from 'svelte';
	import Dice from './Dice.svelte';
	import Overlay from './Overlay.svelte';

	let showOverlayDice = false;

	export let sessionID;

	onMount(async () => {
		const hash = window.location.hash;
		const params = new URLSearchParams(hash.split('?')[1]);
		sessionID = params.get('id');

		const backendPort = window.api.getBackendPort()
        const response = await fetch(`http://127.0.0.1:${backendPort}/init_questions`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': 'new session' }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();
        const initData = result.data

		activeSession.update(store => {
		const updated = {
				...store,
				...initData
			};
			//console.log('Updating session store:', updated);
			return updated;
		});
		console.log('Started session:', sessionID)
		getcolor();
		getallposition();
		getnames();
		getq();
		initPlayerWedges();
		updateGridSize();
		resizeObserver = new ResizeObserver(updateGridSize);
		if (containerRef) resizeObserver.observe(containerRef);

	});

	function updateGridSize() {
		if (containerRef) {
	        const containerWidth = containerRef.offsetWidth;
	        tileSize = containerWidth / boardSize;
	        //console.log(tileSize)
	  	}
	}

	$: if (containerRef) updateGridSize();


	//console.log("Backend port:", window.api.getBackendPort(), sessionID);
	let resizeObserver;
	let displayResultTest;
	let displayMsgTest;
	let displayMsgQ;
	let displayMsgA;
	let displayAnswerTest;
	let containerRef;
	let tileSize;
	let category ='science'; // TEMP: fix at science for now
	let qid;
	let question;
	//let players = ['p1', 'p2', 'p3', 'p4'] // TEMP: from backend
	let players = [];
    //id for current player
	let activePiece = 0; 
	//square type of current player
	let activeSq_type;
	// This is the color dict
    let inverseDictColor = {};
	// player position dic
    let piecesPerTile = {};
	// possible destination after roll dice
	let possibleDestinations = [];
    //let selected_cat = ["Geography", "History", "Math", "Computer Science"]
	// list of all selected question type, get from backend
	let selected_cat = [];
    // Precompute tiles
    let tiles = [];
	// this is the player collected wedges status
	// playerTiles["david"]=[{key:'0,0',rol:0,col:0,tileColor:"#000000",active:True},{},{},{}]
	// each player has four wedges tiles
    let playerTiles = {};
	//winning status
	let Iswin = false;
	//winner list
	let winlist = [];

	function getRandomItem(list) {
		if (!Array.isArray(list) || list.length === 0) return null;
		const index = Math.floor(Math.random() * list.length);
		return list[index];
	}

	// function for fetching question from backend
	async function fetchQuestion() {
		const currCatQlist = [...$activeSession[category]]
		qid = getRandomItem(currCatQlist)

		const backendPort = window.api.getBackendPort()

		const startTime = Date.now();

		console.log('Sending request to get question from front end. Port: ', backendPort);
		const response = await fetch(`http://127.0.0.1:${backendPort}/question?category=${category}&qid=${qid}`, {
			headers: { 'Content-Type': 'application/json' },
            method: 'GET',
		});
		const result = await response.json();


        displayResultTest = true;
        displayMsgQ = result.data.question;
        displayMsgA = result.data.answer;
        // print out the response

        const endTime = Date.now();
        console.log('result QA pair: ', result.data)
        console.log('Fetching question/answer took', endTime-startTime, 'ms')

        displayAnswerTest = false;

	}


    function hideTestDiv () {
    	displayResultTest = false;
    }

    function showAnswerDiv() {
		displayAnswerTest = true;
    }

    const boardSize = 9;

    // This method is to set the active tiles.
    // Hides the "useless" tiles that are not spoke nor edges
    let activeTiles = new Set([
		// Top and bottom rows
		...Array(9).fill(0).map((_, i) => `0,${i}`),
		...Array(9).fill(8).map((_, i) => `8,${i}`),

		// Left and right columns (excluding corners, already included above)
		...Array(7).fill(0).map((_, i) => `${i + 1},0`),
		...Array(7).fill(0).map((_, i) => `${i + 1},8`),

		// Middle row (row 4)
		...Array(9).fill(4).map((r, i) => `${r},${i}`),

		// Middle column (col 4)
		...Array(9).fill(0).map((_, i) => `${i},4`)
    ]);


    // number representing player
    // player 0 = blue, 1 = yellow, 2 = red, 3 = green
    // This is the initial dictionary to update. 
    // TODO: fetch the init pos from backend
    /*let piecesPerTile = {
	    '0,1': [0,1,2],
	    '0,2': [3],
    };*/

	// TODO: get color from backend, run at launch
    async function getcolor() {

        const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};
		console.log('getting color with session: ', sessionID)
		//route to get color
		console.log("getting board color grid", backendPort)
        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getboardcolor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		inverseDictColor = result.color;
        const msg = result.msg;
        console.log('get color result', msg)
    }
    // update current position of all players from backend, run when called
	async function getallposition() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};
		console.log('getting position: ', sessionID)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getallpos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		piecesPerTile = result.pos;
        const msg = result.msg;
        console.log('get pos result', msg)
    }

    // get namelist of all players from backend, run when called
	async function getnames() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};
		console.log('getting names: ', sessionID)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getnames`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		players = result.name;
		console.log('names: ', players)
        const msg = result.msg;
        console.log('get name result', msg)
    }

    // get a complete question category list from backend, run when called
	async function getq() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};
		console.log('getting question: ', sessionID)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getqtype`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		selected_cat = result.qtype;
		console.log('question types', selected_cat)
        const msg = result.msg;
        console.log('get question result', msg)
    }

    // get valid position list from backend, run when called
	async function getvalidmove(tid,steps) {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
			tid: tid,
			steps: steps,
		};
		console.log('getting valid move: ', sessionID)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getvalidmove`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		possibleDestinations = result.valid_list;
		console.log('valid move', possibleDestinations)
        const msg = result.msg;
        console.log('get valid move result', msg)
    }

	// move a player in backend
	async function moveToDes(tid,locationKey) {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
			tid: tid,
			locationKey: locationKey,
		};
		console.log('sending a move on game:', sessionID,' for player', tid)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/moveToDes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
        const msg = result.msg;
        console.log('move result', msg)
    }

	// get and update all player wedges displayed
	async function getallWedge() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};
		console.log('getting player wedges:', sessionID)

        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getallWedge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
        // update the playerTiles object
		playerTiles = result.allwedge;
		const msg = result.msg;
        console.log('update: ', msg)
    }

	// add a wedge to player collected wedges
    // need an input of color
	async function addwedge(tid,qtype) {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
			tid: tid,
			qtype:qtype,
		};
		console.log('updating color of game:', sessionID,' for player', tid, ' with wedge for type: ', qtype)
        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/addwedge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
        const msg = result.msg;
        console.log('added result', msg)
    }

    // get the square type of a current player
	async function getSquareType(tid) {
		const backendPort = window.api.getBackendPort()
		const gameinput = {
			gameid: sessionID,
			tid: tid,
		};
		console.log('getting square type at game:', sessionID,' for player', tid,)
        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getSquareType`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		activeSq_type = result.sqtype;
		console.log('square type got=', activeSq_type)
        const msg = result.msg;
        console.log('square type result', msg)
		return result.sqtype;
    }

    // get the question type of a current square, using current player as reference and update category
	async function getCurrentCat(tid) {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
			tid: tid,
		};

		console.log('getting question type at game:', sessionID,' for player', tid,)
        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/getCurrentCat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		category = result.category;
        const msg = result.msg;
        console.log('question type result', msg)
		return result.category;
    }

    // get the player id who win
	async function anyoneWin() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};

		console.log('find anyone win for game:', sessionID)
        const initialize_response = await fetch(`http://127.0.0.1:${backendPort}/anyoneWin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameinput)
        });
		const result = await initialize_response.json();
		Iswin = result.Winstatus;
        winlist = result.win_list;
        console.log('winning list retrieved');
    }

	/*const inverseDictColor = {
	    "0,1": "#1f77b4",
	    "0,5": "#1f77b4",
	    "1,4": "#1f77b4",
	    "2,8": "#1f77b4",
	    "4,0": "#1f77b4",
	    "4,6": "#1f77b4",
	    "5,4": "#1f77b4",
	    "6,8": "#1f77b4",
	    "8,1": "#1f77b4",
	    "8,5": "#1f77b4",
	    "0,2": "#ff7f0e",
	    "0,6": "#ff7f0e",
	    "2,4": "#ff7f0e",
	    "3,0": "#ff7f0e",
	    "3,8": "#ff7f0e",
	    "4,1": "#ff7f0e",
	    "4,5": "#ff7f0e",
	    "7,0": "#ff7f0e",
	    "7,8": "#ff7f0e",
	    "8,4": "#ff7f0e",
	    "0,3": "#2ca02c",
	    "0,7": "#2ca02c",
	    "2,0": "#2ca02c",
	    "3,4": "#2ca02c",
	    "4,2": "#2ca02c",
	    "4,8": "#2ca02c",
	    "6,0": "#2ca02c",
	    "7,4": "#2ca02c",
	    "8,3": "#2ca02c",
	    "8,7": "#2ca02c",
	    "0,4": "#d62728",
	    "1,0": "#d62728",
	    "1,8": "#d62728",
	    "4,3": "#d62728",
	    "4,7": "#d62728",
	    "5,0": "#d62728",
	    "5,8": "#d62728",
	    "6,4": "#d62728",
	    "8,2": "#d62728",
	    "8,6": "#d62728"
	}
    */

	// reactive statement
	// This will monitor changes on piece pos change
	// also defined what was displayed on which tile
    $: {
        tiles = [];
        for (let row = 0; row < boardSize; row++) {
            for (let col = 0; col < boardSize; col++) {
                const key = `${row},${col}`;
                let currColor;
                let currText;
                let txColor;
                if (key == '0,0' || key == '0,8' ||key == '8,0' ||key == '8,8') {
                	currColor = '#ffffff'
                	txColor = '#000000'
                	currText = 'RA'}
                else if (key == '4,4') {
                	currColor = '#ffffff'
                	txColor = '#000000'
                	currText = 'TC!'
                } else {
                	currColor = inverseDictColor[key]
                }

                if (key == '0,4' ||key == '4,0' || key == '4,8' || key == '8,4') {
                	currText = 'HQ'
                }

                tiles.push({
                	key,
                    row,
                    col,
                    active: activeTiles.has(key),
                    pieces: piecesPerTile[key] ?? [],
                    tileColor: currColor,
                    textColor: txColor,
                    text: currText,
                });
            }
        }
		console.log(playerTiles)
    }

    // This is to initialize the wedges for each player
    // TODO: display according to player count
    function updatePlayerWedges() {
		getallWedge();
    }	
    
    // This is to initialize the wedges for each player
    // TODO: display according to player count
    function initPlayerWedges() {
    	for (let pIndex = 0; pIndex < players.length; pIndex++) {
    		playerTiles[players[pIndex]] = [];
	        for (let row = 0; row < 2; row++) {
	            for (let col = 0; col < 2; col++) {
	                const key = `${row},${col}`;

	                playerTiles[players[pIndex]].push({
	                	key,
	                    row,
	                    col,
						tileColor:"#000000",
	                    active: true,
	                });
	            }
	        }
    	}

    }

    // Function that actually got used by button
    // TODO: hook this with backend return

	function handleRolled(event) {
		let lastRollResult = null;
		lastRollResult = event.detail; // Contains { roll: number }
		console.log("Rolled:", lastRollResult.roll);

		// TODO: get the next piece position
		// This can be done by returning the roll result to backend
		getvalidmove(activePiece,lastRollResult.roll);

	}


	function handleClose() {
		showOverlayDice = false;
	}

	// Handle click outside content (now properly bound to DOM element)
	function handleOverlayClick(e) {
		if (e.target === e.currentTarget) {
			handleClose();
		}
	}

	async function handleTileClick(event) {
		// The key is available in event.detail.key
		const clickedTileKey = event.detail.key;
		console.log('Selected tile:', clickedTileKey);
        //The key is in format str: 0,2
		// Do something with the key, like move a player piece
		await movePlayer(clickedTileKey);
        // clear lighting
		possibleDestinations = [];
		// update all player position
		await getallposition();
		// get the current type of squares from backend for current player
        const temp_type = await getSquareType(activePiece);
		// 1) Roll again->nothing, 2) normal & hq ->get question type, 3) center-->pick question type
        if (temp_type === "HQ") {
			//get the question type of the square
			const temp_cat = await getCurrentCat(activePiece);
		    // fetch question and answer, using the category variable
        
		    // if correct, update wedges, using the category variable
            await addwedge(activePiece,temp_cat);
			activePiece = await (activePiece+1)%players.length;
		}
		else if (temp_type === "NL"){
			//get the question type of the square
			const temp_cat = await getCurrentCat(activePiece);
		    // fetch question and answer, using the category variable
        
			const answercorrect = false
		    // if incorrect, update activepiece
			if (!answercorrect){
				activePiece = await (activePiece+1)%players.length;
			}
		}
		else if (temp_type === "CT"){
			//prompt user to pick question type and update category variable
			const temp_cat = await getCurrentCat(activePiece);
		    // fetch question and answer, using the category variable
        
		    // if correct, update wedges, using the category variable
            await addwedge(activePiece,temp_cat);
			activePiece = await (activePiece+1)%players.length;
		}
		// update the display of player wedges
		await updatePlayerWedges();
		// check winning status
        await anyoneWin();
		if (Iswin){
			//some one win, the global variable winlist will be updated by updatePlayerWedges()
			// check the winner player id from the list, 
			// display winning message
			// end game
			// pending

		}
	}

	function movePlayer(destinationKey) {
		// TODO: send destinationKey to backend, update board layout, then call updateposition()
        moveToDes(activePiece,destinationKey)

    	//updatePieceLoc(newLocObj)
		console.log('Moving player to', destinationKey);
	}

</script>

<main class="min-h-screen bg-slate-900 text-white flex flex-col">
	<!-- header -->
	<section class="flex flex-col justify-center items-center h-24">
		<div class="flex h-10 w-full"></div>
		<div class="flex items-center space-x-4 gap-4 md:gap-16 flex-wrap">
			<a href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/" target="_blank" rel="noreferrer">
				<img
					class="absolute left-4 top-4 h-16 hover:drop-shadow-[0_0_2rem_#ac00ac] transition-all duration-300"
					src={csygcLogo}
					alt="Vite logo"
				/>
			</a>
		<div class="items-center justify-between">
			<button on:click={() => showOverlayDice = true} class="absolute right-4 top-4 h-16   duration-300 p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300">Roll Dice</button>


		<Overlay bind:show={showOverlayDice} >
			<h2> Dice Roll! </h2>
			<Dice 
				autoClose={true}
				on:close={handleClose}
				on:rolled={handleRolled}
			/>
		</Overlay>


		</div>
			
		</div>
		<h1 class="mt-10 text-3xl font-bold">Trivial Compute!</h1>
	</section>

	
	<!-- Middle Part -->
	<section class="flex flex-row items-center justify-center mt-6 mr-10 ml-10">

		<div
			bind:this={containerRef}
		    class="w-full max-w-[80vmin] aspect-square grid relative"
		    style={`grid-template-columns: repeat(${boardSize}, 1fr);`
			}
		>
		    {#each tiles as tile}
		        <Tile key={tile.key} active={tile.active} pieces={tile.pieces} tileColor={tile.tileColor} text={tile.text} textColor={tile.textColor} possibleDest={possibleDestinations.includes(tile.key)} on:tileClick={handleTileClick}/>
		    {/each}
		    <div class="absolute"
		    	style="left: {tileSize}px;
		    			top: {tileSize}px;
		    			width: {tileSize*3}px;
		    			height: {tileSize*3}px;
		    			">
			    <div class="h-1/3 ">

			    		<h2 style=" color: #3b82f6;" > {Object.keys(playerTiles)[0]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[Object.keys(playerTiles)[0]] as ptile}
					        <Tile active={ptile.active} tileColor={ptile.tileColor}/>
					    {/each}
			    	</div>

			    </div>
			</div>
		    <div class="absolute"
		    	style="left: {tileSize*5}px;
		    			top: {tileSize}px;
		    			width: {tileSize*3}px;
		    			height: {tileSize*3}px;
		    			">
			    <div class="h-1/3 ">

			    		<h2 style=" color: #eab308;" > {Object.keys(playerTiles)[1]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[Object.keys(playerTiles)[1]] as ptile}
					        <Tile active={ptile.active} tileColor={ptile.tileColor}/>
					    {/each}
			    	</div>

			    </div>
			</div>
		    <div class="absolute"
		    	style="left: {tileSize}px;
		    			top: {tileSize*5}px;
		    			width: {tileSize*3}px;
		    			height: {tileSize*3}px;
		    			">
			    <div class="h-1/3 ">

			    		<h2 style=" color: #ef4444;" > {Object.keys(playerTiles)[2]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[Object.keys(playerTiles)[2]] as ptile}
					        <Tile active={ptile.active} tileColor={ptile.tileColor}/>
					    {/each}
			    	</div>

			    </div>
			</div>

		    <div class="absolute"
		    	style="left: {tileSize*5}px;
		    			top: {tileSize*5}px;
		    			width: {tileSize*3}px;
		    			height: {tileSize*3}px;
		    			">
			    <div class="h-1/3 ">

			    		<h2 style=" color: #22c55e;" > {Object.keys(playerTiles)[3]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[Object.keys(playerTiles)[3]] as ptile}
					        <Tile active={ptile.active} tileColor={ptile.tileColor}/>
					    {/each}
			    	</div>

			    </div>
			</div>
		</div>

		<div class="aspect-square bg-white-500 border border-gray-400 rounded-sm">
			
		</div>
	</section>


</main>