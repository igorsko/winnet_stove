# SPDX-License-Identifier: GPL-3.0-only
"""Validate local Home Assistant branding images and release identity."""

from pathlib import Path
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "custom_components" / "winnet_stove"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class BrandAssetsTest(unittest.TestCase):
    def test_brand_files_exist_and_are_transparent_rgba(self):
        for name, width in (("icon.png", 256), ("icon@2x.png", 512)):
            with self.subTest(name=name):
                content = (PACKAGE / "brand" / name).read_bytes()
                self.assertTrue(content.startswith(PNG_SIGNATURE))
                self.assertGreater(len(content), 1000)
                self.assertEqual(content[12:16], b"IHDR")
                height = struct.unpack(">I", content[20:24])[0]
                actual_width = struct.unpack(">I", content[16:20])[0]
                self.assertEqual((actual_width, height), (width, width))
                self.assertEqual(content[25], 6, "Expected RGBA PNG with alpha")

    def test_release_version_is_synchronized(self):
        manifest = json.loads((PACKAGE / "manifest.json").read_text())
        self.assertEqual(manifest["version"], "1.3.1")
        version_source = (PACKAGE / "manifest_version.py").read_text()
        self.assertIn('VERSION = "1.3.1"', version_source)


if __name__ == "__main__":
    unittest.main()
