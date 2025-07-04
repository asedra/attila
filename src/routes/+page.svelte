<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  
  onMount(() => {
    goto('/chat');
  });
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-50">
  <div class="text-center">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
    <p class="mt-2 text-sm text-gray-600">Loading Attila AI Assistant...</p>
  </div>
</div> 