"""External-service-free checks for project settings and workflow files."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"


class ProjectBasicsTests(unittest.TestCase):
    def test_all_workflow_json_files_are_valid(self) -> None:
        json_files = sorted(WORKFLOWS_DIR.glob("*.json"))

        self.assertGreater(len(json_files), 0)
        for path in json_files:
            with self.subTest(path=path.name), path.open(encoding="utf-8") as file:
                json.load(file)

    def test_app_config_references_existing_workflow_templates(self) -> None:
        with (WORKFLOWS_DIR / "app_config.json").open(encoding="utf-8") as file:
            config = json.load(file)

        self.assertEqual(config["lmstudio"]["url"], "http://127.0.0.1:1234")
        self.assertEqual(config["comfyui"]["url"], "http://127.0.0.1:8188")

        for template_path in config["workflow"].values():
            if isinstance(template_path, str) and template_path.endswith(".json"):
                self.assertTrue((PROJECT_ROOT / template_path).is_file(), template_path)

    def test_required_workflow_files_are_present(self) -> None:
        expected_files = {
            "app_config.json",
            "checkpoint.json",
            "default_profiles.json",
            "flux_gguf.json",
            "gguf_unet.json",
            "prompt.json",
            "zimage.json",
        }

        self.assertTrue(expected_files.issubset({path.name for path in WORKFLOWS_DIR.glob("*.json")}))

    def test_default_model_profiles_cover_supported_families(self) -> None:
        with (WORKFLOWS_DIR / "default_profiles.json").open(encoding="utf-8") as file:
            profiles = json.load(file)

        for profile_name in ("flux", "zimage", "realvisxl_v5", "juggernautxl_ragnarok"):
            with self.subTest(profile=profile_name):
                self.assertIn(profile_name, profiles)
                self.assertIn("workflow_type", profiles[profile_name])

    def test_documented_and_declared_versions_are_v03(self) -> None:
        app_init = (PROJECT_ROOT / "app" / "__init__.py").read_text(encoding="utf-8")
        help_readme = (PROJECT_ROOT / "assets" / "help" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn('__version__ = "0.3.0"', app_init)
        self.assertIn("**버전**: v0.3", help_readme)


if __name__ == "__main__":
    unittest.main()
