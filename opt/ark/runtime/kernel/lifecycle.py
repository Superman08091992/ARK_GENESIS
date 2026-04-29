from dataclasses import dataclass
from enum import Enum
from .exceptions import InvalidTransition

class LifecycleState(str, Enum):
    RECEIVED='received'; VERIFIED='verified'; STRUCTURED='structured'; APPROVED='approved'; POLICY_ACCEPTED='policy_accepted'; TRANSLATED='translated'; BROKERED='brokered'; RECORDED='recorded'; BLOCKED='blocked'

_ALLOWED={
    LifecycleState.RECEIVED:{LifecycleState.VERIFIED,LifecycleState.BLOCKED},
    LifecycleState.VERIFIED:{LifecycleState.STRUCTURED,LifecycleState.BLOCKED},
    LifecycleState.STRUCTURED:{LifecycleState.APPROVED,LifecycleState.BLOCKED},
    LifecycleState.APPROVED:{LifecycleState.POLICY_ACCEPTED,LifecycleState.BLOCKED},
    LifecycleState.POLICY_ACCEPTED:{LifecycleState.TRANSLATED,LifecycleState.BLOCKED},
    LifecycleState.TRANSLATED:{LifecycleState.BROKERED,LifecycleState.BLOCKED},
    LifecycleState.BROKERED:{LifecycleState.RECORDED,LifecycleState.BLOCKED},
    LifecycleState.RECORDED:set(), LifecycleState.BLOCKED:set(),
}

@dataclass(frozen=True)
class LifecycleRecord:
    state: LifecycleState = LifecycleState.RECEIVED
    def transition(self,next_state:LifecycleState):
        if next_state not in _ALLOWED[self.state]:
            raise InvalidTransition(f'illegal transition: {self.state.value} -> {next_state.value}')
        return LifecycleRecord(next_state)
