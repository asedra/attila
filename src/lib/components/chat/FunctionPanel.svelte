<script>
  import { functionsStore, functionsActions } from '$lib/stores/functionsStore.js';
  import CreateFunctionModal from './CreateFunctionModal.svelte';
  import EditFunctionModal from './EditFunctionModal.svelte';
  import { onMount } from 'svelte';
  
  let selectedCategory = 'all';
  let searchQuery = '';
  let showCreateModal = false;
  let showEditModal = false;
  let showConfirmDelete = null;
  let functionToEdit = null;
  
  onMount(() => {
    functionsActions.loadFunctions();
  });
  
  // Filter functions based on category and search
  $: filteredFunctions = $functionsStore.functions.filter(func => {
    const matchesCategory = selectedCategory === 'all' || func.category === selectedCategory;
    const matchesSearch = !searchQuery || 
      func.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      func.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });
  
  function toggleFunction(functionId) {
    functionsActions.toggleFunction(functionId);
  }
  
  function getIconForFunction(icon) {
    const icons = {
      'lightbulb': '💡',
      'search': '🔍',
      'ticket': '🎫',
      'file-text': '📄',
      'gear': '⚙️'
    };
    return icons[icon] || '🔧';
  }
  
  function getCategoryColor(category) {
    const colors = {
      'idea': 'bg-yellow-100 text-yellow-800',
      'task': 'bg-blue-100 text-blue-800',
      'analysis': 'bg-green-100 text-green-800',
      'integration': 'bg-purple-100 text-purple-800',
      'custom': 'bg-indigo-100 text-indigo-800',
      'automation': 'bg-red-100 text-red-800',
      'communication': 'bg-pink-100 text-pink-800',
      'data': 'bg-teal-100 text-teal-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  }

  function openCreateModal() {
    showCreateModal = true;
  }

  function handleFunctionCreated() {
    // Function successfully created, modal will close automatically
    functionsActions.clearError();
  }

  async function confirmDelete(functionId) {
    try {
      await functionsActions.deleteFunction(functionId);
      showConfirmDelete = null;
    } catch (error) {
      console.error('Failed to delete function:', error);
    }
  }

  async function toggleFunctionEnabled(functionId) {
    try {
      await functionsActions.toggleFunctionEnabled(functionId);
    } catch (error) {
      console.error('Failed to toggle function:', error);
    }
  }

  function openEditModal(func) {
    functionToEdit = func;
    showEditModal = true;
  }

  function handleFunctionUpdated() {
    // Function successfully updated, modal will close automatically
    functionsActions.clearError();
    functionToEdit = null;
  }
</script>

<div class="h-full flex flex-col">
  <!-- Header -->
  <div class="border-b border-gray-200 p-4">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-semibold text-attila-dark">Functions</h2>
      <button
        type="button"
        on:click={openCreateModal}
        class="inline-flex items-center px-3 py-2 text-sm font-medium text-white bg-attila-primary border border-attila-primary rounded-md hover:bg-attila-primary/90 transition-colors"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        Create
      </button>
    </div>
    
    <!-- Search -->
    <div class="relative">
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search functions..."
        class="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-attila-primary focus:border-transparent text-sm"
      />
      <svg class="absolute left-2 top-2.5 h-4 w-4 text-attila-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
      </svg>
    </div>
    
    <!-- Error Display -->
    {#if $functionsStore.error}
      <div class="mt-3 bg-red-50 border border-red-200 rounded-md p-3">
        <div class="flex items-center">
          <svg class="w-4 h-4 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-sm text-red-800">{$functionsStore.error}</span>
          <button
            type="button"
            on:click={functionsActions.clearError}
            class="ml-auto text-red-500 hover:text-red-700"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    {/if}
  </div>
  
  <!-- Categories -->
  <div class="border-b border-gray-200 p-4">
    <div class="flex flex-wrap gap-2">
      <button
        type="button"
        class="px-3 py-1 text-sm rounded-full transition-colors {selectedCategory === 'all' ? 'bg-attila-primary/10 text-attila-primary' : 'bg-gray-100 text-attila-gray hover:bg-attila-primary/5'}"
        on:click={() => selectedCategory = 'all'}
      >
        All
      </button>
      {#each $functionsStore.categories as category}
        <button
          type="button"
          class="px-3 py-1 text-sm rounded-full transition-colors capitalize {selectedCategory === category ? 'bg-attila-primary/10 text-attila-primary' : 'bg-gray-100 text-attila-gray hover:bg-attila-primary/5'}"
          on:click={() => selectedCategory = category}
        >
          {category}
        </button>
      {/each}
    </div>
  </div>
  
  <!-- Functions List -->
  <div class="flex-1 overflow-y-auto p-4 space-y-3">
    {#if $functionsStore.isLoading}
      <div class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-attila-primary mx-auto mb-2"></div>
        <p class="text-sm text-attila-gray">Loading functions...</p>
      </div>
    {:else}
      {#each filteredFunctions as func (func.id)}
        <div class="function-card {$functionsStore.activeFunctions.includes(func.id) ? 'active' : ''}">
          <div class="flex items-start justify-between">
            <div class="flex items-start space-x-3 flex-1">
              <div class="text-2xl">
                {getIconForFunction(func.icon)}
              </div>
              <div class="flex-1">
                <div class="flex items-center space-x-2">
                  <h3 class="text-sm font-medium text-attila-dark">{func.name}</h3>
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium {getCategoryColor(func.category)}">
                    {func.category}
                  </span>
                  {#if func.isSystem}
                    <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-attila-gray">
                      System
                    </span>
                  {/if}
                </div>
                <p class="text-xs text-attila-gray mt-1">{func.description || 'No description'}</p>
                
                {#if func.parameters && func.parameters.length > 0}
                  <div class="mt-2">
                    <div class="text-xs text-gray-500">Parameters:</div>
                    <div class="flex flex-wrap gap-1 mt-1">
                      {#each func.parameters as param}
                        <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                          {param.name}
                          {#if param.required}
                            <span class="text-red-500 ml-1">*</span>
                          {/if}
                        </span>
                      {/each}
                    </div>
                  </div>
                {/if}
              </div>
            </div>
            
            <div class="flex flex-col items-end space-y-2">
              <!-- Activate Button -->
              <button
                type="button"
                class="inline-flex items-center px-3 py-1 rounded-md text-xs font-medium transition-colors {$functionsStore.activeFunctions.includes(func.id) ? 'bg-attila-primary text-white' : 'bg-gray-200 text-attila-gray hover:bg-attila-primary/10'}"
                on:click={() => toggleFunction(func.id)}
              >
                {$functionsStore.activeFunctions.includes(func.id) ? 'Active' : 'Activate'}
              </button>
              
              <!-- Actions -->
              <div class="flex items-center space-x-1">
                <!-- Enable/Disable Toggle -->
                <button
                  type="button"
                  on:click={() => toggleFunctionEnabled(func.id)}
                  class="p-1 text-gray-400 hover:text-gray-600 rounded"
                  title={func.isEnabled ? 'Disable function' : 'Enable function'}
                >
                  <div class="w-2 h-2 rounded-full {func.isEnabled ? 'bg-green-500' : 'bg-gray-400'}"></div>
                </button>
                
                <!-- Edit Button (only for non-system functions) -->
                {#if !func.isSystem}
                  <button
                    type="button"
                    on:click={() => openEditModal(func)}
                    class="p-1 text-gray-400 hover:text-blue-600 rounded"
                    title="Edit function"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                {/if}
                
                <!-- Delete Button (only for non-system functions) -->
                {#if !func.isSystem}
                  <button
                    type="button"
                    on:click={() => showConfirmDelete = func.id}
                    class="p-1 text-gray-400 hover:text-red-600 rounded"
                    title="Delete function"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                {/if}
              </div>
            </div>
          </div>
        </div>
      {/each}
    {/if}
    
    <!-- Empty State -->
    {#if !$functionsStore.isLoading && filteredFunctions.length === 0}
      <div class="text-center py-8">
        <div class="text-gray-400 text-4xl mb-2">🔍</div>
        <p class="text-sm text-gray-500">
          {searchQuery ? 'No functions found' : 'No functions available'}
        </p>
        {#if searchQuery}
          <button
            type="button"
            class="text-xs text-blue-600 hover:text-blue-700 mt-2"
            on:click={() => searchQuery = ''}
          >
            Clear search
          </button>
        {:else}
          <button
            type="button"
            class="text-xs text-blue-600 hover:text-blue-700 mt-2"
            on:click={openCreateModal}
          >
            Create your first function
          </button>
        {/if}
      </div>
    {/if}
  </div>
  
  <!-- Footer -->
  <div class="border-t border-gray-200 p-4">
    <div class="flex items-center justify-between text-xs text-gray-500">
      <span>{$functionsStore.activeFunctions.length} active</span>
      <span>{filteredFunctions.length} available</span>
    </div>
  </div>
</div>

<!-- Create Function Modal -->
<CreateFunctionModal 
  bind:isOpen={showCreateModal}
  on:created={handleFunctionCreated}
  on:close={() => showCreateModal = false}
/>

<!-- Edit Function Modal -->
<EditFunctionModal 
  bind:isOpen={showEditModal}
  bind:functionToEdit={functionToEdit}
  on:updated={handleFunctionUpdated}
  on:close={() => {
    showEditModal = false;
    functionToEdit = null;
  }}
/>

<!-- Delete Confirmation Modal -->
{#if showConfirmDelete}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Delete Function</h3>
        <p class="text-sm text-gray-600 mb-6">
          Are you sure you want to delete this function? This action cannot be undone.
        </p>
        <div class="flex items-center justify-end space-x-3">
          <button
            type="button"
            on:click={() => showConfirmDelete = null}
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            on:click={() => confirmDelete(showConfirmDelete)}
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .function-card {
    background-color: white;
    border-radius: 0.5rem;
    border: 1px solid #e5e7eb;
    padding: 1rem;
    transition: all 0.2s;
  }
  
  .function-card:hover {
    border-color: #22D3EE;
    box-shadow: 0 1px 3px 0 rgba(34, 211, 238, 0.1);
  }
  
  .function-card.active {
    border-color: #22D3EE;
    background-color: rgba(34, 211, 238, 0.05);
  }
</style> 