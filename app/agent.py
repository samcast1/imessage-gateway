import os

from google import genai
from google.genai import types

from app.whoop import run_whoop


SYSTEM_INSTRUCTIONS = """
You are a personal assistant accessed through iMessage.

Keep responses concise and natural because your responses will be sent as
iMessages. Do not use unnecessary formatting, lengthy explanations, or
formal language unless the user asks for it.

You can answer general questions directly.

The user will occasionally ask for a translation.

When translating English into Spanish:
- The user primarily wants English translated into natural, conversational
Latin American Spanish.
- Prefer natural native phrasing over literal word-for-word translation.
- Preserve the original meaning and intent.
- Preserve tone, emotion, humor, sarcasm, slang, and register.
- Use vocabulary and phrasing natural to Latin American Spanish.
- Do not unnecessarily make the translation formal.
- Do not explain the translation unless the user asks.
- If the user asks for another target language, follow that request.
- If the user provides Spanish and asks for translation, infer the requested
  target language from context.

WHOOP:
Use the available WHOOP tools when the user asks for their WHOOP data.
Do not invent WHOOP data.

GENERAL:
Use tools when they provide information you cannot otherwise know.
If a tool fails, explain the failure briefly rather than inventing an answer.
"""


def whoop_morning() -> str:
    """Get the user's WHOOP morning report."""
    return run_whoop("morning")


def whoop_evening() -> str:
    """Get the user's WHOOP evening report."""
    return run_whoop("evening")


TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="whoop_morning",
                description="Get the user's WHOOP morning report.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={},
                ),
            ),
            types.FunctionDeclaration(
                name="whoop_evening",
                description="Get the user's WHOOP evening report.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={},
                ),
            ),
        ]
    )
]


TOOL_FUNCTIONS = {
    "whoop_morning": whoop_morning,
    "whoop_evening": whoop_evening,
}


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def run_agent(user_message: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            tools=TOOLS,
        ),
    )

    while response.function_calls:
        function_responses = []

        for call in response.function_calls:
            function = TOOL_FUNCTIONS.get(call.name)

            if function is None:
                raise RuntimeError(f"Unknown tool requested: {call.name}")

            result = function()

            function_responses.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_message)],
                ),
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=function_responses,
                ),
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
                tools=TOOLS,
            ),
        )

    return response.text.strip()