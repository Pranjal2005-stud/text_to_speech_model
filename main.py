from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import asyncio
import uuid
import os

app = FastAPI()

# Allow frontend access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Edge-TTS service is running!"}

@app.post("/tts")
async def generate_tts(text: str = Form(...)):
    """Generate MP3 speech from given text using Edge-TTS"""
    try:
        # Generate a unique filename
        output_path = f"speech_{uuid.uuid4()}.mp3"
        voice = "en-IN-NeerjaNeural"

        # Run TTS and save file
        tts = edge_tts.Communicate(text, voice)
        await tts.save(output_path)

        # Return file response (no auto-delete for now)
        return FileResponse(output_path, media_type="audio/mpeg")

    except Exception as e:
        return {"error": str(e)}
