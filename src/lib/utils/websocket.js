export class ChatWebSocket {
  constructor() {
    this.socket = null;
    this.onMessage = null;
    this.onConnection = null;
    this.reconnectInterval = null;
    this.maxReconnectAttempts = 5;
    this.reconnectAttempts = 0;
  }
  
  connect() {
    try {
      this.socket = new WebSocket('ws://localhost:8000/ws/chat');
      
      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        if (this.onConnection) {
          this.onConnection(true);
        }
      };
      
      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (this.onMessage) {
            this.onMessage(message);
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
      
      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
        if (this.onConnection) {
          this.onConnection(false);
        }
        this.handleReconnect();
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      this.handleReconnect();
    }
  }
  
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      this.reconnectInterval = setTimeout(() => {
        this.connect();
      }, 2000 * this.reconnectAttempts); // Exponential backoff
    } else {
      console.error('Max reconnection attempts reached');
    }
  }
  
  sendMessage(message, functions = [], sessionId = null) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const data = {
        message,
        functions,
        session_id: sessionId
      };
      this.socket.send(JSON.stringify(data));
    } else {
      console.error('WebSocket is not connected');
    }
  }
  
  disconnect() {
    if (this.reconnectInterval) {
      clearTimeout(this.reconnectInterval);
    }
    
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
} 