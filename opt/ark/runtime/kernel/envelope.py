from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from .checkpoints import Checkpoint
from .cube import CubeState
from .oda import ODAFrame
from .exceptions import ContractViolation

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class OperationEnvelope:
    envelope_id: str
    requested_by: str
    cube: CubeState
    oda: ODAFrame
    aletheia_ref: str
    joey_plan_ref: str
    hrm_approval_ref: str
    checkpoint: Checkpoint
    action_intent_ref: str
    dry_run: bool = True
    created_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self):
        missing=[k for k,v in {'envelope_id':self.envelope_id,'requested_by':self.requested_by,'aletheia_ref':self.aletheia_ref,'joey_plan_ref':self.joey_plan_ref,'hrm_approval_ref':self.hrm_approval_ref,'action_intent_ref':self.action_intent_ref,'created_at':self.created_at}.items() if not v]
        if missing:
            raise ContractViolation('OperationEnvelope missing required fields: '+', '.join(missing))
        self.cube.validate(); self.oda.validate(); self.checkpoint.validate()
        if self.checkpoint.envelope_id != self.envelope_id:
            raise ContractViolation('checkpoint.envelope_id must match envelope_id')
        return self

    def required_refs(self):
        return {'aletheia_ref':self.aletheia_ref,'joey_plan_ref':self.joey_plan_ref,'hrm_approval_ref':self.hrm_approval_ref,'checkpoint_ref':self.checkpoint.as_ref(),'action_intent_ref':self.action_intent_ref}

    def as_dict(self):
        return {'envelope_id':self.envelope_id,'requested_by':self.requested_by,'cube':self.cube.as_dict(),'oda':self.oda.as_dict(),'aletheia_ref':self.aletheia_ref,'joey_plan_ref':self.joey_plan_ref,'hrm_approval_ref':self.hrm_approval_ref,'checkpoint':self.checkpoint.as_dict(),'action_intent_ref':self.action_intent_ref,'dry_run':self.dry_run,'created_at':self.created_at,'metadata':dict(self.metadata)}
