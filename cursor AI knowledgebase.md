
to save token space (you can customize ignore rules) . Indexed data is kept for at least 6 weeks of
inactivity per project . Beyond static code, Cursor’s indexing extends to  Git   history: it
automatically indexes merged PRs and their summaries, so the AI can answer questions about code
changes over time . For example, you can ask in chat  @1234  (where 1234 is a PR number) to
pull that PR’s diff and discussion into context . This deep integration of version control history
(supporting GitHub and Bitbucket for now ) means the assistant is aware of not just the
current code, but how it evolved, which aids in debugging and understanding rationale.
Integration & Extensibility: Cursor is designed to be extended and integrated into your workflows.
The aforementioned MCP (Model Context Protocol) is an open standard that allows anyone to create
a tool “server” accessible to the AI . MCP servers can be local processes (communicating via
stdout) or remote web services (via HTTP or Server-Sent Events) . Many official and community
integrations exist – from databases (Postgres, Redis) to SaaS APIs (Stripe, Shopify) to utilities (a
Browser for web search, Zapier for connecting apps, etc.) . Installing an MCP server is as easy
as adding a few lines to a JSON config ( ~/.cursor/mcp.json  globally, or  .cursor/mcp.json
per project) with the command to run and any environment vars (like API keys) . Cursor also
supports one-click installation via URL deep links (e.g. a docs site can include an “Add to Cursor”
button) that encode the server config . Once installed and running, the new tool appears in
the Cursor UI’s “Available Tools” list for the Agent . You can toggle tools on/off as needed during a
chat session . For example, if you integrate a  Jira   MCP  server, you might see tools like
jql_search   or   get_issue   that the agent can use to query your Jira workspace .
(Atlassian is even offering an official Remote MCP server for Jira/Confluence that uses OAuth and
their Teamwork Graph on the backend – enabling actions like summarizing pages or bulk-creating
issues from the IDE assistant .) This modular MCP architecture means you can tailor Cursor to
your project needs, essentially giving the AI “plugins” to interact with the wider ecosystem.
DevOps & Collaboration: Cursor not only writes code, it also helps manage and discuss it. Through
the Slack integration, your team can converse with Cursor’s Agent directly in Slack channels .
Mentioning  @Cursor  in Slack will spin up a Background Agent linked to your repository – it will
read the thread’s conversation for context and then act on the request . For example, if a few
team members are discussing a bug in Slack, someone can simply write “@Cursor, fix this bug” and
the AI will interpret the preceding messages (stack traces, ideas, etc.), then proceed to write a fix on
a new Git branch . You can refine its work by replying with follow-up instructions in thread.
Slack commands allow targeting a specific repo or branch, listing running agents, and tweaking
settings like which model to use . When the agent finishes, it can post a summary or a link to
the PR it created . This makes Cursor a seamless part of team workflows – issues discussed on
Slack can be turned into code changes without leaving the chat. Additionally, Cursor’s Web and
Mobile interface ( cursor.com/agents ) extends this capability to any device . You can start
an agent task from your phone or browser – say, on your commute – and later “Open in Cursor” on
your desktop to review and merge the changes . The web UI supports sharing agent sessions
via link for collaboration, and even doing PR reviews in-browser with AI assistance . All these
integrations are secured – for example, connecting Slack or GitHub requires OAuth permissions, and
you can enforce org-wide Privacy Mode so that no sensitive code is retained on Cursor’s servers
beyond what’s needed for the task .
Security & Privacy: As an enterprise-focused tool, Cursor provides controls to safeguard your code
and data. Privacy Mode can be enabled such that no code or conversation is stored on Cursor’s
47
48 49
50 51
52
53 51
• 
23
54
55 56
57 58
59 60
24
61
62 63
64 65
• 
37
66 67
68 69
70 71
72
73 74
75 76
77 78
79 80
• 
3
side beyond each request . In Privacy Mode, even model providers (OpenAI/Anthropic) don’t
retain the prompts – Cursor ensures they’re deleted after the API call . By default, Cursor may
collect some usage telemetry and even prompts/snippets to improve the AI (similar to how GitHub
Copilot transmits code), but Pro/Enterprise users can opt out completely. When using background
agents or MCP integrations, any secrets (API keys, DB passwords) are stored encrypted at rest and
only used in-memory for the tool sessions . On Enterprise plans, SAML SSO and SCIM can be
used for identity management, and admins get an Audit Dashboard via the Admin API to track
usage   (who   is   prompting   how   much,   which   models,   etc.) .   The   Admin   API   allows
programmatic retrieval of team metrics, e.g. daily token usage per user, number of suggestions
accepted vs rejected, etc., for integration with your own dashboards . (See Appendix A for
examples of Admin API endpoints and data.) On the model side, your code is processed by either
Cursor’s self-hosted models or trusted third-party providers (OpenAI, Anthropic, etc.) – all hosted in
the US . No matter the model, all generated code is considered your IP (Cursor’s terms ensure
you own the outputs) . Overall, while using an AI coding assistant introduces some new
threat surfaces (e.g. an agent misinterpreting a prompt and deleting code, or leaking data via tool
outputs), Cursor addresses these with a combination of confirmations, robust logging, permission
scopes, and user education (it even shows a warning about prompt injection risks for autonomous
agents ). As a best practice, teams should review AI-generated changes (Cursor makes that easier
by presenting diffs and requiring a human merge for PRs) and limit production-critical actions to
supervised modes initially.
Limitations & Best Practices: Despite its power, Cursor (like all AI systems) has limitations. The
large context windows in Max Mode come at the cost of slower responses and significant token
usage – you wouldn’t use a 1M token context for every small edit . Instead, a common
workflow is to use normal mode for day-to-day work and only invoke Max Mode for tasks like
analyzing a huge log file or refactoring across a giant monorepo. Also note that not all models are
equal: e.g. Anthropic’s Claude is very good at following structured instructions, while OpenAI’s
models might produce more creative code – Cursor lets you switch models per chat to find the best
fit, including an “Auto” mode that picks a model based on current demand and reliability .
Another limitation is that the AI does not compile or run code in its head – so it can introduce syntax
errors or type errors. Cursor mitigates this by using a two-step “apply model” for code edits: the
Agent often outputs a  semantic  diff  (high-level changes with placeholders), which a secondary
model then applies to produce actual code and even fixes trivial mistakes . This improves
correctness, but it’s not foolproof; you should still run your tests. The “Bug Bot” feature (available in
Pro) can be used to scan your code for likely bugs – it’s essentially an AI code reviewer that leaves
comments or suggestions. Many users run Bug Bot after big AI-generated changes to catch issues
proactively. Rule files are another best practice: by writing down project conventions in  .cursor/
rules/*.mdc , you give the AI system-level instructions (e.g. “All API endpoints must use XYZ auth
pattern”) that persist across sessions . These rules act like unit tests for the AI’s output – the
Agent will include them in its prompt and thus avoid suggestions that violate them. Additionally,
rules can include templates or examples. In effect, investing time in Rules and Memories makes
Cursor a domain expert on your codebase. For instance, if your conversation leads to a decision
(“We’ll use a binary search here for efficiency”), you can ask the Agent to “remember this” – it will
save a Memory (with your approval) that becomes a project-specific rule going forward . On
the UI side, one best practice is to explicitly use the  @  syntax to provide context to the AI. Instead of
hoping it will find the relevant file, you can attach files or even entire folders to your prompt
( @filename.py  in chat will feed that file’s content) . Power users often prepend important files
81 82
82
83 84
85 86
87 88
82
89 90
42
• 
12 91
92 93
94 95
7 96
97 98
99
4
at conversation start to ground the AI. In summary, Cursor works best when you treat it as a
junior   engineer: give it clear guidance (and rules), check its work (run Bug Bot or tests), and
gradually trust it with more autonomy as it proves itself.
Comparison with Other Tools: Finally, it’s useful to place Cursor in context with alternatives like
GitHub Copilot, ChatGPT, and Sourcegraph Cody.  Copilot  excels at inline code suggestions but
operates on a single-file context and has no memory of project-wide info – whereas Cursor’s agent
can consider many files and perform multi-file edits (it’s more analogous to having ChatGPT inside
your editor with access to your repo). ChatGPT (OpenAI) in a web browser can chat about code and
even do some function calling, but you must copy/paste code, and it can’t directly apply changes. In
contrast, Cursor is embedded in the development workflow – it understands the open project structure,
can execute git operations, run code, and update files without you leaving the IDE . 
Sourcegraph Cody offers an AI that knows your entire repository (via indexing) and can answer
questions or generate code with references – similar to Cursor’s codebase index + Q&A ability.
However, Cody doesn’t natively modify your files; you’d still do the edits. Cursor goes further by
automating the edit-compile-test loop via its agents. In terms of extensibility, Cursor’s MCP tooling
is emerging as a standard (Anthropic’s Claude and others also adopt it) , whereas something
like Copilot is closed and limited to code completions. Cursor’s “Background Agent” concept is quite
unique right now – it’s comparable to having a Jenkins CI that writes code for you. This makes Cursor
particularly attractive for large organizations: it can automate boilerplate tasks (e.g. adding logging
to all services) or triage issues (the agent could attempt to reproduce and fix a bug, then open a PR).
Of course, with great power comes need for oversight. Unlike an autopilot, Cursor doesn’t guarantee
correctness or code quality – but it dramatically accelerates the drafting and exploration phase of
development. Many teams use Cursor for productivity (it “writes 70% of my code” in practice )
and pair it with code reviews and CI tests as usual. In summary:  Copilot  is like an AI pair
programmer whispering suggestions; ChatGPT is like a powerful advisor you have to copy code to;
Cody is an encyclopedia for your code; and Cursor attempts to be the whole package – an AI partner
that not only advises but actually edits, executes, and manages code under your guidance.
Deep-Dive Sections
Cursor’s Architecture and Internals
Forked VS Code: Cursor’s desktop app is a modified VS Code editor , which means it inherits familiarity
(file explorer, text editor, etc.) while adding custom AI panes and commands. This also allows it to plug into
Git easily and support multi-root workspaces . Cursor’s team has built a cloud backend that interfaces
with various LLM APIs and hosts their proprietary models (for completions and reasoning). The heavy lifting
of prompt orchestration happens client-side and server-side in tandem. For example, when you hit the “Ask
Cursor” chat, the client assembles a JSON payload including: the conversation history, relevant code
snippets (from the index or attached via  @file ), active rules, and tool specifications. This goes to Cursor’s
cloud, which adds authentication and routes it to the selected model (OpenAI, Anthropic, etc.). If the model
then outputs a tool invocation (e.g.  read_file("app.py") ), Cursor’s client intercepts that, executes it
(reads  app.py  from your disk), and streams the file content back into the model prompt . This loop
continues until the model finishes its solution. In effect, Cursor’s architecture is an implementation of an
agentic loop on top of a standard LLM – the model is prompted to use “tools” instead of hallucinating
missing info, and Cursor provides those tools. This design is why smaller models like Cursor’s own ones
• 
20 100
101 102
103
104
105
19 20
5
(e.g. Cursor Small, DeepSeek) are listed in the model menu – they act as helpers. For instance, DeepSeek
models are likely used to embed and retrieve code (a two-pass process: one model creates embeddings,
another ranks results) . There’s also an “apply code” model used when the agent returns a diff to actually
apply changes and fix syntax . By splitting tasks among specialized models, Cursor improves reliability
(the large model focuses on high-level logic, while a smaller one ensures the diff is correctly applied) . All
of this is orchestrated behind the scenes; from the user’s perspective, you just see that the agent’s
suggestion cleanly updates the code with minimal errors.
MCP Protocol: The Model Context Protocol is central to Cursor’s extensibility. Technically, MCP defines a
simple contract for tool processes. A tool can run locally (as a CLI program that reads JSON requests from
stdin and writes JSON responses to stdout), or remotely (as an HTTP server following a specific SSE/
streaming format) . Each MCP server registers one or more “tools” by name along with a JSON schema
for their inputs/outputs . When the agent wants to use a tool, it outputs a JSON blob (this is captured
between special tokens in the model’s output) and Cursor parses it, calls the corresponding MCP server,
then feeds the response back. For example, the Jira MCP (community-built) registers a  jql_search  tool.
The agent might output:  { "tool": "jira.jql_search", "params": {"jql": "project = ABC 
AND status = 'To Do'"} } . Cursor then sends this to the Jira MCP (which calls Jira’s REST API), gets
results, and injects those results into the chat as the assistant’s next message (marked as tool output) .
The model then continues, now knowing the search results. From a  security  standpoint, tools are
sandboxed at the process/API level – e.g. a local CLI tool cannot access your system beyond what it’s coded
to do (though one should still vet any third-party tool’s code before trusting it). That’s why Cursor advises
only installing MCP servers from trusted sources . In enterprise settings, developers might write in-
house MCP servers (e.g. to query an internal knowledge base); these can be distributed within the team via
a config file. Many MCP servers (including Atlassian’s official one) use OAuth for auth – when you add them,
a browser flow asks you to log in and authorize access . The OAuth token is then stored and used by
the MCP server when fulfilling requests. Cursor’s interface clearly shows which MCP servers are “Connected”
and lets you enable/disable them on the fly , so you have control over what the agent can do at any
time.
Data   &   Memory:  Cursor employs both ephemeral and persistent memory mechanisms. Ephemeral
memory is the prompt context: the last few messages, recent code, etc. This is constrained by token limits
(though large in Max Mode). For longer-term memory, Cursor uses two features:  Memories  and
Checkpoints. Memories, as discussed, are essentially chat-derived rules: a background “observer” model
monitors your conversations and suggests important facts to save . If you approve, these get added to
your project’s rules (marked as auto-generated memory) so that even if you start a fresh chat tomorrow,
those points will be re-injected. Checkpoints refer to saving specific conversation states – Cursor’s chat UI
lets you fork or save sessions so you can refer back to them (this is more a UI feature than an AI one,
preventing context loss). As for code indexing data, it’s stored on Cursor’s servers encrypted and isolated
per account. There is no user-facing global view of all your indexed repos yet ; you manage each
project’s index in that project’s settings (you can delete an index by removing the project or your account)
. Code embeddings are typically not the raw code – they are numerical vectors that can’t
reconstruct the code (they capture semantic meaning), but they still represent your proprietary info, so
Cursor treats them as sensitive (and deletes them if you delete your account or after inactivity as noted).
Privacy Mode will prevent storing embeddings on the server long-term, at the cost of having to re-index
frequently (and possibly with slower or less relevant results, since the index can’t be reused as effectively).
In short, Cursor’s design tries to balance leveraging data for AI accuracy with giving users control over that
data lifecycle.
44
94
94
106
63 107
24
108
109 110
61
97
111
111 112
6
Using Cursor for Project Management (Jira, Confluence, etc.)
Cursor’s integration potential isn’t limited to code – it can serve as a general project assistant when
connected to PM tools. Many teams have started using Cursor’s agent to automate project management
tasks that previously required manual updates in systems like Jira. By connecting a Jira MCP server, for
instance, you enable commands like “Create a Jira ticket for this bug” or “What’s the status of ticket
PROJ-123?” directly in the chat. The agent can call the Jira tool to create issues or fetch statuses and
incorporate that info into its response. Atlassian’s own  Remote   MCP  (in beta) goes further: it allows
summarizing Confluence pages or even performing multi-step actions like “find all Jira issues marked
blocking, and draft a Confluence update with their summaries” . Behind the scenes, the agent might call
a  search_issues  tool, then a  get_confluence_page  tool, then synthesize an answer. Because these
operations respect user permissions (OAuth tokens, etc.), the AI cannot access anything a real user couldn’t
– e.g. if a page is restricted, the Confluence MCP won’t return it. One best practice when using Cursor in this
way is to be explicit with your instructions: e.g. “(@Jira) search for issues assigned to me due this week” or
“Use the Confluence tool to create a page titled X with content Y.” You can actually speak to the agent about
using tools – since the Agent has been trained to understand that it can use them, it often decides on its
own. But if it doesn’t, nudging it in the prompt helps. Cursor’s Background Agent can also combine with
project management: imagine telling a background agent to update your project’s CHANGELOG and then
post an update to Confluence. It could use  git log  to compile changes, commit to CHANGELOG.md,
then (via an MCP) create a Confluence page draft. While this is advanced, it illustrates that Cursor’s AI is not
siloed in coding – it can bridge between coding and the meta-work around coding. Comparing to ChatGPT
plugins, which might let ChatGPT interface with, say, Asana or Notion, Cursor’s advantage is the
combination of code context + project context. For example, “Analyze our code for TODO comments and
create Jira tasks for each” is something Cursor could conceivably do (read the codebase for  TODO:  tags,
and for each one, call Jira API to create a ticket with the comment text). This level of integration could save
PMs and engineers a lot of grunt work. That said, it requires careful use – you wouldn’t want duplicates or
incorrect tasks because the AI misinterpreted something. So, test such flows in a sandbox project. In
summary, Cursor can act as a project co-pilot: through MCP, it ties into your planning tools, and through its
coding abilities, it links those plans to the actual code changes. This closes the loop between planning and
execution, all mediated by the AI in natural language.
API Endpoints and SDKs
Currently, Cursor does not offer a public code-generation API in the way OpenAI does – i.e. you can’t
directly send a prompt to Cursor’s servers and get a completion outside the Editor. The focus has been on
in-IDE experience. The closest is the Admin API, which is for analytics (usage data), not for prompting
models . The Admin API uses API keys obtainable by team admins and offers REST endpoints to list
team members, get aggregate daily stats, and fetch detailed usage events . For example, an admin
can  GET /teams/members  to see all users and roles , or  POST /teams/daily-usage-data  with a
date range to get daily counts of lines of code added, AI suggestions accepted, etc., per user . (See
Appendix A for a sample API call and response.) These endpoints enable building custom dashboards or
enforcing internal policy (e.g. if usage exceeds a threshold, maybe prompt the user). As for an SDK, since
Cursor’s main interface is the application itself, there isn’t a separate SDK to embed Cursor into other apps.
Instead, integration is encouraged via MCP or by launching Cursor programmatically with a project (one
could script opening Cursor with a certain file, etc., but that’s just like launching VSCode). Some community
projects have reverse-engineered aspects – for instance, using Cursor’s Slack bot as a pseudo-API: one
could message the bot and get a response. But officially, to leverage Cursor’s models on your own, the
64
113 114
115 87
116
87 88
7
supported way is to bring your own API keys: Cursor allows you to plug in an OpenAI or Anthropic API key
so that the editor uses your quota for completions . This is mostly to bypass Cursor’s request limits if
you have your own high-volume account (or to use models Cursor doesn’t natively provide). However, not all
features work with custom keys – for example, Cursor’s specialized “Reasoning” models (like the  o1  series)
and the Tab auto-complete use Cursor’s hosted models and won’t tap into your key . In practice,
most users rely on Cursor’s provided models and the usage-based pricing for anything beyond the free tier.
Database Schema: The phrase “database schema” in context of Cursor might refer to how it structures
information like code indices, chat histories, etc. While the exact schema isn’t public, one can infer that
Cursor stores: user accounts, team memberships, usage logs (possibly events like “user X made a chat
request of Y tokens”), and indexed code data (probably as vectors in a vector DB, keyed by file and chunk). If
the question is about using Cursor to generate a DB schema – yes, the agent can help there too (for
example, writing SQL migrations or drawing an ER diagram in Markdown). In fact, the Mermaid diagram
support in Cursor is often used to have the AI produce architecture diagrams from code or requirements
. But if by schema we mean how Cursor’s internals are structured, one interesting bit is requests vs
tokens accounting: Cursor’s pricing units (“requests”) abstract away raw tokens. E.g., Pro users get 500 “fast
requests” per month, which correspond roughly to a certain number of messages or tokens with premium
models . In Admin API “usage events,” each event has fields like  requestsCost  and a breakdown
of  inputTokens ,  outputTokens ,  cacheReadTokens  etc., and even whether  maxMode  was true
. This suggests a schema where each AI call is logged with user, model, timestamp, token counts, cost in
“requests,” etc. So, an admin could reconstruct usage costs or identify heavy users . Rate-limits are
enforced in-app (for instance, the free tier might slow down after a certain number of completions). The
Ultra plan ($200/mo) simply raises those limits 20x . 
Appendices
Appendix A: Admin API Example
Using the Admin API requires an API key (generated by a team admin in Cursor’s dashboard). All calls are
basic HTTP requests to  https://api.cursor.com . For example, to fetch team members: 
curl -X GET https://api.cursor.com/teams/members \
-u key_xxxxx:
This returns a JSON listing each member’s name, email, and role (e.g. “owner” or “member”) :
{
"teamMembers": [
{
"name": "Alex",
"email": "developer@company.com",
"role": "member"
},
{
"name": "Sam",
"email": "admin@company.com",
117 118
119 120
121
122 123
124
125
126 127
128 129
116 130
8
"role": "owner"
}
]
}
Another example: getting daily usage stats for a month range, which is a POST to  /teams/daily-usage-
data  with a JSON body of start and end timestamps. The response includes an array of daily data objects
with fields like  totalLinesAdded ,  composerRequests ,  chatRequests , etc. . For instance: 
{
"data": [
{
"date": 1710720000000,
"totalLinesAdded": 1543,
"totalLinesDeleted": 892,
"acceptedLinesAdded": 1102,
"acceptedLinesDeleted": 645,
"composerRequests": 45,
"chatRequests": 128,
"agentRequests": 20,
"mostUsedModel": "claude-3.7-sonnet",
"userEmail": "developer@company.com"
},
{ ... next day ... }
],
"period": {
"startDate": 1710720000000,
"endDate": 1713248400000
}
}
This shows how one might track the impact of Cursor: e.g., out of 1543 lines added on 2025-03-18, 1102
were from AI suggestions (acceptedLinesAdded) – a high adoption rate. Admin API endpoints exist also for
spending reports (cost per user)  and for detailed event logs (each AI request event with token
counts and whether it was usage-based) . In general, the Admin API is RESTful and JSON-based,
making it easy to integrate with reporting tools.
Appendix B: Example MCP Server Configuration
Below is an example of adding a custom MCP server to Cursor. Say we want to integrate a Jira tool (using
the community “jira-mcp” package). We would update our  ~/.cursor/mcp.json  (for a global tool) as
follows:
{
"mcpServers": {
"jira": {
87 131
132 133
124 125
9
"command": "npx",
"args": ["-y", "jira-mcp"],
"env": {
"JIRA_INSTANCE_URL": "https://your-company.atlassian.net",
"JIRA_USER_EMAIL": "your.email@company.com",
"JIRA_API_KEY": "your_generated_api_token"
}
}
}
}
In this JSON, we define a server named “jira” that is launched by running  npx -y jira-mcp  (Node will
download and run the  jira-mcp  package) . We also set environment variables for the Jira instance
URL and credentials that the MCP server will use to call the Jira REST API . After saving this config
and restarting Cursor, the Jira tools (e.g.  jql_search  and  get_issue ) become available in the Cursor
chat’s tool palette. The AI can now execute commands like:
{ "tool": "jira.get_issue", "params": { "issueIdOrKey": "PROJ-123" } }
And Cursor will return the issue details (summary, status, etc.) as if you typed them out . This can
then be used in the assistant’s answer. When adding any MCP server, always consult its documentation for
required env vars or setup steps. Some servers might require running a local service separately, but many
(like the above) run on-demand via the   npx   command. As mentioned, you can also install official
integrations via Cursor’s Integrations UI (under Tools > Browse MCP Tools or the web dashboard), which
automates this process with an OAuth flow for things like Slack or GitHub.
Appendix C: Background Agent Environment Config
To   illustrate   how   one   configures   a   background   agent   environment,   here’s   a   sample   .cursor/
environment.json  for a Node.js project:
{
"install": "npm ci",
"terminals": [
{ "name": "Run Tests", "command": "npm test -- --watchAll=false" },
{ "name": "Dev Server", "command": "npm run start" }
]
}
This tells Cursor to run  npm ci  (clean install) every time a fresh VM is provisioned for the agent . It
also opens two persistent terminal sessions in tmux: one to run tests (so the agent can see test output
continuously) and one to run the dev server. These processes will be running while the agent works,
allowing it to, say, observe the test results after each change (Cursor’s agent is designed to monitor these
outputs). The  snapshot  field (not shown above) could be used if we pre-built a custom Docker image or
snapshot for faster startup – otherwise Cursor uses a default Ubuntu image and caches the state after
134
135 136
137 138
139 140
10
running the install command . If, for example, our project needed a specific version of Chrome for end-
to-end tests, we could extend this config or the Dockerfile. In our simple example, once the background
agent starts, it will have test results streaming in one pane and the dev server logs in another, all accessible
to it. If tests fail, the agent can read those failures from the terminal output and attempt fixes, then re-run
tests (it has permission to rerun the  npm test  command as it’s already running in watch mode). This
autonomous feedback loop is what enables the agent to inch towards a correct solution. From the user’s
perspective, you would see in the Cursor UI (or Slack) that the agent is e.g. “Running tests... 2 failed”, then it
might say “I see 2 tests failing, I will fix those functions,” then it edits files, tests pass, and it reports “All tests
passed and changes have been pushed to branch  cursor-fix-auth  .” Always review environment.json
carefully – a misconfigured command could cause an agent to stall or do nothing useful. Cursor provides a
guided setup for this file ( Cursor > Background Agents > Configure environment ) and even
templates for common setups in the docs. 
Sources:  Cursor official documentation , Cursor community forum and blog posts , and
Atlassian’s announcement . These provide further detail on features, usage, and integration patterns
discussed above. 
Cursor – Models
https://docs.cursor.com/models
Cursor – Concepts
https://docs.cursor.com/get-started/concepts
Cursor – Codebase Indexing
https://docs.cursor.com/context/codebase-indexing
Cursor – Rules
https://docs.cursor.com/context/rules
Cursor – Memories
https://docs.cursor.com/context/memories
Max Mode in Cursor: Power, Access, and Missing Controls - DEV Community
https://dev.to/tawe/max-mode-in-cursor-power-access-and-a-missing-control-panel-4k21
How Cursor (AI IDE) Works - by Shrivu Shankar
https://blog.sshh.io/p/how-cursor-ai-ide-works
Cursor – Model Context Protocol (MCP)
https://docs.cursor.com/context/mcp
Composer access to Jira, Confluence - Feature Requests - Cursor - Community Forum
https://forum.cursor.com/t/composer-access-to-jira-confluence/49734
Cursor – Background Agents
https://docs.cursor.com/background-agent
Cursor – Slack
https://docs.cursor.com/slack
141
81 23 14 94
64
1 2 9 10 11 12 13 81 82 92 93