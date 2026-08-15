NEXORA AI AGENT

Nexora is a general-purpose AI agent developed by Sunayana and her team.

It accepts natural-language requests, identifies the type of task, and selects the appropriate capability to generate a response.

FEATURES

General AI Chat

Handles questions, explanations, coding assistance, learning, writing, brainstorming, and project-related requests.

Calculator

Handles mathematical expressions using a dedicated calculator tool.

Example

Calculate 245 * 67

Web Search

Handles requests that require current, recent, or changing information.

Example

What are the latest AI agent trends in 2026?

Intelligent Routing

Nexora determines which capability should handle the request.

Normal questions are handled through AI chat.

Mathematical requests are handled through the calculator.

Current-information requests are handled through web search.

TECHNOLOGIES

Python

Flask

Groq API

HTML

CSS

JavaScript

Git

GitHub

PROJECT FILES

agent.py

Contains the core Nexora agent logic, including request classification, intelligent routing, AI chat, calculator handling, web search, and conversation handling.

app.py

Provides the Flask backend and connects the web interface with the Nexora agent.

tools.py

Contains the calculator functionality used by Nexora.

frontend/index.html

Contains the web interface built with HTML, CSS, and JavaScript.

requirements.txt

Contains the Python dependencies required by the project.

.gitignore

Prevents sensitive and temporary files from being committed to the repository.

SETUP

Create a virtual environment.

python -m venv venv

Activate the virtual environment on Windows.

venv\Scripts\activate

Install the required packages.

pip install -r requirements.txt

Create a .env file in the project folder and add the Groq API key.

GROQ_API_KEY=your_api_key_here

Do not upload the .env file to GitHub.

Run the application.

python app.py

EXAMPLE REQUESTS

Explain Kubernetes in simple words.

Calculate 20 + 10 * 50 / 3

What are the latest AI agent trends in 2026?

Suggest a simple cloud project for college.

SECURITY

The Groq API key is stored in the .env file and excluded from version control.

The following should remain local:

.env
venv
pycache
*.pyc

Never place API keys directly in source code.

FUTURE IMPROVEMENTS

PDF and document analysis

Image understanding

Voice input and output

Conversation history

User authentication

Additional tools

Cloud deployment

Multi-agent workflows

DEVELOPER

Nexora was developed by Sunayana and her team.
