from flask import Flask, request, jsonify, send_from_directory

from agent import decide_route, extract_expression, chat, web_search
from tools import calculator


# =========================================================
# NEXORA FLASK APPLICATION
# =========================================================

app = Flask(__name__, static_folder="frontend")


# =========================================================
# NEXORA IDENTITY
# =========================================================

conversation = [
    {
        "role": "system",
        "content": """
You are NEXORA, a general-purpose AI agent.

Your name is Nexora.

IMPORTANT IDENTITY RULES:

- Always identify yourself as Nexora when asked who you are.
- Never say that you are ChatGPT.
- Never say that you are created by OpenAI.
- Never introduce yourself as an OpenAI assistant.
- Never claim to be Grok, Gemini, Claude, or another AI.
- You are the AI agent inside the Nexora application.

DEVELOPMENT INFORMATION:

- Nexora was developed by Sunayana and her team.
- If asked "Who developed you?", answer exactly:
  "Nexora was developed by Sunayana and her team."

ABOUT NEXORA:

Nexora is a general-purpose AI agent.

Nexora can:

- Answer general questions
- Explain concepts
- Help with coding
- Help with learning
- Help with writing
- Brainstorm ideas
- Perform calculations
- Search for current information
- Use available tools
- Decide which capability is appropriate for a user's request

When asked what you are, identify yourself as Nexora.

When asked who developed you, identify Sunayana and her team.

Keep answers clear, helpful, natural and easy to understand.
"""
    }
]


# =========================================================
# FRONTEND
# =========================================================

@app.route("/")
def home():
    return send_from_directory(
        "frontend",
        "index.html"
    )


# =========================================================
# CHAT API
# =========================================================

@app.route("/chat", methods=["POST"])
def chat_endpoint():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received."
        }), 400


    user_input = data.get(
        "message",
        ""
    ).strip()


    if not user_input:
        return jsonify({
            "error": "Message is empty."
        }), 400


    try:

        # =================================================
        # NEXORA ROUTER
        # =================================================

        route = decide_route(user_input)


        # =================================================
        # CALCULATOR
        # =================================================

        if route == "CALCULATOR":

            expression = extract_expression(
                user_input
            )

            result = calculator(
                expression
            )


            from agent import client


            response = client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": """
You are Nexora, the calculator capability
of the Nexora AI agent.

Never identify yourself as ChatGPT or OpenAI.

Use the calculator result provided.

Do not perform the calculation again.

Give the user a short and clear answer.
"""
                    },

                    {
                        "role": "user",
                        "content": f"""
User asked:

{user_input}

Expression:

{expression}

Calculator result:

{result}

Give the final answer clearly.
"""
                    }
                ],

                temperature=0
            )


            answer = (
                response
                .choices[0]
                .message
                .content
            )


            return jsonify({
                "route": "CALCULATOR",
                "response": answer
            })


        # =================================================
        # WEB SEARCH
        # =================================================

        elif route == "WEB":

            answer = web_search(
                user_input
            )


            return jsonify({
                "route": "WEB",
                "response": answer
            })


        # =================================================
        # NORMAL AI CHAT
        # =================================================

        else:

            answer = chat(
                user_input,
                conversation
            )


            return jsonify({
                "route": "CHAT",
                "response": answer
            })


    except Exception as error:

        print(
            "Nexora Error:",
            error
        )


        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# START NEXORA
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("          NEXORA AI AGENT")
    print("======================================")
    print("General AI : ON")
    print("Calculator : ON")
    print("Web Search : ON")
    print("Developer  : Sunayana and her team")
    print()
    print("Nexora is running at:")
    print("http://127.0.0.1:5000")
    print("======================================")
    print()


    app.run(
        debug=True,
        port=5000
    )