# Apple Support AI Agent

An AI-powered customer support agent that provides helpful information about Apple products and services through a modern chat interface.

## Features

- AI-Powered Support: Provides helpful responses to Apple support questions
- Retrieval-Augmented Generation: Answers are grounded in Apple support documentation
- Real-time Chat Interface: Modern React-based chat with message history (in-memory only)
- Source Citations: Every response includes relevant Apple support links with confidence scores
- Safety Guardrails: Detects and handles sensitive queries appropriately
- Confidence Scoring: Shows AI confidence levels based on source relevance
- Dark Mode: Beautiful dark/light theme toggle
- Responsive Design: Works seamlessly on desktop and mobile devices

## Architecture

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/     # API endpoints (chat, voice, knowledge, schedule)
│   │   ├── core/           # Configuration and settings
│   │   ├── models/         # Pydantic data models
│   │   ├── services/       # Business logic (AI agent, vector store, guardrails)
│   │   └── scrapers/       # Apple support data scraping
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI application entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components (Chat, About, Knowledge, etc.)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── contexts/       # React contexts (Dark mode)
│   │   └── index.js        # App entry point
│   ├── package.json        # Node.js dependencies
│   └── public/             # Static assets
├── data/                   # Apple support data and evaluation sets
├── scripts/                # Utility and evaluation scripts
└── docs/                   # Documentation
```

## Tech Stack

### Backend

- FastAPI - Modern Python web framework
- Pinecone - Vector database for semantic search
- Uvicorn - ASGI server
- Pydantic - Data validation and settings

### Frontend

- React 18 - UI framework
- Tailwind CSS - Utility-first CSS framework
- React Query - Data fetching and caching
- React Router - Client-side routing
- Axios - HTTP client

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Pinecone account and API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Customer-Support-Agent-Project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Create .env file
# Edit .env with your API keys
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables (optional for local development)
cp .env.example .env  # Create .env file if needed
```

### 4. Run the Application

**Start the backend:**

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Start the frontend (in a new terminal):**

```bash
cd frontend
npm start
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## API Endpoints

- POST /api/chat - Chat with the AI agent
- GET /api/health - Health check
- GET /api/conversations - List conversations
- GET /api/conversations/{id} - Get specific conversation
- DELETE /api/conversations/{id} - Delete conversation

## Testing

### Run Backend Tests

```bash
cd backend
python -m pytest
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

### Evaluate AI Agent

```bash
cd backend
python scripts/evaluate_agent.py
```

## Development

### Project Structure

- Backend: FastAPI application with modular architecture
- Frontend: React application with component-based structure
- Data: Apple support documentation and evaluation datasets
- Scripts: Utility scripts for scraping, evaluation, and maintenance

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Note: This AI agent is designed to assist with Apple product support but is not a replacement for official Apple Support. For critical issues, always contact Apple Support directly.
