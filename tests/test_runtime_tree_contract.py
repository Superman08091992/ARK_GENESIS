import unittest

from scripts.render_runtime_tree import render_tree


class RuntimeTreeContractTests(unittest.TestCase):
    def test_rendered_tree_contains_core_paths(self):
        tree = render_tree()
        for path in ('/opt/ark', '/opt/ark/runtime', '/opt/ark/bus', '/opt/ark/evidence', '/var/log/ark'):
            self.assertIn(path, tree)

    def test_rendered_tree_excludes_legacy_uppercase_root(self):
        self.assertNotIn('/opt/ARK', render_tree())


if __name__ == '__main__':
    unittest.main()
