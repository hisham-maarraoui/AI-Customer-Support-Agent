#!/bin/bash

# Apple Support AI Agent Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🍎 Apple Support AI Agent Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed. Please install Python 3.9+"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed. Please install npm"
        exit 1
    fi
    
    print_success "System requirements met"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=apple-support

# Vapi Configuration (optional)
VAPI_API_KEY=your_vapi_api_key_here
VAPI_PUBLIC_KEY=your_vapi_public_key_here

# Application Configuration
APP_NAME=Apple Support AI Agent
DEBUG=True
RATE_LIMIT_PER_MINUTE=60

# Model Configuration
GEMINI_MODEL=gemini-1.5-pro
EMBEDDING_MODEL=text-embedding-ada-002

# Vector Database Configuration
VECTOR_DIMENSION=1536
VECTOR_METRIC=cosine
EOF
        print_warning "Please update the .env file with your actual API keys"
    else
        print_status ".env file already exists"
    fi
    
    cd ..
    print_success "Backend setup completed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating frontend .env file..."
        cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VAPI_PUBLIC_KEY=your_vapi_public_key_here
EOF
    else
        print_status "Frontend .env file already exists"
    fi
    
    cd ..
    print_success "Frontend setup completed"
}

# Create data directory
create_data_directory() {
    print_status "Creating data directory..."
    mkdir -p data
    print_success "Data directory created"
}

# Setup script permissions
setup_scripts() {
    print_status "Setting up script permissions..."
    chmod +x backend/scripts/evaluate_agent.py
    print_success "Script permissions set"
}

# Display next steps
show_next_steps() {
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "================================"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Configure API Keys:"
echo "   - Edit backend/.env with your Google API key"
echo "   - Edit backend/.env with your Pinecone API key and environment"
echo "   - (Optional) Add Vapi API keys for voice support"
    echo ""
    echo "2. Scrape Apple Support Data:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python -m app.scrapers.apple_scraper"
    echo ""
    echo "3. Start the Backend:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn main:app --reload"
    echo ""
    echo "4. Start the Frontend (in a new terminal):"
    echo "   cd frontend"
    echo "   npm start"
    echo ""
    echo "5. Access the application:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "6. Run Evaluation (optional):"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python scripts/evaluate_agent.py"
    echo ""
    echo "📚 Documentation:"
    echo "   - README.md: Project overview and setup instructions"
    echo "   - API docs: http://localhost:8000/docs (after starting backend)"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   - Check that all API keys are correctly set in .env files"
    echo "   - Ensure Python 3.9+ and Node.js 18+ are installed"
    echo "   - Make sure ports 3000 and 8000 are available"
    echo ""
}

# Main setup function
main() {
    check_requirements
    setup_backend
    setup_frontend
    create_data_directory
    setup_scripts
    show_next_steps
}

# Run main function
main 