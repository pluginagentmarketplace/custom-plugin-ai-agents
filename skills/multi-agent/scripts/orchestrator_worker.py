#!/usr/bin/env python3
"""
Orchestrator-Worker Multi-Agent System
=======================================

Production implementation of the Orchestrator-Worker pattern.
Based on Anthropic's "Building Effective Agents" recommendations.

Requirements:
    pip install langgraph langchain-anthropic

Usage:
    python orchestrator_worker.py "Research AI safety and write a summary report"
"""

import sys
import os
from typing import Annotated, TypedDict, List, Literal, Optional
from dataclasses import dataclass
from enum import Enum
import json

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# =============================================================================
# CONFIGURATION
# =============================================================================

class WorkerType(Enum):
    """Available worker types."""
    RESEARCHER = "researcher"
    WRITER = "writer"
    ANALYST = "analyst"
    CODER = "coder"
    REVIEWER = "reviewer"


@dataclass
class WorkerConfig:
    """Configuration for a worker agent."""
    type: WorkerType
    system_prompt: str
    capabilities: List[str]


WORKER_CONFIGS = {
    WorkerType.RESEARCHER: WorkerConfig(
        type=WorkerType.RESEARCHER,
        system_prompt="""You are a Research Specialist.
Your role is to gather information, find relevant sources, and compile research notes.
Be thorough and cite your sources. Focus on accuracy over speed.""",
        capabilities=["web_search", "document_analysis", "source_verification"]
    ),
    WorkerType.WRITER: WorkerConfig(
        type=WorkerType.WRITER,
        system_prompt="""You are a Content Writer.
Your role is to create clear, well-structured written content.
Focus on readability, proper formatting, and engaging prose.""",
        capabilities=["content_creation", "editing", "formatting"]
    ),
    WorkerType.ANALYST: WorkerConfig(
        type=WorkerType.ANALYST,
        system_prompt="""You are a Data Analyst.
Your role is to analyze information, identify patterns, and provide insights.
Use data-driven reasoning and present findings clearly.""",
        capabilities=["data_analysis", "pattern_recognition", "visualization"]
    ),
    WorkerType.CODER: WorkerConfig(
        type=WorkerType.CODER,
        system_prompt="""You are a Software Developer.
Your role is to write, debug, and optimize code.
Follow best practices, write clean code, and include documentation.""",
        capabilities=["code_generation", "debugging", "optimization"]
    ),
    WorkerType.REVIEWER: WorkerConfig(
        type=WorkerType.REVIEWER,
        system_prompt="""You are a Quality Reviewer.
Your role is to review work, check for errors, and suggest improvements.
Be thorough but constructive in your feedback.""",
        capabilities=["quality_assurance", "fact_checking", "proofreading"]
    ),
}


# =============================================================================
# STATE DEFINITION
# =============================================================================

@dataclass
class Task:
    """A task assigned to a worker."""
    id: str
    description: str
    worker_type: WorkerType
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class OrchestratorState(TypedDict):
    """State for the orchestrator-worker system."""
    messages: Annotated[list, add_messages]
    original_request: str
    plan: List[dict]
    tasks: List[dict]
    current_task_idx: int
    results: dict
    final_output: str
    status: str  # planning, executing, synthesizing, complete


# =============================================================================
# ORCHESTRATOR
# =============================================================================

def create_plan(state: OrchestratorState) -> OrchestratorState:
    """
    Orchestrator creates execution plan.

    Analyzes the request and breaks it into tasks.
    """
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=2048)

    planning_prompt = f"""Analyze this request and create an execution plan.

REQUEST: {state['original_request']}

Available worker types and their capabilities:
{json.dumps({w.value: {"capabilities": c.capabilities} for w, c in WORKER_CONFIGS.items()}, indent=2)}

Create a plan with ordered tasks. Each task should specify:
1. task_id: Unique identifier (e.g., "task_1")
2. description: What needs to be done
3. worker_type: Which worker should handle it
4. dependencies: List of task_ids that must complete first

Respond in JSON format:
{{
    "plan_summary": "Brief description of the approach",
    "tasks": [
        {{
            "task_id": "task_1",
            "description": "...",
            "worker_type": "researcher|writer|analyst|coder|reviewer",
            "dependencies": []
        }}
    ]
}}"""

    response = llm.invoke([
        SystemMessage(content="You are an orchestrator that breaks down complex requests into tasks."),
        HumanMessage(content=planning_prompt)
    ])

    # Parse plan
    try:
        # Extract JSON from response
        content = response.content
        start = content.find("{")
        end = content.rfind("}") + 1
        plan_data = json.loads(content[start:end])

        tasks = []
        for t in plan_data["tasks"]:
            tasks.append({
                "id": t["task_id"],
                "description": t["description"],
                "worker_type": t["worker_type"],
                "status": "pending",
                "result": None,
                "dependencies": t.get("dependencies", [])
            })

        print(f"\n📋 Plan created with {len(tasks)} tasks")
        for t in tasks:
            print(f"   - {t['id']}: {t['description'][:50]}... ({t['worker_type']})")

    except Exception as e:
        print(f"⚠️ Plan parsing failed: {e}")
        tasks = [{
            "id": "task_1",
            "description": state["original_request"],
            "worker_type": "researcher",
            "status": "pending",
            "result": None,
            "dependencies": []
        }]

    return {
        **state,
        "plan": plan_data.get("tasks", []) if 'plan_data' in dir() else [],
        "tasks": tasks,
        "current_task_idx": 0,
        "status": "executing"
    }


