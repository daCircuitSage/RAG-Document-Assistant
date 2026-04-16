# 📚 RAG Document Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** system that leverages Mistral AI and LangChain to provide intelligent document analysis and Q&A capabilities.

## ✨ Features

- 🚀 **Interactive Web UI** - Streamlit-based user-friendly interface
- 📄 **PDF Processing** - Automatic PDF upload and processing
- 🔍 **Intelligent Retrieval** - MMR (Maximum Marginal Relevance) search for better context
- 🧠 **LLM-Powered Responses** - Mistral AI integration for context-aware answers
- 💾 **Persistent Vector Database** - ChromaDB for efficient document embeddings
- 🛡️ **Error Handling** - Comprehensive error handling and logging
- 🔐 **Environment Security** - Secure API key management via `.env`
- 📊 **CLI Support** - Command-line interface for batch processing

## 🏗️ Architecture

```
┌─────────────────┐
│  User (UI/CLI)  │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Streamlit│ (app.py) OR CLI (core.py)
    └────┬────┘
         │
    ┌────▼──────────────────┐
    │  LangChain Pipeline   │
    │  - Document Loading  │
    │  - Text Splitting    │
    │  - Embedding         │
    │  - Retrieval         │
    └────┬──────────────────┘
         │
    ┌────▼────────────────────┐
    │  ChromaDB Vector Store  │ (chroma_db/)
    │  + Mistral Embeddings   │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │  Mistral AI LLM         │
    │  (mistral-small-2506)   │
    └─────────────────────────┘
```

## 📋 Prerequisites

