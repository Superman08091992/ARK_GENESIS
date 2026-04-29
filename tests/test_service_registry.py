import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ServiceRegistryTests(unittest.TestCase):
    def test_local_api_is_registered_as_loopback_read_only(self):
        text = (ROOT / 'deployment/service-registry.yaml').read_text(encoding='utf-8')
        self.assertIn('id: "ark-local-api"', text)
        self.assertIn('bind: "127.0.0.1"', text)
        self.assertIn('authority: "read_only_status"', text)
        self.assertIn('shell_execution', text)
        self.assertIn('account_access', text)

    def test_future_agent_stubs_are_declared(self):
        text = (ROOT / 'deployment/service-registry.yaml').read_text(encoding='utf-8')
        for service in ('ark-kyle', 'ark-aletheia', 'ark-joey', 'ark-hrm', 'ark-kenny', 'ark-watchdog'):
            self.assertIn(service, text)


if __name__ == '__main__':
    unittest.main()
