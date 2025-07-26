<script>
     export let show = false; 
     export let closeOnClickOutside = true; // Close when clicking outside content
     export let position = "center"; 
     export let overlayClass = "";
     export let contentClass = ""; 


     export let bgColor = "bg-slate-900";  
     export let bgOpacity = "bg-opacity-100";

     // Close the overlay
     function handleClose() {
          show = false;
     }

     // Close when clicking outside content
     function handleOverlayClick(event) {
          if (closeOnClickOutside && event.target === event.currentTarget) {
               handleClose();
          }
     }
</script>

{#if show}
     <div
          class="overlay fixed inset-0 z-50 flex {bgColor} {bgOpacity} {position === 'center' ? 'items-center justify-center' : position === 'top' ? 'items-start justify-center' : position === 'right' ? 'items-center justify-end' : position === 'bottom' ? 'items-end justify-center' : 'items-center justify-start'} bg-black bg-opacity-50 transition-opacity duration-300 {overlayClass}"
          on:click={handleOverlayClick}
     >
          <div
               class="overlay-content bg-white rounded-lg shadow-xl p-6 max-w-full max-h-full overflow-auto {contentClass}"
               on:click|stopPropagation
          >
               <slot>

               </slot>
          </div>
     </div>
{/if}

<style>
     .overlay {
          backdrop-filter: blur(2px);
     }
     
     .overlay-content {
          animation: fadeIn 0.3s ease-out;
     }
     
     @keyframes fadeIn {
          from {
               opacity: 0;
               transform: translateY(10px);
          }
          to {
               opacity: 1;
               transform: translateY(0);
          }
     }
</style>