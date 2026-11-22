# SPDX-License-Identifier: GPL-3.0-only
"""Validate local Home Assistant branding images and release identity."""

from pathlib import Path
import json
import struct
import unittest
import zlib

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
                # Color type 3 uses an indexed palette with alpha (tRNS).
                self.assertEqual(content[25], 3, "Expected optimized palette PNG")
                offset = len(PNG_SIGNATURE)
                payload = []
                has_transparency = False
                while offset < len(content):
                    length = struct.unpack(">I", content[offset:offset + 4])[0]
                    kind = content[offset + 4:offset + 8]
                    data = content[offset + 8:offset + 8 + length]
                    expected_crc = struct.unpack(">I",
                        content[offset + 8 + length:offset + 12 + length])[0]
                    self.assertEqual(zlib.crc32(kind + data), expected_crc)
                    if kind == b"IDAT":
                        payload.append(data)
                    if kind == b"tRNS":
                        has_transparency = data[0] == 0 and any(a > 0 for a in data)
                    offset += length + 12
                    if kind == b"IEND":
                        break
                self.assertTrue(has_transparency)
                pixels = zlib.decompress(b"".join(payload))
                self.assertEqual(len(pixels), width * (width + 1))
                self.assertTrue(any(pixels), "Icon must not be empty")

    def test_release_version_is_synchronized(self):
        manifest = json.loads((PACKAGE / "manifest.json").read_text())
        self.assertEqual(len(manifest["version"].split(".")), 3)
        version_source = (PACKAGE / "manifest_version.py").read_text()
        self.assertIn(f'VERSION = "{manifest["version"]}"', version_source)


if __name__ == "__main__":
    unittest.main()
