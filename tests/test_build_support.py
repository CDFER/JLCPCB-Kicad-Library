import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_support import (
    parse_attributes,
    parse_base_price,
    rewrite_footprint_references,
    rewrite_third_party_variable,
    source_catalog_complete,
)
from packageTools import create_target_archives


class SourceCompatibilityTests(unittest.TestCase):
    def test_detects_partial_feed_without_blocking_build(self):
        self.assertFalse(source_catalog_complete(["Diodes", "Transistors", "Inductors"]))

    def test_detects_complete_feed(self):
        self.assertTrue(
            source_catalog_complete(["Resistors", "Capacitors", "Diodes", "Transistors", "Inductors"])
        )

    def test_reads_current_attributes_schema(self):
        self.assertEqual(parse_attributes('{"Current Rating":"2A"}'), {"Current Rating": "2A"})

    def test_reads_legacy_extra_schema(self):
        self.assertEqual(
            parse_attributes('{"attributes":{"Voltage Rated":"50V"}}'), {"Voltage Rated": "50V"}
        )


class PriceParsingTests(unittest.TestCase):
    def test_parses_legacy_json_price(self):
        self.assertEqual(parse_base_price('[{"price": "0.0042"}]'), 0.0042)

    def test_parses_current_tier_price(self):
        self.assertEqual(parse_base_price("1-49:0.0887,50-149:0.0707"), 0.0887)


class PackageTests(unittest.TestCase):
    def test_rewrites_known_missing_footprint_references(self):
        content = '"PCM_JLCPCB:Q_SOT-89-3L" "PCM_JLCPCB:D_DO-214AA(SMB)" "PCM_JLCPCB:D_P600"'
        rewritten = rewrite_footprint_references(content)
        self.assertIn("PCM_JLCPCB:Q_SOT-89", rewritten)
        self.assertIn("PCM_JLCPCB:D_SMB", rewritten)
        self.assertIn("Diode_THT:D_P600_R-6_P15.24mm_Horizontal", rewritten)

    def test_rewrites_versioned_model_path(self):
        original = '(model "${KICAD8_3RD_PARTY}/3dmodels/example.step")'
        self.assertIn("KICAD10_3RD_PARTY", rewrite_third_party_variable(original, "10.0"))

    def test_creates_version_specific_archives(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "footprints" / "Example.pretty").mkdir(parents=True)
            (root / "symbols").mkdir()
            (root / "3dmodels").mkdir()
            (root / "resources").mkdir()
            (root / "footprints" / "Example.pretty" / "Example.kicad_mod").write_text(
                '(footprint "Example"\n\t(model "${KICAD8_3RD_PARTY}/3dmodels/example.step")\n)\n',
                encoding="utf-8",
            )
            (root / "symbols" / "Example.kicad_sym").write_text(
                '(kicad_symbol_lib\n\t(version 20231120)\n\t(symbol "Example"\n'
                '\t\t(property "Footprint" "PCM_JLCPCB:Q_SOT-89-3L")\n\t)\n)\n',
                encoding="utf-8",
            )
            (root / "metadata.json").write_text(
                json.dumps(
                    {
                        "$schema": "https://go.kicad.org/pcm/schemas/v1",
                        "name": "Example",
                        "description": "Example",
                        "description_full": "Example",
                        "identifier": "com.example.library",
                        "type": "library",
                        "author": {"name": "Example"},
                        "license": "MIT",
                        "versions": [{"version": "old", "status": "stable", "kicad_version": "8.0"}],
                    }
                ),
                encoding="utf-8",
            )

            archives = create_target_archives(
                package_version="2026.10.08",
                files_and_dirs=["footprints", "3dmodels", "symbols", "resources", "metadata.json"],
                root=root,
                output_dir=root,
            )

            self.assertEqual(len(archives), 3)
            for target, archive in zip(("8.0", "9.0", "10.0"), archives):
                with zipfile.ZipFile(archive) as package:
                    footprint = package.read("footprints/Example.pretty/Example.kicad_mod").decode()
                    symbol = package.read("symbols/Example.kicad_sym").decode()
                    metadata = json.loads(package.read("metadata.json"))
                self.assertIn(f"KICAD{target.split('.')[0]}_3RD_PARTY", footprint)
                self.assertIn("PCM_JLCPCB:Q_SOT-89", symbol)
                self.assertNotIn("Q_SOT-89-3L", symbol)
                self.assertEqual(metadata["versions"][0]["kicad_version"], target)


if __name__ == "__main__":
    unittest.main()
