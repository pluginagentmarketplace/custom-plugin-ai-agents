#!/usr/bin/env python3
"""
Hybrid RAG Pipeline
===================

Production-ready RAG pipeline with hybrid search (BM25 + Vector),
reranking, and adaptive chunking.

Requirements:
    pip install langchain chromadb sentence-transformers rank-bm25

Usage:
    python hybrid_rag_pipeline.py "path/to/documents" "What is the main topic?"
"""

import sys
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class RAGConfig:
    """RAG pipeline configuration."""
    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50
    min_chunk_size: int = 100

    # Retrieval
    top_k_initial: int = 20
    top_k_final: int = 5
    bm25_weight: float = 0.3
    vector_weight: float = 0.7

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"

    # Storage
    collection_name: str = "documents"
    persist_directory: str = "./chroma_db"


# =============================================================================
# ADAPTIVE CHUNKER
# =============================================================================

@dataclass
class Chunk:
    """Document chunk with metadata."""
    content: str
    metadata: Dict[str, Any]
    chunk_id: str = field(default="")

    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = hashlib.md5(
                self.content.encode()
            ).hexdigest()[:12]


class AdaptiveChunker:
    """
    Adaptive document chunker.

    Adjusts chunk boundaries based on content structure
    (paragraphs, sentences, code blocks).
    """

    def __init__(self, config: RAGConfig):
        self.config = config
        self.separators = [
            "\n\n",     # Paragraphs
            "\n",       # Lines
            ". ",       # Sentences
            "! ",
            "? ",
            "; ",
            ", ",       # Clauses
            " ",        # Words
        ]

    def chunk(self, text: str, metadata: Dict[str, Any] = None) -> List[Chunk]:
        """
        Split text into chunks adaptively.

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach

        Returns:
            List of Chunk objects
        """
        metadata = metadata or {}
        chunks = []

        # Detect content type
        is_code = self._is_code(text)

        if is_code:
            # Code-aware chunking
            raw_chunks = self._chunk_code(text)
        else:
            # Semantic chunking
            raw_chunks = self._chunk_text(text)

        # Create Chunk objects
        for i, content in enumerate(raw_chunks):
            if len(content.strip()) >= self.config.min_chunk_size:
                chunk_meta = {
                    **metadata,
                    "chunk_index": i,
                    "is_code": is_code
                }
                chunks.append(Chunk(
                    content=content.strip(),
                    metadata=chunk_meta
                ))

        return chunks

    def _is_code(self, text: str) -> bool:
        """Detect if text is primarily code."""
        code_indicators = [
            "def ", "class ", "import ",
            "function ", "const ", "let ", "var ",
            "public ", "private ", "static "
        ]
        indicator_count = sum(1 for ind in code_indicators if ind in text)
        return indicator_count >= 2

    def _chunk_text(self, text: str) -> List[str]:
        """Chunk natural language text."""
        chunks = []
        current_chunk = ""

        # Split by paragraphs first
        paragraphs = text.split("\n\n")

        for para in paragraphs:
            if len(current_chunk) + len(para) <= self.config.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                # Handle long paragraphs
                if len(para) > self.config.chunk_size:
                    sentences = self._split_sentences(para)
                    current_chunk = ""
                    for sent in sentences:
                        if len(current_chunk) + len(sent) <= self.config.chunk_size:
                            current_chunk += sent + " "
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = sent + " "
                else:
                    current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk)

        # Add overlap
        return self._add_overlap(chunks)

    def _chunk_code(self, text: str) -> List[str]:
        """Chunk code preserving function boundaries."""
        chunks = []
        lines = text.split("\n")
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1

            # Check for function/class boundaries
            is_boundary = any(
                line.strip().startswith(kw)
                for kw in ["def ", "class ", "function ", "async "]
            )

            if is_boundary and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(line)
            current_size += line_size

            if current_size >= self.config.chunk_size:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        return re.split(r'(?<=[.!?])\s+', text)

    def _add_overlap(self, chunks: List[str]) -> List[str]:
        """Add overlap between chunks."""
        if not chunks or self.config.chunk_overlap == 0:
            return chunks

        overlapped = []
        for i, chunk in enumerate(chunks):
            if i > 0:
                # Add end of previous chunk
                prev_words = chunks[i-1].split()
                overlap_words = prev_words[-self.config.chunk_overlap:]
                chunk = " ".join(overlap_words) + " " + chunk
            overlapped.append(chunk)

        return overlapped


# =============================================================================
# HYBRID RETRIEVER
# =============================================================================

