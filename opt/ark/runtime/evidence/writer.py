import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .hashes import sha256_data
from .manifest import EvidenceRecord

@dataclass(frozen=True)
class EvidenceWriter:
    root: Path

    def __post_init__(self):
        object.__setattr__(self, 'root', Path(self.root))

    @property
    def manifest_path(self) -> Path:
        return self.root / 'manifest.jsonl'

    def write(self, *, kind: str, correlation_id: str, subject_ref: str, payload: Mapping[str, Any], previous_hash: str = '', writer: str = 'ark:evidence-writer') -> EvidenceRecord:
        if not isinstance(payload, Mapping):
            raise ValueError('payload must be a mapping')
        payload_hash = sha256_data(payload)
        evidence_id = payload_hash[:16]
        record = EvidenceRecord(evidence_id, kind, correlation_id, subject_ref, payload_hash, dict(payload), previous_hash, writer).validate()
        target_dir = self.root / kind
        target_dir.mkdir(parents=True, exist_ok=True)
        record_path = target_dir / (record.evidence_id + '.json')
        if record_path.exists():
            existing = json.loads(record_path.read_text(encoding='utf-8'))
            if existing.get('payload_hash') != record.payload_hash:
                raise ValueError('evidence id collision with different payload')
        else:
            record_path.write_text(json.dumps(record.as_dict(), sort_keys=True, indent=2) + '\n', encoding='utf-8')
        self.root.mkdir(parents=True, exist_ok=True)
        with self.manifest_path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record.as_dict(), sort_keys=True, separators=(',', ':')) + '\n')
        return record

    def read_manifest(self):
        if not self.manifest_path.exists():
            return []
        records = []
        with self.manifest_path.open('r', encoding='utf-8') as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
