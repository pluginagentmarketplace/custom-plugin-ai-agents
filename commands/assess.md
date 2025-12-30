---
name: assess
description: AI Agent Skills Assessment
allowed-tools: Read
---

# AI Agent Skills Assessment

Test your understanding of AI agent development, architectures, and best practices.

## Usage

```
/assess [topic] [level]
```

**Parameters:**
- `topic`: The AI agent topic to assess
- `level`: Optional - `beginner`, `intermediate`, `advanced`, or `expert`

## Available Topics

### Core Topics
- `agent-fundamentals` - ReAct, cognitive loops, architectures
- `llm-integration` - API usage, prompting, cost optimization
- `rag-systems` - Embeddings, retrieval, chunking
- `tool-calling` - Function calling, schema design
- `multi-agent` - Orchestration, coordination
- `agent-memory` - Short/long-term, retrieval
- `agent-safety` - Guardrails, filtering, compliance

### Framework-Specific
- `langchain` - LangChain patterns and tools
- `langgraph` - State machines, workflows
- `anthropic` - Claude API, tool use
- `openai` - Function calling, assistants

## Examples

```
/assess agent-fundamentals
/assess tool-calling intermediate
/assess multi-agent advanced
/assess rag-systems beginner
```

---

## Sample Assessment: Tool Calling (Intermediate)

### Question 1: Schema Design
```python
# What's wrong with this tool definition?
{
    "name": "helper",
    "description": "Does stuff",
    "input_schema": {
        "type": "object",
        "properties": {
            "data": {"type": "any"}
        }
    }
}
```

<details>
<summary>Show Answer</summary>

**Issues:**
1. Name is too vague - use `verb_noun` pattern (e.g., `search_products`)
2. Description doesn't explain when to use
3. `"type": "any"` is not valid JSON Schema
4. Missing `required` field
5. Missing `additionalProperties: false` for strict mode

**Better:**
```python
{
    "name": "search_products",
    "description": "Search product database. USE WHEN: User asks about products.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "category": {"type": "string", "enum": ["electronics", "clothing"]}
        },
        "required": ["query"],
        "additionalProperties": false
    }
}
```
</details>

### Question 2: Error Handling
```
How should tool execution errors be returned to the LLM?
```

<details>
<summary>Show Answer</summary>

**Best Practice:** Return errors as tool results, not exceptions.

```python
# Good: Return error in result
tool_results.append({
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": json.dumps({
        "status": "error",
        "error": "Database connection failed",
        "suggestion": "Try again in a few seconds"
    })
})

# Bad: Throw exception
raise ToolExecutionError("Database connection failed")
```

The LLM can then decide how to proceed based on the error.
</details>

### Question 3: Multi-Step Tools
```
When should you use sequential vs parallel tool execution?
```

<details>
<summary>Show Answer</summary>

**Sequential:** When tools depend on each other
```python
# Step 1: Search products
products = await search_products(query)

# Step 2: Get details (depends on step 1)
details = await get_product_details(products[0].id)
```

**Parallel:** When tools are independent
```python
# These can run simultaneously
results = await asyncio.gather(
    get_weather("Tokyo"),
    get_weather("London"),
    get_weather("New York")
)
```

Use `asyncio.gather()` for parallel execution.
</details>

---

## Assessment Results

After completing an assessment, you receive:

### Score & Level
```
📊 Assessment Results: Tool Calling (Intermediate)

Score: 8/10 (80%)
Level: ✅ Intermediate Confirmed

Strengths:
✅ Schema design basics
✅ Error handling patterns
✅ Claude tool use syntax

Areas to improve:
⚠️ OpenAI strict mode configuration
⚠️ MCP (Model Context Protocol)
⚠️ Tool orchestration patterns
```

### Recommended Next Steps
```
📚 Study Plan:

1. Review OpenAI strict mode
   Skill: tool-calling (OpenAI section)

2. Learn MCP patterns
   Resource: MCP documentation

3. Practice tool orchestration
   Project: Build multi-tool agent
```

---

## Quick Assessment Types

### 1. Quick Check (5 questions)
```
/assess rag-systems quick
```

### 2. Comprehensive (20 questions)
```
/assess llm-integration comprehensive
```

### 3. Hands-On Challenge
```
/assess agent-fundamentals challenge
```

You'll get a coding challenge like:
```python
"""
Challenge: Build a ReAct Agent

Requirements:
1. Implement Thought → Action → Observation loop
2. Add max_iterations limit (10)
3. Implement circuit breaker for errors
4. Support parallel tool calls

Time: 45 minutes
"""
```

---

**Start your assessment:** `/assess [topic]`
