import os
import json
import logging
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        self.pinecone_api_key = settings.pinecone_api_key
        self.pinecone_environment = settings.pinecone_environment
        self.pinecone_index_name = settings.pinecone_index_name
        self.google_api_key = settings.google_api_key

        # Check if API keys are provided
        if not self.pinecone_api_key:
            logger.warning("Pinecone API key not provided. Vector store functionality will be limited.")
            self.pc = None
            self.embeddings = None
        else:
        # Initialize Pinecone client
        self.pc = PineconeClient(api_key=self.pinecone_api_key)

        # Initialize Gemini embeddings
            if self.google_api_key:
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=self.google_api_key
        )
            else:
                logger.warning("Google API key not provided. Embeddings will not work.")
                self.embeddings = None

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        self.index = None
        self.vectorstore = None

    def create_index(self):
        """Create Pinecone index if it doesn't exist"""
        try:
            index_names = [idx.name for idx in self.pc.list_indexes()]
            if self.pinecone_index_name not in index_names:
                self.pc.create_index(
                    name=self.pinecone_index_name,
                    dimension=settings.vector_dimension,
                    metric=settings.vector_metric,
                    spec=ServerlessSpec(
                        cloud="aws",  # or "gcp" if you use Google Cloud
                        region=self.pinecone_environment
                    )
                )
                logger.info(f"Created Pinecone index: {self.pinecone_index_name}")
            else:
                logger.info(f"Pinecone index already exists: {self.pinecone_index_name}")
            self.index = self.pc.Index(self.pinecone_index_name)
        except Exception as e:
            logger.error(f"Error creating Pinecone index: {e}")
            raise

    def load_vectorstore(self):
        """Load the vector store"""
        try:
            self.vectorstore = Pinecone.from_existing_index(
                index_name=self.pinecone_index_name,
                embedding=self.embeddings
            )
            logger.info("Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise

    def prepare_documents(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare documents for vector storage"""
        documents = []

        for item in data:
            # Create main document from content
            if item.get('content'):
                content = item['content']
                if len(content) > 100:  # Only process substantial content
                    # Split content into chunks
                    chunks = self.text_splitter.split_text(content)

                    for i, chunk in enumerate(chunks):
                        documents.append({
                            'text': chunk,
                            'metadata': {
                                'url': item.get('url', ''),
                                'title': item.get('title', ''),
                                'product': item.get('product', ''),
                                'chunk_id': i,
                                'total_chunks': len(chunks),
                                'content_type': 'main_content'
                            }
                        })

            # Add FAQ items as separate documents
            for faq in item.get('faq_items', []):
                if faq.get('question') and faq.get('answer'):
                    faq_text = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
                    documents.append({
                        'text': faq_text,
                        'metadata': {
                            'url': item.get('url', ''),
                            'title': item.get('title', ''),
                            'product': item.get('product', ''),
                            'content_type': 'faq',
                            'question': faq['question']
                        }
                    })

            # Add troubleshooting steps
            for i, step in enumerate(item.get('troubleshooting', [])):
                if step and len(step) > 20:  # Only substantial steps
                    documents.append({
                        'text': step,
                        'metadata': {
                            'url': item.get('url', ''),
                            'title': item.get('title', ''),
                            'product': item.get('product', ''),
                            'content_type': 'troubleshooting',
                            'step_number': i + 1
                        }
                    })

        return documents

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store"""
        try:
            if not self.vectorstore:
                self.load_vectorstore()

            # Prepare texts and metadatas
            texts = [doc['text'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]

            # Add to vector store
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)

            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise

    def search(self, query: str, k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search the vector store"""
        try:
            # Check if vector store is available
            if not self.pinecone_api_key or not self.google_api_key:
                logger.warning("API keys not available for vector store search")
                return []
            
            if not self.vectorstore:
                self.load_vectorstore()

            # Perform search
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )

            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score)
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []

    def search_by_product(self, query: str, product: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for a specific product"""
        filter_dict = {'product': product}
        return self.search(query, k, filter_dict)

    def get_product_summary(self, product: str) -> Dict[str, Any]:
        """Get summary information for a specific product"""
        try:
            # Search for general information about the product
            results = self.search_by_product(
                query=f"general information about {product}",
                product=product,
                k=10
            )

            # Extract unique URLs and titles
            urls = set()
            titles = set()

            for result in results:
                metadata = result['metadata']
                if metadata.get('url'):
                    urls.add(metadata['url'])
                if metadata.get('title'):
                    titles.add(metadata['title'])

            return {
                'product': product,
                'document_count': len(results),
                'unique_urls': len(urls),
                'urls': list(urls)[:5],  # Limit to 5 URLs
                'titles': list(titles)[:5]  # Limit to 5 titles
            }

        except Exception as e:
            logger.error(f"Error getting product summary: {e}")
            return {'product': product, 'error': str(e)}

    def get_all_products(self) -> List[str]:
        """Get list of all products in the vector store"""
        try:
            if not self.index:
                self.index = self.pc.Index(self.pinecone_index_name)

            # Get all vectors and extract unique products
            response = self.index.query(
                vector=[0] * settings.vector_dimension,  # Dummy vector
                top_k=10000,  # Get all vectors
                include_metadata=True
            )

            products = set()
            for match in response.matches:
                if match.metadata and 'product' in match.metadata:
                    products.add(match.metadata['product'])

            return list(products)

        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            return []

    def delete_index(self):
        """Delete the Pinecone index"""
        try:
            if self.pinecone_index_name in [idx.name for idx in self.pc.list_indexes()]:
                self.pc.delete_index(self.pinecone_index_name)
                logger.info(f"Deleted Pinecone index: {self.pinecone_index_name}")
        except Exception as e:
            logger.error(f"Error deleting index: {e}")

    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if not self.index:
                self.index = self.pc.Index(self.pinecone_index_name)

            stats = self.index.describe_index_stats()

            return {
                'total_vector_count': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness,
                'namespaces': stats.namespaces
            }

        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {'error': str(e)}

# Global instance
vector_store = VectorStoreService() 