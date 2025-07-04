# Attila AI Assistant

A sophisticated AI assistant application built with SvelteKit and FastAPI, designed to work with Cursor AI's MCP (Model Context Protocol) for seamless integration with Jira, Confluence, and other tools.

## 🏗️ Architecture

### Frontend (SvelteKit + TypeScript)
- **Chat Interface**: Real-time conversation with AI assistant
- **Function Panel**: Categorized functions for different workflows
- **WebSocket Communication**: Real-time messaging
- **State Management**: Reactive stores for chat and functions

### Backend (FastAPI + Python)
- **WebSocket Server**: Real-time chat communication
- **MCP Integration**: Existing Jira/Confluence integrations
- **Function System**: Plugin-based architecture
- **RESTful API**: Function management endpoints

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL (optional, for data persistence)

### Setup

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure environment:**
   ```bash
   # Edit .env file with your API keys
   cp environment-template.env .env
   nano .env
   ```

3. **Start the application:**
   
   **Frontend:**
   ```bash
   npm run dev
   ```
   
   **Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: . venv/Scripts/activate
   python main.py
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Chat Interface: http://localhost:5173/chat

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
```bash
cd backend
python main.py       # Start development server
black .             # Code formatting
ruff .              # Linting
pytest              # Run tests
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