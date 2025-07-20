from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.vector_store import vector_store

router = APIRouter()

@router.get("/search")
async def search_knowledge(
    query: str = Query(..., description="Search query"),
    product: Optional[str] = Query(None, description="Filter by product"),
    k: int = Query(5, ge=1, le=20, description="Number of results to return")
):
    """Search the knowledge base"""
    try:
        if product:
            results = vector_store.search_by_product(query, product, k)
        else:
            results = vector_store.search(query, k)
        
        return {
            "query": query,
            "product": product,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")

@router.get("/products")
async def get_products():
    """Get all available products in the knowledge base"""
    try:
        products = vector_store.get_all_products()
        return {
            "products": products,
            "total_products": len(products)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting products: {str(e)}")

@router.get("/products/{product}")
async def get_product_summary(product: str):
    """Get summary information for a specific product"""
    try:
        summary = vector_store.get_product_summary(product)
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting product summary: {str(e)}")

@router.get("/stats")
async def get_knowledge_stats():
    """Get statistics about the knowledge base"""
    try:
        stats = vector_store.get_index_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting knowledge stats: {str(e)}")

@router.post("/reindex")
async def reindex_knowledge():
    """Reindex the knowledge base (admin only)"""
    try:
        # This would typically require authentication/authorization
        # For now, we'll just return a message
        return {
            "message": "Reindexing would be triggered here. This operation requires admin privileges.",
            "status": "not_implemented"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reindexing knowledge base: {str(e)}")

@router.delete("/index")
async def delete_knowledge_index():
    """Delete the knowledge base index (admin only)"""
    try:
        # This would typically require authentication/authorization
        # For now, we'll just return a message
        return {
            "message": "Index deletion would be triggered here. This operation requires admin privileges.",
            "status": "not_implemented"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting knowledge index: {str(e)}") 