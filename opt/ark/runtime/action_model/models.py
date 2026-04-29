from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class ToolKind(str, Enum):
    NOOP='noop'; BROWSER_STUB='browser_stub'; FILE_STUB='file_stub'; SHELL_STUB='shell_stub'; ACCOUNT_STUB='account_stub'

@dataclass(frozen=True)
class ActionIntent:
    intent_id: str
    summary: str
    requested_tool: ToolKind = ToolKind.NOOP
    parameters: Mapping[str, Any] = field(default_factory=dict)
    risk_tier: str = 'SAFE'
    def validate(self):
        if not self.intent_id: raise ValueError('intent_id is required')
        if not self.summary: raise ValueError('summary is required')
        if not isinstance(self.requested_tool, ToolKind): raise ValueError('requested_tool must be ToolKind')
        return self

@dataclass(frozen=True)
class ActionStep:
    step_id: str
    tool: ToolKind
    instruction: str
    dry_run: bool = True
    parameters: Mapping[str, Any] = field(default_factory=dict)
    def validate(self):
        if not self.step_id: raise ValueError('step_id is required')
        if not isinstance(self.tool, ToolKind): raise ValueError('tool must be ToolKind')
        if not self.instruction: raise ValueError('instruction is required')
        return self

@dataclass(frozen=True)
class ActionPlan:
    plan_id: str
    envelope_id: str
    steps: tuple
    dry_run: bool = True
    policy_decision_ref: str = ''
    def validate(self):
        if not self.plan_id: raise ValueError('plan_id is required')
        if not self.envelope_id: raise ValueError('envelope_id is required')
        if not self.steps: raise ValueError('at least one ActionStep is required')
        for step in self.steps:
            step.validate()
            if not self.dry_run or not step.dry_run: raise ValueError('v0.1 ActionPlan must be dry_run')
        return self
