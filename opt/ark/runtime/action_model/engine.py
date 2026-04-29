from dataclasses import dataclass
from opt.ark.runtime.kernel.envelope import OperationEnvelope
from opt.ark.runtime.policy.action_preconditions import PolicyDecision
from .exceptions import UnauthorizedActionIntent
from .models import ActionIntent, ActionPlan, ActionStep

@dataclass(frozen=True)
class ActionModelEngine:
    def translate(self, *, intent: ActionIntent, envelope: OperationEnvelope, policy_decision: PolicyDecision) -> ActionPlan:
        intent.validate(); envelope.validate()
        if not policy_decision.allowed:
            raise UnauthorizedActionIntent('AEM cannot translate without allowed policy decision')
        if policy_decision.envelope_id != envelope.envelope_id:
            raise UnauthorizedActionIntent('policy decision envelope_id mismatch')
        if not policy_decision.dry_run:
            raise UnauthorizedActionIntent('v0.1 AEM only accepts dry_run policy decisions')
        step=ActionStep('step:'+intent.intent_id+':001', intent.requested_tool, intent.summary, True, dict(intent.parameters))
        return ActionPlan('aem-plan:'+intent.intent_id, envelope.envelope_id, (step,), True, 'policy:'+envelope.envelope_id).validate()
