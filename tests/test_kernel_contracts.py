import unittest

from opt.ark.runtime.kernel import LifecycleRecord, LifecycleState
from opt.ark.runtime.kernel.exceptions import InvalidTransition
from tests.helpers import make_envelope


class KernelContractTests(unittest.TestCase):
    def test_envelope_validates(self):
        self.assertEqual(make_envelope().validate().required_refs()['aletheia_ref'], 'aletheia:verified:1')

    def test_lifecycle_allows_canonical_transition(self):
        self.assertEqual(LifecycleRecord().transition(LifecycleState.VERIFIED).state, LifecycleState.VERIFIED)

    def test_lifecycle_blocks_illegal_jump(self):
        with self.assertRaises(InvalidTransition):
            LifecycleRecord().transition(LifecycleState.BROKERED)


if __name__ == '__main__':
    unittest.main()
