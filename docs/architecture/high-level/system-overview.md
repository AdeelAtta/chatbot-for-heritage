# System Overview - High Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        direction TB
        Browser[Web Browser<br/>Next.js App]
    end

    subgraph "Frontend Layer"
        direction TB
        NextJS[Next.js Framework]
        UI[React Components<br/>ChatInterface, Sidebar, MobileNav]
    end

    subgraph "API Layer"
        direction TB
        FastAPI[FastAPI Backend<br/>Port 8000]
    end

    subgraph "AI/ML Layer"
        direction TB
        HF Inference[HuggingFace Inference API]
        Embeddings[Sentence Transformers<br/>paraphrase-MiniLM-L3-v2]
        LLM[DeepSeek-V3-0324<br/>Text Generation]
        ImageGen[FLUX.1-schnell<br/>Image Generation]
    end

    subgraph "Data Layer"
        direction TB
        ChromaDB[ChromaDB Vector Store]
        KnowledgeBase[Knowledge Base<br/>Text Documents]
    end

    subgraph "External Services"
        direction TB
        HF[🤗 Hugging Face<br/>API Services]
    end

    Browser --> NextJS
    NextJS --> UI
    UI -->|HTTP/WebSocket| FastAPI
    FastAPI -->|Query| Embeddings
    Embeddings -->|Search| ChromaDB
    ChromaDB -->|Retrieve Context| FastAPI
    FastAPI -->|Chat Request| HF Inference
    HF Inference -->|API Call| HF
    HF -->|Response| HF Inference
    HF Inference -->|Stream Response| FastAPI
    FastAPI -->|Stream| UI
    UI -->|Image Request| FastAPI
    FastAPI -->|Generate| ImageGen
    ImageGen -->|API Call| HF
    HF -->|Image| ImageGen
    ImageGen -->|Base64| FastAPI
    FastAPI -->|Image Response| UI

    style Browser fill:#e1f5fe,stroke:#01579b
    style NextJS fill:#e1f5fe,stroke:#01579b
    style FastAPI fill:#e8f5e9,stroke:#2e7d32
    style HF fill:#fff3e0,stroke:#e65100
    style ChromaDB fill:#fce4ec,stroke:#c2185b
```