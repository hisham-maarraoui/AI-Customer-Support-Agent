import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.services.vector_store import VectorStoreService
from app.core.config import settings

def reset_pinecone_index():
    """Delete and recreate the Pinecone index with correct dimensions"""
    
    print("Resetting Pinecone index...")
    
    # Initialize vector store service
    vector_store = VectorStoreService()
    
    try:
        # Delete existing index
        print("Deleting existing index...")
        vector_store.delete_index()
        print("✅ Index deleted successfully")
        
        # Create new index with correct dimensions
        print("Creating new index with correct dimensions...")
        vector_store.create_index()
        print("✅ New index created successfully")
        
        print(f"Index '{settings.pinecone_index_name}' reset with {settings.vector_dimension} dimensions")
        
    except Exception as e:
        print(f"❌ Error resetting index: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_pinecone_index() 