import tempfile
import unittest
from pathlib import Path

from opt.ark.runtime.bus import EventRecord, LocalEventBus


class EventBusTests(unittest.TestCase):
    def test_event_bus_appends_jsonl_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            bus = LocalEventBus(Path(tmp))
            event = bus.append(EventRecord('event:1', 'policy.accepted', 'corr:1', 'ark:policy', {'ok': True}))
            self.assertEqual(event.event_id, 'event:1')
            records = bus.read_all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['event_type'], 'policy.accepted')


if __name__ == '__main__':
    unittest.main()
