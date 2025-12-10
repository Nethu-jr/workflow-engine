from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class GraphCreateRequest(BaseModel):
    name: str
    nodes: List[str]
    edges: Dict[str, Optional[str]]
    start_node: str

class GraphCreateResponse(BaseModel):
    graph_id: UUID

class GraphRunRequest(BaseModel):
    graph_id: UUID
    initial_state: Dict[str, Any]

class ExecutionStepLog(BaseModel):
    step_index: int
    node_id: str
    state_snapshot: Dict[str, Any]

class GraphRunResponse(BaseModel):
    run_id: UUID
    final_state: Dict[str, Any]
    log: List[ExecutionStepLog]

class RunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class RunStateResponse(BaseModel):
    run_id: UUID
    graph_id: UUID
    status: RunStatus
    current_state: Dict[str, Any]
    log: List[ExecutionStepLog]
    error: Optional[str] = None