- **Python 3.11+**
- **API Keys**:
  - [Mistral AI API Key](https://console.mistral.ai/api-keys)
  - (Optional) Google API Key for alternative LLM
  - (Optional) OpenAI API Key for alternative LLM

## 🚀 Quick Start

### 1. Clone & Setup

```bash
# Clone the repository
git clone <repository-url>
cd RAG-Document-Assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# .env should contain:
# MISTRAL_API_KEY=your_mistral_api_key_here
# (Optional) GOOGLE_API_KEY=your_google_api_key_here
# (Optional) OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Create Vector Database

First-time setup: Initialize the vector database from a PDF file.

```bash
# Place your PDF at: documents_loaders/deep_learning.pdf
python create_db.py
```

This will:
- Load the PDF document
- Split it into chunks (1000 chars with 200-char overlap)
- Generate embeddings using Mistral
- Store in ChromaDB for efficient retrieval

### 5. Run the Application

#### Option A: Web UI (Streamlit)

```bash
streamlit run app.py
```

Then:
1. Open your browser to `http://localhost:8501`
2. Upload a PDF file
3. Click "Process Document"
4. Ask questions about your document

#### Option B: CLI (Command Line)

```bash
python core.py
```

Then:
1. Type your questions at the prompt
2. Type `0` to exit

## 📁 Project Structure

```
RAG-Project/
├── app.py                      # Streamlit web interface
├── core.py                     # CLI interface & core RAG logic
├── create_db.py               # Database initialization script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
│
├── documents_loaders/         # Document processing utilities
│   ├── docs.py               # Document summarization script
│   ├── test.py               # Text splitting test script
│   └── notes.txt             # Processing notes
│
├── chroma_db/                # Vector database (generated)
│   └── [database files]
│
└── EnvRAG/                   # Virtual environment (generated)
    └── [venv files]
```

## 🔧 Configuration

### Vector Store Settings

Adjust in `app.py` or `core.py` retriever configuration:

```python
retriever = vectorstore.as_retriever(
    search_type='mmr',  # Maximum Marginal Relevance
    search_kwargs={
        'k': 4,           # Number of results to return
        'fetch_k': 10,    # Number of candidates to fetch
        'lambda_mult': 0.4  # Diversity parameter
    }
)
```

### Text Splitting Parameters

Modify in `create_db.py` and `app.py`:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=200     # Overlap between chunks
)
```

## 🚢 Deployment Guide

### Local Deployment

```bash
# Using Streamlit's built-in server
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t rag-assistant .
docker run -e MISTRAL_API_KEY=your_key -p 8501:8501 rag-assistant
```

### Cloud Deployment (Streamlit Cloud)

1. Push repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy
5. Add secrets in Streamlit Cloud dashboard

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select "Docker" runtime
3. Push your repository with `Dockerfile`
4. Set environment variables in Space settings

## 🧪 Testing

### Test Syntax

```bash
python -m py_compile app.py core.py create_db.py documents_loaders/*.py
```

### Run Database Creation

```bash
python create_db.py
```

### Test CLI Interface

```bash
python core.py
```

### Test Web UI

```bash
streamlit run app.py
```

## 📊 Logging

All operations are logged to console. Check for:

```
INFO - Vector store loaded successfully
INFO - Retrieved 4 relevant documents
INFO - Query answered successfully
ERROR - Error processing document: [details]
```

## 🔒 Security Best Practices

- ✅ Never commit `.env` file (included in `.gitignore`)
- ✅ Use environment variables for all secrets
- ✅ Validate user inputs
- ✅ Use strong API keys
- ✅ Implement rate limiting for production
- ✅ Add authentication layer for multi-user deployments
- ✅ Monitor API usage and costs

## 📦 Dependencies

### Core

- **streamlit** - Web UI framework
- **langchain** - RAG orchestration
- **mistralai** - LLM provider
- **chromadb** - Vector database

### LLM & Embeddings

- **langchain-mistralai** - Mistral integration
- **langchain-google-genai** - Google AI integration
- **langchain-openai** - OpenAI integration

### Document Processing

- **pypdf** - PDF loading
- **python-docx** - Word document support
- **beautifulsoup4** - HTML parsing

## 🐛 Troubleshooting

### "MISTRAL_API_KEY not found"

```bash
# Check .env file exists and has your API key
cat .env
# If missing, create it:
cp .env.example .env
# Edit .env with your actual API key
```

### "Vector database not found"

```bash
# Initialize the database first
python create_db.py
```

### "Connection refused" / "API Error"

- Check internet connection
- Verify API keys are valid
- Check Mistral API rate limits
- Review error logs

### "Out of memory"

- Reduce `chunk_size` in text splitting
- Reduce `fetch_k` in retriever settings
- Process smaller PDFs

### Slow response time

- Check network connectivity
- Reduce `k` parameter in retriever
- Consider smaller chunks
- Verify ChromaDB has adequate indices

## 🚀 Performance Tips

1. **Batch Processing** - Process multiple documents at once
2. **Caching** - Use Streamlit's `@st.cache_data` for expensive operations
3. **Indexing** - ChromaDB automatically optimizes for retrieval
4. **API Optimization** - Batch embeddings when possible
5. **Chunk Size** - Balance between context and retrieval speed

## 📚 References

- [Mistral AI Documentation](https://docs.mistral.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name/Team**

- Core RAG Logic: Created by the author
- Streamlit Frontend: Enhanced with ChatGPT assistance
- Deployment-Ready Updates: Production optimization

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🗺️ Roadmap

- [ ] Multi-document support
- [ ] Web API (FastAPI)
- [ ] Advanced analytics dashboard
- [ ] User authentication
- [ ] Admin panel
- [ ] Query history & bookmarks
- [ ] Custom LLM model support
- [ ] Batch processing UI
- [ ] Cost tracking
- [ ] Multi-language support

## ⚡ Future Enhancements

- Support for more document formats (DOCX, TXT, CSV, etc.)
- Fine-tuned models for domain-specific queries
- Real-time collaboration features
- Advanced search filters
- Export results to PDF/Word
- API rate limiting and usage tracking
- Database backup & recovery
- Performance monitoring

---

**Last Updated:** April 2026  
**Status:** ✅ Production Ready
