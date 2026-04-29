import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingScaffoldTests(unittest.TestCase):
    def test_expected_packages_exist(self):
        for package in ('ark-runtime', 'ark-ui', 'ark-services'):
            path = ROOT / 'packages' / package / 'PKGBUILD'
            self.assertTrue(path.exists(), f'missing {path}')
            self.assertIn('pkgname=' + package, path.read_text(encoding='utf-8'))

    def test_service_packaging_files_exist(self):
        expected = [
            'packaging/ark-local-api',
            'packaging/systemd/ark-local-api.service',
            'packaging/sysusers/ark.conf',
            'packaging/tmpfiles/ark.conf',
            'packaging/env/ark.env.example',
        ]
        for rel in expected:
            self.assertTrue((ROOT / rel).exists(), f'missing {rel}')

    def test_tmpfiles_preserves_runtime_boundaries(self):
        text = (ROOT / 'packaging/tmpfiles/ark.conf').read_text(encoding='utf-8')
        self.assertIn('/opt/ark/bus', text)
        self.assertIn('/opt/ark/evidence', text)
        self.assertIn('/var/log/ark', text)
        self.assertIn('/opt/ark/logs', text)

    def test_local_api_service_is_loopback_runtime_bound(self):
        env = (ROOT / 'packaging/env/ark.env.example').read_text(encoding='utf-8')
        self.assertIn('ARK_RUNTIME_ROOT=/opt/ark', env)
        self.assertIn('ARK_API_HOST=127.0.0.1', env)


if __name__ == '__main__':
    unittest.main()
