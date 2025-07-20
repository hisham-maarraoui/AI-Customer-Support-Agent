import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app.services.ai_agent import AIAgent

def handler(request, context):
    """Vercel serverless function for chat API"""
    
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        if request.method == 'POST':
            # Parse request body
            body = request.body.decode('utf-8')
            request_data = json.loads(body)
            
            message = request_data.get('message', '')
            
            if not message:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Message is required"})
                }
            
            # Initialize AI agent
            ai_agent = AIAgent()
            
            # Get response
            response = ai_agent.get_response(message)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    "response": response,
                    "sources": []  # You can add sources here if needed
                })
            }
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({"error": "Method not allowed"})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        } 