def execute_task(state: OrchestratorState) -> OrchestratorState:
    """
    Execute current task using appropriate worker.
    """
    from langchain_anthropic import ChatAnthropic

    tasks = state["tasks"]
    idx = state["current_task_idx"]

    if idx >= len(tasks):
        return {**state, "status": "synthesizing"}

    task = tasks[idx]

    # Check dependencies
    for dep_id in task["dependencies"]:
        dep_task = next((t for t in tasks if t["id"] == dep_id), None)
        if dep_task and dep_task["status"] != "completed":
            print(f"⏳ Waiting for dependency: {dep_id}")
            return state

    print(f"\n🔧 Executing {task['id']}: {task['description'][:50]}...")

    # Get worker config
    worker_type = WorkerType(task["worker_type"])
    config = WORKER_CONFIGS[worker_type]

    # Build context from completed tasks
    context = ""
    for t in tasks:
        if t["status"] == "completed" and t["result"]:
            context += f"\n[{t['id']} Result]:\n{t['result']}\n"

    # Execute with worker
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=2048)

    worker_prompt = f"""Complete this task:

TASK: {task['description']}

ORIGINAL REQUEST: {state['original_request']}

{f"CONTEXT FROM PREVIOUS TASKS:{context}" if context else ""}

Provide your output directly. Be thorough and focused on the task."""

    response = llm.invoke([
        SystemMessage(content=config.system_prompt),
        HumanMessage(content=worker_prompt)
    ])

    # Update task
    task["status"] = "completed"
    task["result"] = response.content

    print(f"   ✅ Completed: {response.content[:100]}...")

    # Update results
    results = state.get("results", {})
    results[task["id"]] = response.content

    return {
        **state,
        "tasks": tasks,
        "current_task_idx": idx + 1,
        "results": results
    }


def synthesize_results(state: OrchestratorState) -> OrchestratorState:
    """
    Orchestrator synthesizes all results into final output.
    """
    from langchain_anthropic import ChatAnthropic

    print("\n📊 Synthesizing results...")

    llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=4096)

    # Compile all results
    results_text = ""
    for task in state["tasks"]:
        if task["result"]:
            results_text += f"\n## {task['id']}: {task['description']}\n{task['result']}\n"

    synthesis_prompt = f"""Synthesize these task results into a final, cohesive response.

ORIGINAL REQUEST: {state['original_request']}

TASK RESULTS:
{results_text}

Create a well-organized final response that:
1. Addresses the original request completely
2. Integrates insights from all tasks
3. Is clear and actionable
4. Highlights key findings or recommendations"""

    response = llm.invoke([
        SystemMessage(content="You are an orchestrator synthesizing work from multiple specialists."),
        HumanMessage(content=synthesis_prompt)
    ])

    return {
        **state,
        "final_output": response.content,
        "status": "complete"
    }


# =============================================================================
# ROUTING
# =============================================================================

def route_orchestrator(state: OrchestratorState) -> Literal["execute", "synthesize", "end"]:
    """Route based on current state."""
    status = state["status"]

    if status == "executing":
        if state["current_task_idx"] < len(state["tasks"]):
            return "execute"
        return "synthesize"
    elif status == "synthesizing":
        return "synthesize"
    else:
        return "end"


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def build_orchestrator_system() -> StateGraph:
    """Build the orchestrator-worker graph."""

    graph = StateGraph(OrchestratorState)

    # Add nodes
    graph.add_node("plan", create_plan)
    graph.add_node("execute", execute_task)
    graph.add_node("synthesize", synthesize_results)

    # Set entry point
    graph.set_entry_point("plan")

    # Add edges
    graph.add_conditional_edges(
        "plan",
        route_orchestrator,
        {"execute": "execute", "synthesize": "synthesize", "end": END}
    )
    graph.add_conditional_edges(
        "execute",
        route_orchestrator,
        {"execute": "execute", "synthesize": "synthesize", "end": END}
    )
    graph.add_edge("synthesize", END)

    return graph.compile()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run orchestrator-worker demo."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator_worker.py '<complex request>'")
        print("\nExample requests:")
        print("  - 'Research AI safety trends and write a summary'")
        print("  - 'Analyze our sales data and create a report with recommendations'")
        print("  - 'Review this code, fix bugs, and add documentation'")
        sys.exit(1)

    request = sys.argv[1]

    print("\n🎭 Orchestrator-Worker Multi-Agent System")
    print(f"📝 Request: {request}")
    print("=" * 60)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    # Build system
    system = build_orchestrator_system()

    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=request)],
        "original_request": request,
        "plan": [],
        "tasks": [],
        "current_task_idx": 0,
        "results": {},
        "final_output": "",
        "status": "planning"
    }

    # Run system
    final_state = None
    for event in system.stream(initial_state):
        for node, state in event.items():
            final_state = state

    print("\n" + "=" * 60)
    print("📤 FINAL OUTPUT")
    print("=" * 60)

    if final_state and final_state.get("final_output"):
        print(final_state["final_output"])
    else:
        print("No output generated")

    print("\n📊 Execution Summary:")
    if final_state:
        print(f"   - Tasks executed: {len(final_state.get('tasks', []))}")
        completed = sum(1 for t in final_state.get('tasks', []) if t['status'] == 'completed')
        print(f"   - Tasks completed: {completed}")


if __name__ == "__main__":
    main()
