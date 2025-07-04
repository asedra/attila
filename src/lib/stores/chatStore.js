import { writable, get } from 'svelte/store';

// Chat store with session management
const initialState = {
  currentSessionId: null,
  sessions: [],
  messages: [],
  isLoading: false,
  error: null,
  isPendingNewChat: false // New state for pending new chat
};

// Create the store
export const chatStore = writable(initialState);

// Chat session actions
export const chatActions = {
  // Session management
  async loadSessions() {
    try {
      const response = await fetch('/api/chat/sessions');
      if (response.ok) {
        const sessions = await response.json();
        chatStore.update(state => ({
          ...state,
          sessions: sessions
        }));
        return sessions;
      } else {
        throw new Error('Failed to load sessions');
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return [];
    }
  },

  async createSession(title, description = null) {
    try {
      const response = await fetch('/api/chat/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          description: description
        })
      });

      if (response.ok) {
        const newSession = await response.json();
        chatStore.update(state => ({
          ...state,
          sessions: [newSession, ...state.sessions],
          currentSessionId: newSession.id,
          isPendingNewChat: false // Clear pending state
        }));
        return newSession;
      } else {
        throw new Error('Failed to create session');
      }
    } catch (error) {
      console.error('Failed to create session:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return null;
    }
  },

  // Start a new chat without creating a session yet
  startNewChat() {
    chatStore.update(state => ({
      ...state,
      currentSessionId: null,
      messages: [],
      isPendingNewChat: true,
      error: null
    }));
  },

  // Create session after successful API response
  async createSessionAfterResponse(userMessage, assistantMessage) {
    try {
      // Generate title from the user's first message
      const sessionTitle = userMessage.length > 50 ? 
        userMessage.substring(0, 50) + '...' : 
        userMessage;
      
      const newSession = await this.createSession(sessionTitle);
      
      if (newSession) {
        // Save both user message and assistant response
        await this.saveMessage({
          type: 'user',
          content: userMessage,
          timestamp: new Date()
        });
        
        await this.saveMessage({
          type: 'assistant',
          content: assistantMessage,
          timestamp: new Date()
        });
        
        // Generate a better title using the API
        try {
          const response = await fetch(`/api/chat/sessions/${newSession.id}/generate-title`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              message: userMessage
            })
          });
          
          if (response.ok) {
            const result = await response.json();
            if (result.success) {
              await this.updateSessionTitle(newSession.id, result.title);
            }
          }
        } catch (error) {
          console.error('Failed to generate title:', error);
        }
      }
      
      return newSession;
    } catch (error) {
      console.error('Failed to create session after response:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return null;
    }
  },

  async switchSession(sessionId) {
    try {
      // Load messages for the session
      const response = await fetch(`/api/chat/sessions/${sessionId}/messages`);
      if (response.ok) {
        const messages = await response.json();
        chatStore.update(state => ({
          ...state,
          currentSessionId: sessionId,
          messages: messages.map(msg => ({
            id: msg.id,
            type: msg.type,
            content: msg.content,
            timestamp: new Date(msg.timestamp),
            functions: []
          })),
          isPendingNewChat: false // Clear pending state
        }));
        return true;
      } else {
        throw new Error('Failed to load session messages');
      }
    } catch (error) {
      console.error('Failed to switch session:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return false;
    }
  },

  async updateSessionTitle(sessionId, title) {
    try {
      const response = await fetch(`/api/chat/sessions/${sessionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title })
      });

      if (response.ok) {
        const updatedSession = await response.json();
        chatStore.update(state => ({
          ...state,
          sessions: state.sessions.map(session => 
            session.id === sessionId ? updatedSession : session
          )
        }));
        return updatedSession;
      } else {
        throw new Error('Failed to update session title');
      }
    } catch (error) {
      console.error('Failed to update session title:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return null;
    }
  },

  async deleteSession(sessionId) {
    try {
      const response = await fetch(`/api/chat/sessions/${sessionId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        chatStore.update(state => {
          const newState = {
            ...state,
            sessions: state.sessions.filter(session => session.id !== sessionId)
          };
          
          // If we deleted the current session, clear it
          if (state.currentSessionId === sessionId) {
            newState.currentSessionId = null;
            newState.messages = [];
            newState.isPendingNewChat = false;
          }
          
          return newState;
        });
        return true;
      } else {
        throw new Error('Failed to delete session');
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return false;
    }
  },

  // Message management
  async saveMessage(message) {
    const state = get(chatStore); // Fixed: use get() from svelte/store
    
    if (!state.currentSessionId) {
      console.error('No active session to save message to');
      return null;
    }

    try {
      const response = await fetch(`/api/chat/sessions/${state.currentSessionId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: message.content,
          message_type: message.type
        })
      });

      if (response.ok) {
        const savedMessage = await response.json();
        return savedMessage;
      } else {
        throw new Error('Failed to save message');
      }
    } catch (error) {
      console.error('Failed to save message:', error);
      chatStore.update(state => ({
        ...state,
        error: error.message
      }));
      return null;
    }
  },

  // Utility methods
  getCurrentSession() {
    const state = get(chatStore);
    if (state.currentSessionId) {
      return state.sessions.find(s => s.id === state.currentSessionId);
    }
    return null;
  },

  // Check if current session has any messages
  isFirstMessage() {
    const state = get(chatStore);
    return state.messages.length === 0;
  },

  // Initialize with a default session if none exists
  async initializeChat() {
    const sessions = await this.loadSessions();
    
    if (sessions.length === 0) {
      // Create a default session
      const defaultTitle = `Chat ${new Date().toLocaleDateString('tr-TR')}`;
      await this.createSession(defaultTitle);
    } else {
      // Switch to the most recent session
      await this.switchSession(sessions[0].id);
    }
  },

  // Clear error
  clearError() {
    chatStore.update(state => ({
      ...state,
      error: null
    }));
  }
}; 