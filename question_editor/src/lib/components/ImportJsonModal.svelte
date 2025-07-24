<script>
	import { Fileupload, Label, Helper, Button, Modal, Checkbox } from 'flowbite-svelte';
	import { createEventDispatcher } from 'svelte';

	export let open;
	const dispatch = createEventDispatcher();
	let error = "";

	function onaction({ action, data }) {
		error = "";

		if (action === "cancel") return;

		const file = data.get("file");
		const replace = data.get("replace") === "on";

		if (!file || !(file instanceof File) || !file.name) {
			error = "Must choose a file";
			console.log("Must choose a file");
			return false;
		}
		if (file.type !== "application/json") {
			error = "File must be of type JSON";
			console.log("Not a JSON file");
			return false;
		}

		const reader = new FileReader();
		reader.readAsText(file);
		reader.onload = () => {
			try {
				const json = JSON.parse(String(reader.result));
				const backendPort = window.api?.getBackendPort?.() || 5000;
				const endpoint = replace
					? `http://127.0.0.1:${backendPort}/replace_questions_file`
					: `http://127.0.0.1:${backendPort}/add_to_questions_file`;

				fetch(endpoint, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(json)
				})
					.then(async (res) => {
						const result = await res.json();
						if (!res.ok) throw result;
						alert('✅ Questions file successfully updated!');
						open = false;
					})
					.catch((err) => {
						console.error('Failed to update questions file:', err);
						alert(`❌ Error: ${err?.error || 'Unknown error'}`);
					});
			} catch (e) {
				alert("❌ Invalid JSON content.");
				console.error("JSON parse error:", e);
			}
		};
	}
</script>

<Modal title="Add questions using JSON file" form bind:open={open} size="lg" {onaction}>
	<Fileupload id="with_helper" name="file" class="mb-2" />
	{#if error}
		<Label color="red">{error}</Label>
	{/if}
	<Helper>JSON</Helper>
	<Checkbox name='replace'>Replace Current Question Bank</Checkbox>

	{#snippet footer()}
		<Button type="submit" value="submit" color="dark">Accept</Button>
		<Button type="submit" value="cancel" color="alternative">Cancel</Button>
	{/snippet}
</Modal>
