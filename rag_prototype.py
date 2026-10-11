"""
RAG Prototype for MBA FAQ Chatbot Project
Replaces keyword matching with real vector search (ChromaDB + embeddings)
Demonstrates weeks 3-4 deliverable: RAG prototype with off-the-shelf LLM
"""

import os
import numpy as np
from typing import List, Dict, Any

# For the prototype, we'll use sentence-transformers for embeddings
# In production, you could use Ollama, vLLM, or another LLM for generation
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Warning: Install sentence-transformers and chromadb for full RAG:")
    print("pip install sentence-transformers chromadb")

# ============================================================
# BUSINESS FAQ DATA (same as before, now stored in vector DB)
# ============================================================
BUSINESS_FAQ_DATA = [
    {
        "id": "returns_001",
        "question": "What is your return policy?",
        "answer": "We accept returns within 30 days of delivery. Items must be in original packaging with tags. Refunds process in 5-7 business days to original payment method.",
        "topic": "returns"
    },
    {
        "id": "returns_002",
        "question": "Can I exchange an item for a different size?",
        "answer": "Exchanges are free within 30 days. Just return the original item and we'll ship the replacement at no extra cost.",
        "topic": "exchanges"
    },
    {
        "id": "shipping_001",
        "question": "How long does shipping take?",
        "answer": "Standard shipping: 3-5 business days ($5.99). Express: 1-2 days ($12.99). Free standard on orders over $50. International: 7-14 days, rates vary.",
        "topic": "shipping"
    },
    {
        "id": "shipping_002",
        "question": "Do you offer international shipping?",
        "answer": "Yes, we ship to 50+ countries. Duties/taxes may apply - calculated at checkout. Delivery: 7-21 business days.",
        "topic": "shipping"
    },
    {
        "id": "warranty_001",
        "question": "What is your warranty policy?",
        "answer": "All products come with a 1-year manufacturer warranty. Covers defects in materials and workmanship. Extended warranties available at checkout.",
        "topic": "warranty"
    },
    {
        "id": "hours_001",
        "question": "What are your business hours?",
        "answer": "Customer support: Mon-Fri 8AM-8PM EST, Sat 9AM-5PM. Closed Sundays. Online orders 24/7.",
        "topic": "hours"
    },
    {
        "id": "pricing_001",
        "question": "Do you offer student discounts?",
        "answer": "Yes, we offer 15% off for verified students with valid ID. Ask for details at checkout.",
        "topic": "pricing"
    },
    {
        "id": "pricing_002",
        "question": "What are your bulk discount rates?",
        "answer": "We offer competitive pricing with price matching on identical items. Bulk discounts: 10% off $100+, 15% off $250+, 20% off $500+. Student discount: 15% with valid .edu email.",
        "topic": "pricing"
    },
    {
        "id": "contact_001",
        "question": "How can I contact customer support?",
        "answer": "Email: support@yourbusiness.com | Phone: 1-800-555-0123 | Live chat on website. Average response: <2 hours business hours.",
        "topic": "contact"
    },
    {
        "id": "privacy_001",
        "question": "How do you protect my personal data?",
        "answer": "We never sell your data. SSL encryption on all transactions. GDPR/CCPA compliant. You can request data deletion anytime.",
        "topic": "privacy"
    }
]

# ============================================================
# RAG COMPONENTS
# ============================================================

