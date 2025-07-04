# Attila AI Assistant

A sophisticated AI assistant application built with SvelteKit and FastAPI, designed to work with Cursor AI's MCP (Model Context Protocol) for seamless integration with Jira, Confluence, and other tools.

## 🏗️ Architecture

### Frontend (SvelteKit + TypeScript)
- **Chat Interface**: Real-time conversation with AI assistant
- **Function Panel**: Categorized functions for different workflows
- **WebSocket Communication**: Real-time messaging
- **State Management**: Reactive stores for chat and functions
- **Styling**: Tailwind CSS with custom Attila theme

### Backend (FastAPI + Python)
- **WebSocket Server**: Real-time chat communication
- **OpenAI Integration**: GPT models for AI responses
- **Function System**: Plugin-based architecture
- **RESTful API**: Function management endpoints
- **MCP Integration**: Existing Jira/Confluence integrations

### Technology Stack
- **Frontend**: SvelteKit, TypeScript, Tailwind CSS, Vite
- **Backend**: FastAPI, Python 3.11+, Uvicorn, SQLAlchemy
- **AI**: OpenAI GPT models (3.5-turbo, GPT-4, etc.)
- **Database**: SQLite (development), PostgreSQL (production)
- **Communication**: WebSockets, REST API
- **Development**: Hot reload, type checking, linting

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL (optional, for data persistence)
- OpenAI API key (required for AI functionality)

### Setup

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd Attila
   ```

2. **Frontend Setup:**
   ```bash
   npm install
   ```

3. **Backend Setup:**
   
   **Windows:**
   ```cmd
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
   **Linux/macOS:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API:**
   - Get your API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)
   - Start the frontend and click "Settings" in the chat interface
   - Enter your API key and save

5. **Start the servers:**
   
   **Backend (Terminal 1):**
   
   *Windows:*
   ```cmd
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   *Linux/macOS:*
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Frontend (Terminal 2):**
   ```bash
   npm run dev
   ```

6. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Backend Health: http://localhost:8000/health
   - Chat Interface: http://localhost:5173/chat

### Environment Variables (Optional)
Create a `.env` file in the backend directory for additional configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
LOG_LEVEL=info
```

### Verification
1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

2. **OpenAI Status Check:**
   ```bash
   curl http://localhost:8000/api/settings/openai/status
   # Should return configuration status
   ```

## 🎯 Features

### Core Functions

#### 💡 Idea Management
- **Create Ideas**: Convert thoughts into structured ideas
- **Analyze Ideas**: Deep research and feasibility analysis
- **Convert to Tasks**: Generate actionable development tasks

#### 📋 Task Management
- **Jira Integration**: Create and manage tickets
- **Task Assignment**: Delegate to team members
- **Progress Tracking**: Monitor completion status

#### 🔍 Analysis Tools
- **Market Research**: Competitive analysis
- **Technical Assessment**: Feasibility studies
- **Risk Analysis**: Identify potential issues

#### 🔗 Integrations
- **Jira**: Full ticket lifecycle management
- **Confluence**: Documentation and knowledge base
- **Slack**: Team communication (via existing MCP)
- **GitHub**: Repository integration

### Chat Interface Features

- **Natural Language Processing**: Conversational interactions
- **Function Triggers**: Quick function access with @mentions
- **Context Awareness**: Maintains conversation memory
- **Real-time Updates**: Live WebSocket communication
- **Function Cards**: Interactive result displays

## 📁 Project Structure

```
attila/
├── src/                          # Frontend source
│   ├── lib/
│   │   ├── components/
│   │   │   ├── chat/            # Chat interface components
│   │   │   │   └── ui/              # Reusable UI components
│   │   │   └── ui/              # Reusable UI components
│   │   ├── stores/              # Svelte stores
│   │   ├── utils/               # Utility functions
│   │   └── types/               # TypeScript types
│   └── routes/                  # SvelteKit routes
├── backend/                     # Backend source
│   ├── app/
│   │   ├── api/v1/              # API endpoints
│   │   ├── core/                # Core configuration
│   │   ├── services/            # Business logic
│   │   └── models/              # Data models
│   ├── mcp_servers/             # MCP server implementations
│   └── requirements.txt         # Python dependencies
├── .cursor/                     # Cursor AI configuration
│   └── mcp.json                 # MCP server configuration
└── docs/                        # Documentation
```

## 🔧 Development

### Frontend Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run check        # Type checking
npm run lint         # Linting
```

### Backend Development

**Windows:**
```cmd
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Start development server
black .                                                    # Code formatting
ruff .                                                     # Linting
pytest                                                     # Run tests
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Start development server
black .                                                    # Code formatting
ruff .                                                     # Linting
pytest                                                     # Run tests
```

### API Testing
```bash
# Test backend health
curl http://localhost:8000/health

# Test OpenAI configuration status
curl http://localhost:8000/api/settings/openai/status

# Test function endpoints
curl http://localhost:8000/api/functions/

# Test WebSocket connection (requires wscat)
wscat -c ws://localhost:8000/ws/chat
```

## 🎨 Usage Examples

### Basic Chat Interaction
```
User: "I have an idea for a mobile food delivery app"
AI: "I'll help you develop this idea. Let me create a structured analysis."
[Analysis Card Generated]
```

### Function-Based Commands
```
User: "@jira create ticket for authentication bug"
AI: "Creating Jira ticket for authentication bug..."
[Ticket Creation Form]
```

### Idea to Task Workflow
```
User: "Convert my app idea to development tasks"
AI: "I'll create Jira tickets for your project..."
[Multiple Tasks Generated]
```

## 🔐 Security

- **Environment Variables**: All sensitive data in .env
- **MCP Security**: Secure communication with integrated tools
- **CORS Configuration**: Proper cross-origin setup
- **Input Validation**: All API inputs validated

## 📊 Monitoring

- **Health Check**: `/api/health` endpoint
- **WebSocket Status**: Real-time connection monitoring
- **Function Status**: MCP server health tracking
- **Error Handling**: Comprehensive error reporting

## 🔧 Troubleshooting

### Common Issues

**1. Backend Server Won't Start**
```bash
# Ensure virtual environment is activated
cd backend
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# Check if dependencies are installed
pip list | grep fastapi

# Reinstall dependencies if needed
pip install -r requirements.txt
```

**2. "Module not found" errors**
```bash
# Make sure you're in the backend directory
cd backend
# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
# Run with Python module flag
python -m uvicorn app.main:app --reload
```

**3. Port Already in Use**
```bash
# Kill process on port 8000
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -ti:8000 | xargs kill

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**4. OpenAI API Issues**
- Verify API key is correct in Settings modal
- Check billing and usage limits on OpenAI Dashboard
- Test connection using the "Test" button in Settings

**5. WebSocket Connection Failed**
- Ensure backend is running on port 8000
- Check browser console for connection errors
- Verify CORS settings in backend

**6. Virtual Environment Issues**
```bash
# Remove and recreate virtual environment
cd backend
rm -rf venv  # Windows: rmdir /s venv
python -m venv venv
# Activate and reinstall
pip install -r requirements.txt
```

### Logs and Debugging
- Backend logs: Check terminal where uvicorn is running
- Frontend logs: Open browser dev tools (F12)
- Health check: `curl http://localhost:8000/health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed description

## 🔄 Roadmap

- [ ] Voice input/output
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Custom function marketplace
- [ ] Multi-language support
- [ ] Enterprise SSO integration

---

Built with ❤️ using SvelteKit, FastAPI, and Cursor AI's MCP protocol. 