class HybridRetriever:
    """
    Hybrid retriever combining BM25 and vector search.

    Uses reciprocal rank fusion for result combination.
    """

    def __init__(self, config: RAGConfig):
        self.config = config
        self.chunks: List[Chunk] = []
        self.bm25 = None
        self.vector_store = None
        self.embeddings = None

    def index(self, chunks: List[Chunk]) -> None:
        """
        Index chunks for retrieval.

        Args:
            chunks: List of chunks to index
        """
        self.chunks = chunks

        # BM25 index
        from rank_bm25 import BM25Okapi
        tokenized = [c.content.lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)

        # Vector index
        from sentence_transformers import SentenceTransformer
        import chromadb

        self.embeddings = SentenceTransformer(self.config.embedding_model)

        client = chromadb.PersistentClient(
            path=self.config.persist_directory
        )

        # Delete existing collection
        try:
            client.delete_collection(self.config.collection_name)
        except:
            pass

        self.vector_store = client.create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        # Add documents
        embeddings = self.embeddings.encode([c.content for c in chunks])

        self.vector_store.add(
            ids=[c.chunk_id for c in chunks],
            embeddings=embeddings.tolist(),
            documents=[c.content for c in chunks],
            metadatas=[c.metadata for c in chunks]
        )

        print(f"✅ Indexed {len(chunks)} chunks")

    def retrieve(self, query: str) -> List[Chunk]:
        """
        Retrieve relevant chunks using hybrid search.

        Args:
            query: Search query

        Returns:
            Top-k relevant chunks
        """
        # BM25 search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_results = [
            (i, score) for i, score in enumerate(bm25_scores)
        ]
        bm25_results.sort(key=lambda x: x[1], reverse=True)
        bm25_results = bm25_results[:self.config.top_k_initial]

        # Vector search
        query_embedding = self.embeddings.encode([query])[0]
        vector_results = self.vector_store.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=self.config.top_k_initial
        )

        # Reciprocal rank fusion
        scores = {}
        k = 60  # RRF constant

        # BM25 scores
        for rank, (idx, _) in enumerate(bm25_results):
            chunk_id = self.chunks[idx].chunk_id
            scores[chunk_id] = scores.get(chunk_id, 0) + \
                self.config.bm25_weight / (k + rank + 1)

        # Vector scores
        for rank, chunk_id in enumerate(vector_results["ids"][0]):
            scores[chunk_id] = scores.get(chunk_id, 0) + \
                self.config.vector_weight / (k + rank + 1)

        # Sort by combined score
        sorted_ids = sorted(
            scores.keys(),
            key=lambda x: scores[x],
            reverse=True
        )[:self.config.top_k_final]

        # Get chunks
        chunk_map = {c.chunk_id: c for c in self.chunks}
        return [chunk_map[cid] for cid in sorted_ids if cid in chunk_map]


# =============================================================================
# RAG PIPELINE
# =============================================================================

class RAGPipeline:
    """
    Complete RAG pipeline.

    Combines chunking, retrieval, and generation.
    """

    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.chunker = AdaptiveChunker(self.config)
        self.retriever = HybridRetriever(self.config)

    def ingest(self, documents: List[Dict[str, Any]]) -> None:
        """
        Ingest documents into the pipeline.

        Args:
            documents: List of {"content": str, "metadata": dict}
        """
        all_chunks = []

        for doc in documents:
            chunks = self.chunker.chunk(
                doc["content"],
                doc.get("metadata", {})
            )
            all_chunks.extend(chunks)

        self.retriever.index(all_chunks)

    def query(self, query: str) -> Dict[str, Any]:
        """
        Query the RAG pipeline.

        Args:
            query: User query

        Returns:
            Dict with answer and sources
        """
        # Retrieve relevant chunks
        relevant_chunks = self.retriever.retrieve(query)

        # Build context
        context = "\n\n---\n\n".join([
            f"[Source {i+1}]\n{chunk.content}"
            for i, chunk in enumerate(relevant_chunks)
        ])

        # Generate answer (using simple template - replace with LLM)
        answer = self._generate_answer(query, context)

        return {
            "answer": answer,
            "sources": [
                {
                    "content": c.content[:200] + "...",
                    "metadata": c.metadata
                }
                for c in relevant_chunks
            ],
            "context_used": len(relevant_chunks)
        }

    def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer from context. Replace with actual LLM call."""
        # This is a placeholder - in production, use your LLM client
        return f"""Based on the retrieved context, here is information relevant to: "{query}"

Context Summary:
{context[:500]}...

Note: This is a demo response. In production, replace this with an actual LLM call."""


# =============================================================================
# MAIN
# =============================================================================

def load_documents(path: str) -> List[Dict[str, Any]]:
    """Load documents from a directory or file."""
    documents = []
    path = Path(path)

    if path.is_file():
        files = [path]
    else:
        files = list(path.glob("**/*.txt")) + \
                list(path.glob("**/*.md")) + \
                list(path.glob("**/*.py"))

    for file in files:
        try:
            content = file.read_text(encoding="utf-8")
            documents.append({
                "content": content,
                "metadata": {
                    "source": str(file),
                    "filename": file.name
                }
            })
        except Exception as e:
            print(f"⚠️ Could not read {file}: {e}")

    return documents


def main():
    """Run RAG pipeline demo."""
    if len(sys.argv) < 3:
        print("Usage: python hybrid_rag_pipeline.py <doc_path> '<query>'")
        sys.exit(1)

    doc_path = sys.argv[1]
    query = sys.argv[2]

    print("\n🔍 Hybrid RAG Pipeline")
    print("-" * 50)

    # Load documents
    print(f"📂 Loading documents from: {doc_path}")
    documents = load_documents(doc_path)
    print(f"   Found {len(documents)} documents")

    # Initialize pipeline
    config = RAGConfig()
    pipeline = RAGPipeline(config)

    # Ingest documents
    print("\n📥 Ingesting documents...")
    pipeline.ingest(documents)

    # Query
    print(f"\n❓ Query: {query}")
    print("-" * 50)

    result = pipeline.query(query)

    print(f"\n📤 Answer:\n{result['answer']}")
    print(f"\n📚 Sources used: {result['context_used']}")

    for i, source in enumerate(result["sources"]):
        print(f"\n  [{i+1}] {source['metadata'].get('filename', 'Unknown')}")
        print(f"      {source['content'][:100]}...")


if __name__ == "__main__":
    main()
