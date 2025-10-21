"""
RunPod Serverless Handler for Northeastern University Chatbot
GitHub Deployment Version - GPU-optimized RAG chatbot with ChromaDB and OpenAI
"""

import runpod
import os
import sys
import torch
from typing import Dict, Any, List, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import time
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🚀 RUNPOD GITHUB DEPLOYMENT - Northeastern University Chatbot")
print("=" * 80)

# Check GPU availability and optimize
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"✅ GPU Available: {gpu_name}")
    print(f"✅ GPU Memory: {gpu_memory:.1f} GB")
    print(f"✅ CUDA Version: {torch.version.cuda}")
    
    # Optimize GPU settings
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False
    print("✅ GPU optimizations enabled")
else:
    print("⚠️ No GPU available - running on CPU")

# Environment variables with fallbacks
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMA_API_KEY = os.getenv('CHROMA_API_KEY')
CHROMA_TENANT = os.getenv('CHROMA_TENANT', 'default_tenant')
CHROMA_DATABASE = os.getenv('CHROMA_DATABASE', 'default_database')
CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
CHROMA_PORT = int(os.getenv('CHROMA_PORT', '8000'))

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set!")
if not CHROMA_API_KEY:
    print("❌ ERROR: CHROMA_API_KEY not set!")

print(f"✅ ChromaDB Host: {CHROMA_HOST}")
print(f"✅ ChromaDB Port: {CHROMA_PORT}")


class NortheasternChatbot:
    """GPU-optimized RAG chatbot for Northeastern University with GitHub deployment optimizations"""
    
    def __init__(self):
        """Initialize the chatbot with optimized settings for GitHub deployment"""
        print("\n[INIT] Initializing Northeastern Chatbot for GitHub deployment...")
        
        # Initialize ChromaDB client with optimized settings
        self.client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                chroma_client_auth_credentials=CHROMA_API_KEY,
                anonymized_telemetry=False,  # Disable telemetry for faster startup
                allow_reset=False  # Disable reset for performance
            )
        )
        
        # Initialize OpenAI embeddings with optimized settings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # Fastest embedding model
            openai_api_key=OPENAI_API_KEY,
            chunk_size=1000,  # Optimize chunk size
            max_retries=2,  # Reduce retries for speed
            request_timeout=10  # Faster timeout
        )
        
        # Initialize OpenAI LLM with optimized settings
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Fastest GPT-4 model
            temperature=0.2,  # Lower temperature for consistency
            max_tokens=2000,  # Reduced for faster generation
            openai_api_key=OPENAI_API_KEY,
            request_timeout=15,  # Faster timeout
            max_retries=2,  # Reduce retries
            streaming=False  # Disable streaming for simplicity
        )
        
        # Cache for collections to avoid repeated API calls
        self._collections_cache = None
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 5 minutes cache
        
        # Thread pool for concurrent operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        print("✅ GitHub deployment chatbot initialized successfully")
    
    def get_collections_cached(self) -> List:
        """Get collections with caching to avoid repeated API calls"""
        current_time = time.time()
        
        if (self._collections_cache is None or 
            current_time - self._cache_timestamp > self._cache_ttl):
            
            print("[CACHE] Refreshing collections cache...")
            try:
                # Get all collections with pagination
                all_collections = []
                offset = 0
                limit = 1000
                
                while True:
                    try:
                        collections_batch = self.client.list_collections(limit=limit, offset=offset)
                        if not collections_batch or len(collections_batch) == 0:
                            break
                        all_collections.extend(collections_batch)
                        if len(collections_batch) < limit:
                            break
                        offset += limit
                    except:
                        break
                
                # Filter for batch collections
                batch_collections = [
                    col for col in all_collections
                    if 'batch' in col.name.lower() or 'ultra_optimized' in col.name.lower()
                ]
                
                self._collections_cache = batch_collections
                self._cache_timestamp = current_time
                
                print(f"[CACHE] Cached {len(batch_collections)} batch collections")
                
            except Exception as e:
                print(f"[CACHE ERROR] {str(e)}")
                return []
        
        return self._collections_cache
    
    def search_documents_optimized(self, query: str, n_results: int = 8) -> List[Dict]:
        """Optimized document search with concurrent processing for GitHub deployment"""
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
            max_collections = min(50, len(batch_collections))
            collections_to_search = batch_collections[:max_collections]
            
            all_documents = []
            
            # Search collections concurrently
            def search_collection(collection_obj):
                try:
                    collection = self.client.get_collection(collection_obj.name)
                    
                    # Search this collection
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=n_results * 2
                    )
                    
                    documents = []
                    if results and results.get('documents') and results['documents'][0]:
                        for i, doc in enumerate(results['documents'][0]):
                            metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                            distance = results['distances'][0][i] if results.get('distances') else 1.0
                            doc_id = results['ids'][0][i] if results.get('ids') else str(i)
                            
                            documents.append({
                                'id': doc_id,
                                'content': doc,
                                'metadata': metadata,
                                'distance': distance,
                                'similarity': 1 - distance
                            })
                    
                    return documents
                
                except Exception as e:
                    return []
            
            # Use thread pool for concurrent searches
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(search_collection, col) for col in collections_to_search]
                
                for future in futures:
                    try:
                        documents = future.result(timeout=5)  # 5 second timeout per collection
                        all_documents.extend(documents)
                    except:
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
        """Generate answer with optimized prompt and settings for GitHub deployment"""
        try:
            # Prepare context
            if not context_docs:
                return {
                    'answer': "I don't have enough information to answer this question about Northeastern University.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build optimized context (limit to top 3 documents for speed)
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
        """Optimized chat function for 5-8 second response times with GitHub deployment"""
        start_time = time.time()
        
        print(f"\n[CHAT] Question: {question}")
        
        # Search for relevant documents (optimized)
        search_start = time.time()
        documents = self.search_documents_optimized(question, n_results=6)
        search_time = time.time() - search_start
        print(f"[TIMING] Document search: {search_time:.2f}s")
        
        # Generate answer (optimized)
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


# Initialize chatbot (will be cached across invocations)
print("\n[STARTUP] Initializing chatbot instance for GitHub deployment...")
chatbot = None

try:
    chatbot = NortheasternChatbot()
    print("✅ Chatbot instance created successfully")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {str(e)}")


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    RunPod serverless handler function - Optimized for GitHub deployment
    
    Expected input:
    {
        "input": {
            "question": "What programs does Northeastern offer?"
        }
    }
    
    Returns:
    {
        "answer": "...",
        "sources": [...],
        "confidence": "high|medium|low",
        "timing": {...}
    }
    """
    global chatbot
    
    try:
        print("\n" + "=" * 80)
        print("🎯 NEW REQUEST - GitHub Deployment")
        print("=" * 80)
        
        # Extract input
        input_data = event.get('input', {})
        question = input_data.get('question', '')
        
        if not question:
            return {
                'error': 'No question provided',
                'status': 'error'
            }
        
        # Initialize chatbot if needed
        if chatbot is None:
            print("[HANDLER] Initializing chatbot...")
            chatbot = NortheasternChatbot()
        
        # Process question
        result = chatbot.chat(question)
        
        print(f"[SUCCESS] Generated answer in {result['timing']['total']}s")
        
        return result
    
    except Exception as e:
        print(f"[HANDLER ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'error': str(e),
            'status': 'error'
        }


# RunPod serverless entry point
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 Starting RunPod GitHub Deployment Handler")
    print("=" * 80)
    
    runpod.serverless.start({'handler': handler})