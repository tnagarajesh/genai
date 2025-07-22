# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)

openai.api_key = os.getenv("openai.api_key")

system_prompt = "You are an affiliate marketer and suggest best products by summarizing the " \
"web content based on its features and benefits."
user_prompt = "Summarize the content by bullet points in the markdown format.Ensure" \
" to include key features and benefits without too much text." \
"Make it concise and engaging.Be mindful of max 500 tokens in response."

class ContentRequest(BaseModel):
    content: str

@app.post("/summarize")
async def summarize(request: ContentRequest) -> dict[str, str]:
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt + request.content}        
            ],
        max_tokens=500
    )
    summary = response.choices[0].message.content or ""
    return {"summary": summary}

