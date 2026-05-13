# Component Architecture - Low Level

```mermaid
graph TB
    subgraph "Client Components"
        direction TB
        page["app/page.tsx (Main Page)"]
        chat["components/ChatInterface.tsx (Chat Interface)"]
        sidebar["components/Sidebar.tsx (Navigation Sidebar)"]
        mobile["components/MobileNav.tsx (Mobile Navigation)"]
    end

    subgraph "Frontend State"
        direction TB
        messages[Messages State]
        input[Input State]
        loading[Loading State]
        imageToggle[Image Toggle State]
    end

    subgraph "API Client"
        direction TB
        fetch[fetch API]
        stream[ReadableStream (SSE Handler)]
        decoder[TextDecoder]
    end

    subgraph "FastAPI Backend"
        direction TB
        app[FastAPI App]
        chat_endpoint[/chat/stream]
        image_endpoint[/image]
        root_endpoint[/]

        subgraph "Request Handlers"
            parse[Request Parser]
            validate[Input Validation]
            error[Error Handler]
        end

        subgraph "Services"
            embed_service[Embedding Service]
            search_service[Vector Search Service]
            llm_service[LLM Service]
            image_service[Image Service]
        end
    end

    subgraph "AI/ML Services"
        direction TB
        emb_model[Sentence Transformers (paraphrase-MiniLM-L3-v2)]
        llm_client[InferenceClient]
        image_client[Image Generation Client]
    end

    subgraph "Data Store"
        direction TB
        chroma[ChromaDB Client]
        collection[Collection (mohenjo_daro_kb)]
        docs[Documents]
        metadata[Metadata]
    end

    page --> chat
    page --> sidebar
    page --> mobile

    chat --> messages
    chat --> input
    chat --> loading
    chat --> imageToggle

    messages --> fetch
    input --> fetch
    fetch --> chat_endpoint
    fetch --> image_endpoint

    chat_endpoint --> parse
    parse --> validate
    validate --> embed_service

    embed_service --> emb_model
    emb_model --> search_service

    search_service --> chroma
    chroma --> collection
    collection --> docs
    collection --> metadata

    search_service --> llm_service
    llm_service --> llm_client
    llm_client --> stream
    stream --> decoder
    decoder --> chat

    image_endpoint --> image_service
    image_service --> image_client
    image_client --> chat

    style page fill:#e3f2fd,stroke:#1565c0
    style chat fill:#bbdefb,stroke:#1565c0
    style app fill:#c8e6c9,stroke:#2e7d32
    style emb_model fill:#ffe0b2,stroke:#e65100
    style chroma fill:#f8bbd0,stroke:#c2185b
```