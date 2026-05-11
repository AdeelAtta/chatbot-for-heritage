# Mohenjo-daro Knowledge Base - Database Structure Diagram

## Data Architecture Overview

```mermaid
flowchart TD
    subgraph Raw["RAW DATA LAYER"]
        R1[Historical Texts<br/>.txt, .md files]
        R2[PDF Documents<br/>Research papers]
        R3[Web Content<br/>Wikipedia, Articles]
    end

    subgraph Processed["PROCESSED DATA"]
        R1 --> P1[Text Content]
        R2 --> P2[Extracted Text]
        R3 --> P3[Scraped Content]
        P1 --> D1[Data Directory<br/>/data/]
        P2 --> D1
        P3 --> D1
    end

    subgraph Chunked["CHUNKED DATA"]
        D1 --> C1[LangChain Loader]
        C1 --> C2[Recursive Character<br/>Text Splitter]
        C2 --> C3[Document Chunks<br/>~500 tokens each]
    end

    subgraph Embedded["EMBEDDING LAYER"]
        C3 --> E1[Embedding Model<br/>sentence-transformers]
        E1 --> E2[Vector Embeddings<br/>384 dimensions]
    end

    subgraph Storage["CHROMADB STORAGE"]
        E2 --> S1[Collection: mohenjo_daro_kb]
        S1 --> S2[Document Metadata]
        S2 --> S3[Vector Index<br/>for similarity search]
    end

    subgraph Query["QUERY LAYER"]
        Q1[User Query] --> Q2[Query Embedding]
        Q2 --> Q3[Similarity Search]
        Q3 --> S3
        S3 --> Q4[Top-K Results]
    end

    style Raw fill:#e3f2fd
    style Processed fill:#fff3e0
    style Chunked fill:#e8f5e9
    style Embedded fill:#c8e6c9
    style Storage fill:#f3e5f5
    style Query fill:#ce93d8
```

---

## ChromaDB Collection Structure

```mermaid
flowchart TD
    subgraph Collection["Collection: mohenjo_daro_kb"]
        subgraph Metadata["Metadata Schema"]
            M1[category: str]
            M2[source: str]
            M3[chunk_id: int]
            M4[title: str]
            M5[created_at: datetime]
        end

        subgraph Vectors["Vector Storage"]
            V1[Embedding Vector<br/>384 floats]
            V2[Embedding Vector<br/>384 floats]
            V3[Embedding Vector<br/>384 floats]
            V4[... more vectors"]
        end

        subgraph Documents["Document Storage"]
            D1["chunk_001: 'Mohenjo-daro was<br/>one of the largest<br/>settlements of the<br/>ancient Indus Valley...'"]
            D2["chunk_002: 'The city was<br/>founded around 2500<br/>BCE and featured<br/>advanced drainage...'"]
            D3["chunk_003: 'Archaeological<br/>excavations revealed<br/>standardized brick<br/>sizes indicating...'"]
            D4["... more chunks"]
        end
    end
```

---

## Knowledge Categories & Content Structure

```mermaid
flowchart TD
    subgraph Categories["Knowledge Base Categories"]
        C1["HISTORY"]
        C2["ARCHITECTURE"]
        C3["DISCOVERY"]
        C4["CULTURE"]
        C5["ARTIFACTS"]
        C6["TOURISM"]
        C7["PRESERVATION"]
    end

    subgraph HistoryContent["C1: HISTORY"]
        H1[Indus Valley Civilization<br/>Overview]
        H2[Timeline & Chronology<br/>2500-1900 BCE]
        H3[Decline & Abandonment<br/>Reasons]
        H4[Daily Life<br/>Citizens & Activities]
    end

    subgraph ArchitectureContent["C2: ARCHITECTURE"]
        A1[City Planning<br/>Grid Layout]
        A2[Great Bath<br/>Pools & Waterproofing]
        A3[Granary<br/>Storage Facility]
        A4[Residential Houses<br/>Standardized Design]
        A5[Drainage System<br/>Sewage Management]
    end

    subgraph DiscoveryContent["C3: DISCOVERY"]
        D1[First Excavation<br/>1922 by Sir John Marshall]
        D2[Sir John Marshall<br/>Archaeological Team]
        D3[Archaeological<br/>Excavations History]
        D4[Major Discoveries<br/>Timeline]
    end

    subgraph CultureContent["C4: CULTURE"]
        CU1[Trade & Economy<br/>Merchants & Goods]
        CU2[Religion & Beliefs<br/>Seals & Symbols]
        CU3[Arts & Crafts<br/>Pottery & Jewelry]
        CU4[Social Structure<br/>Governance]
    end

    subgraph ArtifactsContent["C5: ARTIFACTS"]
        AR1[Indus Seals<br/>Undeciphered Script]
        AR2[Dancing Girl<br/>Bronze Statue]
        AR3[Priest King<br/>Steatite Bust]
        AR4[Terracotta Toys<br/>Figurines]
    end

    subgraph TourismContent["C6: TOURISM"]
        T1[Visitor Information<br/>Hours & Tickets]
        T2[What to See<br/>Key Sites]
        T3[Visitor Rules<br/>Photography Guidelines]
        T4[Nearby Attractions<br/>Larkana Region]
    end

    subgraph PreservationContent["C7: PRESERVATION"]
        PR1[Environmental Threats<br/>Salinity, Erosion]
        PR2[Conservation Efforts<br/>UNESCO Initiatives]
        PR3[Climate Change Impact<br/>River Shifting]
        PR4[Future Predictions<br/>Risk Assessment]
    end

    C1 --> HistoryContent
    C2 --> ArchitectureContent
    C3 --> DiscoveryContent
    C4 --> CultureContent
    C5 --> ArtifactsContent
    C6 --> TourismContent
    C7 --> PreservationContent

    style C1 fill:#e3f2fd
    style C2 fill:#bbdefb
    style C3 fill:#b3e5fc
    style C4 fill:#e1f5fe
    style C5 fill:#c8e6c9
    style C6 fill:#ffe0b2
    style C7 fill:#fff9c4
```

