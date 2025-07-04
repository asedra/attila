<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  export let isOpen = false;
  
  let settings = {
    openaiApiKey: '',
    selectedModel: 'gpt-3.5-turbo',
    temperature: 0.7,
    maxTokens: 2000,
    systemPrompt: 'You are Attila, a helpful AI assistant for project management, idea development, and task automation. You can help with Jira tickets, Confluence documentation, and idea analysis.'
  };
  
  let isTestingConnection = false;
  let connectionStatus = '';
  
  const availableModels = [
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', description: 'Fast and efficient for most tasks' },
    { id: 'gpt-4', name: 'GPT-4', description: 'More capable, better reasoning' },
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', description: 'Latest GPT-4 with improved performance' },
    { id: 'gpt-4o', name: 'GPT-4o', description: 'Multimodal capabilities' },
    { id: 'gpt-4o-mini', name: 'GPT-4o Mini', description: 'Faster and more affordable' }
  ];
  
  // Load settings from localStorage on component mount
  if (typeof window !== 'undefined') {
    const savedSettings = localStorage.getItem('attila-ai-settings');
    if (savedSettings) {
      settings = { ...settings, ...JSON.parse(savedSettings) };
    }
  }
  
  function closeModal() {
    isOpen = false;
    dispatch('close');
  }
  
  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }
  
  async function testConnection() {
    if (!settings.openaiApiKey.trim()) {
      connectionStatus = 'Please enter an API key';
      return;
    }
    
    isTestingConnection = true;
    connectionStatus = 'Testing connection...';
    
    try {
      const response = await fetch('/api/settings/test-openai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          apiKey: settings.openaiApiKey,
          model: settings.selectedModel
        })
      });
      
      const result = await response.json();
      
      if (result.success) {
        connectionStatus = '✅ Connection successful!';
      } else {
        connectionStatus = `❌ Error: ${result.error}`;
      }
    } catch (error) {
      connectionStatus = `❌ Connection failed: ${error.message}`;
    } finally {
      isTestingConnection = false;
    }
  }
  
  async function saveSettings() {
    // Save to localStorage
    localStorage.setItem('attila-ai-settings', JSON.stringify(settings));
    
    // Send to backend
    try {
      const response = await fetch('/api/settings/openai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
      });
      
      if (response.ok) {
        connectionStatus = '✅ Settings saved successfully!';
        dispatch('saved', settings);
        
        // Close modal after 1 second
        setTimeout(() => {
          closeModal();
        }, 1000);
      } else {
        connectionStatus = '❌ Failed to save settings';
      }
    } catch (error) {
      connectionStatus = `❌ Error saving: ${error.message}`;
    }
  }
  
  function handleKeydown(event) {
    if (event.key === 'Escape') {
      closeModal();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
        on:click={handleBackdropClick}
        on:keydown={(e) => e.key === 'Enter' && handleBackdropClick(e)}
        role="button"
        tabindex="0"
        aria-label="Close modal"
      ></div>
      
      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
        <div class="sm:flex sm:items-start">
          <div class="w-full">
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg leading-6 font-medium text-attila-dark" id="modal-title">
                🤖 OpenAI Configuration
              </h3>
              <button type="button" class="text-attila-gray hover:text-attila-dark" on:click={closeModal}>
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <!-- API Key Section -->
            <div class="mb-6">
              <label for="api-key" class="block text-sm font-medium text-attila-dark mb-2">
                OpenAI API Key
              </label>
              <div class="flex space-x-2">
                <input
                  id="api-key"
                  type="password"
                  bind:value={settings.openaiApiKey}
                  placeholder="sk-..."
                  class="flex-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-attila-primary focus:ring-attila-primary sm:text-sm"
                />
                <button
                  type="button"
                  on:click={testConnection}
                  disabled={isTestingConnection || !settings.openaiApiKey.trim()}
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-attila-primary hover:bg-attila-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-attila-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {#if isTestingConnection}
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Testing...
                  {:else}
                    Test
                  {/if}
                </button>
              </div>
              {#if connectionStatus}
                <p class="mt-2 text-sm {connectionStatus.includes('✅') ? 'text-attila-primary' : 'text-red-600'}">
                  {connectionStatus}
                </p>
              {/if}
              <p class="mt-1 text-xs text-attila-gray">
                Get your API key from <a href="https://platform.openai.com/api-keys" target="_blank" class="text-attila-primary hover:text-attila-primary/80">OpenAI Dashboard</a>
              </p>
            </div>
            
            <!-- Model Selection -->
            <div class="mb-6">
              <label for="model" class="block text-sm font-medium text-attila-dark mb-2">
                Model Selection
              </label>
              <select
                id="model"
                bind:value={settings.selectedModel}
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-attila-primary focus:ring-attila-primary sm:text-sm"
              >
                {#each availableModels as model}
                  <option value={model.id}>{model.name} - {model.description}</option>
                {/each}
              </select>
            </div>
            
            <!-- Advanced Settings -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <!-- Temperature -->
              <div>
                <label for="temperature" class="block text-sm font-medium text-attila-dark mb-2">
                  Temperature: {settings.temperature}
                </label>
                <input
                  id="temperature"
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  bind:value={settings.temperature}
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div class="flex justify-between text-xs text-attila-gray mt-1">
                  <span>Focused (0)</span>
                  <span>Creative (2)</span>
                </div>
              </div>
              
              <!-- Max Tokens -->
              <div>
                <label for="max-tokens" class="block text-sm font-medium text-attila-dark mb-2">
                  Max Tokens
                </label>
                <input
                  id="max-tokens"
                  type="number"
                  min="100"
                  max="4000"
                  bind:value={settings.maxTokens}
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-attila-primary focus:ring-attila-primary sm:text-sm"
                />
              </div>
            </div>
            
            <!-- System Prompt -->
            <div class="mb-6">
              <label for="system-prompt" class="block text-sm font-medium text-attila-dark mb-2">
                System Prompt
              </label>
              <textarea
                id="system-prompt"
                rows="4"
                bind:value={settings.systemPrompt}
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-attila-primary focus:ring-attila-primary sm:text-sm"
                placeholder="Define how the AI should behave..."
              ></textarea>
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="mt-5 sm:mt-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            on:click={saveSettings}
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-attila-primary text-base font-medium text-white hover:bg-attila-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-attila-primary sm:ml-3 sm:w-auto sm:text-sm"
          >
            Save Settings
          </button>
          <button
            type="button"
            on:click={closeModal}
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-attila-dark hover:text-attila-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-attila-primary sm:mt-0 sm:w-auto sm:text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Custom range slider styling */
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
  }
  
  input[type="range"]::-webkit-slider-track {
    width: 100%;
    height: 0.5rem;
    background: #e5e7eb;
    border-radius: 0.25rem;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    height: 1.25rem;
    width: 1.25rem;
    border-radius: 50%;
    background: #22D3EE;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  input[type="range"]::-moz-range-track {
    width: 100%;
    height: 0.5rem;
    background: #e5e7eb;
    border-radius: 0.25rem;
    border: none;
  }
  
  input[type="range"]::-moz-range-thumb {
    height: 1.25rem;
    width: 1.25rem;
    border-radius: 50%;
    background: #22D3EE;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
</style> 