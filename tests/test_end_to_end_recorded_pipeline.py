import tempfile
import unittest
from pathlib import Path

from opt.ark.runtime.action_model import ActionIntent, ActionModelEngine, ToolKind
from opt.ark.runtime.bus import EventRecord, LocalEventBus
from opt.ark.runtime.evidence import EvidenceWriter
from opt.ark.runtime.execution_broker import ExecutionBroker
from opt.ark.runtime.policy import ActionPreconditionPolicy
from tests.helpers import make_envelope


class EndToEndRecordedPipelineTests(unittest.TestCase):
    def test_dry_run_pipeline_records_bus_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            envelope = make_envelope()
            decision = ActionPreconditionPolicy().require(envelope)
            plan = ActionModelEngine().translate(
                intent=ActionIntent('intent:1', 'simulate recorded noop', ToolKind.NOOP),
                envelope=envelope,
                policy_decision=decision,
            )
            run = ExecutionBroker().run(plan)

            writer = EvidenceWriter(root / 'evidence')
            evidence = writer.write(
                kind='broker',
                correlation_id=envelope.envelope_id,
                subject_ref=run.result_refs[0],
                payload={'plan_id': run.plan_id, 'ok': run.ok, 'dry_run': run.dry_run, 'result_refs': run.result_refs},
            )

            bus = LocalEventBus(root / 'bus')
            bus.append(EventRecord(
                'event:env:1:recorded',
                'pipeline.recorded',
                envelope.envelope_id,
                'ark:test',
                {'plan_id': plan.plan_id},
                evidence.as_ref(),
            ))

            self.assertTrue(run.ok)
            self.assertEqual(writer.read_manifest()[0]['evidence_id'], evidence.evidence_id)
            self.assertEqual(bus.read_all()[0]['evidence_ref'], evidence.as_ref())


if __name__ == '__main__':
    unittest.main()