---

## Text Chunking Process

```mermaid
flowchart LR
    subgraph Input["Raw Text Input"]
        I1["Mohenjo-daro was one of the largest
        settlements of the ancient Indus Valley
        Civilization, existing from approximately
        2500 BCE to 1900 BCE. The city was
        remarkable for its advanced urban
        planning, including a sophisticated
        drainage system and standardized brick
        sizes. Archaeological excavations have
        revealed thousands of artifacts that
        provide insights into the daily lives
        of its inhabitants."]
    end

    subgraph Process["Chunking Process"]
        P1[Recursive Character<br/>Text Splitter]
        P2[chunk_size: 500]
        P3[chunk_overlap: 50]
    end

    subgraph Output["Output Chunks"]
        O1["chunk_001: 'Mohenjo-daro was one of
        the largest settlements of the ancient
        Indus Valley Civilization, existing
        from approximately 2500 BCE to 1900
        BCE.'"]
        O2["chunk_002: 'The city was remarkable
        for its advanced urban planning,
        including a sophisticated drainage
        system and standardized brick sizes.'"]
        O3["chunk_003: 'Archaeological excavations
        have revealed thousands of artifacts
        that provide insights into the daily
        lives of its inhabitants.'"]
    end

    I1 --> P1
    P1 --> P2
    P1 --> P3
    P1 --> O1
    P1 --> O2
    P1 --> O3

    style Input fill:#e3f2fd
    style Process fill:#fff3e0
    style Output fill:#e8f5e9
```

---

## Embedding & Retrieval Flow

```mermaid
flowchart TD
    subgraph Ingestion["INGESTION PHASE"]
        I1[Text Chunk] --> I2[Embedding Model]
        I2 --> I3[384-Dim Vector]
        I3 --> I4[Store in ChromaDB]
    end

    subgraph Query["QUERY PHASE"]
        Q1[User Query String] --> Q2[Query Embedding]
        Q2 --> Q3[384-Dim Vector]
    end

    subgraph Search["SIMILARITY SEARCH"]
        Q3 --> S1[Cosine Similarity<br/>Calculation]
        I4 --> S2[Database Vectors]
        S1 --> S2
        S2 --> S3[Ranked Results<br/>by Similarity Score]
    end

    subgraph Results["TOP-K RESULTS"]
        S3 --> R1[chunk_042<br/>score: 0.92]
        S3 --> R2[chunk_017<br/>score: 0.87]
        S3 --> R3[chunk_089<br/>score: 0.81]
        S3 --> R4[chunk_023<br/>score: 0.76]
    end

    subgraph Context["CONTEXT ASSEMBLY"]
        R1 --> C1[Combine Chunks]
        R2 --> C1
        R3 --> C1
        C1 --> C2[Pass to LLM as Context]
    end

    style Ingestion fill:#e8f5e9
    style Query fill:#e3f2fd
    style Search fill:#fff3e0
    style Results fill:#fce4ec
    style Context fill:#f3e5f5
```

---

## File Storage Structure

