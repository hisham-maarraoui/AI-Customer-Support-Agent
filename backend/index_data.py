import json
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.services.vector_store import VectorStoreService
from app.core.config import settings

def load_data_to_vectorstore():
    """Load scraped Apple support data into the vector store"""
    
    # Initialize vector store service
    vector_store = VectorStoreService()
    
    # Load scraped data
    data_file = Path(__file__).parent.parent / "data" / "apple_support_data.json"
    
    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        return
    
    print(f"Loading data from {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)
    
    print(f"Found {len(scraped_data)} pages to index")
    
    try:
        # Create index if it doesn't exist
        print("Creating/checking Pinecone index...")
        vector_store.create_index()
        
        # Load vector store
        print("Loading vector store...")
        vector_store.load_vectorstore()
        
        # Prepare documents for indexing
        print("Preparing documents for indexing...")
        documents = vector_store.prepare_documents(scraped_data)
        
        print(f"Prepared {len(documents)} documents for indexing")
        
        # Add documents to vector store
        print("Adding documents to vector store...")
        vector_store.add_documents(documents)
        
        print("✅ Successfully indexed all Apple support data!")
        
        # Print summary
        products = {}
        for item in scraped_data:
            product = item.get('product', 'Unknown')
            products[product] = products.get(product, 0) + 1
        
        print("\nIndexing Summary:")
        for product, count in products.items():
            print(f"  {product}: {count} pages")
            
    except Exception as e:
        print(f"❌ Error indexing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_data_to_vectorstore() 