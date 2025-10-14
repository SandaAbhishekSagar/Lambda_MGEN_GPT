import os
import time
import hashlib
import pickle
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import chromadb
from chromadb.config import Settings

from services.shared.chroma_service import ChromaService
from services.shared.config import config


class LambdaGPUEmbeddingManager:
    """GPU-optimized embedding manager for Lambda Labs deployment"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "auto"):
        print("[LAMBDA GPU] Initializing Lambda GPU Embedding Manager...")
        start_time = time.time()
        
        # Auto-detect GPU availability
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"[LAMBDA GPU] Using device: {self.device}")
        
        # GPU-specific optimizations
        if self.device == "cuda":
            print(f"[LAMBDA GPU] CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"[LAMBDA GPU] CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Optimize for GPU memory
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
        
        # Initialize embedding model with GPU optimization
        self.model_name = model_name
        self.model = self._load_embedding_model()
        
        # Cache setup
        self.cache_dir = Path("lambda_embeddings_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.embedding_cache = self._load_cache()
        
        init_time = time.time() - start_time
        print(f"[LAMBDA GPU] Embedding manager initialized in {init_time:.2f} seconds")
        print(f"[LAMBDA GPU] Model: {self.model_name}")
        print(f"[LAMBDA GPU] Device: {self.device}")
        print(f"[LAMBDA GPU] Cache size: {len(self.embedding_cache)} embeddings")
    
    def _load_embedding_model(self):
        """Load embedding model with GPU optimizations"""
        try:
            print(f"[LAMBDA GPU] Loading embedding model: {self.model_name}")
            
            # Load model with GPU optimizations
            model = SentenceTransformer(self.model_name, device=self.device)
            
            # GPU-specific optimizations
            if self.device == "cuda":
                model = model.half()  # Use FP16 for memory efficiency
                print(f"[LAMBDA GPU] Model converted to FP16 for GPU efficiency")
            
            print(f"[LAMBDA GPU] Embedding model loaded successfully")
            return model
            
        except Exception as e:
            print(f"[LAMBDA GPU] Error loading embedding model: {e}")
            raise
    
    def _load_cache(self):
        """Load embedding cache with GPU optimizations"""
        cache_file = self.cache_dir / f"lambda_gpu_embeddings_cache.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cache = pickle.load(f)
                print(f"[LAMBDA GPU] Loaded {len(cache)} embeddings from cache")
                return cache
            except Exception as e:
                print(f"[LAMBDA GPU] Error loading cache: {e}")
                return {}
        else:
            print(f"[LAMBDA GPU] No cache found, starting fresh")
            return {}
    
    def _save_cache(self):
        """Save embedding cache"""
        cache_file = self.cache_dir / f"lambda_gpu_embeddings_cache.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(self.embedding_cache, f)
            print(f"[LAMBDA GPU] Saved {len(self.embedding_cache)} embeddings to cache")
        except Exception as e:
            print(f"[LAMBDA GPU] Error saving cache: {e}")
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for query with GPU acceleration"""
        try:
            # Check cache first
            query_hash = hashlib.md5(query.encode()).hexdigest()
            if query_hash in self.embedding_cache:
                return self.embedding_cache[query_hash]
            
            # Generate embedding with GPU
            if self.device == "cuda":
                with torch.cuda.amp.autocast():  # Use mixed precision
                    embedding = self.model.encode([query], convert_to_tensor=True)
                    embedding = embedding.cpu().numpy()[0].tolist()
            else:
                embedding = self.model.encode([query])[0].tolist()
            
            # Cache result
            self.embedding_cache[query_hash] = embedding
            
            return embedding
            
        except Exception as e:
            print(f"[LAMBDA GPU] Error getting query embedding: {e}")
            raise
    
    def get_document_embeddings(self, documents: List[str]) -> List[List[float]]:
        """Get embeddings for multiple documents with GPU batching"""
        try:
            embeddings = []
            uncached_docs = []
            uncached_indices = []
            
            # Check cache for each document
            for i, doc in enumerate(documents):
                doc_hash = hashlib.md5(doc.encode()).hexdigest()
                if doc_hash in self.embedding_cache:
                    embeddings.append(self.embedding_cache[doc_hash])
                else:
                    embeddings.append(None)
                    uncached_docs.append(doc)
                    uncached_indices.append(i)
            
            # Generate embeddings for uncached documents
            if uncached_docs:
                print(f"[LAMBDA GPU] Generating {len(uncached_docs)} new embeddings on GPU")
                
                if self.device == "cuda":
                    # Batch process with mixed precision
                    with torch.cuda.amp.autocast():
                        batch_embeddings = self.model.encode(
                            uncached_docs, 
                            convert_to_tensor=True,
                            batch_size=32,  # Optimize batch size for GPU
                            show_progress_bar=True
                        )
                        batch_embeddings = batch_embeddings.cpu().numpy()
                else:
                    batch_embeddings = self.model.encode(
                        uncached_docs,
                        batch_size=16,
                        show_progress_bar=True
                    )
                
                # Update embeddings list and cache
                for i, embedding in enumerate(batch_embeddings):
                    doc_index = uncached_indices[i]
                    doc_hash = hashlib.md5(documents[doc_index].encode()).hexdigest()
                    
                    embedding_list = embedding.tolist()
                    embeddings[doc_index] = embedding_list
                    self.embedding_cache[doc_hash] = embedding_list
            
            # Save cache periodically
            if len(uncached_docs) > 0:
                self._save_cache()
            
            return embeddings
            
        except Exception as e:
            print(f"[LAMBDA GPU] Error getting document embeddings: {e}")
            raise
    
    def get_document_hash(self, content: str) -> str:
        """Get hash for document content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity"""
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except Exception as e:
            print(f"[LAMBDA GPU] Error calculating cosine similarity: {e}")
            return 0.0


