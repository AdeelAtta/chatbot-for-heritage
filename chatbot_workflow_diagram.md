# Mohenjo-daro AI Chatbot - Detailed Workflow Diagram

## Complete Chatbot Workflow

```mermaid
flowchart TD
    subgraph START["START"]
        A1[User Opens App] --> A2[Load ChromaDB<br/>Knowledge Base]
    end

    subgraph INPUT["USER INPUT"]
        A2 --> B1[User Enters<br/>Question]
        B1 --> B2[Display User<br/>Message in Chat]
    end

    subgraph RETRIEVAL["RETRIEVAL PHASE"]
        B2 --> C1[Semantic Search<br/>Query ChromaDB]
        C1 --> C2[Get Top-K<br/>Relevant Chunks]
        C2 --> C3{Relevant<br/>Results Found?}
        C3 -->|No| C4[Log Warning<br/>Low Context]
        C3 -->|Yes| C5[Assemble Context<br/>from Chunks]
    end

    subgraph TEXT_GEN["TEXT GENERATION"]
        C5 --> D1[Build Prompt<br/>with Context]
        D1 --> D2[Send to LLM API<br/>Mistral / Llama]
        D2 --> D3{LLM API<br/>Response?}
        D3 -->|Error| D4[Show Error<br/>Message]
        D3 -->|Success| D5[Parse Text<br/>Response]
    end

    subgraph INTENT["INTENT DETECTION"]
        D5 --> E1[Analyze Query<br/>Keywords]
        E1 --> E2{Image<br/>Requested?}
        E2 -->|Keywords: show, look like,<br/>what did, imagine, draw,<br/>picture, image, visualize| E3[Flag: Generate Image]
        E2 -->|No Keywords| E4[Flag: No Image]
    end

    subgraph IMAGE_GEN["CONDITIONAL IMAGE GENERATION"]
        E3 --> F1[Build Image<br/>Prompt from Response]
        F1 --> F2[Send to Image Gen API<br/>FLUX.1-dev / SDXL]
        F2 --> F3{Image<br/>Generated?}
        F3 -->|Error| F4[Show Image<br/>Unavailable Msg]
        F3 -->|Success| F5[Receive Generated<br/>Image]
        E4 --> F6[Skip Image Gen]
    end

    subgraph OUTPUT["DISPLAY OUTPUT"]
        D5 --> G1[Display AI<br/>Text Response]
        F5 --> G2[Display AI<br/>Generated Image]
        F6 --> G1
    end

    subgraph LOOP["CONVERSATION LOOP"]
        G1 --> H1{User Sends<br/>Another Message?}
        H1 -->|Yes| B1
        H1 -->|No| H2[End Session]
    end

    style START fill:#e3f2fd
    style INPUT fill:#fff3e0
    style RETRIEVAL fill:#e8f5e9
    style TEXT_GEN fill:#c8e6c9
    style INTENT fill:#fce4ec
    style IMAGE_GEN fill:#f8bbd9
    style OUTPUT fill:#e1f5fe
    style LOOP fill:#f5f5f5
```

---

## Detailed Step-by-Step Flow

```mermaid
flowchart TD
    subgraph Step1["STEP 1: App Initialization"]
        S1_1[App Starts] --> S1_2[Initialize Streamlit]
        S1_2 --> S1_3[Load ChromaDB from Repo]
        S1_3 --> S1_4[Initialize LangChain]
        S1_4 --> S1_5[Setup Hugging Face API Clients]
        S1_5 --> S1_6[Ready for User Input]
    end

    subgraph Step2["STEP 2: User Query Processing"]
        S2_1[User Types Question] --> S2_2[st.chat_input captures input]
        S2_2 --> S2_3[Add to conversation history]
        S2_3 --> S2_4[Display in st.chat_message]
        S2_4 --> S2_5[Store in message history]
    end

    subgraph Step3["STEP 3: RAG Retrieval"]
        S3_1[Extract query string] --> S3_2[Generate query embedding]
        S3_2 --> S3_3[similarity_search in ChromaDB]
        S3_3 --> S3_4[Retrieve top 4-5 chunks]
        S3_4 --> S3_5[Combine as context string]
        S3_5 --> S3_6[Pass to LLM prompt]
    end

    subgraph Step4["STEP 4: LLM Response Generation"]
        S4_1[Build system prompt<br/>with context] --> S4_2[Build user prompt<br/>with question + history]
        S4_2 --> S4_3[Call Hugging Face<br/>LLM Inference API]
        S4_3 --> S4_4{API Success?}
        S4_4 -->|Yes| S4_5[Extract response text]
        S4_4 -->|No| S4_6[Return error message]
        S4_5 --> S4_7[Add to conversation history]
    end

    subgraph Step5["STEP 5: Intent Classification"]
        S5_1[Check keywords in query] --> S5_2{Keywords found?}
        S5_2 -->|show| S5_3[image_needed = True]
        S5_2 -->|look like| S5_3
        S5_2 -->|what did| S5_3
        S5_2 -->|imagine| S5_3
        S5_2 -->|picture| S5_3
        S5_2 -->|visualize| S5_3
        S5_2 -->|other| S5_4[image_needed = False]
        S5_3 --> S5_5[Flag set for image generation]
        S5_4 --> S5_5
    end

    subgraph Step6["STEP 6: Conditional Image Generation"]
        S6_1{image_needed?}
        S6_1 -->|Yes| S6_2[Extract visual description from LLM response]
        S6_2 --> S6_3[Enhance prompt for image model]
        S6_3 --> S6_4[Add historical context to prompt]
        S6_4 --> S6_5[Call Hugging Face Image Gen API]
        S6_5 --> S6_6{API Success?}
        S6_6 -->|Yes| S6_7[Receive image bytes]
        S6_6 -->|No| S6_8[Show fallback message]
        S6_7 --> S6_9[Display image in chat]
        S6_1 -->|No| S6_10[Skip - continue to display]
    end

    subgraph Step7["STEP 7: Display Response"]
        S7_1[Streamlit renders text] --> S7_2[st.chat_message bot]
        S7_2 --> S7_3{Image generated?}
        S7_3 -->|Yes| S7_4[st.image display]
        S7_3 -->|No| S7_5[Skip image]
        S7_4 --> S7_6[Chat history updated]
        S7_5 --> S7_6
    end

    subgraph Step8["STEP 8: Conversation Memory"]
        S8_1[Append user message to history]
        S8_1 --> S8_2[Append bot response to history]
        S8_2 --> S8_3[Pass history to next LLM call]
        S8_3 --> S8_4[Enables multi-turn conversation]
    end
```

