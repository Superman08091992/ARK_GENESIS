import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
from threading import Thread

from opt.ark.runtime.bus import EventRecord, LocalEventBus
from opt.ark.runtime.evidence import EvidenceWriter
from opt.ark.runtime.api import RuntimeStatusReader, make_server


class RuntimeStatusApiTests(unittest.TestCase):
    def test_status_reader_counts_bus_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = EvidenceWriter(root / 'evidence').write(
                kind='test',
                correlation_id='corr:1',
                subject_ref='subject:1',
                payload={'ok': True},
            )
            LocalEventBus(root / 'bus').append(EventRecord(
                'event:1',
                'test.event',
                'corr:1',
                'test',
                {'ok': True},
                evidence.as_ref(),
            ))
            status = RuntimeStatusReader(root).read_status()
            self.assertEqual(status['bus']['event_count'], 1)
            self.assertEqual(status['evidence']['record_count'], 1)
            self.assertEqual(status['authority']['mode'], 'dry_run_only')

    def test_local_api_health_and_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            server = make_server('127.0.0.1', 0, Path(tmp))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                port = server.server_address[1]
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2) as response:
                    health = json.loads(response.read().decode('utf-8'))
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/status', timeout=2) as response:
                    status = json.loads(response.read().decode('utf-8'))
                self.assertTrue(health['ok'])
                self.assertEqual(status['authority']['mode'], 'dry_run_only')
            finally:
                server.shutdown()
                server.server_close()


if __name__ == '__main__':
    unittest.main()
