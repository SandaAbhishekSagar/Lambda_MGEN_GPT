# Northeastern University Chatbot

A GPU-accelerated RAG (Retrieval-Augmented Generation) chatbot for Northeastern University information.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_minimal.txt
```

### 2. Set Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_openai_api_key_here
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
CHROMADB_API_KEY=your_chromadb_api_key_here
```

### 3. Start the Application

```bash
# Linux/Mac
./start_chatbot.sh

# Windows
python services/chat_service/lambda_gpu_api.py
```

### 4. Access the API

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Chat Endpoint: http://localhost:8000/chat

## API Usage

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What programs does Northeastern University offer?"}'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Project Structure

```
├── services/
│   └── chat_service/
│       ├── lambda_gpu_api.py          # Main API server
│       └── lambda_gpu_chatbot.py      # Core chatbot logic
├── frontend/                          # Web interface
├── start_chatbot.sh                   # Startup script
└── requirements_minimal.txt           # Dependencies
```

## Features

- GPU-accelerated embeddings with PyTorch
- Fast document retrieval with ChromaDB
- OpenAI GPT-4 integration
- Comprehensive error handling
- Caching for improved performance
- Health monitoring endpoints

## Troubleshooting

1. **Import Errors**: Make sure all dependencies are installed
2. **GPU Issues**: The system will fallback to CPU if GPU is not available
3. **ChromaDB Connection**: Check your ChromaDB configuration
4. **OpenAI API**: Verify your API key is valid and has credits

## Support

For issues or questions, check the logs or contact the development team.
