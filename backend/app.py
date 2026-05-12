"""
Mohenjo-daro AI Chatbot - Streamlit Application
==============================================
An interactive AI chatbot that answers questions about Mohenjo-daro
and generates contextual images based on the responses.
"""

import os
import streamlit as st
import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

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

# =============================================================================
# INITIALIZATION
# =============================================================================

@st.cache_resource
def load_vector_store():
    """Load the ChromaDB vector store."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    
    return collection, embeddings

@st.cache_resource
def init_llm_client():
    """Initialize Hugging Face LLM client."""
    hf_token = os.environ.get("HF_TOKEN", "") or st.secrets.get("HF_TOKEN", "")
    client = InferenceClient(
        provider="auto",
        token=hf_token
    )
    return client

def test_api_connection():
    """Test if the Hugging Face API is accessible."""
    try:
        client = st.session_state.llm_client
        if not client:
            return False, "No API token configured"
        
        test_messages = [{"role": "user", "content": "Say 'Hello' if you can hear me."}]
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=test_messages,
            max_tokens=10,
        )
        return True, "API connection successful"
    except Exception as e:
        return False, f"API Error: {str(e)}"

def init_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "llm_client" not in st.session_state:
        st.session_state.llm_client = None
    if " kb_loaded" not in st.session_state:
        st.session_state.kb_loaded = False

# =============================================================================
# RAG PIPELINE
# =============================================================================

def retrieve_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant context from the knowledge base."""
    if not st.session_state.vector_store:
        return ""
    
    query_embedding = st.session_state.embeddings.embed_query(query)
    
    results = st.session_state.vector_store.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    contexts = []
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        contexts.append(f"[{metadata.get('category', 'unknown')}]: {doc}")
    
    return "\n\n".join(contexts)

def generate_response(query: str, context: str) -> str:
    """Generate a response using the LLM."""
    client = st.session_state.llm_client
    if not client:
        return "LLM client not initialized. Please set HF_TOKEN."
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "model" in error_msg.lower() or "not found" in error_msg.lower():
            return f"I apologize, but I'm having trouble accessing the AI model. Please ensure your Hugging Face token has access to the model. Error: {error_msg}"
        return f"Error generating response: {error_msg}"

def needs_image(query: str) -> bool:
    """Check if the query requires an image."""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in IMAGE_KEYWORDS)

def generate_image_prompt(text_response: str) -> str:
    """Generate an image prompt from the text response."""
    client = st.session_state.llm_client
    if not client:
        return f"ancient Mohenjo-daro ruins, archaeological site, {text_response[:200]}"
    
    prompt_messages = [
        {"role": "system", "content": "You are an expert at creating image generation prompts. Based on the text description, create a detailed prompt for generating a historically accurate image of Mohenjo-daro. Keep the prompt under 200 characters and focus on key visual elements."},
        {"role": "user", "content": f"Create an image prompt for this description:\n{text_response[:500]}"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=prompt_messages,
            max_tokens=100,
        )
        prompt = response.choices[0].message.content.strip()
        prompt = f"Historical illustration of ancient Mohenjo-daro, {prompt}, archaeological accuracy, detailed, realistic"
        return prompt[:500]
    except Exception as e:
        return f"ancient Mohenjo-daro ruins, archaeological site, {text_response[:200]}"

def generate_image(image_prompt: str):
    """Generate an image using the Hugging Face API."""
    client = st.session_state.llm_client
    if not client:
        st.warning("Image generation unavailable: No API token")
        return None
    
    enhanced_prompt = f"ancient Mohenjo-daro ruins, archaeological site, {image_prompt[:200]}"
    
    try:
        image = client.text_to_image(
            prompt=enhanced_prompt,
            model="stabilityai/stable-diffusion-3-medium",
            negative_prompt="modern, buildings, people, text, watermark",
        )
        return image
    except Exception as e:
        st.warning(f"Image generation unavailable: {str(e)}")
        return None

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_header():
    """Render the app header."""
    st.set_page_config(
        page_title="Mohenjo-daro AI Chatbot",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Mohenjo-daro AI Chatbot")
    st.markdown("*Explore the ancient Indus Valley Civilization*")
    st.divider()

def render_sidebar():
    """Render the sidebar with information."""
    with st.sidebar:
        st.header("About")
        st.info("""
        **Mohenjo-daro** (Mound of the Dead Men) was one of the largest 
        urban settlements of the ancient Indus Valley Civilization, 
        flourishing from approximately 2500-1900 BCE.
        
        This chatbot uses AI to answer your questions and can generate 
        images to help visualize this ancient city.
        """)
        
        st.header("Topics You Can Ask About")
        topics = [
            "History of Mohenjo-daro",
            "City Architecture & Planning",
            "Discovery & Excavations",
            "Daily Life & Culture",
            "Famous Artifacts",
            "Drainage System",
            "Decline & Abandonment",
            "Preservation Efforts",
            "Tourism Information"
        ]
        for topic in topics:
            st.write(f"• {topic}")
        
        st.divider()
        st.caption("Powered by Hugging Face API")

def render_chat_interface():
    """Render the chat interface."""
    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "image" in message and message["image"]:
                    st.image(message["image"], width=400)
    
    st.divider()

def render_input():
    """Render the input area."""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.chat_input("Ask me anything about Mohenjo-daro...")
    
    with col2:
        regenerate = st.button("🔄", help="Regenerate last response")
    
    return user_input, regenerate

def handle_user_input(user_input: str):
    """Process user input and generate response."""
    if not user_input:
        return
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("Thinking..."):
        context = retrieve_context(user_input)
        
        if not context:
            response = "I apologize, but I don't have information about that topic. My knowledge is limited to Mohenjo-daro and the Indus Valley Civilization. Please ask me questions about the heritage site, its history, architecture, artifacts, or related topics."
            image = None
        else:
            response = generate_response(user_input, context)
            
            if needs_image(user_input):
                with st.spinner("Generating image..."):
                    image_prompt = generate_image_prompt(response)
                    image = generate_image(image_prompt)
            else:
                image = None
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "image": image
        })
        
        with st.chat_message("assistant"):
            st.markdown(response)
            if image:
                st.image(image, width=400)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    render_header()
    render_sidebar()
    
    init_session_state()
    
    if not st.session_state.kb_loaded:
        with st.spinner("Loading knowledge base..."):
            try:
                st.session_state.vector_store, st.session_state.embeddings = load_vector_store()
                st.session_state.llm_client = init_llm_client()
                st.session_state.kb_loaded = True
                st.success("Knowledge base loaded successfully!")
                
                with st.expander("🔧 API Status"):
                    connected, message = test_api_connection()
                    if connected:
                        st.success(f"Hugging Face API: {message}")
                    else:
                        st.warning(f"Hugging Face API: {message}")
                        st.info("The app will work without image generation if API is not connected.")
                        
            except Exception as e:
                st.error(f"Error loading knowledge base: {str(e)}")
                return
    
    render_chat_interface()
    user_input, _ = render_input()
    
    if user_input:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()
