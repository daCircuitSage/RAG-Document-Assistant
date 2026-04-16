#load the documents
#split the documents
#making chunks of the documents
#make the embeddings of the documents
#create the vector db and store all the docs in the db

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_mistralai.embeddings import MistralAIEmbeddings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Check for API key
if not os.getenv("MISTRAL_API_KEY"):
    logger.error("MISTRAL_API_KEY not set in environment variables")
    raise ValueError("MISTRAL_API_KEY environment variable is not set")

try:
    embedding_model = MistralAIEmbeddings(model='mistral-embed')
    logger.info("Embedding model initialized successfully")
except Exception as e:
    logger.error(f"Error initializing embedding model: {str(e)}")
    raise

# Check if PDF file exists
pdf_path = Path("documents_loaders/deep_learning.pdf")
if not pdf_path.exists():
    logger.error(f"PDF file not found at {pdf_path}")
    raise FileNotFoundError(f"Please ensure the PDF file exists at {pdf_path}")

try:
    logger.info(f"Loading PDF from {pdf_path}")
    raw_document = PyPDFLoader(str(pdf_path))
    docs = raw_document.load()
    logger.info(f"Successfully loaded {len(docs)} pages from PDF")

    logger.info("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Created {len(chunks)} chunks from document")

    logger.info("Creating vector store and storing embeddings...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory='chroma_db',
    )
    logger.info("✅ Vector database created successfully!")
    logger.info(f"Database stored in 'chroma_db' directory with {len(chunks)} chunks")

except Exception as e:
    logger.error(f"Error creating database: {str(e)}")
    raise