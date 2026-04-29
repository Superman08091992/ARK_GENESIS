from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from opt.ark.runtime.bus import LocalEventBus
from opt.ark.runtime.evidence import EvidenceWriter

@dataclass(frozen=True)
class RuntimeStatusReader:
    runtime_root: Path

    def __post_init__(self):
        object.__setattr__(self, 'runtime_root', Path(self.runtime_root))

    @property
    def bus_root(self) -> Path:
        return self.runtime_root / 'bus'

    @property
    def evidence_root(self) -> Path:
        return self.runtime_root / 'evidence'

    def read_status(self) -> Dict[str, Any]:
        bus = LocalEventBus(self.bus_root)
        evidence = EvidenceWriter(self.evidence_root)
        events = bus.read_all()
        manifest = evidence.read_manifest()
        last_event = events[-1] if events else None
        last_evidence = manifest[-1] if manifest else None
        return {
            'runtime_root': str(self.runtime_root),
            'bus': {
                'path': str(bus.events_path),
                'event_count': len(events),
                'last_event': last_event,
            },
            'evidence': {
                'path': str(evidence.manifest_path),
                'record_count': len(manifest),
                'last_record': last_evidence,
            },
            'authority': {
                'mode': 'dry_run_only',
                'aem_authorizes': False,
                'broker_executes_real_tools': False,
            },
        }
