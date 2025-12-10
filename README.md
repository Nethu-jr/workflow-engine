# Minimal Agent Workflow Engine  
A lightweight workflow/graph execution engine built with **FastAPI**, designed as part of an AI Engineering Assignment.  
This project demonstrates how to design, register, and execute rule-based workflows using a shared state dictionary, a tool registry, and a simple graph engine with branching & looping support.

---

## Features

### ✔️ Workflow Engine
- Node-based execution system  
- Each node is a Python function (a "tool")  
- Shared mutable **state dict** across all nodes  
- Node returns can modify state  
- Supports:
  - Sequential workflows  
  - Branching  
  - Looping via special `_next` override  
  - Execution logs  
  - Error handling  

### ✔️ Graph Management
- Create custom graphs via API  
- Define nodes, edges, and start points  
- Reusable tool functions  

### ✔️ FastAPI Endpoints
- `POST /graph/create` → Create a workflow graph  
- `POST /graph/run` → Execute a graph with initial state  
- `GET /graph/state/{run_id}` → Fetch status, final state, and logs  

### ✔️ Built-In Example Workflow  
Includes **Option A: Code Review Mini-Agent** (rule-based):
1. `extract_functions`  
2. `check_complexity`  
3. `detect_basic_issues`  
4. `suggest_improvements`  
5. `evaluate_quality` (loops until threshold is met)

---

## 📂 Project Structure
