from models.vector_store import VectorStore
from services.storage_service import S3Storage
from services.llm_service import LLMService
from config import Config
import os
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import logging

# Initialize services
vector_store = VectorStore(Config.VECTOR_DB_PATH)
storage_service = S3Storage()
llm_service = LLMService(vector_store)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process_document(file):
    """Process document based on file type and return text chunks"""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save file temporarily
        file.save(temp_path)
        
        # Process based on file type
        if file.filename.endswith('.pdf'):
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
        elif file.filename.endswith('.txt'):
            loader = TextLoader(temp_path)
            documents = loader.load()
        else:
            raise ValueError("Unsupported file type")
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        text_chunks = text_splitter.split_documents(documents)
        
        return text_chunks
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)

