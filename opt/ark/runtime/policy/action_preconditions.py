from dataclasses import dataclass
from opt.ark.runtime.kernel.envelope import OperationEnvelope
from .authority import AuthorityRefs
from .exceptions import PolicyDenied
from .operator_supremacy import OperatorSupremacyPolicy

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    envelope_id: str
    dry_run: bool
    authority_refs: dict
    def require_allowed(self):
        if not self.allowed:
            raise PolicyDenied(self.reason)
        return self

@dataclass(frozen=True)
class ActionPreconditionPolicy:
    operator_policy: OperatorSupremacyPolicy = OperatorSupremacyPolicy()
    require_dry_run_v0_1: bool = True
    def evaluate(self, envelope: OperationEnvelope) -> PolicyDecision:
        try:
            envelope.validate()
            self.operator_policy.validate_requested_by(envelope.requested_by)
            refs=AuthorityRefs(envelope.requested_by,envelope.aletheia_ref,envelope.joey_plan_ref,envelope.hrm_approval_ref,envelope.checkpoint.as_ref()).validate()
            if self.require_dry_run_v0_1 and not envelope.dry_run:
                raise PolicyDenied('v0.1 policy allows dry_run only')
            return PolicyDecision(True,'policy preconditions satisfied',envelope.envelope_id,envelope.dry_run,refs.__dict__)
        except Exception as exc:
            return PolicyDecision(False,str(exc),getattr(envelope,'envelope_id',''),getattr(envelope,'dry_run',True),{})
    def require(self, envelope: OperationEnvelope) -> PolicyDecision:
        return self.evaluate(envelope).require_allowed()