---

## Conversation Memory Flow

```mermaid
flowchart LR
    subgraph History["Conversation History"]
        H1[User: What about drainage?]
        H2[Bot: Mohenjo-daro had...]
        H3[User: How old is it?]
    end

    subgraph Context["Context Window"]
        C1[Current question + history]
        C2[Last 5-10 messages]
    end

    subgraph LLM["LLM Processing"]
        L1[Full context to LLM]
        L2[Maintains coherence]
    end

    H3 --> C1
    H2 --> C1
    C1 --> L1
    L1 --> L2
```

---

## Image Generation Decision Logic

```mermaid
flowchart TD
    A[User Query] --> B{Contains visual keywords?}

    B -->|show me| C[Image Needed]
    B -->|what did it look| C
    B -->|how did it appear| C
    B -->|visualize| C
    B -->|imagine| C
    B -->|picture| C
    B -->|drawing| C
    B -->|image| C
    B -->|ancient times| D

    B -->|why| E[No Image]
    B -->|who| E
    B -->|when| E
    B -->|how many| E
    B -->|describe the significance| E
    B -->|what happened| E

    D --> C
    C --> F[Generate Image Prompt]
    E --> G[Skip Image Gen]

    style C fill:#c8e6c9
    style E fill:#ffcdd2
```

---

## API Error Handling Flow

```mermaid
flowchart TD
    A[API Call] --> B{Success?}

    B -->|200 OK| C[Process Response]
    B -->|429 Rate Limit| D[Show: "Please wait..."]
    D --> E[Wait 30 seconds]
    E --> A
    B -->|500 Server Error| F[Show: "Service unavailable"]
    F --> G[Log error]
    B -->|Timeout| H[Show: "Request timed out"]
    H --> I[Retry once]
    I --> A

    style D fill:#fff3e0
    style F fill:#ffcdd2
    style H fill:#fff3e0
```

---

## Complete User Session Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant RAG as RAG Pipeline
    participant DB as ChromaDB
    participant LLM as LLM API
    participant IMG as Image Gen API

    User->>UI: Opens app
    UI->>DB: Initialize ChromaDB
    DB-->>UI: Knowledge base loaded
    UI->>User: Ready to chat

    User->>UI: "Tell me about Mohenjo-daro"
    UI->>RAG: Process query
    RAG->>DB: Semantic search
    DB-->>RAG: Relevant context chunks
    RAG->>LLM: Generate response
    LLM-->>RAG: Text response
    RAG-->>UI: Response + intent flag
    UI->>User: Display text

    User->>UI: "Show me what it looked like"
    UI->>RAG: Process query
    RAG->>DB: Semantic search
    DB-->>RAG: Context
    RAG->>LLM: Generate response + image prompt
    LLM-->>RAG: Image description
    RAG->>IMG: Generate image
    IMG-->>RAG: Image
    RAG-->>UI: Response + image
    UI->>User: Display text + image

    User->>UI: "How old is it?"
    UI->>RAG: Process query
    RAG->>DB: Search
    DB-->>RAG: Context
    RAG->>LLM: Generate text only
    LLM-->>RAG: Response (no image flag)
    RAG-->>UI: Text response
    UI->>User: Display text only

    User->>UI: "Thanks, goodbye"
    UI->>User: End conversation
```

---

## Workflow Summary Table

| Step | Component | Action | Output |
|------|-----------|--------|--------|
| 1 | Streamlit | Initialize app | App ready |
| 2 | UI | Capture user input | Question stored |
| 3 | ChromaDB | Semantic search | Context chunks |
| 4 | LLM | Generate response | Text answer |
| 5 | Intent | Classify query | Image flag |
| 6 | Image Gen | Generate image | Visual |
| 7 | UI | Display output | Chat message |
| 8 | Memory | Update history | Conversation state |

---

## Key Code Integration Points

```
app.py
│
├── initialize_app()
│   └── load_chroma_db()
│
├── handle_user_input(user_input)
│   └── add_to_history()
│
├── process_query(query)
│   ├── semantic_search(chroma_db, query)
│   ├── generate_response(llm, context, query)
│   └── classify_intent(query)
│
├── generate_image(prompt)
│   └── image_generation_api(flux, prompt)
│
└── display_response(text, image)
    ├── st.chat_message("assistant")
    └── st.image(image)
```
