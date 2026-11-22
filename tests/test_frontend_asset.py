# SPDX-License-Identifier: GPL-3.0-only
"""Ensure the panel URL changes on release and remains a static route."""

from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "winnet_stove"


class FrontendAssetTests(unittest.TestCase):
    def test_versioned_module_path(self):
        version = json.loads((COMPONENT / "manifest.json").read_text())["version"]
        source = (COMPONENT / "manifest_version.py").read_text()
        self.assertIn(f'VERSION = "{version}"', source)
        ui = (COMPONENT / "ui.py").read_text()
        self.assertIn('module_url=f"{PANEL_JS}?v={VERSION}"', ui)
        self.assertIn('PANEL_JS = "/api/winnet_stove/panel.js"', ui)
        self.assertIn("cache_headers=False", ui)


if __name__ == "__main__":
    unittest.main()
