# Mohenjo-daro AI Chatbot - Project Task Tracker

## Project Overview
An AI-powered chatbot and image generation system for educating users about the archaeological site of Mohenjo-daro.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **AI Framework**: LangChain (RAG Pipeline)
- **Vector Database**: ChromaDB
- **LLM**: Mistral-7B / Llama-3 (via Hugging Face API)
- **Image Generation**: FLUX.1-dev / SDXL (via Hugging Face API)
- **Deployment**: Streamlit Cloud

---

## Task Status

### ✅ Completed Tasks

| Task ID | Description | Category | Status | Notes |
|---------|-------------|----------|--------|-------|
| T1 | Create requirements analysis (req.txt) | Documentation | ✅ Done | Requirements from user |
| T2 | Create high-level flow diagram | Documentation | ✅ Done | System architecture overview |
| T3 | Create chatbot workflow diagram | Documentation | ✅ Done | Detailed user interaction flow |
| T4 | Create database structure diagram | Documentation | ✅ Done | Knowledge base architecture |
| T5 | Create knowledge base - history.txt | Knowledge Base | ✅ Done | ~800 lines |
| T6 | Create knowledge base - architecture.txt | Knowledge Base | ✅ Done | ~700 lines |
| T7 | Create knowledge base - discovery.txt | Knowledge Base | ✅ Done | ~700 lines |
| T8 | Create knowledge base - culture.txt | Knowledge Base | ✅ Done | ~700 lines |
| T9 | Create knowledge base - artifacts.txt | Knowledge Base | ✅ Done | ~700 lines |
| T10 | Create knowledge base - tourism.txt | Knowledge Base | ✅ Done | ~600 lines |
| T11 | Create knowledge base - preservation.txt | Knowledge Base | ✅ Done | ~600 lines |
| T12 | Create knowledge base - resources.txt | Knowledge Base | ✅ Done | ~400 lines |
| T13 | Create requirements.txt | Dependencies | ✅ Done | All packages |
| T14 | Create ingest.py script | Setup | ✅ Done | Text → ChromaDB pipeline |
| T15 | Run ingest.py and create ChromaDB | Setup | ✅ Done | 237 chunks created |

---

### 🚧 In Progress

| Task ID | Description | Category | Status | Notes |
|---------|-------------|----------|--------|-------|
| T16 | Create app.py Streamlit application | Development | ✅ Done | Main chatbot UI with RAG + LLM + Image Gen |
| T17 | Implement RAG retrieval pipeline | Development | ✅ Done | retrieve_context() function |
| T18 | Implement LLM integration (Hugging Face API) | Development | ✅ Done | InferenceClient integration |
| T19 | Implement image generation logic | Development | ✅ Done | text_to_image via Stability AI |
| T20 | Implement intent detection for images | Development | ✅ Done | needs_image() function |
| T21 | Test app.py locally | Testing | ✅ Done | Syntax verified |

---

### 📋 Pending Tasks

| Task ID | Description | Category | Priority | Notes |
|---------|-------------|----------|----------|-------|
| T22 | Add conversation memory/history | Development | Medium | Multi-turn support |
| T23 | Add error handling for API failures | Development | High | Retry logic |
| T24 | Create README.md | Documentation | Medium | Setup instructions |
| T26 | Create sample outputs documentation | Documentation | Low | Chat + image examples |
| T27 | Test full app with user interaction | Testing | High | Verify RAG + LLM + Image Gen end-to-end |

---

### 🚫 Blocked Tasks

| Task ID | Description | Category | Blocked By | Notes |
|---------|-------------|----------|------------|-------|
| - | None currently | - | - | - |

---

### ❌ Cancelled Tasks

| Task ID | Description | Reason |
|---------|-------------|--------|
| - | None | - |

---

## File Structure (Current)

```
herit/
├── data/                          ✅ Complete
│   ├── history.txt
│   ├── architecture.txt
│   ├── discovery.txt
│   ├── culture.txt
│   ├── artifacts.txt
│   ├── tourism.txt
│   ├── preservation.txt
│   └── resources.txt
├── chroma_db/                      ✅ Complete
│   ├── chroma.sqlite3
│   └── [collection folders]
├── diagrams/                       ✅ Complete
│   ├── high_level_flow_diagram.md
│   ├── database_structure_diagram.md
│   └── chatbot_workflow_diagram.md
├── requirements.txt                ✅ Complete
├── ingest.py                       ✅ Complete
├── app.py                          ✅ Complete (RAG + LLM + Image Gen)
├── task_tracker.md                ✅ This file
└── README.md                       📋 Pending
```

---

## API Keys Required

| API | Environment Variable | Status |
|-----|---------------------|--------|
| Hugging Face API | `HF_TOKEN` | ⚠️ Needed for deployment |

---

## Dependencies Status

| Package | Version | Status |
|---------|---------|--------|
| langchain | 0.3.0 | ✅ Installed |
| langchain-community | 0.3.0 | ✅ Installed |
| langchain-huggingface | 0.1.0 | ✅ Installed |
| chromadb | 0.4.24 | ✅ Installed |
| huggingface_hub | 0.26.0 | ✅ Installed |
| sentence-transformers | 3.0.0 | ✅ Installed |
| streamlit | 1.40.0 | ✅ Installed |

---

## Next Actions

### Immediate (T16-T20)
1. Complete `app.py` with full RAG + LLM + Image Gen pipeline
2. Test locally with `streamlit run app.py`

### Short-term (T21-T27)
3. Add conversation memory
4. Add error handling
5. Test Hugging Face API
6. Create README.md

### Deployment
7. Push to GitHub
8. Deploy on Streamlit Cloud
9. Add HF_TOKEN to secrets

---

## Changelog

### 2026-05-11
- Created all knowledge base files (7 .txt files)
- Created ingest.py
- Ran ingest.py - created ChromaDB with 237 chunks
- Updated diagrams based on user feedback
- Created app.py with RAG + LLM + Image Gen pipeline
- Updated app.py to load .env for HF_TOKEN
- Created .gitignore
- Fixed Hugging Face API - upgraded huggingface_hub to 1.14.0
- Found working model: **deepseek-ai/DeepSeek-V3-0324**
- Image generation verified working with FLUX.1-dev
- **App ready for testing at http://localhost:8501**

### 2026-05-11 (Initial)
- Created requirements analysis (req.txt)
- Created high-level flow diagram
- Created database structure diagram
- Created chatbot workflow diagram
