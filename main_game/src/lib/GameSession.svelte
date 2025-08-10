<script>
	import csygcLogo from "../assets/csygcLogo.png"
	import Counter from "./Counter.svelte"
	import { writable } from 'svelte/store';
	import { activeqID } from '../session_store.js'
	import { activeSession, playerResponse, selectedCat } from '../session_store.js'
 	import Tile from './Tile.svelte';
	import { onMount } from 'svelte';
	import Dice from './Dice.svelte';
	import Overlay from './Overlay.svelte';
	import QuestionModal from './QuestionModal.svelte';


	let showOverlayDice = false;
	let showCatOverlay = false;
	let currDir
	let playerSwitch = false;


	export let sessionID;

	onMount(async () => {
		const hash = window.location.hash;
		const params = new URLSearchParams(hash.split('?')[1]);
		sessionID = params.get('id');

        currDir = await window.electronAPI.returnDir();
		console.log(currDir)
		console.log(typeof currDir)

		const backendPort = window.api.getBackendPort()
        const response = await fetch(`http://127.0.0.1:${backendPort}/init_questions`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': currDir }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();
        const initData = result.data

		//const selectedDir = await window.electronAPI.selectDir('export');
		//showDataDir = true;
		//selectedDir = handleSelectDir();
        const qdir = '../questions.json'
        const allq = await window.electronAPI.readFile(currDir);

        //console.log(allq)

        console.log('question data:', result)

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
		getallWedge(); // to display wedge at startup
		updateGridSize();
		getColorCatDict();

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
	// piece color
	let pieceColors = ['bg-blue-500', 'bg-yellow-500', 'bg-red-500', 'bg-green-500']; // fixed for now
	let playerTextColor = ['#3b82f6','#eab308','#ef4444','#22c55e']; // fixed for now
    //id for current player
	let activePiece = 0; 
	//square type of current player
	// "CT" "NL" "HQ"
	let activeSq_type;
	// the mapping of color and category
	let colorCatObj = {};
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
	//winning possible player list
	let winlist = [];
	//state of current player winning eligbility
	let ActiveplayerCanWin = false;
	// boolean var to store player answer. Updated by handleAnswered(evt)
	let currentPlayerAnswer = false;

	// Question popup variables ---------------------------------
	let showQuestionModal = false;
	let modalQuestion = "";
	let modalAnswer = "";
	let constested = writable(false);
	let gameWon = writable(false);
	let showDataDir = false;
	let selectedDir;

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
        //console.log('question type result', msg)
		return result.category;
    }
    //get color: category info
	async function getColorCatDict() {
		const backendPort = window.api.getBackendPort()

		const gameinput = {
			gameid: sessionID,
		};

        const res = await fetch(`http://127.0.0.1:${backendPort}/getcolorcatdict`, {
        	method: 'POST',
        	headers: { 'Content-Type': 'application/json' },
        	body: JSON.stringify(gameinput)
        });

		const result = await res.json();
		

		colorCatObj = result.data.reduce((acc, [_, hex, category]) => {
		    acc[hex] = category;
		    return acc;
		}, {});
		console.log('Cat:color', colorCatObj)

		
	}
    // update the list of winning eligible player list:e.g. [0,1]
	async function anyoneCanWin() {
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
        console.log('winning list retrieved', winlist);
    }

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
                let currCategory; //for hover text
                if (key == '0,0' || key == '0,8' ||key == '8,0' ||key == '8,8') {
                	currColor = '#ffffff'
                	txColor = '#000000'
                	currText = 'RA'
                	currCategory = 'Roll Again!'}
                else if (key == '4,4') {
                	currColor = '#ffffff'
                	txColor = '#000000'
                	currText = 'TC!'
                	currCategory = 'Trivial Compute!'
                } else {
                	currColor = inverseDictColor[key]
                	currCategory = colorCatObj[currColor]
                }

                if (key == '0,4' ||key == '4,0' || key == '4,8' || key == '8,4') {
                	currText = 'HQ'
                }
                //console.log(tiles)
                tiles.push({
                	key,
                    row,
                    col,
                    active: activeTiles.has(key),
                    pieces: piecesPerTile[key] ?? [],
                    tileColor: currColor,
                    category: currCategory,
                    textColor: txColor,
                    text: currText,
                });
            }
        }
		//console.log(playerTiles)
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
		getColorCatDict();
		// get the current type of squares from backend for current player
        let temp_type = await getSquareType(activePiece);
		// 1) Roll again->nothing, 2) normal & hq ->get question type, 3) center-->pick question type
        if (temp_type === "HQ") {
			//get the question type of the square
			let temp_cat = await getCurrentCat(activePiece);
			await openQuestionModal(temp_cat);
			//let answercorrect = currentPlayerAnswer;
		    // fetch question and answer, using the category variable
        
			// temporarily assume correct for game testing
			//answercorrect = true;
		    // if correct, update wedges, using the category variable
		    const isCorrect = await waitForUserAnswer();
		    console.log(isCorrect)
			if (isCorrect){
				await addwedge(activePiece,temp_cat);
			}
			//revert to false
			currentPlayerAnswer = false;	
		}
		else if (temp_type === "NL"){
			//get the question type of the square

			let temp_cat = await getCurrentCat(activePiece);
			await openQuestionModal(temp_cat);

		}
		else if (temp_type === "CT"){

			//prompt user to pick question type and update category variable
			//temp_cat e.g. Math
			//showCatOverlay = true; //question handled in handle

			//$selectedCat = '';
			//update the list of players who has all 4 wedges
			await anyoneCanWin();
			ActiveplayerCanWin = false;
			playerTiles[players[activePiece]]

			const colorExists = playerTiles[players[activePiece]].some(tile => tile.tileColor === "#000000");

			console.log(colorExists)

			if (!colorExists) {
				ActiveplayerCanWin = true;
				$constested = true;
				showCatOverlay = true;
			} else {
				showCatOverlay = true; //question handled in handle
			}


			// temp frontend fix

			// if (winlist.includes(activePiece)){
			// //Iswin = true when winlist is not empty, updated by anyoneCanWin()
			// // check if the winner player id inside the list, if yes, store winning possible states
			// 	ActiveplayerCanWin = true;
			// }

		    // fetch question and answer, using the category variable
			// then update the answercorrect
			

		    // if correct, and ActiveplayerCanWin=true,player win.
			// if correct, and ActiveplayerCanWin=false, update wedges, using the category variable
			// if not correct, nothing happen, next player
			if ($playerResponse == true && ActiveplayerCanWin){
				//display winning msg
				//end the game

				console.log(players[activePiece], ' wins!')

			}
			// else if(answercorrect && !ActiveplayerCanWin)
			// {
			// 	//add the wedges and next player
			// 	//await addwedge(activePiece,temp_cat);
			// 	activePiece = await (activePiece+1)%players.length;
			// }
			// else if(!answercorrect && !ActiveplayerCanWin)
			// {
			// 	//next player
			// 	activePiece = await (activePiece+1)%players.length;
			// }
			
		}
		// update the display of player wedges
		await updatePlayerWedges();
		// check winning status
		// anyoneCanWin update the list of winning eligible player list:e.g. [0,1]
        await anyoneCanWin();
	}

	async function movePlayer(destinationKey) {
		// TODO: send destinationKey to backend, update board layout, then call updateposition()
        await moveToDes(activePiece,destinationKey)
        console.log(activePiece, destinationKey)

    	//updatePieceLoc(newLocObj)
		console.log('Moving player to', destinationKey);
	}
	// to remove a used question from session store
	function removeElement(category, qid) {
	    activeSession.update(current => {
	        // Create a new object with the updated array
	        return {
	            ...current,
	            [category]: current[category].filter(item => item !== qid)
	        };
	    });
	}


	// reset the ctegory if list got used up
	async function resetCatList(category) {
		const backendPort = window.api.getBackendPort()
        const response = await fetch(`http://127.0.0.1:${backendPort}/init_questions`, {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'data': currDir }),
            method: 'POST',
        });
        // wait for result. If anything goes wrong it will fail to fetch
        const result = await response.json();
        const catData = result.data[category]
        console.log('Resetting category', category)
	    activeSession.update(current => {
	        // Create a new object with the updated array
	        return {
	            ...current,
	            [category]: catData,
	        };
	    });

	}
	/**
	 * Function to open question modal
	 */
	async function openQuestionModal(category) {
		const currCatQlist = [...$activeSession[category]];

		//reset if used up
		if (currCatQlist.length === 0) {
			resetCatList(category)
		};
		const qid = getRandomItem(currCatQlist);
		const backendPort = window.api.getBackendPort();

		const question_param = {
			'category': category,
			'qid': qid,
			'path': currDir,
		}
		try {
	        const res = await fetch(`http://127.0.0.1:${backendPort}/get_question`, {
	        	method: 'POST',
	        	headers: { 'Content-Type': 'application/json' },
	        	body: JSON.stringify(question_param)
	        });
			const result = await res.json();
			modalQuestion = result.data.question;
			modalAnswer = result.data.answer;
			showQuestionModal = true;
			console.log("Fetched Q&A:", result.data);
			removeElement(category, qid)
			// to remove question to avoid redundancy
			//console.log($activeSession)
			return 
		} catch (err) {
			console.error("Failed to fetch question:", err);
		}
	}

	let resolveUserAnswer; // Stores the Promise resolver

	// Function that returns a Promise waiting for the user's answer
	function waitForUserAnswer() {
		return new Promise((resolve) => {
			resolveUserAnswer = resolve; // Save the resolver for later
		});
	}
	function handleAnswered(event) {
		const isCorrect = event.detail.wasCorrect;

		if (!isCorrect) {
			console.log('Wrong!');
			playerSwitch = true;
			activePiece = (activePiece + 1) % players.length;
			$constested = false;
		} else {
			console.log('Right!');
			if ($constested) {
				console.log('Somebody Wins!!!');
				$gameWon = true;
			}
		$constested = false;
		}

		// Resolve the Promise (if it exists)
		if (resolveUserAnswer) {
			resolveUserAnswer(isCorrect); 
			resolveUserAnswer = null; // Clean up
		}
	}

	function handleSelectCat(cat){
		console.log('Selected ', cat)
		showCatOverlay = false;
		$selectedCat = cat;
		openQuestionModal(cat);
	}

	async function handleSelectDir() {
		selectedDir = await window.electronAPI.selectDir('export');
		
	}

	function togglePlayerSwitch () {
		playerSwitch = false;
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
			<button
				disabled={possibleDestinations.length !== 0}
				on:click={() => showOverlayDice = true}
				class="absolute right-4 top-4 h-16 p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md
					transition-all duration-300
					hover:border-indigo-500 hover:bg-slate-800
					disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-gray-700 disabled:border-gray-500"
			>
				Roll Dice
			</button>

		<Overlay bind:show={showOverlayDice} >
			<h2> Dice Roll! </h2>
			<Dice
				disabled={false}
				autoClose={true}
				on:close={handleClose}
				on:rolled={handleRolled}
			/>
		</Overlay>



		<Overlay bind:show={showCatOverlay} >
			{#if ActiveplayerCanWin}
			<h2> Opponents choose a WINNING category!! </h2>
			<div class="flex  flex-col">
				{#each selected_cat as cat}
					<button class="duration-300 p-4 mt-4 bg-slate-800 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-700 transition-all duration-300 mt-4 ml-4 mr-4" on:click={() => handleSelectCat(cat)}>
						{cat}
					</button>
				{/each}
			</div>
			{:else}
			<h2> {players[activePiece]} choose a category! </h2>
			<div class="flex  flex-col">
				{#each selected_cat as cat}
					<button class="duration-300 p-4 mt-4 bg-slate-800 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-700 transition-all duration-300 mt-4 ml-4 mr-4" on:click={() => handleSelectCat(cat)}>
						{cat}
					</button>
				{/each}
			</div>
			{/if}
		</Overlay>
		<Overlay bind:show={showDataDir} >
			<button class="duration-300 p-4 mt-4 bg-slate-800 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-700 transition-all duration-300 mt-4 ml-4 mr-4" on:click={() => handleSelectDir()}>
				Select data directory
			</button>
		</Overlay>

		<Overlay bind:show={playerSwitch} on:close={() => togglePlayerSwitch()}>
			<h1> {players[activePiece]}'s turn!</h1>
		</Overlay>
		<Overlay bind:show={showDataDir} >
			<button class="duration-300 p-4 mt-4 bg-slate-800 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-700 transition-all duration-300 mt-4 ml-4 mr-4" on:click={() => handleSelectDir()}>
				Select data directory
			</button>
		</Overlay>

		<Overlay bind:show={playerSwitch} on:close={() => togglePlayerSwitch()}>
			<h1> {players[activePiece]}'s turn!</h1>
		</Overlay>

		<Overlay bind:show={$gameWon} >
			<h1> {players[activePiece]} Won!!! </h1>
		</Overlay>


		</div>
			
		</div>
		<h1 class="pt-10  text-3xl font-bold">Trivial Compute!</h1>
		<div class="flex flex-row">
			<h2 class="mt-6 mb-2 text-xl font-bold" style="color: white;"> Now playing: </h2>
			<h2 class="pl-2 mt-6 mb-2 text-xl font-bold" style="color: {playerTextColor[activePiece]};"> {players[activePiece]} </h2>
		</div>
	</section>

	
	<!-- Middle Part -->
	<section class="flex flex-row items-center justify-center mt-6 mr-10 ml-10 min-h-96">

		<div
			bind:this={containerRef}
		    class="w-full max-w-[80vmin] aspect-square grid relative"
		    style={`grid-template-columns: repeat(${boardSize}, 1fr);`
			}
		>
		    {#each tiles as tile}
		        <Tile key={tile.key} active={tile.active} pieces={tile.pieces} tileColor={tile.tileColor} text={tile.text} category={tile.category} textColor={tile.textColor} possibleDest={possibleDestinations.includes(tile.key)} on:tileClick={handleTileClick}/>
		    {/each}
		    <div class="absolute"
		    	style="left: {tileSize}px;
		    			top: {tileSize}px;
		    			width: {tileSize*3}px;
		    			height: {tileSize*3}px;
		    			">
			    <div class="h-1/3 ">

			    		<h2 style=" color: #3b82f6;" > {players[0]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[players[0]] as ptile}
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

			    		<h2 style=" color: #eab308;" > {players[1]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[players[1]] as ptile}
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

			    		<h2 style=" color: #ef4444;" > {players[2]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[players[2]] as ptile}
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

			    		<h2 style=" color: #22c55e;" > {players[3]} </h2>
			    </div>
			    <div class="h-2/3 flex items-center justify-center">
			    	<div class="h-3/4 aspect-square grid relative"
			    	style={`grid-template-columns: repeat(2, 1fr);`
					}>
					    {#each playerTiles[players[3]] as ptile}
					        <Tile active={ptile.active} tileColor={ptile.tileColor}/>
					    {/each}
			    	</div>

			    </div>
			</div>
		</div>

		<div class="aspect-square bg-white-500 border border-gray-400 rounded-sm">
			<QuestionModal bind:open={showQuestionModal} category={category} question={modalQuestion} answer={modalAnswer} on:answered={handleAnswered} />
		</div>
	</section>
</main>