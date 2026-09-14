# 🤖 AI Text Summarizer

An AI-powered web application that converts long text and TXT documents into clear, concise summaries.

The application uses **FastAPI** for the backend and **Groq AI** for fast and intelligent text summarization.

---

## 🚀 Features

- ✨ AI-powered text summarization
- 📝 Summarize pasted text
- 📄 Upload `.txt` files
- 🧠 Handles long documents using text chunking
- 📏 Choose summary length:
  - Short
  - Medium
  - Detailed
- 🔹 Choose summary format:
  - Paragraph
  - Bullet Points
- 🔢 Real-time word counter
- 📋 Copy generated summaries
- ⏳ Loading indicator while AI processes the text
- 📱 Responsive design for different screen sizes

---

## 🛠️ Tech Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn

### AI

- Groq API
- `openai/gpt-oss-120b`

### Deployment

- Render

### Version Control

- Git
- GitHub

---

## 🏗️ How It Works

```text
User
 │
 ├── Paste text
 │
 └── Upload TXT file
        │
        ▼
   FastAPI Backend
        │
        ▼
  Long text detection
        │
        ▼
  Split into chunks
        │
        ▼
      Groq AI
        │
        ▼
  Generate summaries
        │
        ▼
 Combine results
        │
        ▼
 Display final summary