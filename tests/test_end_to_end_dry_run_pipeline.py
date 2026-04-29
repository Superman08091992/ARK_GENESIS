import unittest

from opt.ark.runtime.action_model import ActionIntent, ActionModelEngine, ToolKind
from opt.ark.runtime.execution_broker import ExecutionBroker
from opt.ark.runtime.policy import ActionPreconditionPolicy
from tests.helpers import make_envelope


class EndToEndDryRunPipelineTests(unittest.TestCase):
    def test_canonical_dry_run_pipeline(self):
        envelope = make_envelope()
        decision = ActionPreconditionPolicy().require(envelope)
        plan = ActionModelEngine().translate(
            intent=ActionIntent('intent:1', 'simulate account-safe noop', ToolKind.ACCOUNT_STUB, {'target': 'account_stub'}),
            envelope=envelope,
            policy_decision=decision,
        )
        run = ExecutionBroker().run(plan)
        self.assertTrue(decision.allowed)
        self.assertTrue(plan.dry_run)
        self.assertTrue(run.dry_run)
        self.assertEqual(run.result_refs, ('broker-result:step:intent:1:001',))


if __name__ == '__main__':
    unittest.main()
