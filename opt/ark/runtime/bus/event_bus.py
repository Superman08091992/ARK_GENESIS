import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .models import EventRecord

@dataclass(frozen=True)
class LocalEventBus:
    root: Path

    def __post_init__(self):
        object.__setattr__(self, 'root', Path(self.root))

    @property
    def events_path(self) -> Path:
        return self.root / 'events.jsonl'

    def append(self, event: EventRecord) -> EventRecord:
        event.validate()
        self.root.mkdir(parents=True, exist_ok=True)
        with self.events_path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(event.as_dict(), sort_keys=True, separators=(',', ':')) + '\n')
        return event

    def append_many(self, events: Iterable[EventRecord]) -> List[EventRecord]:
        written = []
        for event in events:
            written.append(self.append(event))
        return written

    def read_all(self) -> List[dict]:
        if not self.events_path.exists():
            return []
        records = []
        with self.events_path.open('r', encoding='utf-8') as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
