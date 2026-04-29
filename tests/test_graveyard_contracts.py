import unittest
from pathlib import Path

from opt.ark.scripts.validate_graveyard import validate_graveyard


class GraveyardContractTests(unittest.TestCase):
    def test_graveyard_scaffold_validates(self):
        result = validate_graveyard(Path.cwd())
        self.assertTrue(result.ok, result.errors)


if __name__ == '__main__':
    unittest.main()
