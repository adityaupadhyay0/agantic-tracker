import os
from openai import AsyncOpenAI
from app.schemas.telemetry import TelemetryEvent, WorkState
from typing import List, Tuple

class LLMInterpreter:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def interpret(self, events: List[TelemetryEvent]) -> Tuple[WorkState, float, List[str]]:
        """
        Uses LLM to interpret complex/ambiguous sequences of telemetry events.
        """
        if not os.getenv("OPENAI_API_KEY"):
            # Fallback if no key provided during dev
            return WorkState.RESEARCH, 0.4, ["LLM skipped: API Key missing"]

        events_summary = "\n".join([f"{e.timestamp}: {e.source} - {e.event_type} ({e.metadata})" for e in events])

        prompt = f"""
        As an organizational intelligence expert, classify the following sequence of human work telemetry into one of the CORTEX work states:
        deep_focus, research, implementation, review, debugging, coordination, planning, learning, idle.

        Telemetry Events:
        {events_summary}

        Return ONLY a JSON object with:
        {{
            "state": "one_of_the_states",
            "confidence": 0.0-1.0,
            "evidence": ["point 1", "point 2"]
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = response.choices[0].message.content
            import json
            result = json.loads(data)
            return WorkState(result["state"]), result["confidence"], result["evidence"]
        except Exception as e:
            print(f"LLM Error: {e}")
            return WorkState.RESEARCH, 0.3, [f"LLM Interpretation failed: {str(e)}"]
