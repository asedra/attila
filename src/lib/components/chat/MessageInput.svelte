<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { functionsStore } from '$lib/stores/functionsStore.js';
  
  const dispatch = createEventDispatcher();
  
  let message = '';
  let isSubmitting = false;
  let textareaElement: HTMLTextAreaElement;
  
  // Auto-resize textarea
  function handleInput(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }
  
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }
  
  function handleSubmit() {
    if (!message.trim() || isSubmitting) return;
    
    isSubmitting = true;
    
    // Get active functions
    const activeFunctions = $functionsStore.activeFunctions;
    
    dispatch('send', {
      message: message.trim(),
      functions: activeFunctions
    });
    
    // Clear input
    message = '';
    textareaElement.style.height = 'auto';
    
    // Reset submitting state after a short delay
    setTimeout(() => {
      isSubmitting = false;
    }, 500);
  }
  
  // Function shortcuts
  function insertFunctionShortcut(functionId: string) {
    const shortcuts = {
      'idea-create': '@idea ',
      'idea-analyze': '@analyze ',
      'jira-create': '@jira ',
      'confluence-save': '@confluence '
    };
    
    const shortcut = shortcuts[functionId] || `@${functionId} `;
    message = message + shortcut;
    textareaElement.focus();
  }
</script>

<div class="flex flex-col space-y-3">
  <!-- Active Functions Display -->
  {#if $functionsStore.activeFunctions.length > 0}
    <div class="flex flex-wrap gap-2">
      <span class="text-sm text-gray-500">Active functions:</span>
      {#each $functionsStore.activeFunctions as functionId}
        {#each $functionsStore.functions as func}
          {#if func.id === functionId}
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {func.name}
            </span>
          {/if}
        {/each}
      {/each}
    </div>
  {/if}
  
  <!-- Function Shortcuts -->
  <div class="flex flex-wrap gap-2">
    <span class="text-sm text-gray-500">Quick functions:</span>
    <button
      type="button"
      class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors"
      on:click={() => insertFunctionShortcut('idea-create')}
    >
      💡 @idea
    </button>
    <button
      type="button"
      class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors"
      on:click={() => insertFunctionShortcut('jira-create')}
    >
      🎫 @jira
    </button>
    <button
      type="button"
      class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors"
      on:click={() => insertFunctionShortcut('confluence-save')}
    >
      📄 @confluence
    </button>
  </div>
  
  <!-- Input Area -->
  <div class="flex items-end space-x-3">
    <div class="flex-1 relative">
      <textarea
        bind:this={textareaElement}
        bind:value={message}
        on:input={handleInput}
        on:keydown={handleKeyDown}
        placeholder="Type your message... Try 'Hello!' or '@idea create a mobile app'"
        class="w-full resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        rows="1"
        disabled={isSubmitting}
      />
      <div class="absolute bottom-2 right-2 text-xs text-gray-400">
        Shift+Enter for new line
      </div>
    </div>
    
    <button
      type="button"
      on:click={handleSubmit}
      disabled={!message.trim() || isSubmitting}
      class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
    >
      {#if isSubmitting}
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Sending...
      {:else}
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
        </svg>
        Send
      {/if}
    </button>
  </div>
</div> 