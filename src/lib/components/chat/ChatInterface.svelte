<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { chatStore, chatActions } from '$lib/stores/chatStore.js';
  import { functionsStore, functionsActions } from '$lib/stores/functionsStore.js';
  import MessageList from './MessageList.svelte';
  import MessageInput from './MessageInput.svelte';
  import FunctionPanel from './FunctionPanel.svelte';
  import ChatHistory from './ChatHistory.svelte';
  import SettingsModal from '../ui/SettingsModal.svelte';
  import { ChatWebSocket } from '$lib/utils/websocket.js';
  
  let chatWs;
  let isConnected = false;
  let showSettings = false;
  let activeTab = 'functions'; // 'functions' or 'history'
  
  onMount(async () => {
    chatWs = new ChatWebSocket();
    chatWs.connect();
    
    chatWs.onConnection = (connected) => {
      isConnected = connected;
    };
    
    chatWs.onMessage = async (message) => {
      // Add AI response to store
      const aiMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: message.content || message.message || 'No response received',
        timestamp: new Date(),
        functions: []
      };
      
      // Add message and save
      chatStore.update(store => ({
        ...store,
        messages: [...store.messages, aiMessage],
        isLoading: false
      }));
      
      // Save AI response to database if we have a session
      if ($chatStore.currentSessionId) {
        await chatActions.saveMessage(aiMessage);
      }
    };
    
    // Initialize chat system
    await chatActions.initializeChat();
    
    // Load available functions
    functionsActions.loadFunctions();
  });
  
  async function handleSendMessage(message, activeFunctions) {
    // If pending new chat, create session first
    if ($chatStore.isPendingNewChat) {
      try {
        // Generate title from user's message
        const sessionTitle = message.length > 50 ? 
          message.substring(0, 50) + '...' : 
          message;
        
        const newSession = await chatActions.createSession(sessionTitle);
        
        if (newSession) {
          // Navigate to the session URL
          goto(`/chat/${newSession.id}`);
        }
      } catch (error) {
        console.error('Failed to create session on send:', error);
        return; // Don't send message if session creation failed
      }
    }
    
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date(),
      functions: activeFunctions
    };
    
    // Add user message to store
    chatStore.update(store => ({
      ...store,
      messages: [...store.messages, userMessage],
      isLoading: true
    }));
    
    // If we have an active session, save the message
    if ($chatStore.currentSessionId) {
      await chatActions.saveMessage(userMessage);
    }
    
    // Send to WebSocket with session ID
    chatWs.sendMessage(message, activeFunctions, $chatStore.currentSessionId);
  }
  
  function openSettings() {
    showSettings = true;
  }
  
  function handleSettingsSaved(event) {
    // Settings saved, you could show a notification here
    console.log('Settings saved:', event.detail);
  }
  
  function setActiveTab(tab) {
    activeTab = tab;
  }
  

</script>

<div class="flex h-full bg-gray-50">
  <!-- Left Panel with Tabs -->
  <div class="w-80 border-r border-gray-200 bg-white flex flex-col">
    <!-- Tab Navigation -->
    <div class="border-b border-gray-200 bg-gray-50">
      <nav class="flex space-x-8 px-4" aria-label="Tabs">
        <button
          type="button"
          on:click={() => setActiveTab('functions')}
          class="py-3 px-1 border-b-2 font-medium text-sm transition-colors {activeTab === 'functions' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
          aria-current={activeTab === 'functions' ? 'page' : undefined}
        >
          <div class="flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.78 0-2.678-2.153-1.415-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            <span>Functions</span>
          </div>
          {#if $functionsStore.activeFunctions.length > 0}
            <span class="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {$functionsStore.activeFunctions.length}
            </span>
          {/if}
        </button>
        
        <button
          type="button"
          on:click={() => setActiveTab('history')}
          class="py-3 px-1 border-b-2 font-medium text-sm transition-colors {activeTab === 'history' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
          aria-current={activeTab === 'history' ? 'page' : undefined}
        >
          <div class="flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>History</span>
          </div>
        </button>
      </nav>
    </div>
    
    <!-- Tab Content -->
    <div class="flex-1 overflow-hidden">
      {#if activeTab === 'functions'}
        <FunctionPanel />
      {:else if activeTab === 'history'}
        <ChatHistory />
      {/if}
    </div>
  </div>

  <!-- Chat Area -->
  <div class="flex-1 flex flex-col h-full min-h-0">
    <!-- Header -->
    <div class="border-b border-gray-200 bg-white px-6 py-4 flex-shrink-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-xl font-semibold text-gray-900">Attila AI Assistant</h1>
          
          <!-- Current Session Info -->
          {#if $chatStore.currentSessionId}
            <div class="flex items-center space-x-2 text-sm text-gray-600">
              <div class="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>
                {$chatStore.sessions.find(s => s.id === $chatStore.currentSessionId)?.title || 'Active Session'}
              </span>
            </div>
          {:else if $chatStore.isPendingNewChat}
            <div class="flex items-center space-x-2 text-sm text-gray-600">
              <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span>New Chat - Start typing...</span>
            </div>
          {/if}
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Connection Status -->
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full {isConnected ? 'bg-green-500' : 'bg-red-500'}"></div>
            <span class="text-sm text-gray-600">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          
          <!-- Settings Button -->
          <button
            type="button"
            on:click={openSettings}
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            title="OpenAI Settings"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            Settings
          </button>
        </div>
      </div>
    </div>
    
    <!-- Messages -->
    <div class="flex-1 overflow-hidden" style="height: calc(100vh - 180px);">
      {#if $chatStore.currentSessionId}
        <MessageList />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-500">
          <div class="text-center">
            <div class="text-6xl mb-4">💬</div>
            <h3 class="text-lg font-medium mb-2">Welcome to Attila AI</h3>
            <p class="text-sm">
              {#if $chatStore.isPendingNewChat}
                Type your message below to start a new conversation.
              {:else}
                Start a new conversation or select an existing one from the history panel.
              {/if}
            </p>
          </div>
        </div>
      {/if}
    </div>
    
    <!-- Input -->
    {#if $chatStore.currentSessionId || $chatStore.isPendingNewChat}
      <div class="border-t border-gray-200 bg-white p-4 flex-shrink-0">
        <MessageInput 
          on:send={(e) => handleSendMessage(e.detail.message, e.detail.functions)}
        />
      </div>
    {/if}
  </div>
</div>

<!-- Settings Modal -->
<SettingsModal 
  bind:isOpen={showSettings} 
  on:close={() => showSettings = false}
  on:saved={handleSettingsSaved}
/>

<style>
  :global(html, body) {
    height: 100%;
    margin: 0;
    padding: 0;
  }
</style> 