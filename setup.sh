#!/bin/bash

echo "🚀 Setting up Attila AI Assistant..."

# Create directory structure
echo "📁 Creating project structure..."
mkdir -p src/lib/{components/chat,components/functions,components/ui,stores,utils,types}
mkdir -p src/routes/{chat,functions}
mkdir -p backend/app/{api/v1,core,services,models}
mkdir -p backend/mcp_servers
mkdir -p .cursor

# Initialize SvelteKit project
echo "🔧 Initializing SvelteKit..."
npm create svelte@latest . --template skeleton --types typescript --prettier --eslint --playwright

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install
npm install -D @tailwindcss/forms @tailwindcss/typography tailwindcss postcss autoprefixer
npm install @tabler/icons-svelte lucide-svelte marked ws @types/ws date-fns

# Initialize Tailwind CSS
echo "🎨 Setting up Tailwind CSS..."
npx tailwindcss init -p

# Setup Python virtual environment
echo "🐍 Setting up Python backend..."
cd backend
python -m venv venv
source venv/bin/activate || . venv/Scripts/activate
pip install -r requirements.txt
cd ..

# Copy environment file
echo "🔐 Setting up environment..."
cp environment-template.env .env

# Create basic configuration files
echo "⚙️ Creating configuration files..."

# Create tailwind.config.js
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
EOF

# Create app.css
cat > src/app.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
.chat-message {
  @apply rounded-lg p-4 mb-4 max-w-4xl;
}

.function-card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow;
}

.function-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors;
}
EOF

# Create svelte.config.js
cat > svelte.config.js << 'EOF'
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    alias: {
      $lib: './src/lib'
    }
  }
};

export default config;
EOF

# Create vite.config.js
cat > vite.config.js << 'EOF'
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
});
EOF

# Create basic Python configuration
cat > backend/app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = "Attila AI Assistant"
    debug: bool = False
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost/attila")
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Jira Integration
    jira_instance_url: Optional[str] = os.getenv("JIRA_INSTANCE_URL")
    jira_user_email: Optional[str] = os.getenv("JIRA_USER_EMAIL")
    jira_api_key: Optional[str] = os.getenv("JIRA_API_KEY")
    
    # Confluence Integration
    confluence_url: Optional[str] = os.getenv("CONFLUENCE_URL")
    confluence_username: Optional[str] = os.getenv("CONFLUENCE_USERNAME")
    confluence_api_key: Optional[str] = os.getenv("CONFLUENCE_API_KEY")
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# Create MCP configuration
cat > .cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["backend/mcp_servers/jira_server.py"],
      "env": {
        "JIRA_INSTANCE_URL": "",
        "JIRA_USER_EMAIL": "",
        "JIRA_API_KEY": ""
      }
    },
    "confluence": {
      "command": "python",
      "args": ["backend/mcp_servers/confluence_server.py"],
      "env": {
        "CONFLUENCE_URL": "",
        "CONFLUENCE_USERNAME": "",
        "CONFLUENCE_API_KEY": ""
      }
    }
  }
}
EOF

echo "✅ Project setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Fill in your API keys in .env file"
echo "2. Run 'npm run dev' to start frontend"
echo "3. Run 'cd backend && python main.py' to start backend"
echo "4. Open http://localhost:5173 in your browser"
echo ""
echo "💡 Tips:"
echo "- Update .cursor/mcp.json with your actual credentials"
echo "- The chat interface will be available at /chat route"
echo "- Check the documentation in chat-architecture.md" 