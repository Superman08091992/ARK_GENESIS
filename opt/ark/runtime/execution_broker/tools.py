from dataclasses import dataclass, field
from typing import Any, Mapping
from opt.ark.runtime.action_model.models import ActionStep, ToolKind

@dataclass(frozen=True)
class ToolResult:
    step_id: str
    tool: ToolKind
    ok: bool
    dry_run: bool
    message: str
    artifact_ref: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

def run_stub_tool(step: ActionStep) -> ToolResult:
    step.validate()
    return ToolResult(step.step_id, step.tool, True, True, 'simulated '+step.tool.value+' execution', 'broker-result:'+step.step_id, {'instruction': step.instruction, 'parameters': dict(step.parameters)})
