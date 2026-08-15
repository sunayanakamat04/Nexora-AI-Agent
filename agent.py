import os

from dotenv import load_dotenv
from groq import Groq

from tools import calculator


# =========================================================
# 1. LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)


# =========================================================
# 2. NEXORA IDENTITY
# =========================================================

NEXORA_IDENTITY = """
You are NEXORA, a general-purpose AI agent.

Your name is Nexora.

Nexora can:
- answer questions
- explain concepts
- help with coding
- help with college projects
- perform calculations
- search current information
- brainstorm ideas

IMPORTANT IDENTITY RULES:

Always identify yourself as Nexora.

Never say you are ChatGPT.

Never say you were created by OpenAI.

Never identify yourself as Grok, Gemini, Claude,
or another AI assistant.

DEVELOPER:

Nexora was developed by Sunayana and her team.

If asked who developed you, answer:

Nexora was developed by Sunayana and her team.


IMPORTANT RESPONSE STYLE:

Always answer in plain text.

Do NOT use:
- asterisks for bold or italics
- Markdown headings
- tables
- horizontal lines
- emojis
- decorative symbols
- excessive formatting

Use short paragraphs or simple numbered points.

Keep answers concise and natural.

For simple questions, answer in 3 to 8 sentences.

For technical explanations, use a simple real-life example
when useful.

Do not give long reports unless the user specifically asks
for a detailed report.

Do not repeat the user's question.

Do not unnecessarily mention which AI model you are using.
"""


# =========================================================
# 3. INPUT LIMIT
# =========================================================

MAX_INPUT_LENGTH = 8000


def clean_input(text):

    text = str(text).strip()

    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]

    return text


# =========================================================
# 4. CALCULATOR DETECTION
# =========================================================

def looks_like_calculation(text):

    text = text.lower().strip()

    calculation_words = [
        "calculate",
        "calculation",
        "compute",
        "evaluate",
        "solve",
        "find the value"
    ]

    math_symbols = [
        "+",
        "-",
        "*",
        "/",
        "%",
        "^",
        "="
    ]

    has_word = any(
        word in text
        for word in calculation_words
    )

    has_symbol = any(
        symbol in text
        for symbol in math_symbols
    )

    has_number = any(
        character.isdigit()
        for character in text
    )

    if has_number and (
        has_word or has_symbol
    ):
        return True

    return False


# =========================================================
# 5. WEB DETECTION
# =========================================================

def looks_like_web_request(text):

    text = text.lower().strip()

    web_words = [
        "latest",
        "current",
        "recent",
        "today",
        "today's",
        "news",
        "live",
        "price",
        "prices",
        "weather",
        "events",
        "2026",
        "right now",
        "currently"
    ]

    return any(
        word in text
        for word in web_words
    )


# =========================================================
# 6. INTELLIGENT ROUTER
# =========================================================

def decide_route(user_input):

    user_input = clean_input(user_input)

    # Calculator first
    if looks_like_calculation(user_input):
        return "CALCULATOR"

    # Current information
    if looks_like_web_request(user_input):
        return "WEB"

    # AI routing
    prompt = f"""
You are the routing brain of Nexora.

Choose exactly one:

CALCULATOR
WEB
CHAT

CALCULATOR:
Mathematical calculations.

WEB:
Latest, current, recent, news, live information,
prices, events, or information that may have changed.

CHAT:
Normal questions, explanations, coding, writing,
learning, project help, brainstorming and conversation.

Return only one word.

User request:
{user_input}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=10
    )

    route = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .upper()
    )

    if "CALCULATOR" in route:
        return "CALCULATOR"

    if "WEB" in route:
        return "WEB"

    return "CHAT"


# =========================================================
# 7. EXTRACT MATH EXPRESSION
# =========================================================

def extract_expression(user_input):

    user_input = clean_input(user_input)

    prompt = f"""
Extract only the mathematical expression.

Examples:

Calculate 245 * 67
245 * 67

What is 500 + 250?
500 + 250

Calculate 20+10*50/3
20+10*50/3

Return only the expression.
No words.
No explanation.
No markdown.

User request:
{user_input}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=100
    )

    expression = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    expression = expression.replace(
        "```python",
        ""
    )

    expression = expression.replace(
        "```",
        ""
    )

    return expression.strip()


# =========================================================
# 8. NORMAL CHAT
# =========================================================

