from dataclasses import dataclass
from opt.ark.runtime.action_model.models import ActionPlan
from .policy import BrokerPolicy
from .tools import ToolResult, run_stub_tool

@dataclass(frozen=True)
class BrokerRun:
    plan_id: str
    results: tuple
    ok: bool
    dry_run: bool
    @property
    def result_refs(self):
        return tuple(result.artifact_ref for result in self.results)

@dataclass(frozen=True)
class ExecutionBroker:
    policy: BrokerPolicy = BrokerPolicy()
    def run(self, plan: ActionPlan) -> BrokerRun:
        plan.validate()
        results=[]
        for step in plan.steps:
            self.policy.validate_tool(step.tool, dry_run=step.dry_run)
            results.append(run_stub_tool(step))
        return BrokerRun(plan.plan_id, tuple(results), all(r.ok for r in results), True)
