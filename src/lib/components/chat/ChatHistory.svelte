<script>
  import { goto } from '$app/navigation';
  import { chatStore, chatActions } from '$lib/stores/chatStore.js';
  import { onMount } from 'svelte';
  
  let searchQuery = '';
  let editingSessionId = null;
  let editingTitle = '';
  
  // Filter sessions based on search
  $: filteredSessions = $chatStore.sessions.filter(session => {
    if (!searchQuery) return true;
    return session.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
           (session.description && session.description.toLowerCase().includes(searchQuery.toLowerCase()));
  });
  
  onMount(() => {
    chatActions.loadSessions();
  });
  
  function formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString('tr-TR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }
  
  function formatDate(timestamp) {
    return new Date(timestamp).toLocaleDateString('tr-TR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }
  
  function formatDateRelative(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return 'Bugün';
    } else if (diffInHours < 48) {
      return 'Dün';
    } else if (diffInHours < 168) { // 7 days
      return `${Math.floor(diffInHours / 24)} gün önce`;
    } else {
      return formatDate(timestamp);
    }
  }
  
  function createNewChat() {
    // Yeni chat başlat ama henüz session oluşturma
    chatActions.startNewChat();
    // Ana chat sayfasına yönlendir
    goto('/chat');
  }
  
  async function switchToSession(sessionId) {
    try {
      // URL'i session ID ile güncelle
      goto(`/chat/${sessionId}`);
    } catch (error) {
      console.error('Failed to switch session:', error);
    }
  }
  
  async function deleteSession(sessionId, event) {
    event.stopPropagation();
    
    if (!confirm('Bu sohbeti silmek istediğinizden emin misiniz?')) {
      return;
    }
    
    try {
      await chatActions.deleteSession(sessionId);
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  }
  
  function startEditing(sessionId, currentTitle, event) {
    event.stopPropagation();
    editingSessionId = sessionId;
    editingTitle = currentTitle;
  }
  
  async function saveTitle(sessionId) {
    if (!editingTitle.trim()) return;
    
    try {
      await chatActions.updateSessionTitle(sessionId, editingTitle.trim());
      editingSessionId = null;
      editingTitle = '';
    } catch (error) {
      console.error('Failed to update session title:', error);
    }
  }
  
  function cancelEditing() {
    editingSessionId = null;
    editingTitle = '';
  }
  
  function handleKeydown(event, sessionId) {
    if (event.key === 'Enter') {
      saveTitle(sessionId);
    } else if (event.key === 'Escape') {
      cancelEditing();
    }
  }
</script>

<div class="h-full flex flex-col">
  <!-- Header -->
  <div class="border-b border-gray-200 p-4">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-semibold text-attila-dark">Chat History</h2>
      <button
        type="button"
        on:click={createNewChat}
        class="inline-flex items-center px-3 py-2 text-sm font-medium text-white bg-attila-primary border border-attila-primary rounded-md hover:bg-attila-primary/90 transition-colors"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        New Chat
      </button>
    </div>
    
    <!-- Search -->
    <div class="relative">
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search chats..."
        class="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent text-sm"
      />
      <svg class="absolute left-2 top-2.5 h-4 w-4 text-attila-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
      </svg>
    </div>
  </div>
  
  <!-- Sessions List -->
  <div class="flex-1 overflow-y-auto p-4 space-y-3">
    {#each filteredSessions as session}
      <div 
        class="session-card border-l-4 cursor-pointer transition-colors {$chatStore.currentSessionId === session.id ? 'border-attila-primary bg-attila-primary/5' : 'border-gray-200 hover:border-attila-primary/30'}"
        on:click={() => switchToSession(session.id)}
        on:keydown={(e) => e.key === 'Enter' && switchToSession(session.id)}
        role="button"
        tabindex="0"
      >
        <div class="bg-white rounded-lg border border-gray-200 p-3 hover:shadow-sm transition-shadow">
          <!-- Session Header -->
          <div class="flex items-start justify-between mb-2">
            <div class="flex-1 min-w-0">
              {#if editingSessionId === session.id}
                <input
                  type="text"
                  bind:value={editingTitle}
                  class="w-full text-sm font-medium text-attila-dark bg-transparent border-b border-attila-primary focus:outline-none"
                  on:keydown={(e) => handleKeydown(e, session.id)}
                  on:blur={() => saveTitle(session.id)}
                />
              {:else}
                <h3 
                  class="text-sm font-medium text-attila-dark truncate"
                  on:dblclick={(e) => startEditing(session.id, session.title, e)}
                >
                  {session.title}
                </h3>
              {/if}
              
              <div class="flex items-center space-x-2 mt-1">
                <span class="text-xs text-attila-gray">
                  {formatDateRelative(session.updated_at)}
                </span>
                <span class="text-xs text-gray-400">•</span>
                <span class="text-xs text-attila-gray">
                  {session.message_count} messages
                </span>
              </div>
              
              {#if session.description}
                <p class="text-xs text-attila-gray mt-1 line-clamp-2">
                  {session.description}
                </p>
              {/if}
            </div>
            
            <!-- Actions -->
            <div class="flex items-center space-x-1 ml-2">
              <button
                type="button"
                on:click={(e) => startEditing(session.id, session.title, e)}
                class="p-1 text-gray-400 hover:text-attila-primary rounded"
                title="Edit title"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              
              <button
                type="button"
                on:click={(e) => deleteSession(session.id, e)}
                class="p-1 text-gray-400 hover:text-red-600 rounded"
                title="Delete chat"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Current Session Indicator -->
          {#if $chatStore.currentSessionId === session.id}
            <div class="flex items-center text-xs text-attila-primary font-medium">
              <div class="w-2 h-2 bg-attila-primary rounded-full mr-2"></div>
              Active Session
            </div>
          {/if}
        </div>
      </div>
    {/each}
    
    <!-- Empty State -->
    {#if filteredSessions.length === 0}
      <div class="text-center py-8">
        <div class="text-gray-400 text-4xl mb-2">💬</div>
        <p class="text-sm text-attila-gray">
          {searchQuery ? 'No chats found' : 'No chat history yet'}
        </p>
        {#if searchQuery}
          <button
            type="button"
            class="text-xs text-attila-primary hover:text-attila-primary/80 mt-2"
            on:click={() => searchQuery = ''}
          >
            Clear search
          </button>
        {:else}
          <button
            type="button"
            class="text-xs text-attila-primary hover:text-attila-primary/80 mt-2"
            on:click={createNewChat}
          >
            Start your first chat
          </button>
        {/if}
      </div>
    {/if}
  </div>
  
  <!-- Footer -->
  <div class="border-t border-gray-200 p-4">
    <div class="flex items-center justify-between text-xs text-attila-gray">
      <span>{filteredSessions.length} chats</span>
      <span>
        {#if $chatStore.currentSessionId}
          Session: {$chatStore.currentSessionId.slice(-8)}
        {:else}
          No active session
        {/if}
      </span>
    </div>
  </div>
</div>

<style>
  .session-card {
    transition: border-color 0.2s ease;
  }
  
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style> 