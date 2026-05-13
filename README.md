![Logo](frontend/public/logo.png)

# Moḥenjo-daro AI Chatbot

An AI-powered chatbot exploring the ancient Indus Valley Civilization with RAG (Retrieval-Augmented Generation) and image generation capabilities.

## 🌟 Features

- **RAG-Powered Chat**: Uses ChromaDB vector database for accurate answers from knowledge base
- **Streaming Responses**: Real-time text generation with word-by-word display
- **Image Generation**: Generate historical illustrations of Mohenjo-daro
- **Sindhi Culture Theme**: Beautiful UI inspired by Ajrak patterns and Sindhi heritage
- **Responsive Design**: Works on desktop and mobile devices

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                      │
│                   http://localhost:3000                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  - React UI with Ajrak themed design                │    │
│  │  - Chat interface with streaming responses          │    │
│  │  - Image generation toggle                          │    │
│  │  - Collapsible sidebar                              │    │
│  └──────────────────────────┬──────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────┘
                              │ HTTP
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│                   http://localhost:8000                     │
│  ┌────────────────────────┬────────────────────────────┐    │
│  │  /chat/stream          │  /image                    │    │
│  │  - RAG pipeline        │  - Image generation        │    │
│  │  - LLM integration     │  - SDXL model              │    │
│  └───────────┬────────────┴───────────────────────────┘    │
└──────────────┼──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE (ChromaDB)                      │
│                   chroma_db/                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  - Vector embeddings from text files                │    │
│  │  - Semantic search for relevant context             │    │
│  │  - 5 nearest neighbors per query                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Hugging Face API token

### 1. Clone and Setup Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Hugging Face token
echo "HF_TOKEN=your_huggingface_token_here" > .env

# Ingest knowledge base
python ingest.py

# Start server
python main.py
```

Backend will run at: `http://localhost:8000`

### 2. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:3000`

### 3. Open Browser

Navigate to `http://localhost:3000`

---

## 📁 Project Structure

```
herit/
├── backend/
│   ├── main.py              # FastAPI server (chat & image APIs)
│   ├── ingest.py            # Knowledge base ingestion script
│   ├── requirements.txt     # Python dependencies
│   ├── .env                  # Environment variables (HF_TOKEN)
│   ├── data/                 # Text files for knowledge base
│   │   ├── history.txt
│   │   ├── architecture.txt
│   │   └── ...
│   └── chroma_db/            # Vector database (auto-generated)
│
└── frontend/
    ├── app/
    │   ├── page.tsx          # Main page with header
    │   ├── layout.tsx        # Root layout
    │   └── globals.css       # Global styles
    ├── components/
    │   ├── ChatInterface.tsx # Chat UI component
    │   ├── Sidebar.tsx       # Collapsible sidebar
    │   └── MobileNav.tsx      # Mobile navigation
    ├── package.json
    ├── tailwind.config.ts
    └── next.config.js
```

---

## 📚 Updating the Knowledge Base

Your chatbot's knowledge comes from text files in `backend/data/`.

### To Add New Information:

1. **Create or edit text files** in `backend/data/`:
   ```
   backend/data/
   ├── history.txt        → category: "history"
   ├── architecture.txt   → category: "architecture"
   ├── drainage.txt       → category: "drainage"
   └── your_topic.txt     → category: "your_topic"
   ```

2. **Add content to files** (plain text, can use markdown):
   ```txt
   # History of Mohenjo-daro
   
   Moḥenjo-daro (مُھن جو دڙو) was discovered in 1922 by R. D. Banerji...
   
   ## Key Facts:
   - Flourished: 2500-1900 BCE
   - Population: Estimated 40,000+
   - Location: Present-day Sindh, Pakistan
   ```

3. **Re-ingest the database:**
   ```bash
   cd backend
   python ingest.py
   ```

4. **Restart the backend server** (Ctrl+C then `python main.py`)

### How Ingestion Works:

```
data/*.txt
    │
    ▼
[Load Documents] ──► [Split into Chunks] ──► [Generate Embeddings]
                                                  │
                                                  ▼
                                           [Store in ChromaDB]
                                                  │
                                                  ▼
                                            chroma_db/
```

---

## 🔌 API Reference

### Chat API

**Endpoint:** `POST /chat/stream`

**Request:**
```json
{
  "message": "Tell me about the Great Bath"
}
```

**Response:** Server-Sent Events (SSE) stream
```
data: The
data: Great
data: Bath
data: of
data: Mohenjo-daro
data: [DONE]
```

### Image Generation API

**Endpoint:** `POST /image`

**Request:**
```json
{
  "prompt": "Show me what the Great Bath looked like"
}
```

**Response:**
```json
{
  "image_base64": "data:image/png;base64,..."
}
```

### Health Check

**Endpoint:** `GET /`

**Response:**
```json
{
  "status": "ok",
  "message": "Mohenjo-daro API"
}
```

---

## 🎨 UI Features

### Sidebar
- Collapsible with toggle button on the edge
- Shows topics about Mohenjo-daro
- Sindhi cultural information

### Chat Interface
- Streaming text responses
- Markdown rendering (headers, lists, bold, etc.)
- Image generation option (toggle)
- Suggested questions on empty state

### Header
- Ajrak-inspired gradient design
- Online status indicator
- Cultural branding

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env`:
```
HF_TOKEN=your_huggingface_token_here
```

### Models Used

| Task | Model | Provider |
|------|-------|----------|
| Chat | deepseek-ai/DeepSeek-V3-0324 | HuggingFace |
| Image Prompt | deepseek-ai/DeepSeek-V3-0324 | HuggingFace |
| Image Gen | stabilityai/stable-diffusion-xl-base-1.0 | HuggingFace |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Local |

### Adjusting Chunk Size

In `backend/ingest.py`:
```python
CHUNK_SIZE = 500      # Characters per chunk
CHUNK_OVERLAP = 50    # Overlap between chunks
```

---

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure backend is running: `python main.py`
- Check if port 8000 is not blocked

### "Model not found" error
- Verify `HF_TOKEN` is set correctly in `.env`
- Check HuggingFace token has access to required models

### "Knowledge base not found" error
- Run `python ingest.py` to create the database
- Check `backend/data/` has `.txt` files

### Images not showing
- Check browser console for errors
- Ensure backend is running on port 8000

---

## 📝 License

This project is for educational purposes. Content about Mohenjo-daro is based on publicly available archaeological research.

---

## 🙏 Acknowledgments

- **Hugging Face** - For providing LLM and image generation APIs
- **Indus Valley Civilization** - The fascinating subject of this chatbot
- **Sindhi Culture** - For inspiring the UI design with Ajrak patterns

---

> "سندھ سنسار" - Wisdom of Sindh