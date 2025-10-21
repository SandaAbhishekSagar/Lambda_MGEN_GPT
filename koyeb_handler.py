"""
Koyeb Handler for Northeastern University Chatbot
Optimized for CPU deployment on Koyeb platform
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional
import chromadb
from chromadb.config import Settings
from chromadb import CloudClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🚀 KOYEB DEPLOYMENT - Northeastern University Chatbot")
print("=" * 80)

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMA_API_KEY = os.getenv('CHROMA_API_KEY')
CHROMA_TENANT = os.getenv('CHROMA_TENANT', '28757e4a-f042-4b0c-ad7c-9257cd36b130')
CHROMA_DATABASE = os.getenv('CHROMA_DATABASE', 'newtest')

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set!")
if not CHROMA_API_KEY:
    print("❌ ERROR: CHROMA_API_KEY not set!")

print(f"✅ ChromaDB Tenant: {CHROMA_TENANT}")
print(f"✅ ChromaDB Database: {CHROMA_DATABASE}")


class NortheasternChatbot:
    """CPU-optimized RAG chatbot for Northeastern University on Koyeb"""
    
    def __init__(self):
        """Initialize the chatbot with optimized settings for Koyeb"""
        print("\n[INIT] Initializing Northeastern Chatbot for Koyeb...")
        
        # Initialize ChromaDB Cloud client
        self.client = CloudClient(
            api_key=CHROMA_API_KEY,
            tenant=CHROMA_TENANT,
            database=CHROMA_DATABASE
        )
        
        # Initialize OpenAI embeddings with optimized settings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # Fastest embedding model
            openai_api_key=OPENAI_API_KEY,
            chunk_size=1000,
            max_retries=2,
            request_timeout=10
        )
        
        # Initialize OpenAI LLM with optimized settings
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Fastest GPT-4 model
            temperature=0.2,
            max_tokens=2000,
            openai_api_key=OPENAI_API_KEY,
            request_timeout=15,
            max_retries=2,
            streaming=False
        )
        
        # Cache for collections
        self._collections_cache = None
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 5 minutes cache
        
        # Thread pool for concurrent operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        print("✅ Koyeb chatbot initialized successfully")
    
    def get_collections_cached(self) -> List:
        """Get collections with caching"""
        current_time = time.time()
        
        if (self._collections_cache is None or 
            current_time - self._cache_timestamp > self._cache_ttl):
            
            print("[CACHE] Refreshing collections cache...")
            try:
                collections = self.client.list_collections()
                
                # Filter for batch collections
                batch_collections = [
                    col for col in collections
                    if 'batch' in col.name.lower() or 'ultra_optimized' in col.name.lower()
                ]
                
                self._collections_cache = batch_collections
                self._cache_timestamp = current_time
                
                print(f"[CACHE] Cached {len(batch_collections)} batch collections")
                
            except Exception as e:
                print(f"[CACHE ERROR] {str(e)}")
                return []
        
        return self._collections_cache
    
    def search_documents_optimized(self, query: str, n_results: int = 6) -> List[Dict]:
        """Optimized document search for Koyeb CPU deployment"""
        try:
            start_time = time.time()
            
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            embedding_time = time.time() - start_time
            print(f"[TIMING] Embedding generation: {embedding_time:.2f}s")
            
            # Get cached collections
            batch_collections = self.get_collections_cached()
            
            if not batch_collections:
                print("[SEARCH] No batch collections found")
                return []
            
            print(f"[SEARCH] Searching {len(batch_collections)} collections")
            
            # Limit collections for faster search
            max_collections = min(30, len(batch_collections))
            collections_to_search = batch_collections[:max_collections]
            
            all_documents = []
            
            # Search collections
            for collection_obj in collections_to_search:
                try:
                    collection = self.client.get_collection(collection_obj.name)
                    
                    # Search this collection
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=n_results * 2
                    )
                    
                    if results and results.get('documents') and results['documents'][0]:
                        for i, doc in enumerate(results['documents'][0]):
                            metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                            distance = results['distances'][0][i] if results.get('distances') else 1.0
                            doc_id = results['ids'][0][i] if results.get('ids') else str(i)
                            
                            all_documents.append({
                                'id': doc_id,
                                'content': doc,
                                'metadata': metadata,
                                'distance': distance,
                                'similarity': 1 - distance
                            })
                
                except Exception as e:
                    continue
            
            search_time = time.time() - start_time
            print(f"[TIMING] Total search time: {search_time:.2f}s")
            print(f"[SEARCH] Total documents found: {len(all_documents)}")
            
            # Deduplicate by document ID
            seen_ids = {}
            for doc in all_documents:
                doc_id = doc['id']
                if doc_id not in seen_ids or doc['distance'] < seen_ids[doc_id]['distance']:
                    seen_ids[doc_id] = doc
            
            unique_documents = list(seen_ids.values())
            print(f"[SEARCH] Unique documents after deduplication: {len(unique_documents)}")
            
            # Sort by similarity and return top N
            unique_documents.sort(key=lambda x: x['distance'])
            return unique_documents[:n_results]
        
        except Exception as e:
            print(f"[SEARCH ERROR] {str(e)}")
            return []
    
    def generate_answer_optimized(self, question: str, context_docs: List[Dict]) -> Dict[str, Any]:
        """Generate answer with optimized prompt for Koyeb"""
        try:
            if not context_docs:
                return {
                    'answer': "I don't have enough information to answer this question about Northeastern University.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build optimized context (limit to top 3 documents)
            context_parts = []
            for i, doc in enumerate(context_docs[:3], 1):
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                source = metadata.get('source', 'Unknown')
                
                # Truncate content for faster processing
                if len(content) > 1000:
                    content = content[:1000] + "..."
                
                context_parts.append(f"[Source {i}] {source}\n{content}\n")
            
            context = "\n".join(context_parts)
            
            # Optimized prompt for faster generation
            prompt_template = """Answer this question about Northeastern University using the provided context.

