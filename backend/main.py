from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os


# Find the project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env from the project folder
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found in .env")

# Create Groq client
client = Groq(api_key=api_key)

app = FastAPI()


class TextRequest(BaseModel):
    text: str


frontend_path = os.path.join(BASE_DIR, "frontend")


app.mount(
    "/static",
    StaticFiles(directory=frontend_path),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(
        os.path.join(frontend_path, "index.html")
    )


@app.post("/summarize")
def summarize(request: TextRequest):

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert text summarizer. "
                    "Create clear, accurate and concise summaries."
                )
            },
            {
                "role": "user",
                "content": f"Summarize this text:\n\n{request.text}"
            }
        ],
        temperature=0.3
    )

    return {
        "summary": completion.choices[0].message.content
    }