<script lang="ts">
	import { Table } from "@flowbite-svelte-plugins/datatable";
	import rawData from "../../../questions.json";
	import csygcLogo from "../assets/csygcLogo.png";
	import type { DataTable, DataTableOptions } from "simple-datatables";
	import AddQuestionModal from "./AddQuestionModal.svelte";
	import ImportJsonModal from "./ImportJsonModal.svelte";
	let openAddQuestionModal = $state<boolean>(false);
	let selectedId = $state<string>("");
	let selectedCategory = $state<string>("");
	let selectedQuestion = $state<string>("");
	let selectedAnswer = $state<string>("");
	const buttonClass =
		"p-4 mt-4 border border-indigo-900 border-opacity-80 rounded-md hover:border-indigo-500 hover:bg-slate-800 transition-all duration-300";
	let isEditMode = $state<boolean>(false);
	let editPrefill = $state<{
		id?: string;
		category?: string;
		question?: string;
		answer?: string;
	} | null>(null);

	let openAddByJsonModal = $state<boolean>(false);

	function showJsonModalClick() {
		openAddByJsonModal = true;
		console.log("tada")
	}

	function handleRowSelect(
		rowIndex: number,
		_event: Event,
		dataTable: DataTable,
	) {
		const rowObj = (dataTable as any).data?.data?.[rowIndex];
		if (!rowObj) return;

		const rowTexts: string[] = rowObj.cells.map((c: any) => c.text);
		// Destructure correctly into your module-level vars

		if (!rowObj.selected) {
			// not selected and will become selected after click
			[selectedId, selectedCategory, selectedQuestion, selectedAnswer] =
				rowTexts;
		} else {
			selectedId = "";
			selectedCategory = "";
			selectedQuestion = "";
			selectedAnswer = "";
		}

		console.log("saved vars", {
			selectedId,
			selectedCategory,
			selectedQuestion,
			selectedAnswer,
		});
	}

	// Transform nested object into flat array for the table
	const items = Object.entries(rawData).flatMap(([category, questions]) =>
		Object.entries(questions).map(([id, q]) => ({
			id,
			category,
			question: q.question,
			answer: q.answer,
		})),
	);

	const { onBack } = $props<{
		onBack: () => void;
	}>();

	const selectRowsOptions = {
		rowRender: (row: any, tr: any, _index: number) => {
			if (!tr.attributes) {
				tr.attributes = {};
			}
			if (!tr.attributes.class) {
				tr.attributes.class = "";
			}
			if (row.selected) {
				tr.attributes.class += " selected";
			} else {
				tr.attributes.class = tr.attributes.class.replace(
					" selected",
					"",
				);
			}
			return tr;
		},
	};

	const filterOptions: DataTableOptions = {
		tableRender: (data: any[], table: any, type: string) => {
			if (type === "print") {
				return table;
			}

			const tHead = table.childNodes[0];
			const filterHeaders = {
				nodeName: "TR",
				attributes: {
				class: "search-filtering-row"
				},
				childNodes: tHead.childNodes[0].childNodes.map((_th: any, index: number) => ({
				nodeName: "TH",
				childNodes: [
					{
					nodeName: "INPUT",
					attributes: {
						class: "datatable-input",
						type: "search",
						placeholder: `Filter column ${index + 1}`,
						"data-columns": `[${index}]`
					}
					}
				]
				}))
			};

			tHead.childNodes.push(filterHeaders);
			return table;
		},
		rowRender: (row: any, tr: any, _index: number) => {
			if (!tr.attributes) {
				tr.attributes = {};
			}
			if (!tr.attributes.class) {
				tr.attributes.class = "";
			}
			if (row.selected) {
				tr.attributes.class += " selected";
			} else {
				tr.attributes.class = tr.attributes.class.replace(
					" selected",
					"",
				);
			}
			return tr;
		},
	};

	// ---- Button method stubs ----
	function handleEdit() {
		if (!selectedId) {
			alert("Please select a row to edit.");
			return;
		}
		// Build prefill from the saved selection
		editPrefill = {
			id: selectedId,
			category: selectedCategory,
			question: selectedQuestion,
			answer: selectedAnswer,
		};
		isEditMode = true;
		openAddQuestionModal = true;
	}

	function handleAdd() {
		isEditMode = false;
		editPrefill = null;
		openAddQuestionModal = true;
	}

	async function handleDelete(): Promise<void> {
		if (!selectedId) {
			alert("Pick a row first");
			return;
		}

		const msg =
			`Are you sure you want to delete question ${selectedId}: "${selectedQuestion}" ` +
			`from category "${selectedCategory}"?\nThis action cannot be undone.`;

		if (!window.confirm(msg)) return;

		try {
			const backendPort = window.api?.getBackendPort?.() || 5000;
			const res = await fetch(
				`http://127.0.0.1:${backendPort}/questions/${selectedCategory.toLowerCase()}/${selectedId}`,
				{ method: "DELETE" },
			);
			const json = await res.json().catch(() => ({}));
			if (!res.ok) throw new Error(json.error || "Delete failed");

			alert("Deleted!");

			selectedId = "";
			selectedCategory = "";
			selectedQuestion = "";
			selectedAnswer = "";
		} catch (err: any) {
			console.error("Delete failed:", err);
			alert(`❌ ${err?.message || "Delete failed"}`);
		}
	}
</script>

<div class="min-h-screen dark: bg-slate-900 text-white flex flex-col">

	


	<section class="flex items-center justify-center relative p-4">
	<!-- Logo in top-left -->
	<a
		href="https://e-catalogue.jhu.edu/course-descriptions/computer_science_601/"
		target="_blank"
		rel="noreferrer"
		class="absolute left-4 flex items-center"
	>
		<img
			class="h-10 hover:drop-shadow-[0_0_1rem_#ac00ac] transition-all duration-300"
			src={csygcLogo}
			alt="Logo"
		/>
	</a>

	<!-- Title centered -->
	<h1 class="text-4xl font-bold">Question Editor</h1>
</section>

	<button onclick={onBack}>Back to Welcom Page</button>
	<div
		style="display:flex; style=margin: 1rem 0; gap:8px; justify-content:center; margin-bottom: 1rem;"
	>
		<button onclick={showJsonModalClick} class={buttonClass}
			>Import From JSON</button
		>
		<button onclick={handleEdit} class={buttonClass}>Edit</button>
		<button onclick={handleAdd} class={buttonClass}>Add</button>
		<button onclick={handleDelete} class={buttonClass}>Delete</button>
	</div>
	<Table
		selectable
		{items}
		dataTableOptions={filterOptions}
		multiSelect={false}
		onSelectRow={handleRowSelect}
	/>
</div>
<AddQuestionModal
	bind:open={openAddQuestionModal}
	mode={isEditMode ? "edit" : "add"}
	prefill={editPrefill}
/>
<ImportJsonModal bind:open={openAddByJsonModal} />
