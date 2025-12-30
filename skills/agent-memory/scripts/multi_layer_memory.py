#!/usr/bin/env python3
"""
Multi-Layer Memory System
=========================

Production implementation of agent memory with multiple layers:
- Short-term buffer memory
- Long-term vector memory
- Summary memory for compression

Requirements:
    pip install chromadb sentence-transformers

Usage:
    python multi_layer_memory.py
"""

import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from collections import deque
from abc import ABC, abstractmethod


# =============================================================================
# MEMORY INTERFACES
# =============================================================================

@dataclass
class MemoryItem:
    """A single memory item."""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    importance: float = 0.5
    access_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance,
            "access_count": self.access_count
        }


class MemoryLayer(ABC):
    """Abstract base for memory layers."""

    @abstractmethod
    def add(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add item to memory. Returns memory ID."""
        pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[MemoryItem]:
        """Search memory for relevant items."""
        pass

    @abstractmethod
    def get(self, memory_id: str) -> Optional[MemoryItem]:
        """Get specific memory by ID."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all memories."""
        pass


# =============================================================================
# BUFFER MEMORY (Short-term)
# =============================================================================

class BufferMemory(MemoryLayer):
    """
    Short-term buffer memory.

    Stores recent interactions in a fixed-size buffer.
    Uses FIFO eviction when full.
    """

    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.buffer: deque = deque(maxlen=max_size)
        self._index: Dict[str, MemoryItem] = {}

    def add(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add item to buffer."""
        memory_id = hashlib.md5(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        item = MemoryItem(
            id=memory_id,
            content=content,
            metadata=metadata or {},
            importance=self._calculate_importance(content)
        )

        # Remove oldest if at capacity
        if len(self.buffer) >= self.max_size:
            oldest = self.buffer[0]
            self._index.pop(oldest.id, None)

        self.buffer.append(item)
        self._index[memory_id] = item

        return memory_id

    def search(self, query: str, k: int = 5) -> List[MemoryItem]:
        """Search buffer using keyword matching."""
        query_words = set(query.lower().split())

        scored = []
        for item in self.buffer:
            content_words = set(item.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                scored.append((item, overlap))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in scored[:k]]

    def get(self, memory_id: str) -> Optional[MemoryItem]:
        """Get item by ID."""
        item = self._index.get(memory_id)
        if item:
            item.access_count += 1
        return item

    def clear(self) -> None:
        """Clear buffer."""
        self.buffer.clear()
        self._index.clear()

    def get_recent(self, n: int = 5) -> List[MemoryItem]:
        """Get n most recent items."""
        return list(self.buffer)[-n:]

    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score for content."""
        # Simple heuristics
        importance = 0.5

        # Longer content = potentially more important
        if len(content) > 200:
            importance += 0.1
        if len(content) > 500:
            importance += 0.1

        # Questions are important
        if "?" in content:
            importance += 0.1

        # Certain keywords increase importance
        important_words = ["important", "critical", "remember", "key", "must"]
        if any(word in content.lower() for word in important_words):
            importance += 0.2

        return min(importance, 1.0)


# =============================================================================
# VECTOR MEMORY (Long-term)
# =============================================================================

class VectorMemory(MemoryLayer):
    """
    Long-term vector memory.

    Uses embeddings for semantic search.
    Stores in ChromaDB for persistence.
    """

    def __init__(
        self,
        collection_name: str = "agent_memory",
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./memory_db"
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize embedding model
        from sentence_transformers import SentenceTransformer
        self.embeddings = SentenceTransformer(embedding_model)

        # Initialize ChromaDB
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        # Local index for metadata
        self._metadata_index: Dict[str, Dict] = {}

    def add(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add item to vector memory."""
        memory_id = hashlib.md5(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        # Create embedding
        embedding = self.embeddings.encode([content])[0]

        # Store metadata
        full_metadata = {
            **(metadata or {}),
            "timestamp": datetime.now().isoformat(),
            "importance": self._calculate_importance(content),
            "access_count": 0
        }

        # Add to ChromaDB
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding.tolist()],
            documents=[content],
            metadatas=[{k: str(v) for k, v in full_metadata.items()}]
        )

        self._metadata_index[memory_id] = full_metadata

        return memory_id

    def search(self, query: str, k: int = 5) -> List[MemoryItem]:
        """Search using semantic similarity."""
        query_embedding = self.embeddings.encode([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )

        items = []
        if results["ids"][0]:
            for i, memory_id in enumerate(results["ids"][0]):
                content = results["documents"][0][i]
                raw_meta = results["metadatas"][0][i]

                item = MemoryItem(
                    id=memory_id,
                    content=content,
                    metadata=raw_meta,
                    timestamp=datetime.fromisoformat(raw_meta.get("timestamp", datetime.now().isoformat())),
                    importance=float(raw_meta.get("importance", 0.5))
                )
                items.append(item)

        return items

    def get(self, memory_id: str) -> Optional[MemoryItem]:
        """Get specific memory by ID."""
        results = self.collection.get(ids=[memory_id])

        if results["ids"]:
            content = results["documents"][0]
            raw_meta = results["metadatas"][0]

            return MemoryItem(
                id=memory_id,
                content=content,
                metadata=raw_meta,
                timestamp=datetime.fromisoformat(raw_meta.get("timestamp", datetime.now().isoformat())),
                importance=float(raw_meta.get("importance", 0.5))
            )
        return None

    def clear(self) -> None:
        """Clear all memories."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self._metadata_index.clear()

    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score."""
        importance = 0.5
        if len(content) > 200:
            importance += 0.1
        if "?" in content:
            importance += 0.1
        return min(importance, 1.0)


# =============================================================================
# SUMMARY MEMORY
# =============================================================================

class SummaryMemory(MemoryLayer):
    """
    Summary memory for conversation compression.

    Maintains a running summary of interactions.
    """

    def __init__(self, max_summary_length: int = 1000):
        self.max_length = max_summary_length
        self.summaries: List[MemoryItem] = []
        self.current_summary: str = ""
        self._buffer: List[str] = []
        self._buffer_threshold = 5  # Summarize after N items

    def add(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add content and potentially trigger summarization."""
        self._buffer.append(content)

        if len(self._buffer) >= self._buffer_threshold:
            summary = self._create_summary()
            memory_id = hashlib.md5(summary.encode()).hexdigest()[:12]

            item = MemoryItem(
                id=memory_id,
                content=summary,
                metadata={"type": "summary", "items_summarized": len(self._buffer)}
            )

            self.summaries.append(item)
            self.current_summary = self._merge_summaries()
            self._buffer.clear()

            return memory_id

        return ""

    def search(self, query: str, k: int = 5) -> List[MemoryItem]:
        """Search summaries."""
        query_words = set(query.lower().split())

        scored = []
        for item in self.summaries:
            content_words = set(item.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                scored.append((item, overlap))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in scored[:k]]

    def get(self, memory_id: str) -> Optional[MemoryItem]:
        """Get summary by ID."""
        for item in self.summaries:
            if item.id == memory_id:
                return item
        return None

    def clear(self) -> None:
        """Clear all summaries."""
        self.summaries.clear()
        self.current_summary = ""
        self._buffer.clear()

    def get_current_summary(self) -> str:
        """Get the current running summary."""
        return self.current_summary

    def _create_summary(self) -> str:
        """Create summary from buffer. Replace with LLM in production."""
        # Simple extraction - in production, use LLM for better summaries
        combined = " ".join(self._buffer)
        sentences = combined.split(". ")

        # Keep first and last sentences, key phrases
        if len(sentences) > 3:
            key_sentences = [sentences[0], sentences[-1]]
        else:
            key_sentences = sentences

        return ". ".join(key_sentences)

    def _merge_summaries(self) -> str:
        """Merge all summaries into one."""
        all_content = " ".join(s.content for s in self.summaries[-5:])

        if len(all_content) > self.max_length:
            all_content = all_content[:self.max_length] + "..."

        return all_content


# =============================================================================
# MULTI-LAYER MEMORY SYSTEM
# =============================================================================

class MultiLayerMemory:
    """
    Complete multi-layer memory system.

    Combines buffer, vector, and summary memory.
    """

    def __init__(
        self,
        buffer_size: int = 10,
        collection_name: str = "agent_memory",
        persist_directory: str = "./memory_db"
    ):
        self.buffer = BufferMemory(max_size=buffer_size)
        self.vector = VectorMemory(
            collection_name=collection_name,
            persist_directory=persist_directory
        )
        self.summary = SummaryMemory()

    def add(
        self,
        content: str,
        metadata: Dict[str, Any] = None,
        to_long_term: bool = True
    ) -> Dict[str, str]:
        """
        Add memory to all appropriate layers.

        Args:
            content: Content to remember
            metadata: Optional metadata
            to_long_term: Whether to store in vector memory

        Returns:
            Dict of memory IDs for each layer
        """
        ids = {}

        # Always add to buffer
        ids["buffer"] = self.buffer.add(content, metadata)

        # Add to summary
        summary_id = self.summary.add(content, metadata)
        if summary_id:
            ids["summary"] = summary_id

        # Optionally add to long-term
        if to_long_term:
            ids["vector"] = self.vector.add(content, metadata)

        return ids

    def search(
        self,
        query: str,
        k: int = 5,
        layers: List[str] = None
    ) -> Dict[str, List[MemoryItem]]:
        """
        Search across memory layers.

        Args:
            query: Search query
            k: Number of results per layer
            layers: Which layers to search (default: all)

        Returns:
            Dict mapping layer name to results
        """
        layers = layers or ["buffer", "vector", "summary"]
        results = {}

        if "buffer" in layers:
            results["buffer"] = self.buffer.search(query, k)

        if "vector" in layers:
            results["vector"] = self.vector.search(query, k)

        if "summary" in layers:
            results["summary"] = self.summary.search(query, k)

        return results

    def get_context(self, query: str, max_tokens: int = 1000) -> str:
        """
        Get relevant context for a query.

        Combines results from all layers into a single context string.
        """
        results = self.search(query, k=3)

        context_parts = []

        # Add recent buffer items
        recent = self.buffer.get_recent(3)
        if recent:
            context_parts.append("Recent interactions:")
            for item in recent:
                context_parts.append(f"  - {item.content[:100]}...")

        # Add relevant long-term memories
        if results.get("vector"):
            context_parts.append("\nRelevant memories:")
            for item in results["vector"][:3]:
                context_parts.append(f"  - {item.content[:100]}...")

        # Add summary
        summary = self.summary.get_current_summary()
        if summary:
            context_parts.append(f"\nConversation summary: {summary[:200]}...")

        context = "\n".join(context_parts)

        # Truncate if needed
        if len(context) > max_tokens * 4:  # Rough char estimate
            context = context[:max_tokens * 4] + "..."

        return context

    def clear_all(self) -> None:
        """Clear all memory layers."""
        self.buffer.clear()
        self.vector.clear()
        self.summary.clear()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Demonstrate multi-layer memory system."""
    print("\n🧠 Multi-Layer Memory System Demo")
    print("=" * 50)

    # Initialize memory
    memory = MultiLayerMemory(
        buffer_size=5,
        collection_name="demo_memory",
        persist_directory="./demo_memory_db"
    )

    # Clear previous demo data
    memory.clear_all()

    # Add some memories
    print("\n📥 Adding memories...")

    memories = [
        ("The user's name is Alice and she works as a data scientist.", {"type": "user_info"}),
        ("Alice prefers Python for data analysis tasks.", {"type": "preference"}),
        ("We discussed machine learning model optimization yesterday.", {"type": "conversation"}),
        ("Alice is interested in natural language processing.", {"type": "interest"}),
        ("The project deadline is next Friday.", {"type": "task"}),
        ("Alice mentioned she has experience with TensorFlow and PyTorch.", {"type": "skill"}),
    ]

    for content, metadata in memories:
        ids = memory.add(content, metadata)
        print(f"  ✅ Added: {content[:40]}...")
        print(f"     IDs: {ids}")

    # Search memories
    print("\n🔍 Searching memories...")

    queries = [
        "What programming language does Alice prefer?",
        "Tell me about Alice's background",
        "What are the upcoming deadlines?"
    ]

    for query in queries:
        print(f"\n  Query: {query}")
        results = memory.search(query, k=2)

        print("  Results:")
        for layer, items in results.items():
            if items:
                print(f"    [{layer}]:")
                for item in items:
                    print(f"      - {item.content[:60]}...")

    # Get context
    print("\n📋 Getting context for query...")
    context = memory.get_context("Tell me about Alice")
    print(context)

    print("\n✅ Demo complete!")


if __name__ == "__main__":
    main()
