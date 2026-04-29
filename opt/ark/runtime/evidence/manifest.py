from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    kind: str
    correlation_id: str
    subject_ref: str
    payload_hash: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    previous_hash: str = ''
    writer: str = 'ark:evidence-writer'
    created_at: str = field(default_factory=utc_now_iso)

    def validate(self):
        required = {
            'evidence_id': self.evidence_id,
            'kind': self.kind,
            'correlation_id': self.correlation_id,
            'subject_ref': self.subject_ref,
            'payload_hash': self.payload_hash,
            'writer': self.writer,
            'created_at': self.created_at,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError('EvidenceRecord missing required fields: ' + ', '.join(missing))
        if not isinstance(self.payload, Mapping):
            raise ValueError('payload must be a mapping')
        return self

    def as_ref(self):
        return 'evidence:' + self.evidence_id

    def as_dict(self):
        return {
            'evidence_id': self.evidence_id,
            'kind': self.kind,
            'correlation_id': self.correlation_id,
            'subject_ref': self.subject_ref,
            'payload_hash': self.payload_hash,
            'payload': dict(self.payload),
            'previous_hash': self.previous_hash,
            'writer': self.writer,
            'created_at': self.created_at,
        }
