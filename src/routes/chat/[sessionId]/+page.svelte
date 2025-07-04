<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { chatActions } from '$lib/stores/chatStore.js';
  import ChatInterface from '$lib/components/chat/ChatInterface.svelte';
  
  let sessionId: string;
  
  // Get session ID from URL params and switch session when it changes
  $: {
    sessionId = $page.params.sessionId;
    if (sessionId) {
      chatActions.switchSession(sessionId);
    }
  }
</script>

<svelte:head>
  <title>Attila AI Assistant - Chat {sessionId}</title>
</svelte:head>

<ChatInterface /> 