import tempfile
import unittest
from pathlib import Path

from opt.ark.runtime.evidence import EvidenceWriter, sha256_data


class EvidenceWriterTests(unittest.TestCase):
    def test_evidence_writer_persists_manifest_and_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = EvidenceWriter(Path(tmp))
            payload = {'result': 'simulated', 'ok': True}
            record = writer.write(kind='broker', correlation_id='corr:1', subject_ref='broker-result:1', payload=payload)
            self.assertEqual(record.payload_hash, sha256_data(payload))
            self.assertTrue((Path(tmp) / 'broker' / (record.evidence_id + '.json')).exists())
            self.assertEqual(len(writer.read_manifest()), 1)


if __name__ == '__main__':
    unittest.main()
