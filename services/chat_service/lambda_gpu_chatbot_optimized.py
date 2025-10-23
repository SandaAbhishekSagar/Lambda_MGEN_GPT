"""
Lambda Labs GPU-Optimized Northeastern University Chatbot
Ultra-fast RAG chatbot with GPU acceleration for Lambda Labs deployment
"""

import os
import sys
import time
import torch
import numpy as np
import hashlib
import pickle
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatResponse:
    """Structured response from the chatbot"""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str
    timing: Dict[str, float]
    gpu_info: Dict[str, Any]

class LambdaGPUEmbeddingManager:
    """Ultra-optimized GPU embedding manager for Lambda Labs"""
    
    def __init__(self, cache_file: str = "lambda_gpu_embeddings_cache.pkl"):
        self.cache_file = cache_file
        self.embeddings_cache = {}
        self.document_embeddings = {}
        self.model = None
        self.device = self._get_optimal_device()
        self.batch_size = 32  # Optimized for GPU memory
        self.load_cache()
        
        logger.info(f"[LAMBDA GPU] Initialized on device: {self.device}")
    
    def _get_optimal_device(self) -> str:
        """Get optimal device for Lambda Labs GPU"""
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"[LAMBDA GPU] GPU: {gpu_name}, Memory: {gpu_memory:.1f}GB")
            
            # Optimize for Lambda Labs GPUs
            if "A100" in gpu_name or "H100" in gpu_name:
                self.batch_size = 64
            elif "4090" in gpu_name or "3090" in gpu_name:
                self.batch_size = 48
            elif "3080" in gpu_name:
                self.batch_size = 32
            else:
                self.batch_size = 24
                
            return "cuda"
        else:
            logger.warning("[LAMBDA GPU] No GPU available, using CPU")
            self.batch_size = 16
            return "cpu"
    
    def load_cache(self):
        """Load embeddings cache with error handling"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.embeddings_cache = cache_data.get('query_cache', {})
                    self.document_embeddings = cache_data.get('document_embeddings', {})
                logger.info(f"[LAMBDA GPU] Loaded cache: {len(self.embeddings_cache)} queries, {len(self.document_embeddings)} documents")
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error loading cache: {e}")
            self.embeddings_cache = {}
            self.document_embeddings = {}
    
    def save_cache(self):
        """Save embeddings cache with error handling"""
        try:
            cache_data = {
                'query_cache': self.embeddings_cache,
                'document_embeddings': self.document_embeddings
            }
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info(f"[LAMBDA GPU] Saved cache: {len(self.embeddings_cache)} queries, {len(self.document_embeddings)} documents")
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error saving cache: {e}")
    
    def get_embedding_model(self):
        """Get or create GPU-optimized embedding model"""
        if self.model is None:
            logger.info(f"[LAMBDA GPU] Loading embedding model on {self.device}...")
            
            # Use faster, smaller model for Lambda Labs
            model_name = "all-MiniLM-L6-v2"  # Fast and efficient
            
            self.model = SentenceTransformer(model_name, device=self.device)
            
            # Optimize for GPU
            if self.device == "cuda":
                self.model = self.model.half()  # Use FP16 for memory efficiency
                torch.cuda.empty_cache()
            
            logger.info(f"[LAMBDA GPU] Model loaded on {self.device}")
        return self.model
    
    def get_document_hash(self, content: str) -> str:
        """Generate hash for document content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_query_embedding(self, content: str) -> np.ndarray:
        """Get embedding for query content with GPU acceleration"""
        doc_hash = self.get_document_hash(content)
        
        if doc_hash in self.embeddings_cache:
            return self.embeddings_cache[doc_hash]
        
        model = self.get_embedding_model()
        
        # GPU-optimized embedding generation
        with torch.cuda.amp.autocast() if self.device == "cuda" else torch.no_grad():
            embedding = model.encode([content], convert_to_tensor=True, show_progress_bar=False)
            if self.device == "cuda":
                embedding = embedding.cpu().numpy()[0]
            else:
                embedding = embedding.numpy()[0]
        
        self.embeddings_cache[doc_hash] = embedding
        return embedding
    
    def get_document_embedding(self, doc_id: str, content: str) -> np.ndarray:
        """Get embedding for document content with GPU acceleration"""
        if doc_id in self.document_embeddings:
            return self.document_embeddings[doc_id]
        
        model = self.get_embedding_model()
        
        # GPU-optimized embedding generation
        with torch.cuda.amp.autocast() if self.device == "cuda" else torch.no_grad():
            embedding = model.encode([content], convert_to_tensor=True, show_progress_bar=False)
            if self.device == "cuda":
                embedding = embedding.cpu().numpy()[0]
            else:
                embedding = embedding.numpy()[0]
            
        self.document_embeddings[doc_id] = embedding
        return embedding
            
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def batch_embed_documents(self, documents: List[Tuple[str, str]]) -> Dict[str, np.ndarray]:
        """Batch embed documents for efficiency"""
        model = self.get_embedding_model()
        embeddings = {}
        
        # Process in batches for GPU efficiency
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i + self.batch_size]
            doc_ids, contents = zip(*batch)
            
            with torch.cuda.amp.autocast() if self.device == "cuda" else torch.no_grad():
                batch_embeddings = model.encode(
                    contents, 
                    convert_to_tensor=True, 
                    show_progress_bar=False,
                    batch_size=self.batch_size
                )
                
                if self.device == "cuda":
                    batch_embeddings = batch_embeddings.cpu().numpy()
                else:
                    batch_embeddings = batch_embeddings.numpy()
            
            for j, doc_id in enumerate(doc_ids):
                embeddings[doc_id] = batch_embeddings[j]
            
        return embeddings
            
