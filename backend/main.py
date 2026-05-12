"""
Mohenjo-daro AI Chatbot - FastAPI Backend
==========================================
RAG-powered API for chat and image generation.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, AsyncIterator
import os
import asyncio
import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import tracemalloc
import gc

load_dotenv()

app = FastAPI(title="Mohenjo-daro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chatbot-for-heritage.vercel.app","http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "mohenjo_daro_kb"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L3-v2"

SYSTEM_PROMPT = """You are an expert historian specializing in the ancient Indus Valley Civilization, 
with particular expertise in Mohenjo-daro. Your knowledge is based on archaeological evidence 
and scholarly research. Answer questions accurately and provide historical context. 
If you don't know something, say so rather than making up information."""

IMAGE_KEYWORDS = [
    "show", "look like", "what did", "imagine", "draw", "picture",
    "image", "visualize", "ancient times", "appearance", "reconstruction",
    "depict", "illustrate", "generate image", "create image"
]

embeddings = None
chroma_client = None
collection = None

def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return embeddings

def get_collection():
    global chroma_client, collection
    if collection is None:
        chroma_client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
    return collection

hf_token = os.environ.get("HF_TOKEN", "")

def get_llm_client():
    if not hf_token:
        print("WARNING: HF_TOKEN not set")
    return InferenceClient(provider="auto", token=hf_token)

@app.on_event("startup")
async def startup_event():
    tracemalloc.start()
    gc.collect()
    current, peak = tracemalloc.get_traced_memory()
    print("=" * 50)
    print("Starting Mohenjo-daro API...")
    print(f"Memory (current): {current / 1024 / 1024:.1f} MB")
    print(f"Memory (peak): {peak / 1024 / 1024:.1f} MB")
    print(f"ChromaDB path: {CHROMA_DIR}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    try:
        coll = get_collection()
        count = coll.count()
        print(f"Collection loaded: {count} documents")
    except Exception as e:
        print(f"Warning: Could not load collection: {e}")
    gc.collect()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory after startup: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory so far: {peak / 1024 / 1024:.1f} MB")
    print("Startup complete")
    print("=" * 50)


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
    gc.collect()
    current, peak = tracemalloc.get_traced_memory()
    print(f"[Request] Memory before embedding: {current / 1024 / 1024:.1f} MB")
    query_embedding = get_embeddings().embed_query(query)
    gc.collect()
    current, peak = tracemalloc.get_traced_memory()
    print(f"[Request] Memory after embedding: {current / 1024 / 1024:.1f} MB")
    results = get_collection().query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    contexts = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {}
            if doc:
                category = (metadata.get("category") or "unknown") if metadata else "unknown"
                contexts.append(f"[{category}]: {doc}")

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
            llm_client = get_llm_client()
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

    gc.collect()
    current, peak = tracemalloc.get_traced_memory()
    print(f"[Request] Memory after LLM: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB")
    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


class ImageRequest(BaseModel):
    prompt: str


class ImageResponse(BaseModel):
    image_base64: Optional[str] = None


@app.post("/image", response_model=ImageResponse)
async def generate_image_endpoint(request: ImageRequest):
    try:
        llm_client = get_llm_client()
        prompt_messages = [
            {"role": "system", "content": "Create a detailed prompt for generating a historically accurate image of Mohenjo-daro. Keep it under 150 characters, focusing on key visual elements."},
            {"role": "user", "content": f"Create an image prompt based on:\n{request.prompt[:300]}"}
        ]

        prompt_response = llm_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=prompt_messages,
            max_tokens=80,
        )
        prompt = prompt_response.choices[0].message.content.strip()
        prompt = f"Ancient Mohenjo-daro ruins, archaeological site, {prompt}, historical accuracy, detailed, realistic, warm lighting"

        image = llm_client.text_to_image(
            prompt=prompt[:300],
            model="stabilityai/stable-diffusion-xl-base-1.0",
            negative_prompt="modern, buildings, people, text, watermark, blurry",
        )

        import base64
        from io import BytesIO
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return ImageResponse(image_base64=f"data:image/png;base64,{img_str}")
    except Exception as e:
        print(f"Image generation error: {e}")
        return ImageResponse(image_base64=None)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
