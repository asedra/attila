import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    from ..core.config import settings
except ImportError:
    # Fallback if config is not available
    class FallbackSettings:
        jira_instance_url = None
        jira_api_key = None
        jira_user_email = None
        confluence_url = None
        confluence_api_key = None
        confluence_username = None
    
    settings = FallbackSettings()


class MCPService:
    def __init__(self):
        # Initialize client attributes first
        self.jira_client = None
        self.confluence_client = None
        
        # Initialize external clients
        self._initialize_clients()
        
        # Load functions after clients are initialized
        self.available_functions = self._load_default_functions()
    
    def _initialize_clients(self):
        """Initialize external service clients"""
        # Initialize Jira client if credentials are available
        if hasattr(settings, 'jira_instance_url') and settings.jira_instance_url and settings.jira_api_key:
            try:
                from jira import JIRA
                self.jira_client = JIRA(
                    server=settings.jira_instance_url,
                    basic_auth=(settings.jira_user_email, settings.jira_api_key)
                )
            except ImportError:
                print("Jira library not installed. Install with: pip install jira")
            except Exception as e:
                print(f"Failed to initialize Jira client: {e}")
        
        # Initialize Confluence client if credentials are available
        if hasattr(settings, 'confluence_url') and settings.confluence_url and settings.confluence_api_key:
            try:
                from atlassian import Confluence
                self.confluence_client = Confluence(
                    url=settings.confluence_url,
                    username=settings.confluence_username,
                    password=settings.confluence_api_key
                )
            except ImportError:
                print("Atlassian library not installed. Install with: pip install atlassian-python-api")
            except Exception as e:
                print(f"Failed to initialize Confluence client: {e}")
    
    def _load_default_functions(self) -> List[Dict[str, Any]]:
        """Load default available functions"""
        return [
            {
                "id": "idea-create",
                "name": "Create Idea",
                "description": "Convert thoughts into structured ideas",
                "icon": "lightbulb",
                "category": "idea",
                "parameters": [
                    {"name": "title", "type": "string", "description": "Idea title", "required": True},
                    {"name": "description", "type": "string", "description": "Idea description", "required": True}
                ],
                "isEnabled": True,
                "isActive": False
            },
            {
                "id": "idea-analyze",
                "name": "Analyze Idea",
                "description": "Perform deep analysis on an idea",
                "icon": "search",
                "category": "idea",
                "parameters": [
                    {"name": "ideaId", "type": "string", "description": "ID of the idea to analyze", "required": True}
                ],
                "isEnabled": True,
                "isActive": False
            },
            {
                "id": "jira-create",
                "name": "Create Jira Ticket",
                "description": "Create a new Jira ticket from conversation",
                "icon": "ticket",
                "category": "task",
                "parameters": [
                    {"name": "title", "type": "string", "description": "Ticket title", "required": True},
                    {"name": "description", "type": "string", "description": "Ticket description", "required": True},
                    {"name": "priority", "type": "string", "description": "Priority level", "required": False, "default": "Medium"}
                ],
                "isEnabled": bool(self.jira_client),
                "isActive": False
            },
            {
                "id": "confluence-save",
                "name": "Save to Confluence",
                "description": "Save analysis or documentation to Confluence",
                "icon": "file-text",
                "category": "integration",
                "parameters": [
                    {"name": "title", "type": "string", "description": "Page title", "required": True},
                    {"name": "content", "type": "string", "description": "Page content", "required": True},
                    {"name": "spaceKey", "type": "string", "description": "Confluence space key", "required": True}
                ],
                "isEnabled": bool(self.confluence_client),
                "isActive": False
            }
        ]
    
    async def get_available_functions(self) -> List[Dict[str, Any]]:
        """Get list of available functions"""
        return self.available_functions
    
    async def execute_function(self, function_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific function"""
        try:
            if function_id == "jira-create":
                return await self.call_jira_function("create_issue", params)
            elif function_id == "confluence-save":
                return await self.call_confluence_function("create_page", params)
            elif function_id in ["idea-create", "idea-analyze"]:
                return await self._handle_idea_function(function_id, params)
            else:
                return {"error": f"Unknown function: {function_id}"}
        except Exception as e:
            return {"error": f"Error executing function {function_id}: {str(e)}"}
    
    async def call_jira_function(self, function_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Jira MCP function"""
        if not self.jira_client:
            return {"error": "Jira client not initialized. Check your configuration."}
        
        try:
            if function_name == "create_issue":
                # Create Jira issue
                issue_dict = {
                    'project': {'key': 'PROJ'},  # Default project key
                    'summary': params.get('title', params.get('summary', 'New Issue')),
                    'description': params.get('description', ''),
                    'issuetype': {'name': params.get('issue_type', 'Story')},
                    'priority': {'name': params.get('priority', 'Medium')}
                }
                
                new_issue = self.jira_client.create_issue(fields=issue_dict)
                
                jira_url = getattr(settings, 'jira_instance_url', 'https://your-jira.atlassian.net')
                
                return {
                    "success": True,
                    "data": {
                        "key": new_issue.key,
                        "id": new_issue.id,
                        "summary": new_issue.fields.summary,
                        "status": new_issue.fields.status.name,
                        "url": f"{jira_url}/browse/{new_issue.key}"
                    }
                }
            
            elif function_name == "search_issues":
                # Search Jira issues
                jql = params.get('jql', 'assignee = currentUser() AND resolution = Unresolved')
                issues = self.jira_client.search_issues(jql, maxResults=10)
                
                return {
                    "success": True,
                    "data": [
                        {
                            "key": issue.key,
                            "summary": issue.fields.summary,
                            "status": issue.fields.status.name,
                            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
                        }
                        for issue in issues
                    ]
                }
            
            else:
                return {"error": f"Unknown Jira function: {function_name}"}
                
        except Exception as e:
            return {"error": f"Jira operation failed: {str(e)}"}
    
    async def call_confluence_function(self, function_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Confluence MCP function"""
        if not self.confluence_client:
            return {"error": "Confluence client not initialized. Check your configuration."}
        
        try:
            if function_name == "create_page":
                # Create Confluence page
                space_key = params.get('spaceKey', params.get('space', 'PROJ'))
                title = params.get('title', 'New Page')
                content = params.get('content', '')
                
                # Convert markdown to Confluence format if needed
                formatted_content = self._format_confluence_content(content)
                
                page = self.confluence_client.create_page(
                    space=space_key,
                    title=title,
                    body=formatted_content
                )
                
                confluence_url = getattr(settings, 'confluence_url', 'https://your-org.atlassian.net/wiki')
                
                return {
                    "success": True,
                    "data": {
                        "id": page['id'],
                        "title": page['title'],
                        "url": f"{confluence_url}/pages/viewpage.action?pageId={page['id']}"
                    }
                }
            
            elif function_name == "search_pages":
                # Search Confluence pages
                query = params.get('query', '')
                space = params.get('space', None)
                
                results = self.confluence_client.cql(
                    f"text ~ '{query}'" + (f" AND space = '{space}'" if space else ""),
                    limit=10
                )
                
                return {
                    "success": True,
                    "data": [
                        {
                            "id": result['id'],
                            "title": result['title'],
                            "url": result['_links']['webui']
                        }
                        for result in results['results']
                    ]
                }
            
            else:
                return {"error": f"Unknown Confluence function: {function_name}"}
                
        except Exception as e:
            return {"error": f"Confluence operation failed: {str(e)}"}
    
    async def _handle_idea_function(self, function_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle idea management functions"""
        if function_id == "idea-create":
            return {
                "success": True,
                "data": {
                    "id": f"idea-{datetime.now().timestamp()}",
                    "title": params.get('title', 'New Idea'),
                    "description": params.get('description', ''),
                    "timestamp": datetime.now().isoformat(),
                    "status": "created"
                }
            }
        
        elif function_id == "idea-analyze":
            # Simulate idea analysis
            return {
                "success": True,
                "data": {
                    "feasibility": "high",
                    "market_potential": "medium",
                    "technical_complexity": "medium",
                    "estimated_timeline": "3-6 months",
                    "key_challenges": ["User acquisition", "Competition", "Scaling"],
                    "next_steps": ["Market research", "MVP development", "User testing"],
                    "analysis_timestamp": datetime.now().isoformat()
                }
            }
        
        return {"error": f"Unknown idea function: {function_id}"}
    
    def _format_confluence_content(self, content: str) -> str:
        """Format content for Confluence"""
        # Basic formatting - convert markdown to Confluence markup
        formatted = content
        
        # Convert headers
        formatted = formatted.replace('# ', '<h1>').replace('\n', '</h1>\n')
        formatted = formatted.replace('## ', '<h2>').replace('\n', '</h2>\n')
        formatted = formatted.replace('### ', '<h3>').replace('\n', '</h3>\n')
        
        # Convert lists
        import re
        formatted = re.sub(r'^\* ', '<ul><li>', formatted, flags=re.MULTILINE)
        formatted = re.sub(r'^\d+\. ', '<ol><li>', formatted, flags=re.MULTILINE)
        
        return formatted
    
    def get_function_status(self, function_id: str) -> Dict[str, Any]:
        """Get status of a specific function"""
        for func in self.available_functions:
            if func['id'] == function_id:
                return {
                    "id": func['id'],
                    "name": func['name'],
                    "enabled": func['isEnabled'],
                    "active": func['isActive'],
                    "status": "ready" if func['isEnabled'] else "disabled"
                }
        return {"error": f"Function {function_id} not found"}
    
    def update_function_status(self, function_id: str, enabled: bool = None, active: bool = None) -> Dict[str, Any]:
        """Update function status"""
        for func in self.available_functions:
            if func['id'] == function_id:
                if enabled is not None:
                    func['isEnabled'] = enabled
                if active is not None:
                    func['isActive'] = active
                return {"success": True, "function": func}
        return {"error": f"Function {function_id} not found"}

# Global service instance
mcp_service = MCPService() 