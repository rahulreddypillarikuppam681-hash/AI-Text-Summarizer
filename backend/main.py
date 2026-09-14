from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException
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
# Generate AI summary
# ==========================================

def generate_summary(
    text,
    length_instruction,
    format_instruction
):

    completion = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",

                "content": (
                    "You are an expert text summarizer. "
                    "Create accurate, clear and easy-to-understand "
                    "summaries. "
                    "Do not add information that is not present "
                    "in the original text."
                )
            },

            {
                "role": "user",

                "content": (
                    f"{length_instruction}\n\n"
                    f"{format_instruction}\n\n"
                    f"Text to summarize:\n\n"
                    f"{text}"
                )
            }

        ],

        temperature=0.3

    )


    return completion.choices[0].message.content


# ==========================================
# Summarization endpoint
# ==========================================

@app.post("/summarize")
def summarize(request: TextRequest):

    text = request.text.strip()


    # --------------------------------------
    # Validate input
    # --------------------------------------

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )


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


    # ======================================
    # Split large text into chunks
    # ======================================

    words = text.split()

    chunk_size = 2500

    chunks = [
        words[i:i + chunk_size]
        for i in range(
            0,
            len(words),
            chunk_size
        )
    ]


    # ======================================
    # Summarize each chunk
    # ======================================

    chunk_summaries = []


    for index, chunk in enumerate(chunks):

        chunk_text = " ".join(chunk)


        chunk_instruction = (
            "Summarize this section of a larger "
            "document. Keep the important facts "
            "and ideas because the section summary "
            "will later be combined with other "
            "section summaries."
        )


        chunk_summary = generate_summary(

            chunk_text,

            chunk_instruction,

            format_instruction

        )


        chunk_summaries.append(
            chunk_summary
        )


    # ======================================
    # Combine summaries
    # ======================================

    if len(chunk_summaries) == 1:

        final_summary = chunk_summaries[0]


    else:

        combined_summaries = "\n\n".join(
            chunk_summaries
        )


        final_instruction = (
            "Create one final summary from the "
            "section summaries below. "
            "Remove repeated information, "
            "combine related ideas and keep "
            "the most important information. "
            f"{length_instruction}"
        )


        final_summary = generate_summary(

            combined_summaries,

            final_instruction,

            format_instruction

        )


    # ======================================
    # Return result
    # ======================================

    return {

        "summary": final_summary,

        "chunks_processed": len(chunks)

    }


# ==========================================
# TXT file upload endpoint
# ==========================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    # --------------------------------------
    # Check filename
    # --------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )


    # --------------------------------------
    # Check extension
    # --------------------------------------

    if not file.filename.lower().endswith(".txt"):

        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported."
        )


    # --------------------------------------
    # Read file
    # --------------------------------------

    contents = await file.read()


    # --------------------------------------
    # Check empty file
    # --------------------------------------

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )


    # --------------------------------------
    # Convert file to text
    # --------------------------------------

    try:

        text = contents.decode("utf-8")

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail=(
                "The file could not be read. "
                "Please use a UTF-8 encoded TXT file."
            )
        )


    # --------------------------------------
    # Return extracted text
    # --------------------------------------

    return {

        "filename": file.filename,

        "text": text

    }