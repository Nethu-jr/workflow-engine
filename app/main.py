from fastapi import FastAPI, HTTPException
from uuid import UUID
from .models import GraphCreateRequest, GraphCreateResponse, GraphRunRequest, GraphRunResponse, RunStateResponse
from .storage import storage
from .engine import engine
from .workflows import register_default_workflow

app = FastAPI()

@app.on_event("startup")
async def startup():
    wid = register_default_workflow()
    print("Workflow registered:", wid)

@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(p: GraphCreateRequest):
    g = storage.create_graph(p.name, p.nodes, p.edges, p.start_node)
    return GraphCreateResponse(graph_id=g.id)

@app.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(p: GraphRunRequest):
    try:
        storage.get_graph(p.graph_id)
    except:
        raise HTTPException(404, "Graph not found")

    rid = await engine.run_graph(p.graph_id, p.initial_state)
    r = storage.get_run(rid)
    return GraphRunResponse(run_id=rid, final_state=r.current_state, log=r.log)

@app.get("/graph/state/{rid}", response_model=RunStateResponse)
async def state(rid: UUID):
    try:
        r = storage.get_run(rid)
    except:
        raise HTTPException(404, "Run not found")

    return RunStateResponse(
        run_id=r.id,
        graph_id=r.graph_id,
        status=r.status,
        current_state=r.current_state,
        log=r.log,
        error=r.error,
    )
