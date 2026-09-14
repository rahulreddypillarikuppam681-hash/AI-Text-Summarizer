from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os


# ==========================================
# Project configuration
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ==========================================
# Load environment variables
# ==========================================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found in .env"
    )


# ==========================================
# Groq client
# ==========================================

client = Groq(
    api_key=api_key
)


# ==========================================
# FastAPI application
# ==========================================

app = FastAPI(
    title="AI Text Summarizer",
    description="AI-powered text summarization API",
    version="1.0.0"
)


# ==========================================
# Request model
# ==========================================

class TextRequest(BaseModel):

    text: str

    length: str = "medium"

    format: str = "paragraph"


# ==========================================
# Frontend
# ==========================================

frontend_path = os.path.join(
    BASE_DIR,
    "frontend"
)


app.mount(
    "/static",
    StaticFiles(
        directory=frontend_path
    ),
    name="static"
)


@app.get("/")
def home():

    return FileResponse(
        os.path.join(
            frontend_path,
            "index.html"
        )
    )


# ==========================================
# Summarization endpoint
# ==========================================

@app.post("/summarize")
def summarize(request: TextRequest):


    # --------------------------------------
    # Summary length
    # --------------------------------------

    if request.length == "short":

        length_instruction = (
            "Create a very short summary "
            "in 2 to 3 sentences. "
            "Keep only the most important information."
        )


    elif request.length == "detailed":

        length_instruction = (
            "Create a detailed summary covering "
            "the important ideas, facts and key points. "
            "Include useful supporting details."
        )


    else:

        length_instruction = (
            "Create a medium-length summary "
            "covering the main ideas and important details."
        )


    # --------------------------------------
    # Summary format
    # --------------------------------------

    if request.format == "bullets":

        format_instruction = (
            "Present the summary as clear bullet points. "
            "Use a separate bullet point for each important idea. "
            "Do not use a large paragraph."
        )


    else:

        format_instruction = (
            "Present the summary as clear, "
            "well-written paragraphs."
        )


    # --------------------------------------
    # AI request
    # --------------------------------------

    completion = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",

                "content": (
                    "You are an expert text summarizer. "
                    "Create accurate, clear and easy-to-understand "
                    "summaries. Do not add information that is "
                    "not present in the original text."
                )
            },

            {
                "role": "user",

                "content": (
                    f"{length_instruction}\n\n"
                    f"{format_instruction}\n\n"
                    f"Text to summarize:\n\n"
                    f"{request.text}"
                )
            }

        ],

        temperature=0.3

    )


    # --------------------------------------
    # Return result
    # --------------------------------------

    return {

        "summary":
            completion.choices[0].message.content

    }