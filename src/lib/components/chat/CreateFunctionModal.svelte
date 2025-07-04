<script>
  import { createEventDispatcher } from 'svelte';
  import { functionsActions } from '$lib/stores/functionsStore.js';
  
  const dispatch = createEventDispatcher();
  
  export let isOpen = false;
  
  let formData = {
    name: '',
    description: '',
    icon: 'gear',
    category: 'custom',
    parameters: []
  };
  
  let newParameter = {
    name: '',
    type: 'string',
    description: '',
    required: false
  };
  
  let isSubmitting = false;
  let error = null;
  
  const iconOptions = [
    { value: 'gear', label: '⚙️ Gear', icon: '⚙️' },
    { value: 'lightbulb', label: '💡 Lightbulb', icon: '💡' },
    { value: 'search', label: '🔍 Search', icon: '🔍' },
    { value: 'ticket', label: '🎫 Ticket', icon: '🎫' },
    { value: 'file-text', label: '📄 Document', icon: '📄' },
    { value: 'database', label: '💾 Database', icon: '💾' },
    { value: 'code', label: '💻 Code', icon: '💻' },
    { value: 'mail', label: '✉️ Mail', icon: '✉️' },
    { value: 'calendar', label: '📅 Calendar', icon: '📅' },
    { value: 'chart', label: '📊 Chart', icon: '📊' }
  ];
  
  const categoryOptions = [
    'custom',
    'idea',
    'task',
    'analysis',
    'integration',
    'automation',
    'communication',
    'data'
  ];
  
  const parameterTypes = [
    'string',
    'number',
    'boolean',
    'array',
    'object'
  ];
  
  function addParameter() {
    if (newParameter.name.trim()) {
      formData.parameters = [...formData.parameters, { ...newParameter }];
      newParameter = {
        name: '',
        type: 'string',
        description: '',
        required: false
      };
    }
  }
  
  function removeParameter(index) {
    formData.parameters = formData.parameters.filter((_, i) => i !== index);
  }
  
  async function handleSubmit() {
    if (!formData.name.trim()) {
      error = 'Function name is required';
      return;
    }
    
    isSubmitting = true;
    error = null;
    
    try {
      await functionsActions.createFunction(formData);
      
      // Reset form
      formData = {
        name: '',
        description: '',
        icon: 'gear',
        category: 'custom',
        parameters: []
      };
      
      dispatch('created');
      close();
      
    } catch (err) {
      error = err.message;
    } finally {
      isSubmitting = false;
    }
  }
  
  function close() {
    isOpen = false;
    error = null;
    dispatch('close');
  }
  
  function handleKeydown(event) {
    if (event.key === 'Escape') {
      close();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-attila-dark">Create New Function</h2>
        <button
          type="button"
          on:click={close}
          class="text-attila-gray hover:text-attila-dark transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- Content -->
      <form on:submit|preventDefault={handleSubmit} class="p-6 space-y-6">
        <!-- Error Message -->
        {#if error}
          <div class="bg-red-50 border border-red-200 rounded-md p-4">
            <div class="flex">
              <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
              </svg>
              <div class="text-sm text-red-800">{error}</div>
            </div>
          </div>
        {/if}
        
        <!-- Basic Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-attila-dark mb-2">
              Function Name *
            </label>
            <input
              id="name"
              type="text"
              bind:value={formData.name}
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent"
              placeholder="e.g., Send Email"
              required
            />
          </div>
          
          <!-- Category -->
          <div>
            <label for="category" class="block text-sm font-medium text-attila-dark mb-2">
              Category
            </label>
            <select
              id="category"
              bind:value={formData.category}
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent"
            >
              {#each categoryOptions as category}
                <option value={category}>{category}</option>
              {/each}
            </select>
          </div>
        </div>
        
        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-attila-dark mb-2">
            Description
          </label>
          <textarea
            id="description"
            bind:value={formData.description}
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent"
            placeholder="Describe what this function does..."
          ></textarea>
        </div>
        
        <!-- Icon -->
        <div>
          <fieldset class="block text-sm font-medium text-attila-dark mb-2">
            <legend class="text-sm font-medium text-attila-dark mb-2">Icon</legend>
            <div class="grid grid-cols-5 gap-2">
              {#each iconOptions as option}
                <label class="flex flex-col items-center p-3 border border-gray-200 rounded-md cursor-pointer hover:bg-attila-light transition-colors {formData.icon === option.value ? 'bg-attila-primary/10 border-attila-primary' : ''}">
                  <input
                    type="radio"
                    bind:group={formData.icon}
                    value={option.value}
                    class="sr-only"
                    name="function-icon"
                  />
                  <span class="text-2xl mb-1">{option.icon}</span>
                  <span class="text-xs text-attila-gray">{option.value}</span>
                </label>
              {/each}
            </div>
          </fieldset>
        </div>
        
        <!-- Parameters -->
        <div>
          <fieldset>
            <legend class="block text-sm font-medium text-attila-dark mb-2">Parameters</legend>
            
            <!-- Existing Parameters -->
            {#if formData.parameters.length > 0}
              <div class="space-y-2 mb-4">
                {#each formData.parameters as param, index}
                  <div class="flex items-center justify-between p-3 bg-attila-light rounded-md">
                    <div class="flex-1">
                      <div class="flex items-center space-x-2">
                        <span class="font-medium">{param.name}</span>
                        <span class="text-sm text-attila-gray">({param.type})</span>
                        {#if param.required}
                          <span class="text-xs bg-red-100 text-red-800 px-1 rounded">required</span>
                        {/if}
                      </div>
                      {#if param.description}
                        <p class="text-sm text-attila-gray mt-1">{param.description}</p>
                      {/if}
                    </div>
                    <button
                      type="button"
                      on:click={() => removeParameter(index)}
                      class="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                {/each}
              </div>
            {/if}
            
            <!-- Add Parameter Form -->
            <div class="border border-gray-200 rounded-md p-4">
              <h4 class="text-sm font-medium text-attila-dark mb-3">Add Parameter</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                <input
                  type="text"
                  bind:value={newParameter.name}
                  placeholder="Parameter name"
                  class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent text-sm"
                />
                <select
                  bind:value={newParameter.type}
                  class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent text-sm"
                >
                  {#each parameterTypes as type}
                    <option value={type}>{type}</option>
                  {/each}
                </select>
              </div>
              <div class="mb-3">
                <input
                  type="text"
                  bind:value={newParameter.description}
                  placeholder="Parameter description (optional)"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent text-sm"
                />
              </div>
              <div class="flex items-center justify-between">
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    bind:checked={newParameter.required}
                    class="mr-2"
                  />
                  <span class="text-sm text-attila-dark">Required parameter</span>
                </label>
                <button
                  type="button"
                  on:click={addParameter}
                  disabled={!newParameter.name.trim()}
                  class="px-3 py-1 bg-attila-primary text-white rounded-md hover:bg-attila-primary/90 disabled:opacity-50 disabled:cursor-not-allowed text-sm transition-colors"
                >
                  Add
                </button>
              </div>
            </div>
          </fieldset>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            on:click={close}
            class="px-4 py-2 border border-gray-300 rounded-md text-attila-dark hover:bg-attila-light transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting || !formData.name.trim()}
            class="px-4 py-2 bg-attila-primary text-white rounded-md hover:bg-attila-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {#if isSubmitting}
              Creating...
            {:else}
              Create Function
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if} 