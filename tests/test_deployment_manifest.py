import unittest
from pathlib import Path

from scripts.validate_deployment_manifest import validate_deployment


ROOT = Path(__file__).resolve().parents[1]


class DeploymentManifestTests(unittest.TestCase):
    def test_deployment_contracts_validate(self):
        ok, errors = validate_deployment(ROOT)
        self.assertTrue(ok, errors)

    def test_runtime_manifest_uses_canonical_root(self):
        text = (ROOT / 'deployment/runtime-manifest.yaml').read_text(encoding='utf-8')
        self.assertIn('installed_root: "/opt/ark"', text)
        self.assertNotIn('/opt/ARK', text)


if __name__ == '__main__':
    unittest.main()