class LambdaGPUUniversityRAGChatbot:
    """Lambda GPU-optimized RAG Chatbot for maximum performance"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", openai_api_key: Optional[str] = None):
        print("[LAMBDA GPU] Initializing Lambda GPU RAG Chatbot...")
        start_time = time.time()
        
        # Initialize ChromaDB service
        self.chroma_service = ChromaService()
        
        # Initialize GPU-optimized embedding manager
        self.embedding_manager = LambdaGPUEmbeddingManager()
        
        # Get API key from parameter or config
        api_key = openai_api_key or config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in config or pass as parameter.")
        
        # Initialize OpenAI LLM with GPU-optimized settings
        print(f"[LAMBDA GPU] Loading OpenAI {model_name}...")
        
        # Handle o4-mini model restrictions (requires temperature=1)
        if "o4-mini" in model_name.lower() or "o1" in model_name.lower():
            print(f"[LAMBDA GPU] Using o4-mini/o1 model - temperature fixed at 1.0")
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=1.0,          # Required for o4-mini models
                max_tokens=3000,          # Increased for detailed responses
                openai_api_key=api_key,
                request_timeout=60,       # Longer timeout for reasoning models
                max_retries=3
            )
        else:
            # Standard models with optimized settings
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.3,          # Balanced for detailed but accurate responses
                max_tokens=3000,          # Increased for detailed responses
                openai_api_key=api_key,
                request_timeout=45,
                max_retries=3
            )
        
        self.model_name = model_name
        
        # Enhanced prompt templates optimized for GPU deployment
        self.query_expansion_prompt = PromptTemplate(
            input_variables=["question", "conversation_history"],
            template="""Generate 3 different ways to ask the same specific question to improve search results. Focus on the exact topic being asked.

Question: {question}
Conversation History: {conversation_history}

Generate 3 alternative questions that ask about the SAME specific topic (one per line):
1. """
        )
        
        self.answer_prompt = PromptTemplate(
            input_variables=["context", "question", "conversation_history"],
            template="""You are an expert Northeastern University assistant running on Lambda GPU infrastructure. Provide a DETAILED, COMPREHENSIVE, and WELL-STRUCTURED answer to the student's question using the provided context.

CRITICAL INSTRUCTIONS:
- Answer ONLY the specific question asked
- Use EXACT information from the provided context
- Provide DETAILED and COMPREHENSIVE answers - don't be brief
- Structure your response clearly with:
  * An overview/introduction
  * Main points organized with bullet points or numbered lists when appropriate
  * Specific details, numbers, dates, requirements, or procedures
  * Additional relevant information that helps fully answer the question
- Quote specific details from the context (costs, dates, requirements, procedures, etc.)
- If the context contains multiple relevant pieces of information, include ALL of them
- Use clear formatting: paragraphs, bullet points, or numbered lists for readability
- Be thorough but stay focused on the specific question
- If the context doesn't contain specific information, provide helpful general guidance about Northeastern University
- Do NOT provide generic information not found in the context
- Be conversational, helpful, and professional