class LambdaGPUChromaService:
    """GPU-optimized ChromaDB service for Lambda Labs"""
    
    def __init__(self):
        self.client = None
        self.collections_cache = []
        self.last_cache_update = 0
        self.cache_ttl = 300  # 5 minutes
        
    def get_client(self):
        """Get or create ChromaDB client with multiple authentication methods"""
        if self.client is None:
            try:
                # Try cloud ChromaDB first
                use_cloud = os.getenv('USE_CLOUD_CHROMA', 'false').lower() == 'true'
                
                if use_cloud:
                    chroma_api_key = os.getenv('CHROMADB_API_KEY')
                    chroma_tenant = os.getenv('CHROMADB_TENANT')
                    chroma_database = os.getenv('CHROMADB_DATABASE')
                    
                    if chroma_api_key and chroma_tenant and chroma_database:
                        logger.info(f"[LAMBDA GPU] Connecting to ChromaDB Cloud...")
                        self.client = chromadb.HttpClient(
                            host="https://api.trychroma.com",
                            settings=Settings(
                                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                                chroma_client_auth_credentials=chroma_api_key,
                                chroma_client_auth_token_transport_header="X-Chroma-Token"
                            )
                        )
                        logger.info(f"[LAMBDA GPU] Connected to ChromaDB Cloud")
                    else:
                        raise ValueError("ChromaDB Cloud credentials not found")
                else:
                    # Local ChromaDB
                    chroma_host = os.getenv('CHROMADB_HOST', 'localhost')
                    chroma_port = int(os.getenv('CHROMADB_PORT', '8000'))
                    chroma_api_key = os.getenv('CHROMADB_API_KEY')
                    
                    if chroma_api_key:
                        self.client = chromadb.HttpClient(
                            host=chroma_host,
                            port=chroma_port,
                            settings=Settings(
                                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                                chroma_client_auth_credentials=chroma_api_key
                            )
                        )
                    else:
                        self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
                        logger.info(f"[LAMBDA GPU] ChromaDB connected to {chroma_host}:{chroma_port}")
                        
            except Exception as e:
                logger.error(f"[LAMBDA GPU] ChromaDB connection failed: {e}")
                # Fallback to local client
                try:
                    self.client = chromadb.HttpClient(host="localhost", port=8000)
                    logger.info(f"[LAMBDA GPU] Fallback to local ChromaDB")
                except Exception as fallback_e:
                    logger.error(f"[LAMBDA GPU] Fallback connection also failed: {fallback_e}")
                    raise
                    
        return self.client
    
    def get_batch_collections(self, force_refresh: bool = False) -> List[str]:
        """Get batch collections with caching and fallback"""
        current_time = time.time()
        
        if not force_refresh and self.collections_cache and (current_time - self.last_cache_update) < self.cache_ttl:
            return self.collections_cache
        
        try:
            client = self.get_client()
            all_collections = []
            offset = 0
            limit = 1000
            
            # Get all collections with pagination
            while True:
                try:
                    collections_batch = client.list_collections(limit=limit, offset=offset)
                    if not collections_batch or len(collections_batch) == 0:
                        break
                    all_collections.extend(collections_batch)
                    if len(collections_batch) < limit:
                        break
                    offset += limit
                except Exception as e:
                    logger.warning(f"[LAMBDA GPU] Error fetching collections batch: {e}")
                    break
            
            # Filter for batch collections
            batch_collections = [
                col.name for col in all_collections
                if 'batch' in col.name.lower() or 'ultra_optimized' in col.name.lower()
            ]
            
            self.collections_cache = batch_collections
            self.last_cache_update = current_time
            
            logger.info(f"[LAMBDA GPU] Found {len(batch_collections)} batch collections")
            return batch_collections
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error getting collections: {e}")
            # Fallback: Generate collection names based on known pattern
            logger.warning("[LAMBDA GPU] Using fallback collection names due to error")
            fallback_collections = []
            for i in range(1, 1001):  # Generate 1000 collection names
                fallback_collections.append(f"documents_ultra_optimized_batch_{i}")
            
            # Update cache
            self.collections_cache = fallback_collections
            self.last_cache_update = current_time
            logger.info(f"[LAMBDA GPU] Using fallback: {len(fallback_collections)} collections")
            return fallback_collections
    
    def search_documents_parallel(self, query_embedding: np.ndarray, n_results: int = 10) -> List[Dict[str, Any]]:
        """Parallel search across collections for maximum speed"""
        try:
            collections = self.get_batch_collections()
            if not collections:
                return []
            
            # Limit collections for performance (optimized for Lambda Labs)
            max_collections = int(os.getenv('MAX_COLLECTIONS', '150'))
            collections_to_search = collections[:max_collections]
            
            logger.info(f"[LAMBDA GPU] Searching {len(collections_to_search)} collections in parallel")
            
            all_documents = []
            
            # Use ThreadPoolExecutor for parallel search
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = []
                
                for collection_name in collections_to_search:
                    future = executor.submit(self._search_single_collection, collection_name, query_embedding, n_results * 2)
                    futures.append(future)
                
                # Collect results
                for future in futures:
                    try:
                        results = future.result(timeout=5)  # 5 second timeout per collection
                        if results:
                            all_documents.extend(results)
                    except Exception as e:
                        logger.warning(f"[LAMBDA GPU] Collection search timeout/error: {e}")
                        continue
            
            logger.info(f"[LAMBDA GPU] Found {len(all_documents)} total documents")
            return all_documents[:n_results]
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error in parallel search: {e}")
            return []
            
    def _search_single_collection(self, collection_name: str, query_embedding: np.ndarray, n_results: int) -> List[Dict[str, Any]]:
        """Search a single collection"""
        try:
            client = self.get_client()
            collection = client.get_collection(collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
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
            logger.warning(f"[LAMBDA GPU] Error searching collection {collection_name}: {e}")
            return []
    
class LambdaGPUUniversityRAGChatbot:
    """Ultra-optimized GPU RAG Chatbot for Lambda Labs"""
    
    def __init__(self):
        """Initialize the GPU-optimized chatbot"""
        logger.info("[LAMBDA GPU] Initializing Northeastern Chatbot...")
        
        # Initialize components
        self.embedding_manager = LambdaGPUEmbeddingManager()
        self.chroma_service = LambdaGPUChromaService()
        
        # Initialize OpenAI components
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI LLM with optimized settings
        self.llm = ChatOpenAI(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.3')),
            max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '2500')),
            openai_api_key=self.openai_api_key,
            request_timeout=20,  # Reduced timeout for faster responses
            streaming=False
        )
        
        # Initialize OpenAI embeddings for fallback
        self.openai_embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        logger.info("[LAMBDA GPU] Chatbot initialized successfully")
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information for monitoring"""
        gpu_info = {
            'cuda_available': torch.cuda.is_available(),
            'device': self.embedding_manager.device,
            'batch_size': self.embedding_manager.batch_size
        }
        
        if torch.cuda.is_available():
            gpu_info.update({
                'gpu_name': torch.cuda.get_device_name(0),
                'gpu_memory_total': torch.cuda.get_device_properties(0).total_memory / 1024**3,
                'gpu_memory_allocated': torch.cuda.memory_allocated(0) / 1024**3,
                'gpu_memory_cached': torch.cuda.memory_reserved(0) / 1024**3,
                'cuda_version': torch.version.cuda
            })
        
        return gpu_info
    
    def search_documents(self, query: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """Ultra-fast document search with GPU acceleration and quality filtering"""
        try:
            start_time = time.time()
            
            # Generate query embedding with GPU acceleration
            query_embedding = self.embedding_manager.get_query_embedding(query)
            embedding_time = time.time() - start_time
            
            # Parallel search across collections
            search_start = time.time()
            documents = self.chroma_service.search_documents_parallel(query_embedding, n_results * 2)  # Get more for filtering
            search_time = time.time() - search_start
            
            # Quality filtering and relevance scoring
            filtered_docs = self._filter_and_rank_documents(documents, query, n_results)
            
            total_time = time.time() - start_time
            
            logger.info(f"[LAMBDA GPU] Search completed in {total_time:.2f}s (embedding: {embedding_time:.2f}s, search: {search_time:.2f}s)")
            logger.info(f"[LAMBDA GPU] Found {len(documents)} documents, filtered to {len(filtered_docs)} high-quality results")
            
            return filtered_docs
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error in document search: {e}")
            return []
    
    def _filter_and_rank_documents(self, documents: List[Dict[str, Any]], query: str, n_results: int) -> List[Dict[str, Any]]:
        """Filter and rank documents by relevance and quality"""
        try:
            if not documents:
                return []
    
            # Extract query terms for relevance scoring
            query_terms = set(query.lower().split())
            
            # Score and filter documents
            scored_docs = []
            for doc in documents:
                # Calculate relevance score
                relevance_score = self._calculate_relevance_score(doc, query_terms)
                
                # Only include documents with reasonable relevance
                if relevance_score > 0.1:  # Minimum relevance threshold
                    doc['relevance_score'] = relevance_score
                    scored_docs.append(doc)
            
            # Sort by relevance score (higher is better)
            scored_docs.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Return top N results
            return scored_docs[:n_results]
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error filtering documents: {e}")
            return documents[:n_results]  # Fallback to original results
    
    def _calculate_relevance_score(self, doc: Dict[str, Any], query_terms: set) -> float:
        """Calculate relevance score for a document"""
        try:
            content = doc.get('content', '').lower()
            metadata = doc.get('metadata', {})
            
            # Base similarity from embedding
            similarity = doc.get('similarity', 0)
            
            # Boost score for title matches
            title = metadata.get('title', '').lower()
            title_matches = sum(1 for term in query_terms if term in title)
            title_boost = title_matches / len(query_terms) if query_terms else 0
            
            # Boost score for content matches
            content_matches = sum(1 for term in query_terms if term in content)
            content_boost = content_matches / len(query_terms) if query_terms else 0
            
            # Combine scores
            relevance_score = similarity + (title_boost * 0.3) + (content_boost * 0.2)
            
            return min(relevance_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error calculating relevance: {e}")
            return doc.get('similarity', 0)
    
    def generate_answer(self, question: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate answer using optimized LLM"""
        try:
            if not context_docs:
                return {
                    'answer': "I don't have enough information to answer this question about Northeastern University.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build optimized context with better metadata extraction
            context_parts = []
            sources = []
            
            for i, doc in enumerate(context_docs[:5], 1):
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                
                # Extract meaningful title from metadata
                title = metadata.get('title', metadata.get('source', metadata.get('file_name', 'Northeastern University Document')))
                if title == 'Unknown' or not title:
                    title = f"Northeastern University Document {i}"
                
                # Extract URL if available
                url = metadata.get('url', metadata.get('source_url', ''))
                
                # Truncate content for efficiency
                if len(content) > 1000:
                    content = content[:1000] + "..."
                
                context_parts.append(f"[Source {i}] {title}\n{content}\n")
                
                # Prepare source information
                sources.append({
                    'title': title,
                    'similarity': round(doc.get('similarity', 0), 3),
                    'url': url,
                    'content_preview': content[:200] + "..." if len(content) > 200 else content,
                    'rank': i
                })
            
            context = "\n".join(context_parts)
            
            # Enhanced prompt for better responses
            prompt_template = """You are a knowledgeable assistant for Northeastern University. Answer the question based on the provided context from official Northeastern University documents.

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
- If you cannot find relevant information in the context, say so clearly

Answer:"""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Generate answer with optimized settings
            formatted_prompt = prompt.format(context=context, question=question)
            response = self.llm.invoke(formatted_prompt)
            answer = response.content
            
            # Determine confidence based on similarity scores
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
            logger.error(f"[LAMBDA GPU] Error generating answer: {e}")
            return {
                'answer': f"I encountered an error generating the answer: {str(e)}",
                'sources': [],
                'confidence': 'low'
            }
    
    def chat(self, question: str) -> ChatResponse:
        """Main chat function with comprehensive timing"""
        start_time = time.time()
        
        logger.info(f"[LAMBDA GPU] Processing question: {question[:100]}...")
        
        # Search for relevant documents
        search_start = time.time()
        documents = self.search_documents(question, n_results=10)
        search_time = time.time() - search_start
        
        # Generate answer
        generation_start = time.time()
        result = self.generate_answer(question, documents)
        generation_time = time.time() - generation_start
        
        total_time = time.time() - start_time
            
        logger.info(f"[LAMBDA GPU] Total response time: {total_time:.2f}s (search: {search_time:.2f}s, generation: {generation_time:.2f}s)")
        
        # Add timing information
        timing = {
            'search': round(search_time, 2),
            'generation': round(generation_time, 2),
            'total': round(total_time, 2)
        }
        
        # Get GPU info
        gpu_info = self.get_gpu_info()
        
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources'],
            confidence=result['confidence'],
            timing=timing,
            gpu_info=gpu_info
        )
    
    def clear_cache(self):
        """Clear GPU cache and embeddings cache"""
        try:
            # Clear GPU cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Clear embeddings cache
            self.embedding_manager.embeddings_cache = {}
            self.embedding_manager.document_embeddings = {}
            
            logger.info("[LAMBDA GPU] Cache cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"[LAMBDA GPU] Error clearing cache: {e}")
            return False

# Global chatbot instance for Lambda Labs
chatbot_instance = None

def get_chatbot() -> LambdaGPUUniversityRAGChatbot:
    """Get or create chatbot instance"""
    global chatbot_instance
    
    if chatbot_instance is None:
        logger.info("[LAMBDA GPU] Creating new chatbot instance...")
        chatbot_instance = LambdaGPUUniversityRAGChatbot()
    
    return chatbot_instance

def clear_gpu_cache():
    """Clear GPU cache for memory management"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("[LAMBDA GPU] GPU cache cleared")

if __name__ == "__main__":
    # Test the chatbot
    logger.info("[LAMBDA GPU] Testing chatbot...")
    
    try:
        chatbot = get_chatbot()
        
        # Test question
        test_question = "What programs does Northeastern University offer?"
        response = chatbot.chat(test_question)
        
        print(f"\nQuestion: {test_question}")
        print(f"Answer: {response.answer}")
        print(f"Confidence: {response.confidence}")
        print(f"Timing: {response.timing}")
        print(f"GPU Info: {response.gpu_info}")
        
    except Exception as e:
        logger.error(f"[LAMBDA GPU] Test failed: {e}")
