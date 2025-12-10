from typing import Any, Dict
from uuid import UUID
from .registry import get_tool
from .models import ExecutionStepLog, RunStatus
from .storage import storage

class WorkflowEngine:
    def __init__(self):
        self.max_steps = 500

    async def run_graph(self, gid: UUID, initial_state: Dict[str, Any]):
        graph = storage.get_graph(gid)
        run = storage.create_run(gid, initial_state)
        state = initial_state.copy()
        node = graph.start_node
        step = 0

        try:
            while node and step < self.max_steps:
                step += 1
                tool = get_tool(node)
                result = tool(state) or {}

                for k, v in result.items():
                    if k != "_next":
                        state[k] = v

                storage.update_run(
                    run.id,
                    state=state,
                    step_log=ExecutionStepLog(step, node, state.copy()),
                )

                next_node = result.get("_next") or graph.edges.get(node)
                node = next_node

            storage.update_run(run.id, status=RunStatus.COMPLETED, state=state)

        except Exception as e:
            storage.update_run(run.id, status=RunStatus.FAILED, error=str(e), state=state)

        return run.id

engine = WorkflowEngine()
