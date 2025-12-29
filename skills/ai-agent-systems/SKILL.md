---
name: ai-agent-systems
description: Build intelligent AI agents with LangChain, RAG pipelines, vector databases, tool use, multi-agent systems, and autonomous agents. Use when developing conversational AI, agents, and retrieval-augmented generation systems.
---

# AI Agent Systems

Master AI agent development with LangChain, retrieval-augmented generation (RAG), vector databases, tool integration, and multi-agent architectures.

## Quick Start

### Basic LangChain Agent
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Define tools
@tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [calculate_sum, get_weather]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use agent
result = executor.invoke({"input": "What's 5 + 3 and the weather in NYC?"})
print(result["output"])
```

## RAG Pipelines

### Basic RAG System
```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Load documents
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Create RAG chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# Query
answer = qa_chain.invoke({"query": "What is the main topic?"})
print(answer["result"])
```

### Advanced RAG with Metadata
```python
from langchain.chains import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMCompressor
from langchain.retrievers.document_compressors import EmbeddingsFilter

# Base retriever
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Filter by relevance
embeddings_filter = EmbeddingsFilter(
    embeddings=embeddings,
    similarity_threshold=0.76
)

# Compress results with LLM
compressor = LLMCompressor.from_llm_and_filter(llm, embeddings_filter)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Create chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compression_retriever
)
```

## Vector Databases

### FAISS
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Create FAISS store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Search
results = vectorstore.similarity_search("query", k=3)
for doc in results:
    print(doc.page_content)

# Save and load
vectorstore.save_local("faiss_index")
loaded_vectorstore = FAISS.load_local("faiss_index", embeddings)
```

### Pinecone
```python
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Initialize Pinecone
pc = Pinecone(api_key="api-key")
index = pc.Index("index-name")

# Create vector store
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="content"
)

# Add documents
vectorstore.add_documents(chunks)

# Search
results = vectorstore.similarity_search("query", k=3)
```

### Chroma
```python
from langchain_community.vectorstores import Chroma

# Create Chroma store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Query
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
results = retriever.get_relevant_documents("query")
```

## Tool Use

### Custom Tool Implementation
```python
from langchain_core.tools import tool, ToolException
from typing import Any
import json

@tool(error_handling="raise")
def fetch_api(endpoint: str, method: str = "GET") -> str:
    """Fetch data from an API endpoint."""
    if not endpoint.startswith("https://"):
        raise ToolException("Invalid URL")

    import requests
    response = requests.request(method, endpoint)
    return response.json()

@tool
def calculate_discount(price: float, discount_percent: float) -> dict:
    """Calculate discount on a price."""
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return {
        "original": price,
        "discount": discount_amount,
        "final": final_price
    }

# Use in agent
tools = [fetch_api, calculate_discount]
```

### Tool Input Validation
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    operation: str = Field(description="Mathematical operation: add, subtract, multiply, divide")
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

@tool("calculator", args_schema=CalculatorInput)
def calculator(operation: str, a: float, b: float) -> float:
    """Perform mathematical operations."""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else None
    }
    return operations.get(operation)
```

## Multi-Agent Systems

### Agent Team with Supervisor
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Define specialist agents
@tool
def research_tool(topic: str) -> str:
    """Research information on a topic."""
    return f"Research results for {topic}"

@tool
def analysis_tool(data: str) -> str:
    """Analyze data and provide insights."""
    return f"Analysis of: {data}"

# Create agents
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Research Agent
research_agent = create_tool_calling_agent(
    llm, [research_tool],
    ChatPromptTemplate.from_messages([
        ("system", "You are a research specialist."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
)
research_executor = AgentExecutor(agent=research_agent, tools=[research_tool])

# Analysis Agent
analysis_agent = create_tool_calling_agent(
    llm, [analysis_tool],
    ChatPromptTemplate.from_messages([
        ("system", "You are a data analyst."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
)
analysis_executor = AgentExecutor(agent=analysis_agent, tools=[analysis_tool])

# Supervisor
supervisor_tools = [research_executor, analysis_executor]
```

### Sequential Agent Chain
```python
from langchain.chains import SequentialChain
from langchain.chains import LLMChain

# First agent processes input
chain1 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Summarize: {text}")
)

# Second agent uses output
chain2 = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Analyze sentiment: {summary}")
)

# Sequential execution
overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["text"],
    output_variables=["output"]
)

result = overall_chain({"text": "Your input text"})
```

## Autonomous Agents

### ReAct Pattern (Reasoning + Acting)
```python
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Agent with memory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Think step by step."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
    ("human", "{chat_history}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Conversational interaction
executor.invoke({"input": "Help me with this task"})
```

### Agentic Loop with State
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    input: str
    chat_history: Annotated[list, operator.add]
    output: str

# Define workflow
workflow = StateGraph(AgentState)

def agent_node(state: AgentState):
    # Agent logic
    response = executor.invoke({"input": state["input"]})
    return {
        "output": response["output"],
        "chat_history": [{"role": "assistant", "content": response["output"]}]
    }

def should_continue(state: AgentState):
    if "final answer" in state["output"].lower():
        return END
    return "agent"

# Add nodes and edges
workflow.add_node("agent", agent_node)
workflow.add_conditional_edges("agent", should_continue)
workflow.set_entry_point("agent")

# Compile and run
graph = workflow.compile()
result = graph.invoke({"input": "Your query", "chat_history": []})
```

## Chains and Chains of Thought

### Simple Chain
```python
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

template = "You are a helpful assistant. Answer this question: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(question="What is Python?")
```

### Chain of Thought Prompting
```python
prompt = ChatPromptTemplate.from_template("""
You are an expert problem solver.

Solve this step by step:
1. First, understand the problem
2. Then, develop a strategy
3. Finally, provide the solution

Problem: {problem}

Let's think step by step:
""")

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(problem="Your problem")
```

## Memory Management

### Conversation Buffer
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.save_context({"input": "Hi"}, {"output": "Hello!"})
history = memory.load_memory_variables({})
```

### Conversation Summary
```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history")
```

## Best Practices

✅ **Clear tool descriptions** for accurate tool selection
✅ **Proper error handling** in tools
✅ **Validate inputs** using Pydantic schemas
✅ **Use streaming** for better UX
✅ **Implement memory** for context awareness
✅ **Test agent behavior** thoroughly
✅ **Monitor token usage** and costs
✅ **Use appropriate LLM models** for tasks
✅ **Implement fallbacks** for tool failures

## Common Pitfalls

❌ Vague tool descriptions leading to wrong selections
❌ No error handling in tools
❌ Infinite loops in agent logic
❌ Token limit exceeded with large contexts
❌ No fallback when tools fail
❌ Over-complex agent hierarchies
❌ Hardcoding API credentials
❌ Not testing edge cases

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenAI API](https://platform.openai.com/docs/)
- [RAG Best Practices](https://www.promptingguide.ai/)
- [Agent Design Patterns](https://www.anthropic.com/research)
