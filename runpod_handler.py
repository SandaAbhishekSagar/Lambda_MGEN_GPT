"""
RunPod Serverless Handler for Northeastern University Chatbot
GPU-optimized RAG chatbot with ChromaDB and OpenAI
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

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🚀 RUNPOD SERVERLESS - Northeastern University Chatbot")
print("=" * 80)

# Check GPU availability
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"✅ GPU Available: {gpu_name}")
    print(f"✅ GPU Memory: {gpu_memory:.1f} GB")
    print(f"✅ CUDA Version: {torch.version.cuda}")
else:
    print("⚠️ No GPU available - running on CPU")

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMA_API_KEY = os.getenv('CHROMA_API_KEY')
CHROMA_TENANT = os.getenv('CHROMA_TENANT', 'default_tenant')
CHROMA_DATABASE = os.getenv('CHROMA_DATABASE', 'default_database')
CHROMA_HOST = os.getenv('CHROMA_HOST')
CHROMA_PORT = int(os.getenv('CHROMA_PORT', '8000'))

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set!")
if not CHROMA_API_KEY:
    print("❌ ERROR: CHROMA_API_KEY not set!")

print(f"✅ ChromaDB Host: {CHROMA_HOST}")
print(f"✅ ChromaDB Port: {CHROMA_PORT}")


class NortheasternChatbot:
    """GPU-optimized RAG chatbot for Northeastern University"""
    
    def __init__(self):
        """Initialize the chatbot with ChromaDB and OpenAI"""
        print("\n[INIT] Initializing Northeastern Chatbot...")
        
        # Initialize ChromaDB client
        self.client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                chroma_client_auth_credentials=CHROMA_API_KEY
            )
        )
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=2500,
            openai_api_key=OPENAI_API_KEY,
            request_timeout=30
        )
        
        print("✅ Chatbot initialized successfully")
    
    def search_documents(self, query: str, n_results: int = 10) -> List[Dict]:
        """Search ChromaDB for relevant documents"""
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search across batch collections
            all_documents = []
            
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
            
            print(f"[SEARCH] Found {len(all_collections)} total collections")
            
            # Filter for batch collections
            batch_collections = [
                col for col in all_collections
                if 'batch' in col.name.lower() or 'ultra_optimized' in col.name.lower()
            ]
            print(f"[SEARCH] Searching {len(batch_collections)} batch collections")
            
            # Search up to 100 collections
            max_collections_to_search = 100
            collections_searched = 0
            
            for collection_obj in batch_collections[:max_collections_to_search]:
                try:
                    collection = self.client.get_collection(collection_obj.name)
                    
                    # Search this collection
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=n_results * 2
                    )
                    
                    # Process results
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
                    
                    collections_searched += 1
                    
                    if collections_searched % 20 == 0:
                        print(f"[SEARCH] Searched {collections_searched} collections, found {len(all_documents)} documents")
                
                except Exception as e:
                    continue
            
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
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> Dict[str, Any]:
        """Generate answer using LLM with retrieved context"""
        try:
            # Prepare context
            if not context_docs:
                return {
                    'answer': "I don't have enough information to answer this question about Northeastern University.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build context string
            context_parts = []
            for i, doc in enumerate(context_docs[:5], 1):
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                source = metadata.get('source', 'Unknown')
                
                context_parts.append(f"[Source {i}] {source}\n{content}\n")
            
            context = "\n".join(context_parts)
            
            # Create prompt
            prompt_template = """You are a helpful assistant for Northeastern University. Answer the question based on the provided context.

Context from Northeastern University documents:
{context}

Question: {question}

Instructions:
- Provide a detailed, comprehensive answer about Northeastern University
- Use information from the context provided above
- Structure your response clearly with bullet points or paragraphs
- Include specific details like numbers, dates, requirements, or procedures when available
- If the context contains relevant information, provide a thorough answer
- Be helpful and informative about Northeastern's programs, policies, and offerings

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
            for doc in context_docs[:5]:
                metadata = doc.get('metadata', {})
                sources.append({
                    'source': metadata.get('source', 'Unknown'),
                    'similarity': round(doc.get('similarity', 0), 2),
                    'url': metadata.get('url', '')
                })
            
            # Determine confidence
            avg_similarity = sum(doc.get('similarity', 0) for doc in context_docs[:5]) / min(5, len(context_docs))
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
        """Main chat function"""
        start_time = time.time()
        
        print(f"\n[CHAT] Question: {question}")
        
        # Search for relevant documents
        search_start = time.time()
        documents = self.search_documents(question, n_results=10)
        search_time = time.time() - search_start
        print(f"[TIMING] Document search: {search_time:.2f}s")
        
        # Generate answer
        generation_start = time.time()
        result = self.generate_answer(question, documents)
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
print("\n[STARTUP] Initializing chatbot instance...")
chatbot = None

try:
    chatbot = NortheasternChatbot()
    print("✅ Chatbot instance created successfully")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {str(e)}")


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    RunPod serverless handler function
    
    Expected input:
    {
        "input": {
            "question": "What programs does Northeastern offer?",
            "n_results": 10  # optional
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
        print("🎯 NEW REQUEST")
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
    print("🚀 Starting RunPod Serverless Handler")
    print("=" * 80)
    
    runpod.serverless.start({'handler': handler})