Previous conversation:
{conversation_history}

Relevant context from university documents:
{context}

Question: {question}

Provide a detailed, well-structured answer:"""
        )
        
        # Initialize utility methods for enhanced processing
        self.generic_phrases = [
            'northeastern university offers a variety',
            'northeastern university provides',
            'as an expert assistant',
            'based on the context',
            'i can provide you with information',
            'northeastern university is',
            'the university offers',
            'northeastern provides'
        ]
        
        init_time = time.time() - start_time
        print(f"[LAMBDA GPU] Initialization completed in {init_time:.2f} seconds")
        print(f"[LAMBDA GPU] Model: {self.model_name}")
        print(f"[LAMBDA GPU] Embedding Device: {self.embedding_manager.device}")
        print(f"[LAMBDA GPU] Documents to analyze: 10")
    
    def expand_query(self, query: str, conversation_history: Optional[List[Dict]] = None) -> List[str]:
        """Expand query for better search results with GPU optimization"""
        try:
            if not conversation_history:
                conversation_history = []
            
            history_text = "\n".join([f"Q: {conv['question']}\nA: {conv['answer']}" 
                                    for conv in conversation_history[-3:]])
            
            prompt = self.query_expansion_prompt.format(
                question=query,
                conversation_history=history_text
            )
            
            # Use GPU-optimized LLM call
            response = self.llm.invoke(prompt)
            expanded_text = response.content if hasattr(response, 'content') else str(response)
            
            # Parse expanded queries
            queries = [query]  # Always include original
            for line in expanded_text.split('\n'):
                line = line.strip()
                if line and (line.startswith(('1.', '2.', '3.')) or 
                           (line and not line.startswith('Generate'))):
                    # Clean up the query
                    clean_query = line.lstrip('123456789. ').strip()
                    if clean_query and len(clean_query) > 10:
                        queries.append(clean_query)
            
            # Limit to 4 queries total (original + 3 expanded)
            queries = queries[:4]
            print(f"[LAMBDA GPU] Generated {len(queries)-1} query variations")
            return queries
            
        except Exception as e:
            print(f"[LAMBDA GPU] Query expansion error: {e}")
            return [query]
    
    def validate_and_improve_answer(self, question: str, answer: str, context: str) -> str:
        """Validate answer and regenerate if needed"""
        
        answer_lower = answer.lower()
        
        # Check for generic indicators
        is_generic = any(phrase in answer_lower for phrase in self.generic_phrases)
        
        # Check if answer directly addresses the question
        question_terms = self.extract_key_terms(question)
        answer_contains_question_terms = any(term in answer_lower for term in question_terms)
        
        # If answer is generic or off-topic, regenerate
        if is_generic or not answer_contains_question_terms:
            print(f"[LAMBDA GPU] Regenerating answer - detected generic response")
            specific_prompt = f"""Answer this specific question: "{question}"
Use information from this context: {context}

CRITICAL INSTRUCTIONS:
- Provide a DETAILED, COMPREHENSIVE answer about Northeastern University programs
- Use information from the provided context, but also draw reasonable conclusions
- Structure your response clearly with bullet points or organized paragraphs
- Include ALL relevant details: specific numbers, dates, requirements, procedures
- Be thorough and well-organized, not brief
- If you find relevant information about programs, degrees, or academic offerings, include it
- Focus on being helpful and informative about Northeastern's academic programs
- Use the context as your primary source but provide a complete answer

