#!/usr/bin/env python3
"""
Claude Tool Use Implementation
==============================

Production-ready tool calling with Anthropic Claude.
Demonstrates complete tool use loop with error handling.

Requirements:
    pip install anthropic

Usage:
    python claude_tool_use.py "What's 25 * 47 plus the current weather in London?"
"""

import sys
import os
import json
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from anthropic import Anthropic


# =============================================================================
# TOOL DEFINITIONS
# =============================================================================

TOOLS = [
    {
        "name": "calculator",
        "description": "Perform mathematical calculations. Use this for any math operations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '25 * 47')"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name (e.g., 'London', 'New York')"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units",
                    "default": "celsius"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "search_database",
        "description": "Search a database for information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

def calculator(expression: str) -> Dict[str, Any]:
    """
    Safe calculator implementation.

    Only allows basic math operations.
    """
    # Define safe operations
    allowed_chars = set("0123456789+-*/.() ")
    allowed_funcs = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "pow": pow,
    }

    # Validate expression
    if not all(c in allowed_chars for c in expression.replace(" ", "")):
        # Check for allowed function names
        clean_expr = expression
        for func in allowed_funcs:
            clean_expr = clean_expr.replace(func, "")
        if not all(c in allowed_chars for c in clean_expr.replace(" ", "")):
            return {
                "success": False,
                "error": "Invalid characters in expression"
            }

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_funcs)
        return {
            "success": True,
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_weather(location: str, units: str = "celsius") -> Dict[str, Any]:
    """
    Weather lookup (simulated).

    In production, replace with real weather API.
    """
    # Simulated weather data
    weather_data = {
        "london": {"temp": 12, "condition": "Cloudy", "humidity": 75},
        "new york": {"temp": 18, "condition": "Sunny", "humidity": 45},
        "tokyo": {"temp": 22, "condition": "Partly cloudy", "humidity": 60},
        "paris": {"temp": 15, "condition": "Rainy", "humidity": 80},
    }

    location_lower = location.lower()

    if location_lower not in weather_data:
        return {
            "success": False,
            "error": f"Weather data not available for {location}"
        }

    data = weather_data[location_lower]
    temp = data["temp"]

    if units == "fahrenheit":
        temp = (temp * 9/5) + 32

    return {
        "success": True,
        "location": location,
        "temperature": temp,
        "units": units,
        "condition": data["condition"],
        "humidity": data["humidity"]
    }


def search_database(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Database search (simulated).

    In production, replace with real database query.
    """
    # Simulated database
    records = [
        {"id": 1, "title": "Introduction to AI", "category": "technology"},
        {"id": 2, "title": "Machine Learning Basics", "category": "technology"},
        {"id": 3, "title": "Python Programming", "category": "programming"},
        {"id": 4, "title": "Data Science Guide", "category": "technology"},
        {"id": 5, "title": "Web Development", "category": "programming"},
    ]

    # Simple search
    query_lower = query.lower()
    results = [
        r for r in records
        if query_lower in r["title"].lower() or
           query_lower in r["category"].lower()
    ][:limit]

    return {
        "success": True,
        "query": query,
        "results": results,
        "total_found": len(results)
    }


# Tool registry
TOOL_REGISTRY: Dict[str, Callable] = {
    "calculator": calculator,
    "get_weather": get_weather,
    "search_database": search_database,
}


# =============================================================================
# TOOL USE LOOP
# =============================================================================

@dataclass
class ToolUseResult:
    """Result from a tool use loop."""
    final_response: str
    tool_calls_made: List[Dict[str, Any]]
    total_iterations: int


def execute_tool(name: str, input_data: Dict[str, Any]) -> str:
    """
    Execute a tool by name.

    Args:
        name: Tool name
        input_data: Tool input parameters

    Returns:
        JSON string of tool result
    """
    if name not in TOOL_REGISTRY:
        return json.dumps({
            "success": False,
            "error": f"Unknown tool: {name}"
        })

    try:
        result = TOOL_REGISTRY[name](**input_data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        })


def run_tool_use_loop(
    prompt: str,
    system: Optional[str] = None,
    max_iterations: int = 10
) -> ToolUseResult:
    """
    Run complete tool use loop with Claude.

    Args:
        prompt: User prompt
        system: Optional system message
        max_iterations: Maximum tool use iterations

    Returns:
        ToolUseResult with final response and history
    """
    client = Anthropic()

    messages = [{"role": "user", "content": prompt}]
    tool_calls_made = []

    for iteration in range(max_iterations):
        print(f"\n🔄 Iteration {iteration + 1}")

        # Call Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system or "You are a helpful assistant with access to tools.",
            tools=TOOLS,
            messages=messages
        )

        print(f"   Stop reason: {response.stop_reason}")

        # Check if we're done
        if response.stop_reason == "end_turn":
            # Extract text response
            text_content = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text_content += block.text

            return ToolUseResult(
                final_response=text_content,
                tool_calls_made=tool_calls_made,
                total_iterations=iteration + 1
            )

        # Process tool use
        if response.stop_reason == "tool_use":
            # Add assistant response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Process each tool use block
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"   🔧 Tool: {block.name}")
                    print(f"      Input: {json.dumps(block.input)}")

                    # Execute tool
                    result = execute_tool(block.name, block.input)
                    print(f"      Result: {result[:100]}...")

                    # Record tool call
                    tool_calls_made.append({
                        "tool": block.name,
                        "input": block.input,
                        "result": json.loads(result)
                    })

                    # Add tool result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })

    # Max iterations reached
    return ToolUseResult(
        final_response="Maximum iterations reached without final response.",
        tool_calls_made=tool_calls_made,
        total_iterations=max_iterations
    )


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run tool use demo."""
    if len(sys.argv) < 2:
        print("Usage: python claude_tool_use.py '<prompt>'")
        print("\nExample prompts:")
        print("  - 'What is 25 * 47?'")
        print("  - 'What's the weather in London?'")
        print("  - 'Calculate 100/4 and tell me the weather in Tokyo'")
        sys.exit(1)

    prompt = sys.argv[1]

    print("\n🤖 Claude Tool Use Demo")
    print(f"📝 Prompt: {prompt}")
    print("-" * 50)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    # Run tool use loop
    result = run_tool_use_loop(
        prompt=prompt,
        system="You are a helpful assistant. Use the available tools to help answer questions accurately."
    )

    print("\n" + "=" * 50)
    print("📤 FINAL RESPONSE")
    print("=" * 50)
    print(result.final_response)

    print(f"\n📊 Statistics:")
    print(f"   - Total iterations: {result.total_iterations}")
    print(f"   - Tool calls made: {len(result.tool_calls_made)}")

    if result.tool_calls_made:
        print("\n🔧 Tool calls:")
        for i, call in enumerate(result.tool_calls_made):
            print(f"   {i+1}. {call['tool']}({json.dumps(call['input'])})")
            print(f"      → {json.dumps(call['result'])[:80]}...")


if __name__ == "__main__":
    main()