```mermaid
flowchart TD
    subgraph Project["Project Directory"]
        P1[mohenjo_daro_chatbot/]

        subgraph DataFolder["data/"]
            D1[history.txt]
            D2[architecture.txt]
            D3[discovery.txt]
            D4[culture.txt]
            D5[artifacts.txt]
            D6[tourism.txt]
            D7[preservation.txt]
        end

        subgraph ChromaFolder["chroma_db/"]
            C1[chroma.sqlite3]
            C2[*.bin<br/>Index files]
            C3[*.h5<br/>Embeddings]
        end

        subgraph Scripts["Root"]
            S1[ingest.py]
            S2[app.py]
            S3[requirements.txt]
        end
    end

    D1 -.->|processed by| S1
    D2 -.->|processed by| S1
    D3 -.->|processed by| S1
    D4 -.->|processed by| S1
    D5 -.->|processed by| S1
    D6 -.->|processed by| S1

    S1 -.->|creates| C1
    S1 -.->|creates| C2
    S1 -.->|creates| C3

    S1 --> P1
    C1 --> P1
    C2 --> P1
    C3 --> P1
    S2 --> P1
    S3 --> P1

    style Project fill:#f5f5f5
    style DataFolder fill:#e3f2fd
    style ChromaFolder fill:#e8f5e9
    style Scripts fill:#fff3e0
```

---

## Query-to-Context Pipeline

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant RAG as RAG Pipeline
    participant Embed as Embedding Model
    participant DB as ChromaDB
    participant LLM as LLM

    User->>UI: "What was the drainage system like?"
    UI->>RAG: Pass query

    RAG->>Embed: Generate query embedding
    Embed-->>RAG: [0.23, -0.45, 0.89, ...]

    RAG->>DB: similarity_search(query_embedding, k=5)
    DB-->>RAG: Top 5 relevant chunks

    Note over RAG: Assembling context from chunks:

    RAG->>RAG: Chunk 1: "The advanced drainage..."
    RAG->>RAG: Chunk 2: "Every house had..."
    RAG->>RAG: Chunk 3: "Covered brick drains..."
    RAG->>RAG: Chunk 4: "The Great Bath was..."
    RAG->>RAG: Chunk 5: "Water management in..."

    RAG->>LLM: Build prompt with context + query
    LLM-->>RAG: Comprehensive text response
    RAG-->>UI: Response
    UI->>User: Display answer
```

---

## Database Schema Details

### ChromaDB Collection: `mohenjo_daro_kb`

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | str | Unique chunk identifier | `chunk_001` |
| `embedding` | float[384] | Vector representation | `[0.23, -0.45, ...]` |
| `document` | str | Raw text content | `"Mohenjo-daro was..."` |
| `metadata.category` | str | Content category | `"architecture"` |
| `metadata.source` | str | Original source | `"history.txt"` |
| `metadata.chunk_id` | int | Sequential ID | `1` |
| `metadata.title` | str | Section title | `"Drainage System"` |

---

## Data Processing Configuration

```mermaid
flowchart TD
    subgraph Config["Ingestion Configuration"]
        C1[Chunk Size: 500 tokens]
        C2[Chunk Overlap: 50 tokens]
        C3[Embedding Model: all-MiniLM-L6-v2]
        C4[Vector Dimensions: 384]
        C5[Top-K Retrieval: 5 chunks]
        C6[Similarity Metric: Cosine]
    end

    subgraph Models["Embedding Models (Options)"]
        M1[all-MiniLM-L6-v2<br/>384 dims (default)]
        M2[all-mpnet-base-v2<br/>768 dims (high quality)]
        M3[paraphrase-MiniLM-L6-v2<br/>384 dims (semantic)]
    end
```

---

## Knowledge Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE BASE FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐                                                   │
│  │  SOURCE FILES   │  history.txt, architecture.txt, discovery.txt      │
│  │  (data/)        │  culture.txt, artifacts.txt, tourism.txt,          │
│  │                 │  preservation.txt                                  │
│  └────────┬────────┘                                                   │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                   │
│  │  INGEST.PY      │  Load → Chunk → Embed → Store                      │
│  │                 │                                                    │
│  │  • TextLoader   │                                                    │
│  │  • Recursive    │                                                    │
│  │    Character    │                                                    │
│  │    TextSplitter │                                                    │
│  │  • Sentence     │                                                    │
│  │    Transformers │                                                    │
│  └────────┬────────┘                                                   │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                   │
│  │  CHROMADB       │  Vector Database (deployed with app)                │
│  │                 │                                                    │
│  │  Collection:    │                                                    │
│  │  mohenjo_daro   │                                                    │
│  │  _kb            │                                                    │
│  │                 │                                                    │
│  │  ~100-200       │                                                    │
│  │  chunks         │                                                    │
│  └────────┬────────┘                                                   │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                   │
│  │  QUERY TIME     │  User Question → Embed → Search → Context           │
│  │                 │                                                    │
│  │  1. User asks   │                                                    │
│  │  2. Query       │                                                    │
│  │     embedded    │                                                    │
│  │  3. Semantic    │                                                    │
│  │     search      │                                                    │
│  │  4. Top-K       │                                                    │
│  │     chunks      │                                                    │
│  │  5. Combined    │                                                    │
│  │     context     │                                                    │
│  └────────┬────────┘                                                   │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                   │
│  │  LLM PROMPT     │  Context + Question → LLM → Response                │
│  └─────────────────┘                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```
