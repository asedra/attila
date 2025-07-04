<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  
  onMount(() => {
    goto('/chat');
  });
</script>

<div class="flex items-center justify-center min-h-screen bg-attila-light">
  <div class="text-center">
    <div class="w-20 h-20 rounded-xl overflow-hidden bg-attila-darker flex items-center justify-center mb-4 mx-auto">
      <!-- Attila Warrior Helmet SVG -->
      <svg class="w-16 h-16" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Helmet Base -->
        <path d="M16 4C12 4 8 6 8 10V20C8 22 10 24 12 24H20C22 24 24 22 24 20V10C24 6 20 4 16 4Z" fill="#F59E0B"/>
        <!-- Helmet Crest -->
        <path d="M16 2C14 2 12 3 12 4C12 5 14 6 16 6C18 6 20 5 20 4C20 3 18 2 16 2Z" fill="#F59E0B"/>
        <!-- Face Guard -->
        <path d="M12 12V18C12 19 13 20 14 20H18C19 20 20 19 20 18V12H12Z" fill="#1F2937"/>
        <!-- Eye Slots -->
        <rect x="14" y="14" width="2" height="1" fill="#22D3EE"/>
        <rect x="16" y="14" width="2" height="1" fill="#22D3EE"/>
        <!-- Tech Elements -->
        <line x1="26" y1="12" x2="28" y2="12" stroke="#22D3EE" stroke-width="1"/>
        <line x1="26" y1="16" x2="28" y2="16" stroke="#22D3EE" stroke-width="1"/>
        <line x1="26" y1="20" x2="28" y2="20" stroke="#22D3EE" stroke-width="1"/>
        <circle cx="29" cy="12" r="1" fill="#22D3EE"/>
        <circle cx="29" cy="16" r="1" fill="#22D3EE"/>
        <circle cx="29" cy="20" r="1" fill="#22D3EE"/>
      </svg>
    </div>
    <h1 class="text-2xl font-bold text-attila-dark mb-2">
      ATTILA <span class="text-attila-primary">AI</span>
    </h1>
    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-attila-primary mx-auto mb-2"></div>
    <p class="text-sm text-attila-gray">Loading Assistant...</p>
  </div>
</div> 