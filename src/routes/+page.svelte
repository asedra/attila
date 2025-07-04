<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  
  onMount(() => {
    goto('/chat');
  });
</script>

<div class="flex items-center justify-center min-h-screen bg-attila-light">
  <div class="text-center">
    <div class="w-16 h-16 bg-attila-dark rounded-xl flex items-center justify-center mb-4 mx-auto">
      <svg class="w-8 h-8 text-attila-secondary" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
        <path d="M8 11l2 2 4-4" stroke="white" stroke-width="2" fill="none"/>
      </svg>
    </div>
    <h1 class="text-2xl font-bold text-attila-dark mb-2">
      ATTILA <span class="text-attila-primary">AI</span>
    </h1>
    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-attila-primary mx-auto mb-2"></div>
    <p class="text-sm text-attila-gray">Loading Assistant...</p>
  </div>
</div> 