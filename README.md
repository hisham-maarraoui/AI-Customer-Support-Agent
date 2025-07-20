# AI Apple Customer Support Agent

An intelligent customer support agent that can answer questions about Apple products and services through both text chat and voice interactions.

## Features

- 🤖 **AI-Powered Support**: Uses RAG (Retrieval-Augmented Generation) to provide accurate, up-to-date information
- 💬 **Text Chat Interface**: Real-time chat with the AI agent
- 🎤 **Voice Support**: Voice interactions powered by Vapi.ai
- 📚 **Knowledge Base**: Scraped and indexed Apple support information
- 🛡️ **Safety Guardrails**: Detects and handles sensitive queries appropriately
- 📅 **Meeting Scheduling**: Tool calls for scheduling appointments
- 📊 **Evaluation Framework**: Comprehensive testing with 50+ realistic scenarios

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and utilities
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── scrapers/       # Web scraping modules
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── public/
├── data/                   # Scraped data and evaluation sets
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Pinecone account
- Vapi.ai account
- OpenAI API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

**Backend (.env):**
```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_env
PINECONE_INDEX_NAME=apple-support
VAPI_API_KEY=your_vapi_key
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VAPI_PUBLIC_KEY=your_vapi_public_key
```

### Running the Application

1. **Start the backend:**
```bash
cd backend
uvicorn main:app --reload
```

2. **Start the frontend:**
```bash
cd frontend
npm start
```

3. **Scrape Apple support data:**
```bash
cd backend
python -m app.scrapers.apple_scraper
```

## API Endpoints

- `POST /api/chat` - Text chat with the AI agent
- `POST /api/voice/start` - Start voice session
- `POST /api/voice/end` - End voice session
- `GET /api/knowledge/search` - Search knowledge base
- `POST /api/schedule` - Schedule a meeting

## Evaluation

Run the evaluation framework:

```bash
cd backend
python -m scripts.evaluate_agent
```

This will test the agent against 50+ realistic scenarios and provide accuracy, helpfulness, and citation quality scores.

## Safety Features

- Personal data detection and redaction
- Legal/financial advice filtering
- Toxicity detection
- Rate limiting
- Input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License 