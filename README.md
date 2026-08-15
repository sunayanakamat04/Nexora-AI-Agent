Nexora AI Agent

Nexora is a general-purpose AI agent developed by Sunayana and her team. It accepts natural-language requests, determines what type of task the user wants to perform, and selects an appropriate capability to generate a response.

Overview

Nexora currently provides three main capabilities:

General AI chat

Mathematical calculations

Web search for current information

The project demonstrates a simple agent architecture in which a router analyzes the user request and selects the required capability.

Architecture

User
  |
  v
Nexora Web Interface
  |
  v
Flask Backend
  |
  v
Nexora Router
  |
  +----------------+------------------+
  |                |                  |
  v                v                  v
AI Chat        Calculator          Web Search
  |                |                  |
  +----------------+------------------+
                   |
                   v
             Final Response
                   |
                   v
                  User

Features

General AI Chat

Handles normal questions, explanations, coding assistance, learning, writing, brainstorming, and project-related requests.

Calculator

Detects mathematical requests and sends the expression to the calculator tool instead of relying only on the language model.

Example:

Calculate 20 + 10 * 50 / 3

Web Search

Routes requests involving current, recent, or changing information to a browser-search capability.

Example:

What are the latest AI agent trends in 2026?

Intelligent Routing

The router decides which capability should handle a request.

Normal question      -> AI Chat
Mathematical request -> Calculator
Current information  -> Web Search

Technologies

Python

Flask

Groq API

HTML

CSS

JavaScript

Git

GitHub

Project Structure

Nexora-AI-Agent/
|
├── agent.py
├── app.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
|
└── frontend/
    └── index.html

File Description

agent.py

Contains the core Nexora agent logic.

It handles:

Request routing

General AI chat

Calculator request handling

Web search

Conversation context

Web search fallback handling

app.py

Runs the Flask backend and connects the frontend to the Nexora agent.

It provides the /chat endpoint used by the web interface.

tools.py

Contains the calculator tool used for mathematical requests.

frontend/index.html

Contains the Nexora user interface built with HTML, CSS, and JavaScript.

requirements.txt

Contains the Python dependencies required to run the project.

.gitignore

Prevents sensitive and temporary files from being committed to GitHub.

Setup

1. Clone the repository

git clone <your-repository>
cd Nexora-AI-Agent

2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure the Groq API key

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here

Do not upload the .env file to GitHub.

5. Run Nexora

python app.py

Open the application in a browser:

http://127.0.0.1:5000

Example Requests

General AI:

Explain Kubernetes in simple words.

Calculator:

Calculate 245 * 67.

Web Search:

What are the latest AI agent trends in 2026?

Project Assistance:

Suggest a simple cloud project for college.

Request Flow

For a normal question:

User
  -> Router
  -> AI Chat
  -> Response

For a calculation:

User
  -> Router
  -> Calculator
  -> Result
  -> Response

For current information:

User
  -> Router
  -> Web Search
  -> Search Result
  -> Response

Security

The Groq API key is stored in .env and excluded from version control.

The following files should not be committed:

.env
venv/
__pycache__/
*.pyc

Never place an API key directly inside Python, HTML, CSS, or JavaScript source code.

Current Limitations

Nexora currently focuses on text-based interaction and provides three main capabilities: AI chat, calculation, and web search.

Possible future additions include:

PDF and document analysis

Image understanding

Voice input and output

Conversation history

User authentication

Additional external tools

Cloud deployment

Multi-agent workflows

Development

Nexora was developed as a practical project to demonstrate how a language model can be combined with routing logic and external tools to create a useful AI agent.

Developer

Nexora was developed by Sunayana and her team.