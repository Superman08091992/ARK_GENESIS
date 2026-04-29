import unittest

from opt.ark.runtime.policy import ActionPreconditionPolicy
from opt.ark.runtime.policy.exceptions import PolicyDenied
from tests.helpers import make_envelope


class ActionAuthorizationFlowTests(unittest.TestCase):
    def test_policy_allows_complete_dry_run_envelope(self):
        decision = ActionPreconditionPolicy().require(make_envelope())
        self.assertTrue(decision.allowed)

    def test_policy_blocks_missing_aletheia_prefix(self):
        decision = ActionPreconditionPolicy().evaluate(make_envelope(aletheia_ref='raw:bad'))
        self.assertFalse(decision.allowed)

    def test_policy_blocks_real_execution_in_v0_1(self):
        with self.assertRaises(PolicyDenied):
            ActionPreconditionPolicy().require(make_envelope(dry_run=False))


if __name__ == '__main__':
    unittest.main()
