from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()


class TextRequest(BaseModel):
    text: str


# Serve frontend files
frontend_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

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

    prompt = f"""
Summarize the following text clearly and concisely.

Text:
{request.text}

Summary:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return {
        "summary": result["response"]
    }