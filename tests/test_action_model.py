import unittest

from opt.ark.runtime.action_model import ActionIntent, ActionModelEngine, ToolKind
from opt.ark.runtime.action_model.exceptions import UnauthorizedActionIntent
from opt.ark.runtime.policy import ActionPreconditionPolicy
from tests.helpers import make_envelope


class ActionModelTests(unittest.TestCase):
    def test_aem_translates_only_after_policy(self):
        envelope = make_envelope()
        decision = ActionPreconditionPolicy().require(envelope)
        plan = ActionModelEngine().translate(
            intent=ActionIntent('intent:1', 'simulate noop', ToolKind.NOOP),
            envelope=envelope,
            policy_decision=decision,
        )
        self.assertEqual(plan.steps[0].tool, ToolKind.NOOP)
        self.assertTrue(plan.dry_run)

    def test_aem_rejects_denied_policy(self):
        envelope = make_envelope(aletheia_ref='bad')
        decision = ActionPreconditionPolicy().evaluate(envelope)
        with self.assertRaises(UnauthorizedActionIntent):
            ActionModelEngine().translate(
                intent=ActionIntent('intent:1', 'simulate noop'),
                envelope=envelope,
                policy_decision=decision,
            )


if __name__ == '__main__':
    unittest.main()
