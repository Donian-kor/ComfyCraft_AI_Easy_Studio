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

    def test_ernie_profiles_not_mistaken_for_zimage(self) -> None:
        registry = get_model_registry()

        # ERNIE Base/Turbo → checkpoint 프로필로 잡히고 ZImage가 아님
        ernie_base = registry.detect("ERNIE-AIO-Base-fp8.safetensors")
        self.assertEqual(ernie_base.name, "ernie-aio-base")
        self.assertEqual(ernie_base.workflow_type, "checkpoint")
        self.assertEqual(ernie_base.default_steps, 50)
        self.assertEqual(ernie_base.default_cfg, 4.0)

        ernie_turbo = registry.detect("ERNIE-AIO-Turbo-fp8.safetensors")
        self.assertEqual(ernie_turbo.name, "ernie-aio-turbo")
        self.assertEqual(ernie_turbo.workflow_type, "checkpoint")
        self.assertEqual(ernie_turbo.default_steps, 8)
        self.assertEqual(ernie_turbo.default_cfg, 1.0)

    def test_is_zimage_model_no_longer_matches_bare_turbo(self) -> None:
        from app.core.workflow_manager import WorkflowManager

        manager = WorkflowManager()

        # ERNIE Turbo는 ZImage로 판별하지 않음
        self.assertFalse(manager.is_zimage_model("ERNIE-AIO-Turbo-fp8.safetensors"))
        # ZImage 계열은 그대로 판별
        self.assertTrue(manager.is_zimage_model("z_image_turbo_fp8.safetensors"))
        self.assertTrue(manager.is_zimage_model("zimage_turbo-Q4_K_S.gguf"))
        self.assertFalse(manager.is_zimage_model(""))

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
