<script lang="ts">
  import { chatStore } from '$lib/stores/chatStore.js';
  import { onMount } from 'svelte';
  
  let messagesContainer;
  let isNearBottom = true;
  let previousMessageCount = 0;
  let userScrolled = false;
  
  // Auto-scroll to bottom only when new messages arrive and user is near bottom
  $: {
    if ($chatStore.messages.length > previousMessageCount && messagesContainer) {
      // New message arrived
      if (isNearBottom && !userScrolled) {
        setTimeout(() => {
          scrollToBottom();
          userScrolled = false; // Reset flag after auto-scroll
        }, 50);
      }
      previousMessageCount = $chatStore.messages.length;
    }
  }
  
  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }
  
  function handleScroll() {
    if (messagesContainer) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
      
      // Check if user is near bottom (within 100px)
      const nearBottom = scrollTop + clientHeight >= scrollHeight - 100;
      
      // If user manually scrolled and moved away from bottom, mark as user scrolled
      if (!nearBottom && isNearBottom) {
        userScrolled = true;
      } else if (nearBottom) {
        userScrolled = false; // Reset when user scrolls back to bottom
      }
      
      isNearBottom = nearBottom;
    }
  }
  
  // Force scroll to bottom on component mount
  onMount(() => {
    setTimeout(() => {
      scrollToBottom();
      previousMessageCount = $chatStore.messages.length;
    }, 100);
  });
  
  function formatTime(date) {
    return new Date(date).toLocaleTimeString();
  }
  
  function renderMarkdown(content) {
    return content; // Simple text for now, can add markdown later
  }
</script>

<div 
  class="h-full overflow-y-auto p-4 space-y-4" 
  bind:this={messagesContainer}
  on:scroll={handleScroll}
  style="max-height: 100%; height: 100%;"
>
  {#each $chatStore.messages as message (message.id)}
    <div class="flex {message.type === 'user' ? 'justify-end' : 'justify-start'}">
      <div class="max-w-3xl w-full">
        <div class="flex items-start space-x-3">
          <!-- Avatar -->
          <div class="flex-shrink-0">
            {#if message.type === 'user'}
              <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                <span class="text-white text-sm font-medium">U</span>
              </div>
            {:else}
              <div class="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                <span class="text-white text-sm font-medium">AI</span>
              </div>
            {/if}
          </div>
          
          <!-- Message Content -->
          <div class="flex-1">
            <div class="flex items-baseline space-x-2">
              <span class="text-sm font-medium text-gray-900">
                {message.type === 'user' ? 'You' : 'AI Assistant'}
              </span>
              <span class="text-xs text-gray-500">
                {formatTime(message.timestamp)}
              </span>
            </div>
            
            <div class="mt-1">
              <div class="bg-white rounded-lg border border-gray-200 p-3 shadow-sm">
                <div class="prose prose-sm max-w-none">
                  {renderMarkdown(message.content)}
                </div>
              </div>
            </div>
            
            <!-- Function Result -->
            {#if message.functionResult}
              <div class="mt-2">
                <div class="bg-gray-50 rounded-lg border border-gray-200 p-3">
                  <h4 class="text-sm font-medium text-gray-900 mb-2">Function Result</h4>
                  <div class="text-sm text-gray-700">
                    <pre class="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
                      {JSON.stringify(message.functionResult, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  {/each}
  
  <!-- Loading indicator -->
  {#if $chatStore.isLoading}
    <div class="flex justify-start">
      <div class="max-w-3xl w-full">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
            <span class="text-white text-sm font-medium">AI</span>
          </div>
          <div class="flex-1">
            <div class="bg-white rounded-lg border border-gray-200 p-3 shadow-sm">
              <div class="flex items-center space-x-2">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-green-500"></div>
                <span class="text-sm text-gray-500">AI is thinking...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Empty state -->
  {#if $chatStore.messages.length === 0 && !$chatStore.isLoading}
    <div class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
        <p class="text-sm text-gray-500">Ask me anything or use functions to manage your ideas and tasks.</p>
      </div>
    </div>
  {/if}
</div> 