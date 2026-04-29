import unittest

from opt.ark.runtime.action_model import ActionIntent, ActionModelEngine, ToolKind
from opt.ark.runtime.execution_broker import ExecutionBroker
from opt.ark.runtime.policy import ActionPreconditionPolicy
from tests.helpers import make_envelope


class ExecutionBrokerTests(unittest.TestCase):
    def test_broker_runs_stub_tools_only(self):
        envelope = make_envelope()
        decision = ActionPreconditionPolicy().require(envelope)
        plan = ActionModelEngine().translate(
            intent=ActionIntent('intent:1', 'simulate file action', ToolKind.FILE_STUB),
            envelope=envelope,
            policy_decision=decision,
        )
        run = ExecutionBroker().run(plan)
        self.assertTrue(run.ok)
        self.assertEqual(run.results[0].artifact_ref, 'broker-result:step:intent:1:001')


if __name__ == '__main__':
    unittest.main()
