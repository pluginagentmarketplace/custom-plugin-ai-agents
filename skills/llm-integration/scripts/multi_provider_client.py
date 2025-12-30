#!/usr/bin/env python3
"""
Multi-Provider LLM Client
==========================

Production-ready LLM client with automatic failover between providers.
Supports Anthropic Claude, OpenAI, and local models via Ollama.

Requirements:
    pip install anthropic openai httpx tenacity

Usage:
    python multi_provider_client.py "Explain quantum computing"
"""

import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, AsyncIterator, List, Dict, Any
from enum import Enum
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


# =============================================================================
# CONFIGURATION
# =============================================================================

class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OLLAMA = "ollama"


@dataclass
class ModelConfig:
    """Configuration for a model."""
    provider: Provider
    model_id: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 30.0
    priority: int = 1  # Lower = higher priority


# Default provider chain with failover
DEFAULT_MODELS = [
    ModelConfig(Provider.ANTHROPIC, "claude-sonnet-4-20250514", priority=1),
    ModelConfig(Provider.OPENAI, "gpt-4o", priority=2),
    ModelConfig(Provider.OLLAMA, "llama3.1", priority=3),
]


# =============================================================================
# BASE CLIENT
# =============================================================================

@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    provider: Provider
    usage: Dict[str, int]
    finish_reason: str


class BaseLLMClient(ABC):
    """Abstract base for LLM clients."""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> LLMResponse:
        """Generate a response."""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> AsyncIterator[str]:
        """Stream a response."""
        pass


# =============================================================================
# ANTHROPIC CLIENT
# =============================================================================

class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client."""

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    async def generate(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> LLMResponse:
        """Generate using Claude."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": config.model_id,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages
                }
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data["content"][0]["text"],
                model=config.model_id,
                provider=Provider.ANTHROPIC,
                usage={
                    "input_tokens": data["usage"]["input_tokens"],
                    "output_tokens": data["usage"]["output_tokens"]
                },
                finish_reason=data["stop_reason"]
            )

    async def stream(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> AsyncIterator[str]:
        """Stream using Claude."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": config.model_id,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if data["type"] == "content_block_delta":
                            yield data["delta"]["text"]


# =============================================================================
# OPENAI CLIENT
# =============================================================================

class OpenAIClient(BaseLLMClient):
    """OpenAI GPT client."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    async def generate(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> LLMResponse:
        """Generate using GPT."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config.model_id,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages
                }
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data["choices"][0]["message"]["content"],
                model=config.model_id,
                provider=Provider.OPENAI,
                usage={
                    "input_tokens": data["usage"]["prompt_tokens"],
                    "output_tokens": data["usage"]["completion_tokens"]
                },
                finish_reason=data["choices"][0]["finish_reason"]
            )

    async def stream(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> AsyncIterator[str]:
        """Stream using GPT."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config.model_id,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        data = json.loads(line[6:])
                        if data["choices"][0]["delta"].get("content"):
                            yield data["choices"][0]["delta"]["content"]


# =============================================================================
# OLLAMA CLIENT
# =============================================================================

class OllamaClient(BaseLLMClient):
    """Ollama local model client."""

    def __init__(self):
        self.base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    async def generate(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> LLMResponse:
        """Generate using Ollama."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": config.model_id,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": config.temperature,
                        "num_predict": config.max_tokens
                    }
                }
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data["message"]["content"],
                model=config.model_id,
                provider=Provider.OLLAMA,
                usage={
                    "input_tokens": data.get("prompt_eval_count", 0),
                    "output_tokens": data.get("eval_count", 0)
                },
                finish_reason="stop"
            )

    async def stream(
        self,
        messages: List[Dict[str, str]],
        config: ModelConfig
    ) -> AsyncIterator[str]:
        """Stream using Ollama."""
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": config.model_id,
                    "messages": messages,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if data.get("message", {}).get("content"):
                            yield data["message"]["content"]


# =============================================================================
# MULTI-PROVIDER CLIENT
# =============================================================================

class MultiProviderClient:
    """
    Multi-provider LLM client with automatic failover.

    Tries providers in priority order and fails over on errors.
    """

    def __init__(self, models: Optional[List[ModelConfig]] = None):
        self.models = sorted(
            models or DEFAULT_MODELS,
            key=lambda m: m.priority
        )
        self.clients = {
            Provider.ANTHROPIC: AnthropicClient(),
            Provider.OPENAI: OpenAIClient(),
            Provider.OLLAMA: OllamaClient(),
        }

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> LLMResponse:
        """
        Generate a response with automatic failover.

        Args:
            prompt: User prompt
            system: Optional system message

        Returns:
            LLMResponse from first successful provider
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        errors = []

        for config in self.models:
            try:
                client = self.clients[config.provider]
                print(f"🔄 Trying {config.provider.value}/{config.model_id}...")
                response = await client.generate(messages, config)
                print(f"✅ Success with {config.provider.value}")
                return response
            except Exception as e:
                errors.append(f"{config.provider.value}: {e}")
                print(f"❌ Failed: {e}")
                continue

        raise RuntimeError(f"All providers failed: {errors}")

    async def stream(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream a response with automatic failover."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        for config in self.models:
            try:
                client = self.clients[config.provider]
                async for chunk in client.stream(messages, config):
                    yield chunk
                return
            except Exception:
                continue

        raise RuntimeError("All providers failed for streaming")


# =============================================================================
# MAIN
# =============================================================================

async def main():
    """Run multi-provider demo."""
    if len(sys.argv) < 2:
        print("Usage: python multi_provider_client.py '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]

    print("\n🌐 Multi-Provider LLM Client")
    print(f"📝 Prompt: {prompt}\n")
    print("-" * 50)

    client = MultiProviderClient()

    try:
        response = await client.generate(
            prompt=prompt,
            system="You are a helpful assistant. Be concise."
        )

        print(f"\n📤 Response from {response.provider.value}/{response.model}:")
        print("-" * 50)
        print(response.content)
        print("-" * 50)
        print(f"📊 Tokens: {response.usage}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