class SimpleRAG:
    def __init__(self, use_mock: bool = True):
        """
        Initialize RAG system.

        Args:
            use_mock: If True, uses mock embeddings for demo without dependencies
                     If False, tries to use real sentence-transformers + chromadb
        """
        self.use_mock = use_mock or not HAS_DEPS
        self.embedding_model = None
        self.collection = None

        if not self.use_mock and HAS_DEPS:
            try:
                # Initialize embedding model
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

                # Initialize ChromaDB (in-memory for prototype)
                self.chroma_client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=None  # In-memory
                ))

                # Get or create collection
                self.collection = self.chroma_client.get_or_create_collection(
                    name="business_faq",
                    metadata={"hnsw:space": "cosine"}
                )

                # Populate with FAQ data if empty
                if self.collection.count() == 0:
                    self._populate_database()

                print("[OK] RAG system initialized with real embeddings + ChromaDB")
            except Exception as e:
                print(f"[WARN] Failed to initialize real RAG: {e}")
                print("  Falling back to mock embeddings")
                self.use_mock = True

        if self.use_mock:
            print("[OK] RAG system initialized with mock embeddings (demo mode)")
            self._setup_mock()

    def _setup_mock(self):
        """Setup mock embeddings for demonstration using bag-of-words similarity."""
        # Build a vocabulary from all FAQ questions and answers
        self.vocabulary = set()
        for faq in BUSINESS_FAQ_DATA:
            self.vocabulary.update(faq["question"].lower().split())
            self.vocabulary.update(faq["answer"].lower().split())
        self.vocabulary = sorted(self.vocabulary)
        self.word_to_idx = {w: i for i, w in enumerate(self.vocabulary)}

        # Create bag-of-words vectors for each FAQ
        self.faq_vectors = []
        for faq in BUSINESS_FAQ_DATA:
            vec = np.zeros(len(self.vocabulary))
            text = (faq["question"] + " " + faq["answer"]).lower()
            for word in text.split():
                if word in self.word_to_idx:
                    vec[self.word_to_idx[word]] += 1
            # Normalize
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            self.faq_vectors.append(vec)
        self.faq_vectors = np.array(self.faq_vectors)

    def _populate_database(self):
        """Populate ChromaDB with FAQ data."""
        documents = [faq["answer"] for faq in BUSINESS_FAQ_DATA]
        metadatas = [{"topic": faq["topic"], "id": faq["id"]} for faq in BUSINESS_FAQ_DATA]
        ids = [faq["id"] for faq in BUSINESS_FAQ_DATA]

        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[OK] Populated ChromaDB with {len(documents)} FAQ entries")

    def encode_query(self, query: str) -> List[float]:
        """Encode query into embedding vector."""
        if self.use_mock:
            # Mock encoding: bag-of-words over vocabulary
            query_vec = np.zeros(len(self.vocabulary))
            for word in query.lower().split():
                if word in self.word_to_idx:
                    query_vec[self.word_to_idx[word]] += 1
            norm = np.linalg.norm(query_vec)
            if norm > 0:
                query_vec = query_vec / norm
            return query_vec.tolist()
        else:
            # Real encoding
            return self.embedding_model.encode([query])[0].tolist()

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant FAQ entries for a query.

        Returns:
            List of dicts with keys: id, question, answer, topic, score
        """
        query_embedding = self.encode_query(query)

        if self.use_mock:
            # Mock similarity search (cosine similarity) using bag-of-words vectors
            query_vec = np.array(query_embedding)
            faq_vecs = self.faq_vectors

            # Normalize (already normalized in encode_query and _setup_mock)
            # Cosine similarity
            similarities = np.dot(faq_vecs, query_vec)

            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]

            results = []
            for idx in top_indices:
                faq = BUSINESS_FAQ_DATA[idx]
                results.append({
                    "id": faq["id"],
                    "question": faq["question"],
                    "answer": faq["answer"],
                    "topic": faq["topic"],
                    "score": float(similarities[idx])
                })
            return results
        else:
            # Real ChromaDB search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            # Format results
            formatted = []
            for i in range(len(results["ids"][0])):
                formatted.append({
                    "id": results["ids"][0][i],
                    "question": self._get_question_by_id(results["ids"][0][i]),
                    "answer": results["documents"][0][i],
                    "topic": results["metadatas"][0][i]["topic"],
                    "score": 1 - results["distances"][0][i]  # Convert distance to similarity
                })
            return formatted

    def _get_question_by_id(self, faq_id: str) -> str:
        """Get question text by ID."""
        for faq in BUSINESS_FAQ_DATA:
            if faq["id"] == faq_id:
                return faq["question"]
        return "Unknown question"

# ============================================================
# NEEDLE 3 INTEGRATION
# ============================================================

import needle
import random

# Greeting/Farewell handling
GREETING_KEYWORDS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy", "greetings", "hiya", "yo", "sup"]
FAREWELL_KEYWORDS = ["bye", "goodbye", "see you", "farewell", "cya", "later", "quit", "exit"]

GREETING_RESPONSES = [
    "Hello! Welcome to YourBusiness. How can I help you today?",
    "Hi there! What can I help you find?",
    "Hey! Ask me anything about returns, shipping, products, or policies.",
    "Good to see you! What questions do you have?",
]

FAREWELL_RESPONSES = [
    "Thanks for chatting! Have a great day!",
    "Goodbye! Come back anytime you have questions.",
    "See you later! We're here if you need anything.",
]

def detect_greeting(query: str) -> str | None:
    """Check if query is a greeting or farewell."""
    q = query.lower().strip()
    if any(q.startswith(k) or q == k for k in GREETING_KEYWORDS):
        return "greeting"
    if any(q.startswith(k) or q == k for k in FAREWELL_KEYWORDS):
        return "farewell"
    return None

def get_greeting_response() -> str:
    return random.choice(GREETING_RESPONSES)

def get_farewell_response() -> str:
    return random.choice(FAREWELL_RESPONSES)


@needle.tool
def faq_lookup(query: str):
    """
    Tool for Needle 3: Retrieve business FAQ answer using RAG.
    This replaces the simple keyword matching with real vector search.
    """
    # Initialize RAG system (cached)
    if not hasattr(faq_lookup, '_rag'):
        faq_lookup._rag = SimpleRAG(use_mock=not HAS_DEPS)

    # Retrieve relevant FAQs
    results = faq_lookup._rag.retrieve(query, top_k=3)

    if not results:
        return {
            "query": query,
            "answer": "I don't have that information. Please contact support@yourbusiness.com for help.",
            "confidence": 0.0,
            "sources": [],
            "grounded": True
        }

    # Get the best match
    best = results[0]

    # Format answer with confidence based on score
    confidence = best["score"]

    # For demo, we'll show the top result
    # In production, you might combine multiple results or use an LLM to synthesize
    answer = best["answer"]

    # Add source attribution for transparency (optional)
    if confidence < 0.7:  # Low confidence
        answer += "\n\nNote: This is the closest match I found. For precise information, please contact support."

    return {
        "query": query,
        "answer": answer,
        "confidence": confidence,
        "sources": [r["id"] for r in results],
        "grounded": True
    }

# ============================================================
# AGENT SETUP (same as before but with RAG tool)
# ============================================================

agent = needle.Needle(
    tools=[faq_lookup],
    system="You are BizAssist, a friendly and professional support assistant for YourBusiness. "
           "When a customer asks a question, ALWAYS call faq_lookup with their exact question. "
           "Respond using ONLY the answer from faq_lookup. Never invent policies, prices, or procedures. "
           "Keep answers conversational but concise (2-3 sentences max). Be helpful and warm."
)

# ============================================================
# DEMO / TEST FUNCTIONS
# ============================================================

def demo_rag():
    """Demonstrate the RAG system with various queries."""
    print("=" * 60)
    print("RAG PROTOTYPE DEMO - Needle 3 + ChromaDB + Embeddings")
    print("=" * 60)

    test_queries = [
        "Can I return an item I bought last week?",
        "How long does shipping take?",
        "What is your warranty policy?",
        "Do you offer student discounts?",
        "How can I contact customer support?",
        "What if I receive a damaged item?",
        "Do you ship internationally?",
        "What are your business hours?",
        "I want to exchange a gift",
        "Is there a bulk discount for orders over $500?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        agent.reset()
        result = agent.run(query)

        # Extract answer from agent results
        answer = "No answer generated"
        if result.get('results'):
            for r in result['results']:
                if isinstance(r, dict) and 'answer' in r:
                    answer = r['answer']
                    break

        # Fallback to direct tool call if needed
        if answer == "No answer generated":
            direct = faq_lookup(query)
            answer = direct['answer']

        print(f"Answer: {answer}")
        if isinstance(result.get('results'), list) and len(result['results']) > 0:
            # Show retrieval info if available
            first_result = result['results'][0]
            if isinstance(first_result, dict) and 'confidence' in first_result:
                print(f"Confidence: {first_result['confidence']:.3f}")
        print("-" * 50)

def interactive_chat():
    """Run interactive chat session."""
    print("=" * 55)
    print("  [BOT] YourBusiness Support Bot - RAG Prototype")
    print("  Type 'quit', 'exit', or 'bye' to end")
    print("  Demo mode: " + ("MOCK" if not HAS_DEPS else "REAL EMBEDDINGS"))
    print("=" * 55)

    # Initial greeting
    print(f"\nBot: Hello! Welcome to YourBusiness. How can I help you today?")

    while True:
        try:
            query = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n\nBot: Goodbye! Have a great day!")
            break

        query = query.strip()
        if not query:
            continue

        # Check for farewell
        if query.lower() in ['quit', 'exit', 'bye']:
            print(f"Bot: Goodbye! Have a great day!")
            break

        # Check for greeting/farewell FIRST
        greeting_type = detect_greeting(query)
        if greeting_type == "greeting":
            print(f"Bot: {get_greeting_response()}")
            agent.reset()
            continue
        elif greeting_type == "farewell":
            print(f"Bot: {get_farewell_response()}")
            break

        # Get answer from agent
        agent.reset()
        result = agent.run(query)

        answer = "I'm having trouble processing that. Could you rephrase?"
        if result.get('results'):
            for r in result['results']:
                if isinstance(r, dict) and 'answer' in r:
                    answer = r['answer']
                    break

        # Fallback to direct tool call
        if answer == "I'm having trouble processing that. Could you rephrase?":
            direct = faq_lookup(query)
            answer = direct['answer']

        print(f"Bot: {answer}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_rag()
    elif len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
    else:
        # Default: show brief help
        print("RAG Prototype for MBA FAQ Chatbot Project")
        print("Usage:")
        print("  python rag_prototype.py --demo      # Run demonstration queries")
        print("  python rag_prototype.py --interactive  # Start interactive chat")
        print("  python -c \"from rag_prototype import agent; print(agent.run('your query'))\"  # Programmatic use")
        print("")
        print("Dependencies:")
        print("  pip install sentence-transformers chromadb  # For real embeddings")
        print("  Without deps: runs in mock mode (still demonstrates concept)")