Context:
{context}

Question: {question}

Provide a concise, accurate answer based on the context. Include specific details when available.

Answer:"""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Generate answer
            formatted_prompt = prompt.format(context=context, question=question)
            response = self.llm.invoke(formatted_prompt)
            answer = response.content
            
            # Prepare sources
            sources = []
            for doc in context_docs[:3]:
                metadata = doc.get('metadata', {})
                sources.append({
                    'source': metadata.get('source', 'Unknown'),
                    'similarity': round(doc.get('similarity', 0), 2),
                    'url': metadata.get('url', '')
                })
            
            # Determine confidence
            avg_similarity = sum(doc.get('similarity', 0) for doc in context_docs[:3]) / min(3, len(context_docs))
            if avg_similarity > 0.7:
                confidence = 'high'
            elif avg_similarity > 0.5:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': confidence,
                'documents_searched': len(context_docs)
            }
        
        except Exception as e:
            print(f"[GENERATION ERROR] {str(e)}")
            return {
                'answer': f"I encountered an error generating the answer: {str(e)}",
                'sources': [],
                'confidence': 'low'
            }
    
    def chat(self, question: str) -> Dict[str, Any]:
        """Optimized chat function for Koyeb CPU deployment"""
        start_time = time.time()
        
        print(f"\n[CHAT] Question: {question}")
        
        # Search for relevant documents
        search_start = time.time()
        documents = self.search_documents_optimized(question, n_results=6)
        search_time = time.time() - search_start
        print(f"[TIMING] Document search: {search_time:.2f}s")
        
        # Generate answer
        generation_start = time.time()
        result = self.generate_answer_optimized(question, documents)
        generation_time = time.time() - generation_start
        print(f"[TIMING] Answer generation: {generation_time:.2f}s")
        
        total_time = time.time() - start_time
        print(f"[TIMING] Total response time: {total_time:.2f}s")
        
        # Add timing information
        result['timing'] = {
            'search': round(search_time, 2),
            'generation': round(generation_time, 2),
            'total': round(total_time, 2)
        }
        
        return result


# Initialize chatbot
print("\n[STARTUP] Initializing chatbot instance for Koyeb...")
chatbot = None

try:
    chatbot = NortheasternChatbot()
    print("✅ Chatbot instance created successfully")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {str(e)}")

# FastAPI app for Koyeb
app = FastAPI(
    title="Northeastern University Chatbot API",
    description="CPU-optimized chatbot for Koyeb deployment",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict]
    confidence: str
    timing: Dict[str, float]

@app.get("/")
async def root():
    return {"message": "Northeastern University Chatbot API", "status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint for Koyeb deployment"""
    global chatbot
    
    try:
        if chatbot is None:
            chatbot = NortheasternChatbot()
        
        result = chatbot.chat(request.question)
        
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources'],
            confidence=result['confidence'],
            timing=result['timing']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/runpod")
async def runpod_endpoint(event: Dict[str, Any]):
    """RunPod-compatible endpoint for Koyeb"""
    global chatbot
    
    try:
        if chatbot is None:
            chatbot = NortheasternChatbot()
        
        # Extract input
        input_data = event.get('input', {})
        question = input_data.get('question', '')
        
        if not question:
            return {
                'error': 'No question provided',
                'status': 'error'
            }
        
        result = chatbot.chat(question)
        return result
    
    except Exception as e:
        return {
            'error': str(e),
            'status': 'error'
        }

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 Starting Koyeb Northeastern Chatbot API")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
