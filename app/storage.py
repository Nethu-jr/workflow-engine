from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from .models import ExecutionStepLog, RunStatus

@dataclass
class GraphDefinition:
    id: UUID
    name: str
    nodes: List[str]
    edges: Dict[str, Optional[str]]
    start_node: str

@dataclass
class RunRecord:
    id: UUID
    graph_id: UUID
    status: RunStatus = RunStatus.RUNNING
    current_state: Dict[str, Any] = field(default_factory=dict)
    log: List[ExecutionStepLog] = field(default_factory=list)
    error: Optional[str] = None

class InMemoryStorage:
    def __init__(self):
        self.graphs = {}
        self.runs = {}

    def create_graph(self, name, nodes, edges, start_node):
        g = GraphDefinition(uuid4(), name, nodes, edges, start_node)
        self.graphs[g.id] = g
        return g

    def get_graph(self, gid):
        return self.graphs[gid]

    def create_run(self, gid, state):
        r = RunRecord(uuid4(), gid, current_state=state.copy())
        self.runs[r.id] = r
        return r

    def update_run(self, rid, **kwargs):
        r = self.runs[rid]
        for k, v in kwargs.items():
            if v is not None:
                setattr(r, k, v)
        return r

    def get_run(self, rid):
        return self.runs[rid]

storage = InMemoryStorage()
