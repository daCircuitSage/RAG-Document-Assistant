import streamlit as st
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env
load_dotenv()

# Check for required API keys
if not os.getenv("MISTRAL_API_KEY"):
    st.error("❌ MISTRAL_API_KEY not found. Please set it in your .env file")
    st.stop()

# Page config
st.set_page_config(page_title="RAG Assistant", layout="wide")

# Sidebar
st.sidebar.title("Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])

# Title
st.title("📚 RAG Document Assistant")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if uploaded_file is not None:
    try:
        # Save uploaded file with cleanup
        temp_pdf_path = Path("temp.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        logger.info(f"PDF uploaded: {uploaded_file.name}")
        st.success("PDF uploaded successfully!")

        # Process button
        if st.button("Process Document"):
            with st.spinner("Processing..."):
                try:
                    # Load
                    loader = PyPDFLoader(str(temp_pdf_path))
                    docs = loader.load()
                    logger.info(f"Loaded {len(docs)} pages from PDF")

                    # Split
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    chunks = splitter.split_documents(docs)
                    logger.info(f"Created {len(chunks)} chunks from document")

                    # Embedding
                    embedding_model = MistralAIEmbeddings(model="mistral-embed")

                    # Vector DB
                    vectorstore = Chroma.from_documents(
                        documents=chunks,
                        embedding=embedding_model,
                        persist_directory="chroma_db"
                    )

                    st.session_state.vectorstore = vectorstore
                    st.success("✅ Document processed and stored!")
                    logger.info("Vector store created successfully")
                    
                except Exception as e:
                    logger.error(f"Error processing document: {str(e)}")
                    st.error(f"❌ Error processing document: {str(e)}")
                finally:
                    # Clean up temp file
                    if temp_pdf_path.exists():
                        temp_pdf_path.unlink()
                        logger.info("Temporary PDF file cleaned up")
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        st.error(f"❌ Error uploading file: {str(e)}")

# Chat Section
if st.session_state.vectorstore:
    query = st.text_input("Ask a question from the document:")

    if query:
        try:
            retriever = st.session_state.vectorstore.as_retriever(
                search_type='mmr',
                search_kwargs={'k': 4, 'fetch_k': 10, 'lambda_mult': 0.4}
            )

            docs = retriever.invoke(query)
            logger.info(f"Retrieved {len(docs)} relevant documents for query")

            if not docs:
                st.warning("⚠️ No relevant documents found for your query.")
            else:
                context = "\n\n".join([doc.page_content for doc in docs])

                prompt = ChatPromptTemplate([
                    ("system", """You are a helpful AI assistant. Use only the provided context to answer questions.
If the answer is not present in the context, say 'I could not find the answer in the document'."""),
                    ("human", "Context: {context}\nQuestion: {question}")
                ])

                final_prompt = prompt.invoke({
                    "context": context,
                    "question": query
                })

                llm = ChatMistralAI(model="mistral-small-2506")
                response = llm.invoke(final_prompt)

                st.write("### Answer:")
                st.write(response.content)
                logger.info("Query answered successfully")
        except Exception as e:
            logger.error(f"Error during query: {str(e)}")
            st.error(f"❌ Error processing your query: {str(e)}")
else:
    st.info("📤 Please upload and process a PDF first.")
