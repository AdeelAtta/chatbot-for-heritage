"""
Mohenjo-daro AI Chatbot - FastAPI Backend
==========================================
RAG-powered API for chat and image generation.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncIterator
import os
import asyncio
import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Mohenjo-daro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "mohenjo_daro_kb"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SYSTEM_PROMPT = """You are an expert historian specializing in the ancient Indus Valley Civilization, 
with particular expertise in Mohenjo-daro. Your knowledge is based on archaeological evidence 
and scholarly research. Answer questions accurately and provide historical context. 
If you don't know something, say so rather than making up information."""

IMAGE_KEYWORDS = [
    "show", "look like", "what did", "imagine", "draw", "picture",
    "image", "visualize", "ancient times", "appearance", "reconstruction",
    "depict", "illustrate", "generate image", "create image"
]

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

hf_token = os.environ.get("HF_TOKEN", "")
llm_client = InferenceClient(provider="auto", token=hf_token)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    image_url: Optional[str] = None


@app.get("/")
async def root():
    return {"status": "ok", "message": "Mohenjo-daro API"}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    query = request.message

    query_embedding = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    contexts = []
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        contexts.append(f"[{metadata.get('category', 'unknown')}]: {doc}")

    context = "\n\n".join(contexts)

    if not context:
        async def error_stream():
            yield "data: I apologize, but I don't have information about that topic.\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    async def stream_response() -> AsyncIterator[str]:
        try:
            response = llm_client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=messages,
                max_tokens=512,
                temperature=0.7,
                stream=True,
            )

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {content}\n\n"
                    await asyncio.sleep(0)

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


async def generate_image(text_response: str) -> Optional[str]:
    try:
        prompt_messages = [
            {"role": "system", "content": "You are an expert at creating image generation prompts. Based on the text description, create a detailed prompt for generating a historically accurate image of Mohenjo-daro. Keep the prompt under 200 characters."},
            {"role": "user", "content": f"Create an image prompt:\n{text_response[:500]}"}
        ]
        
        prompt_response = llm_client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=prompt_messages,
            max_tokens=100,
        )
        prompt = prompt_response.choices[0].message.content.strip()
        prompt = f"Historical illustration of ancient Mohenjo-daro, {prompt}, archaeological accuracy, detailed, realistic"
        
        image = llm_client.text_to_image(
            prompt=prompt[:500],
            model="stabilityai/stable-diffusion-xl-base-1.0",
            negative_prompt="modern, buildings, people, text, watermark",
        )
        
        image_path = "static/generated_image.png"
        image.save(image_path)
        return f"/{image_path}"
    except Exception as e:
        print(f"Image generation error: {e}")
        return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
