from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class EventRecord:
    event_id: str
    event_type: str
    correlation_id: str
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    evidence_ref: str = ''
    created_at: str = field(default_factory=utc_now_iso)

    def validate(self):
        required = {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'correlation_id': self.correlation_id,
            'source': self.source,
            'created_at': self.created_at,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError('EventRecord missing required fields: ' + ', '.join(missing))
        if not isinstance(self.payload, Mapping):
            raise ValueError('payload must be a mapping')
        return self

    def as_dict(self):
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'correlation_id': self.correlation_id,
            'source': self.source,
            'payload': dict(self.payload),
            'evidence_ref': self.evidence_ref,
            'created_at': self.created_at,
        }
