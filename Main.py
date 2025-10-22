from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
app = FastAPI()

SYSTEM_PROMPT = (
    "You are a relationship interpreter. When given a message from one romantic partner to another, "
    "explain the emotional context and what they really mean. Be concise, direct, and supportive. "
    "Focus on decoding ambiguous phrases (like 'I'm fine', 'Nothing's wrong', 'Do whatever you want')."
)

@app.post("/layercode-backend")
async def handle_layercode(request: Request):
    payload = await request.json()
    user_input = payload.get("text", "")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    def stream_gpt():
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # Update to latest model if you want
            messages=messages,
            stream=True,
        )
        for chunk in response:
            content = chunk['choices'][0].get('delta', {}).get('content', '')
            if content:
                yield content

    return StreamingResponse(stream_gpt(), media_type="text/event-stream")