Provide a detailed, well-structured answer about Northeastern University programs:"""
            response = self.llm.invoke(specific_prompt)
            return response.content if hasattr(response, 'content') else str(response)
        
        return answer
    
    def hybrid_search(self, query: str, k: int = 10, university_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Enhanced hybrid search with GPU acceleration"""
        try:
            start_time = time.time()
            
            # Get conversation history for context
            conversation_history = self.get_conversation_history("current_session", limit=3)
            
            # Expand query (with timeout protection)
            try:
                expanded_queries = self.expand_query(query, conversation_history)
                print(f"[LAMBDA GPU] Generated {len(expanded_queries)} query variations")
            except Exception as e:
                print(f"[LAMBDA GPU] Query expansion failed, using original query: {e}")
                expanded_queries = [query]
            
            # Perform semantic search for each expanded query
            all_semantic_results = []
            for expanded_query in expanded_queries:
                semantic_results = self.semantic_search(expanded_query, k=k, university_id=university_id)
                all_semantic_results.extend(semantic_results)
            
            # Remove duplicates and rerank
            unique_results = self.remove_duplicates(all_semantic_results)
            
            # Rerank based on relevance to original query
            reranked_results = self.rerank_results(unique_results, query, k=k)
            
            search_time = time.time() - start_time
            print(f"[LAMBDA GPU] Hybrid search completed in {search_time:.2f} seconds")
            print(f"[LAMBDA GPU] Found {len(reranked_results)} unique documents")
            
            return reranked_results
            
        except Exception as e:
            print(f"[LAMBDA GPU] Hybrid search error: {e}")
            return self.semantic_search(query, k=k, university_id=university_id)
    
    def semantic_search(self, query: str, k: int = 10, university_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """GPU-accelerated semantic search"""
        try:
            # Get query embedding with GPU acceleration
            query_embedding = self.embedding_manager.get_query_embedding(query)
            
            # Search ChromaDB
            results = self.chroma_service.search_documents(
                query="",  # Empty query since we're using embedding
                embedding=query_embedding,
                n_results=k * 2  # Get more results for reranking
            )
            
            # Process results
            processed_results = []
            for i, (doc_version, distance) in enumerate(results):
                # Convert distance to similarity
                similarity = 1 - (distance / 2)
                
                processed_results.append({
                    'id': doc_version.id,
                    'content': doc_version.content,
                    'title': doc_version.title,
                    'url': doc_version.url,
                    'similarity': similarity,
                    'distance': distance
                })
            
            return processed_results
            
        except Exception as e:
            print(f"[LAMBDA GPU] Semantic search error: {e}")
            return []
    
    def remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate documents based on document ID"""
        unique_results = []
        seen_ids = set()
        
        for result in results:
            # Use document ID for deduplication (more reliable than content hashing)
            doc_id = result.get('id', '')
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                unique_results.append(result)
            elif not doc_id:
                # If no ID, keep it anyway (shouldn't happen but be safe)
                unique_results.append(result)
        
        print(f"[LAMBDA GPU] Deduplicated {len(results)} results to {len(unique_results)} unique documents")
        return unique_results
    
    def question_specific_rerank(self, results: List[Dict], question: str) -> List[Dict]:
        """Rerank based on how well each document answers the specific question"""
        
        question_terms = self.extract_key_terms(question)
        
        for result in results:
            # Calculate how well this document answers the specific question
            content = result['content'].lower()
            term_matches = sum(1 for term in question_terms if term in content)
            question_relevance = term_matches / len(question_terms) if question_terms else 0.0
            
            # Combine with similarity score
            result['final_score'] = (result['similarity'] * 0.6) + (question_relevance * 0.4)
        
        # Sort by final score
        results.sort(key=lambda x: x['final_score'], reverse=True)
        return results
    
    def rerank_results(self, results: List[Dict], original_query: str, k: int = 10) -> List[Dict]:
        """Rerank results based on relevance to original query"""
        try:
            # Use question-specific reranking for better results
            reranked_results = self.question_specific_rerank(results, original_query)
            return reranked_results[:k]
            
        except Exception as e:
            print(f"[LAMBDA GPU] Reranking error: {e}")
            return results[:k]
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        # Simple key term extraction
        words = text.lower().split()
        # Filter out common words and keep meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'about', 'how', 'what', 'when', 'where', 'why', 'who'}
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return key_terms
    
    def calculate_confidence(self, relevant_docs: List[Dict], question: str, answer: str) -> float:
        """Calculate confidence score based on multiple factors"""
        try:
            if not relevant_docs:
                return 0.0
            
            # Factor 1: Document relevance scores
            avg_similarity = sum(doc.get('similarity', 0) for doc in relevant_docs) / len(relevant_docs)
            
            # Factor 2: Number of relevant documents
            doc_count_score = min(len(relevant_docs) / 10, 1.0)  # Normalize to 0-1
            
            # Factor 3: Answer length (more detailed = higher confidence)
            answer_length_score = min(len(answer) / 500, 1.0)  # Normalize to 0-1
            
            # Factor 4: Question-answer alignment
            question_terms = self.extract_key_terms(question)
            answer_lower = answer.lower()
            term_coverage = sum(1 for term in question_terms if term in answer_lower) / max(len(question_terms), 1)
            
            # Combine factors
            confidence = (avg_similarity * 0.4 + 
                         doc_count_score * 0.2 + 
                         answer_length_score * 0.2 + 
                         term_coverage * 0.2)
            
            return min(confidence, 1.0)  # Cap at 1.0
            
        except Exception as e:
            print(f"[LAMBDA GPU] Confidence calculation error: {e}")
            return 0.5  # Default moderate confidence
    
    def generate_lambda_gpu_response(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate response using Lambda GPU-optimized pipeline"""
        try:
            start_time = time.time()
            
            # Step 1: Hybrid search with GPU acceleration
            search_start = time.time()
            relevant_docs = self.hybrid_search(question, k=10)
            search_time = time.time() - search_start
            
            # Step 2: Prepare context
            context_start = time.time()
            if not relevant_docs:
                return {
                    'answer': "I don't have enough specific information about this topic in my knowledge base.",
                    'sources': [],
                    'confidence': 0.0,
                    'response_time': time.time() - start_time,
                    'search_time': search_time,
                    'context_time': 0,
                    'llm_time': 0,
                    'documents_analyzed': 0,
                    'model': self.model_name,
                    'device': self.embedding_manager.device,
                    'query_expansions': False
                }
            
            # Build context from documents
            context = "\n\n".join([
                f"Document {i+1}: {doc['title']}\nURL: {doc['url']}\nContent: {doc['content'][:1000]}..."
                for i, doc in enumerate(relevant_docs)
            ])
            
            # Prepare sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    'title': doc['title'],
                    'url': doc['url'],
                    'relevance': f"{doc.get('similarity', 0) * 100:.1f}%"
                })
            
            context_time = time.time() - context_start
            
            # Step 3: Generate comprehensive answer
            llm_start = time.time()
            
            # Get conversation history for context
            conversation_history = self.get_conversation_history(session_id or "current_session", limit=3)
            history_text = "\n".join([f"Q: {conv['question']}\nA: {conv['answer']}" 
                                    for conv in conversation_history])
            
            prompt = self.answer_prompt.format(
                context=context,
                question=question,
                conversation_history=history_text
            )
            
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            llm_time = time.time() - llm_start
            
            # Step 4: Validate and improve answer if needed
            answer = answer.strip()
            answer = self.validate_and_improve_answer(question, answer, context)
            
            # Step 5: Calculate confidence
            confidence = self.calculate_confidence(relevant_docs, question, answer)
            
            # Step 6: Store conversation
            if session_id:
                self.store_conversation(session_id, question, answer, sources)
            
            total_time = time.time() - start_time
            
            print(f"[LAMBDA GPU] Response generated in {total_time:.2f}s (search: {search_time:.2f}s, context: {context_time:.2f}s, LLM: {llm_time:.2f}s)")
            print(f"[LAMBDA GPU] Documents analyzed: {len(relevant_docs)}")
            print(f"[LAMBDA GPU] Confidence: {confidence:.2f}")
            
            return {
                'answer': answer.strip(),
                'sources': sources,
                'confidence': confidence,
                'response_time': total_time,
                'search_time': search_time,
                'context_time': context_time,
                'llm_time': llm_time,
                'documents_analyzed': len(relevant_docs),
                'model': self.model_name,
                'device': self.embedding_manager.device,
                'query_expansions': True
            }
            
        except Exception as e:
            print(f"[LAMBDA GPU] Error generating response: {e}")
            return {
                'answer': f"I'm sorry, I encountered an error while processing your question. Please try again.",
                'sources': [],
                'confidence': 0.0,
                'response_time': time.time() - start_time,
                'search_time': 0,
                'context_time': 0,
                'llm_time': 0,
                'documents_analyzed': 0,
                'model': self.model_name,
                'device': self.embedding_manager.device,
                'query_expansions': False,
                'error': str(e)
            }
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for session"""
        # Simplified conversation history storage
        # In production, you'd use Redis or a database
        return []
    
    def store_conversation(self, session_id: str, question: str, answer: str, sources: List[Dict]):
        """Store conversation for session"""
        # Simplified conversation storage
        # In production, you'd use Redis or a database
        pass
