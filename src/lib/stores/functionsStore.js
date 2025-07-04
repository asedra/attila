import { writable, get } from 'svelte/store';

// Get unique categories from functions
const getCategories = (functions) => {
  return [...new Set(functions.map(func => func.category))];
};

// Initial functions state
const initialState = {
  functions: [],
  categories: [],
  activeFunctions: [],
  isLoading: false,
  error: null
};

// Create the store
export const functionsStore = writable(initialState);

// Helper actions
export const functionsActions = {
  loadFunctions: async () => {
    functionsStore.update(state => ({ ...state, isLoading: true, error: null }));
    
    try {
      const response = await fetch('/api/functions/');
      if (response.ok) {
        const functions = await response.json();
        functionsStore.update(state => ({
          ...state,
          functions: functions,
          categories: getCategories(functions),
          isLoading: false
        }));
      } else {
        throw new Error('Failed to load functions');
      }
    } catch (error) {
      console.error('Failed to load functions:', error);
      functionsStore.update(state => ({
        ...state,
        error: error.message,
        isLoading: false
      }));
    }
  },

  createFunction: async (functionData) => {
    try {
      const response = await fetch('/api/functions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(functionData)
      });

      if (response.ok) {
        const newFunction = await response.json();
        functionsStore.update(state => ({
          ...state,
          functions: [newFunction, ...state.functions],
          categories: getCategories([newFunction, ...state.functions])
        }));
        return newFunction;
      } else {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create function');
      }
    } catch (error) {
      console.error('Failed to create function:', error);
      functionsStore.update(state => ({
        ...state,
        error: error.message
      }));
      throw error;
    }
  },

  updateFunction: async (functionId, updateData) => {
    try {
      const response = await fetch(`/api/functions/${functionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        const updatedFunction = await response.json();
        functionsStore.update(state => ({
          ...state,
          functions: state.functions.map(func => 
            func.id === functionId ? updatedFunction : func
          ),
          categories: getCategories(state.functions.map(func => 
            func.id === functionId ? updatedFunction : func
          ))
        }));
        return updatedFunction;
      } else {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update function');
      }
    } catch (error) {
      console.error('Failed to update function:', error);
      functionsStore.update(state => ({
        ...state,
        error: error.message
      }));
      throw error;
    }
  },

  deleteFunction: async (functionId) => {
    try {
      const response = await fetch(`/api/functions/${functionId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        functionsStore.update(state => ({
          ...state,
          functions: state.functions.filter(func => func.id !== functionId),
          activeFunctions: state.activeFunctions.filter(id => id !== functionId)
        }));
        return true;
      } else {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete function');
      }
    } catch (error) {
      console.error('Failed to delete function:', error);
      functionsStore.update(state => ({
        ...state,
        error: error.message
      }));
      throw error;
    }
  },
  
  toggleFunction: (functionId) => {
    functionsStore.update(state => {
      const isActive = state.activeFunctions.includes(functionId);
      const activeFunctions = isActive
        ? state.activeFunctions.filter(id => id !== functionId)
        : [...state.activeFunctions, functionId];
      
      return {
        ...state,
        activeFunctions
      };
    });
  },

  toggleFunctionEnabled: async (functionId) => {
    try {
      // Get current state using get()
      const currentState = get(functionsStore);
      const functions = currentState.functions || [];
      const func = functions.find(f => f.id === functionId);
      
      if (!func) throw new Error('Function not found');
      
      await functionsActions.updateFunction(functionId, {
        is_enabled: !func.isEnabled
      });
    } catch (error) {
      console.error('Failed to toggle function enabled state:', error);
      throw error;
    }
  },
  
  setActiveFunctions: (functionIds) => {
    functionsStore.update(state => ({
      ...state,
      activeFunctions: functionIds
    }));
  },

  clearError: () => {
    functionsStore.update(state => ({
      ...state,
      error: null
    }));
  }
}; 