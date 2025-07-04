<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { chatActions } from '$lib/stores/chatStore.js';
  import ChatInterface from '$lib/components/chat/ChatInterface.svelte';
  
  let sessionId: string;
  
  // Get session ID from URL params
  $: sessionId = $page.params.sessionId;
  
  // Switch session only on client side
  onMount(() => {
    if (sessionId) {
      chatActions.switchSession(sessionId);
    }
  });
  
  // Also switch when sessionId changes after mount
  $: if (typeof window !== 'undefined' && sessionId) {
    chatActions.switchSession(sessionId);
  }
</script>

<svelte:head>
  <title>Attila AI Assistant - Chat {sessionId}</title>
</svelte:head>

<ChatInterface /> 