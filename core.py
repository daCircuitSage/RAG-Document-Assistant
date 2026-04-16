#load_database
#retrive database

import logging
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

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
    llm = ChatMistralAI(model="mistral-small-2506")
    logger.info("LLM and embedding models initialized successfully")
except Exception as e:
    logger.error(f"Error initializing models: {str(e)}")
    raise

# Check if chroma_db exists
db_path = Path("chroma_db")
if not db_path.exists():
    logger.error(f"Vector database not found at {db_path}")
    logger.info("Please run create_db.py first to create the database")
    raise FileNotFoundError(f"Vector database not found at {db_path}")

try:
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )
    logger.info("Vector store loaded successfully")
except Exception as e:
    logger.error(f"Error loading vector store: {str(e)}")
    raise

retriver = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={
        'k': 4,
        'fetch_k': 10,
        'lambda_mult': 0.4
    }
)

promt = ChatPromptTemplate([
    ('system', """You are a helpful AI assistant. Use only the provided context to answer questions.
If the answer is not present in the context, say 'I could not find the answer in the document'."""),
    ('human', """Context: {context}
Question: {question}""")
])

print('=' * 80)
print('RAG System is Running')
print('Type "0" to EXIT')
print('=' * 80)

try:
    while True:
        query = input("\nYou: ").strip()
        
        if query == "0":
            logger.info("User exited the application")
            print("Goodbye!")
            break
        
        if not query:
            print("Please enter a valid question.\n")
            continue

        try:
            docs = retriver.invoke(query)
            logger.info(f"Retrieved {len(docs)} documents for query")

            if not docs:
                print("\n⚠️ No relevant information found in the document.\n")
                continue

            context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

            final_prompt = promt.invoke({
                'context': context,
                'question': query
            })
            
            respone = llm.invoke(final_prompt)
            print(f"\nAI: {respone.content}\n")
            logger.info("Query processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            print(f"\n❌ Error processing your query: {str(e)}\n")

except KeyboardInterrupt:
    logger.info("Application interrupted by user")
    print("\n\nApplication interrupted.")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    print(f"Unexpected error: {str(e)}")

