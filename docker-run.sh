#!/bin/bash

# Build Docker image
docker build -t rag-document-assistant:latest .

# Run with environment variables
docker run -it \
  -e MISTRAL_API_KEY=$MISTRAL_API_KEY \
  -p 8501:8501 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  rag-document-assistant:latest
