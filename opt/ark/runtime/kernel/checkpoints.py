from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from .exceptions import ContractViolation

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id: str
    envelope_id: str
    state_hash: str
    created_by: str
    created_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self):
        missing=[k for k,v in {'checkpoint_id':self.checkpoint_id,'envelope_id':self.envelope_id,'state_hash':self.state_hash,'created_by':self.created_by,'created_at':self.created_at}.items() if not v]
        if missing:
            raise ContractViolation('Checkpoint missing required fields: '+', '.join(missing))
        return self

    def as_ref(self):
        return 'checkpoint:'+self.checkpoint_id

    def as_dict(self):
        return {'checkpoint_id':self.checkpoint_id,'envelope_id':self.envelope_id,'state_hash':self.state_hash,'created_by':self.created_by,'created_at':self.created_at,'metadata':dict(self.metadata)}
