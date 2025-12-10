from .storage import storage
from .registry import register_tool

@register_tool("extract_functions")
def extract_functions(state):
    code = state.get("code", "")
    funcs = []
    for l in code.splitlines():
        if l.strip().startswith("def "):
            funcs.append(l.split("def ")[1].split("(")[0])
    return {"functions": funcs, "function_count": len(funcs)}

@register_tool("check_complexity")
def check_complexity(state):
    code = state.get("code","")
    score = sum(code.count(k) for k in [" if ", " for ", " while ", " elif "])
    fn = max(state.get("function_count",1),1)
    return {"complexity": score/fn}

@register_tool("detect_basic_issues")
def detect_issues(state):
    code = state.get("code","")
    issues=[]
    if "TODO" in code: issues.append("todo")
    if "print(" in code: issues.append("debug print")
    return {"issues": issues, "issue_count": len(issues)}

@register_tool("suggest_improvements")
def suggest(state):
    out=[]
    if state.get("issue_count",0)>0: out.append("Fix issues")
    if state.get("complexity",0)>5: out.append("Reduce complexity")
    if not out: out.append("Looks good")
    return {"suggestions":out}

@register_tool("evaluate_quality")
def evaluate(state):
    score=1
    score -= min(state.get("complexity",0)*0.05,0.5)
    score -= min(state.get("issue_count",0)*0.1,0.4)
    thr = state.get("quality_threshold",0.8)
    res={"quality_score":score}
    if score < thr:
        res["_next"]="suggest_improvements"
    return res

def register_default_workflow():
    return storage.create_graph(
        "code_review",
        ["extract_functions","check_complexity","detect_basic_issues","suggest_improvements","evaluate_quality"],
        {
            "extract_functions":"check_complexity",
            "check_complexity":"detect_basic_issues",
            "detect_basic_issues":"suggest_improvements",
            "suggest_improvements":"evaluate_quality",
            "evaluate_quality":None
        },
        "extract_functions"
    ).id
