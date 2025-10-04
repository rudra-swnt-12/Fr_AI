#!/bin/bash
# run.sh - Quick start script for Proactive AI Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Proactive AI Assistant Launcher${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import cv2" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not installed. Installing...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}\n"
fi

# Check if Ollama is running
echo -e "${BLUE}Checking Ollama status...${NC}"
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}\n"
else
    echo -e "${RED}✗ Ollama is not running${NC}"
    echo -e "${YELLOW}Please start Ollama in another terminal:${NC}"
    echo -e "  ${YELLOW}$ ollama serve${NC}\n"
    read -p "Press Enter when Ollama is ready, or Ctrl+C to exit..."
fi

# Check if model is available
echo -e "${BLUE}Checking for LLM models...${NC}"
if curl -s http://localhost:11434/api/tags | grep -q "llama3.1\|phi3"; then
    echo -e "${GREEN}✓ Model available${NC}\n"
else
    echo -e "${YELLOW}No suitable model found${NC}"
    echo -e "${YELLOW}Downloading llama3.1 (this may take a while)...${NC}"
    ollama pull llama3.1
    echo -e "${GREEN}✓ Model downloaded${NC}\n"
fi

# Create necessary directories
mkdir -p logs data/models data/cache

# Run the assistant
echo -e "${GREEN}Starting Proactive AI Assistant...${NC}\n"
python main.py

# Deactivate on exit
deactivate