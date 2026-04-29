from dataclasses import dataclass
from .exceptions import PolicyDenied

@dataclass(frozen=True)
class AuthorityRefs:
    requested_by: str
    aletheia_ref: str
    joey_plan_ref: str
    hrm_approval_ref: str
    checkpoint_ref: str

    def validate(self):
        missing=[k for k,v in self.__dict__.items() if not v]
        if missing:
            raise PolicyDenied('authority refs missing: '+', '.join(missing))
        if not self.aletheia_ref.startswith('aletheia:'):
            raise PolicyDenied("aletheia_ref must start with 'aletheia:'")
        if not self.joey_plan_ref.startswith('joey:'):
            raise PolicyDenied("joey_plan_ref must start with 'joey:'")
        if not self.hrm_approval_ref.startswith('hrm:'):
            raise PolicyDenied("hrm_approval_ref must start with 'hrm:'")
        if not self.checkpoint_ref.startswith('checkpoint:'):
            raise PolicyDenied("checkpoint_ref must start with 'checkpoint:'")
        return self
