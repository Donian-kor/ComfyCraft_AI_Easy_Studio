"""Tests for core application components without external dependencies."""

from __future__ import annotations

import unittest
from pathlib import Path

from app.core.config_manager import AppConfig, ConfigManager
from app.core.model_registry import ModelRegistry, get_model_registry
from app.sections.connection import check_connection_silent


class CoreComponentsTests(unittest.TestCase):
    def test_model_registry_detect_profiles(self) -> None:
        registry = get_model_registry()
        # Flux profile detection
        flux_profile = registry.detect("flux1-dev-Q4_0.gguf")
        self.assertIsNotNone(flux_profile)
        self.assertEqual(flux_profile.family, "flux")

        # ZImage profile detection
        zimage_profile = registry.detect("z_image_turbo_fp8.safetensors")
        self.assertIsNotNone(zimage_profile)
        self.assertEqual(zimage_profile.workflow_type, "zimage")

        # Fallback / checkpoint detection
        sdxl_profile = registry.detect("unknown_sdxl_model.safetensors")
        self.assertIsNotNone(sdxl_profile)

    def test_config_manager_accessors(self) -> None:
        mgr = ConfigManager()
        cfg = mgr.get()
        self.assertIsInstance(cfg, AppConfig)

        # Test set_config and property
        mgr.set_config(cfg)
        self.assertEqual(mgr.config.lmstudio.url, cfg.lmstudio.url)

    def test_check_connection_silent_does_not_raise_import_error(self) -> None:
        # Invalid localhost port should return False safely without crashing or throwing ImportError
        result = check_connection_silent("lm", "http://127.0.0.1:9999", timeout=0.05)
        self.assertFalse(result)

        result_comfy = check_connection_silent("comfy", "http://127.0.0.1:9999", timeout=0.05)
        self.assertFalse(result_comfy)


if __name__ == "__main__":
    unittest.main()
