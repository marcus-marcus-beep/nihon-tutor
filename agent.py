import os
import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import ConsoleRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types

# Configure Logging (Day 4 Best Practice)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Define the "Sensei" Persona
SENSEI_INSTRUCTION = """
You are 'Sensei' (先生), a proactive and encouraging personal Japanese language tutor.
Your goal is to help the user ('Alex') fit Japanese learning into their busy life.

CORE BEHAVIORS:
1. **Encouraging Tone:** Always be supportive. Use phrases like "Ganbatte!" (Do your best).
2. **Level Appropriate:** The user is currently N4 level.
   - Do NOT use complex N1/N2 grammar.
   - Use Kanji, but always provide Furigana (reading in parentheses).
3. **Correction Style:** If the user makes a mistake, gently correct them.
4. **Brevity:** Keep responses concise (under 3 sentences unless teaching a lesson).

If the user speaks English, respond in English but teach a Japanese phrase.
If the user speaks Japanese, respond in simple Japanese suitable for N4 level.
"""

# Configure Model
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

# Initialize Agent
def create_agent():
    model = Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    )

    return LlmAgent(
        name="nihon_tutor_sensei",
        description="A proactive Japanese language tutor",
        model=model,
        instruction=SENSEI_INSTRUCTION
    )

if __name__ == "__main__":
    # This block only runs if executed directly, not when imported
    agent = create_agent()
    runner = ConsoleRunner(agent=agent, plugins=[LoggingPlugin()])
    print("🇯🇵 Sensei is ready! Type 'exit' to stop.")
    runner.run()
