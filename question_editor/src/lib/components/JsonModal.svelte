<script>
  import { Button, Modal, P } from "flowbite-svelte";
  let {form, open }= $props()

  function handleAction(action, data) {
    console.log("User action: ", action);
    console.log("ata", data)
    open = false;
  }

  function handleReject() {
    console.log("User rejects the terms");
    open = false;
  }
</script>

<Modal title="Terms of Service" bind:open={open} form onAction={handleAction}>
  <P>With less than a month to go before the European Union enacts new consumer privacy laws for its citizens, companies around the world are updating their terms of service agreements to comply.</P>
  <P>The European Union’s General Data Protection Regulation (G.D.P.R.) goes into effect on May 25 and is meant to ensure a common set of data rights in the European Union. It requires organizations to notify users as soon as possible of high-risk data breaches that could personally affect them.</P>

  {#snippet footer()}
    <Button type="submit" value="success">I accept</Button>
    <Button type="submit" value="decline" color="alternative">Decline</Button>
  {/snippet}
</Modal>