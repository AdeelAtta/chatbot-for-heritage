# Data Flow Diagram - High Level

```mermaid
flowchart TD
    User((User))

    subgraph Frontend["Frontend (Next.js/React)"]
        Input[User Input]
        ChatUI[Chat Interface]
        Display[Message Display]
        Stream[Stream Handler]
    end

    subgraph Backend["Backend (FastAPI)"]
        API[API Endpoint (/chat/stream)]
        Embed[Embedding Generator]
        Search[Vector Search]
        Context[Context Builder]
        LLM[LLM Client]
        Response[Response Formatter]
    end

    subgraph External["External Services"]
        HF_API[HuggingFace API]
        HF_LLM[DeepSeek V3 LLM]
        HF_Embed[Embedding Model]
        HF_Image[FLUX Image Gen]
    end

    User -->|Types Message| Input
    Input -->|Submit| ChatUI
    ChatUI -->|POST /chat/stream| API

    API -->|Query| Embed
    Embed -->|Text| HF_Embed
    HF_Embed -->|Embedding Vector| Embed
    Embed -->|Embedding| Search

    Search -->|Search| ChromaDB[(ChromaDB)]
    ChromaDB -->|Relevant Docs| Search
    Search -->|Context Docs| Context

    Context -->|Context + Query| LLM
    LLM -->|Chat API| HF_API
    HF_API -->|Forward| HF_LLM
    HF_LLM -->|Token Stream| HF_API
    HF_API -->|Stream| LLM

    LLM -->|Stream Response| API
    API -->|SSE Stream| Stream
    Stream -->|Update UI| Display
    Display -->|Shows to User| User

    style User fill:#ffeb3b,stroke:#f57f17
    style Frontend fill:#e3f2fd,stroke:#1565c0
    style Backend fill:#e8f5e9,stroke:#2e7d32
    style External fill:#fff3e0,stroke:#e65100
```