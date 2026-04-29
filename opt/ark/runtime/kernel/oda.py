from dataclasses import dataclass, field
from typing import Any, Mapping
from .exceptions import ContractViolation

@dataclass(frozen=True)
class ODAFrame:
    observation_ref: str
    decision_ref: str
    action_ref: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self):
        missing=[k for k,v in {'observation_ref':self.observation_ref,'decision_ref':self.decision_ref,'action_ref':self.action_ref}.items() if not v]
        if missing:
            raise ContractViolation('ODAFrame missing required refs: '+', '.join(missing))
        return self

    def as_dict(self):
        return {'observation_ref':self.observation_ref,'decision_ref':self.decision_ref,'action_ref':self.action_ref,'metadata':dict(self.metadata)}
