from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AgentIdentity:
    agent_id: str
    role: str
    authority: str

    def validate(self) -> 'AgentIdentity':
        if not self.agent_id:
            raise ValueError('agent_id is required')
        if not self.role:
            raise ValueError('role is required')
        if not self.authority:
            raise ValueError('authority is required')
        return self


@dataclass(frozen=True)
class AgentHeartbeat:
    agent_id: str
    role: str
    authority: str
    status: str = 'ready'
    message: str = 'status stub online'
    created_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'authority': self.authority,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at,
            'metadata': dict(self.metadata),
        }


@dataclass(frozen=True)
class RuntimeAgent:
    identity: AgentIdentity

    def heartbeat(self) -> AgentHeartbeat:
        self.identity.validate()
        return AgentHeartbeat(
            agent_id=self.identity.agent_id,
            role=self.identity.role,
            authority=self.identity.authority,
        )
