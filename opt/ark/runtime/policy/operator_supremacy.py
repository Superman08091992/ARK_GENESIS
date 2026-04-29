from dataclasses import dataclass
from .exceptions import PolicyDenied

@dataclass(frozen=True)
class OperatorSupremacyPolicy:
    operator_id: str = 'operator:local'
    allow_agent_override: bool = False

    def validate_requested_by(self, requested_by: str) -> str:
        if not requested_by:
            raise PolicyDenied('requested_by is required')
        if requested_by.startswith('operator:') or requested_by.startswith('agent:'):
            return requested_by
        raise PolicyDenied('requested_by must identify an operator or agent')
