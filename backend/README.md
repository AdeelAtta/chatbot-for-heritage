---
title: Moḥenjo-daro AI Chatbot
emoji: 🏛️
colorFrom: indigo
colorTo: orange
sdk: docker
app_port: 7860
pinned: false
suggested_storage: smallest
---

# Moḥenjo-daro AI Chatbot Backend

RAG-powered API for chat and image generation about the ancient Indus Valley Civilization.

## Setup

1. Create a Hugging Face Space with **Docker** SDK
2. Add `HF_TOKEN` as a secret in Space settings
3. Push this code - it will auto-deploy

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | Your Hugging Face API token (required) |
| `PORT` | Server port (default: 7860) |

## API Endpoints

- `GET /` - Health check
- `POST /chat/stream` - Streaming chat with RAG
- `POST /image` - Image generation
