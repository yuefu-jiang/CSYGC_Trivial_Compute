<script>
	import {
		Input,
		Label,
		Helper,
		Button,
		Modal,
		Select,
	} from "flowbite-svelte";

	import { ChevronDownOutline } from "flowbite-svelte-icons";
	export let open;
	export let mode = "add";
	export let prefill = null;
	let categoryVal = "";
	let questionVal = "";
	let answerVal = "";
	let qidVal = "";
	let error = "";

	let categoryList = [
		"Geography",
		"History",
		"Math",
		"Computer Science",
		"Spanish",
		"English",
		"Physics",
	];
	let categoryOptions = categoryList.map((cat) => ({
		value: cat.toLowerCase(), // "Computer Science" → "computer science"
		name: cat,
	}));

	// re-seed when opening for edit
	$: if (open && mode === "edit" && prefill) {
		categoryVal = prefill.category.toLowerCase?.() || "";
		questionVal = prefill.question || "";
		answerVal = prefill.answer || "";
		qidVal = prefill.id || "";
	}

	// data is FormData
	async function onaction({ action, data }) {
		error = "";
		if (action === "cancel") return;
		for (let [key, value] of data.entries()) {
  			console.log(key, value);
}
		const question = data?.get("question")?.toString().trim();
		const answer = data?.get("answer")?.toString().trim();
		const qid = data?.get("qid")?.toString().trim();
		console.log("cat", data?.get("category"));
		const category = data?.get("category")?.toString().trim();

		if (!question || !answer || !qid) {
			error = "Please fill in Question, Answer, and Question ID.";
			return false; // keep modal open
		}

		const payload = {
			[category]: {
				[qid]: {
					question,
					answer,
					used: false,
				},
			},
		};
		console.log(JSON.stringify(payload));

		try {
			const backendPort = window.api?.getBackendPort?.() || 5000;
			const addEndpoint = `http://127.0.0.1:${backendPort}/add_to_questions_file`;
			const deleteEndpoint = `http://127.0.0.1:${backendPort}/questions/${categoryVal}/${qidVal}`;

			if (mode === "edit") {
				const res = await fetch(deleteEndpoint, {
					method: "DELETE",
				});
				const json = await res.json().catch(() => ({}));
				if (!res.ok) throw new Error(json.error || "Edit failed");
			}
			const res = await fetch(addEndpoint, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(payload),
			});
			const result = await res.json().catch(() => ({}));
			if (!res.ok) throw result;

			alert("✅ Questions successfully updated!");
			open = false;
		} catch (e) {
			console.error("Failed to update questions:", e);
			alert(`❌ Error: ${e?.error || e?.message || "Unknown error"}`);
			return false; // keep modal open on error
		}
	}
</script>

<Modal 
 form bind:open size="lg" 
 {onaction}>

	 {#snippet header()}
		<h3 class="text-lg font-semibold">
		{mode === 'edit' ? `Edit Question ${qidVal}` : 'Add Question'}
		</h3>
	{/snippet}
	<Label for="question" class="mb-2">Question</Label>
	<Input
		id="question"
		name="question"
		type="text"
		placeholder="What is the capital of France?"
		bind:value={questionVal}
		required
	/>

	<Label for="answer" class="mb-2">Answer</Label>
	<Input
		id="answer"
		name="answer"
		type="text"
		placeholder="Paris"
		bind:value={answerVal}
		required
	/>

	<Label for="qid" class="mb-2">Question ID</Label>
	<Input
		id="qid"
		name="qid"
		type="text"
		placeholder="Q00001"
		bind:value={qidVal}
		required
	/>
	<Label>
		Select an option
		<Select
			id="category"
			name="category"
			class="mt-2"
			items={categoryOptions}
			bind:value={categoryVal}
			required
		/>
	</Label>

	{#if error}
		<Helper color="red">{error}</Helper>
	{/if}

	{#snippet footer()}
		<Button type="submit" value="submit" color="dark">Accept</Button>
		<Button type="submit" value="cancel" color="alternative">Cancel</Button>
	{/snippet}
</Modal>