def chat(user_input, conversation):

    user_input = clean_input(user_input)

    conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Keep conversation small
    if len(conversation) > 9:
        conversation[:] = (
            conversation[:1]
            + conversation[-8:]
        )

    # Add a strict formatting instruction
    style_message = {
        "role": "system",
        "content": """
For this response, follow these rules strictly:

Use plain text only.

Do not use:
asterisks
Markdown headings
Markdown tables
horizontal lines
emojis
decorative symbols

Keep the response concise.

Use simple sentences and short paragraphs.

For technical explanations, give one simple example if useful.

Do not produce a long report unless specifically requested.
"""
    }

    messages_for_model = [
        conversation[0],
        style_message
    ] + conversation[1:]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages_for_model,
        temperature=0.5,
        max_completion_tokens=600
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    conversation.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer


# =========================================================
# 9. WEB SEARCH
# =========================================================

def web_search_with_model(user_input, model):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
You are Nexora's web-search capability.

Search for current or recent information.

Answer in plain text only.

Do not use:
asterisks
Markdown headings
tables
horizontal lines
emojis
decorative symbols

Keep the answer concise.

Give only the most useful information.

You are Nexora.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        tools=[
            {
                "type": "browser_search"
            }
        ],
        tool_choice="required",
        temperature=1,
        max_completion_tokens=1200
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    if not answer:
        raise Exception(
            "Web search returned an empty response."
        )

    return answer


def web_search(user_input):

    user_input = clean_input(user_input)

    try:

        print(
            "Web Search: using GPT-OSS-20B..."
        )

        return web_search_with_model(
            user_input,
            "openai/gpt-oss-20b"
        )

    except Exception as first_error:

        error_text = str(first_error).lower()

        if (
            "429" in error_text
            or "rate_limit" in error_text
            or "rate limit" in error_text
            or "tokens per day" in error_text
            or "request too large" in error_text
        ):

            print(
                "Primary web model unavailable."
            )

            print(
                "Switching to GPT-OSS-120B..."
            )

            try:

                return web_search_with_model(
                    user_input,
                    "openai/gpt-oss-120b"
                )

            except Exception:
                raise Exception(
                    "Web search is temporarily unavailable."
                )

        raise first_error


# =========================================================
# 10. CALCULATOR RESPONSE
# =========================================================

def calculator_response(user_input):

    expression = extract_expression(
        user_input
    )

    result = calculator(
        expression
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are Nexora.

Return only a short plain-text answer.

Do not use:
asterisks
Markdown
emojis
decorative symbols

Use the calculator result exactly as provided.
Do not calculate it again.
"""
            },
            {
                "role": "user",
                "content": f"""
User request:
{user_input}

Expression:
{expression}

Calculator result:
{result}
"""
            }
        ],
        temperature=0,
        max_completion_tokens=100
    )

    return (
        response
        .choices[0]
        .message
        .content
    )


# =========================================================
# 11. TERMINAL MODE
# =========================================================

def run_terminal_agent():

    conversation = [
        {
            "role": "system",
            "content": NEXORA_IDENTITY
        }
    ]

    print()
    print("==========================================")
    print("              NEXORA")
    print("==========================================")
    print("General AI : ON")
    print("Calculator : ON")
    print("Web Search : ON")
    print("Developer  : Sunayana and her team")
    print()
    print("Nexora AI Agent is ready.")
    print("Type 'exit' to stop.")
    print("==========================================")
    print()

    while True:

        user_input = input(
            "You: "
        ).strip()

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            print(
                "\nNexora: Goodbye!"
            )
            break

        if not user_input:
            continue

        try:

            route = decide_route(
                user_input
            )

            print(
                f"Decision: {route}"
            )

            if route == "CALCULATOR":

                answer = calculator_response(
                    user_input
                )

                print(
                    "\nNexora:",
                    answer
                )

            elif route == "WEB":

                answer = web_search(
                    user_input
                )

                print(
                    "\nNexora:",
                    answer
                )

            else:

                answer = chat(
                    user_input,
                    conversation
                )

                print(
                    "\nNexora:",
                    answer
                )

        except Exception as error:

            print(
                "\nNexora error:",
                error
            )

        print()


# =========================================================
# 12. START
# =========================================================

if __name__ == "__main__":
    run_terminal_agent()