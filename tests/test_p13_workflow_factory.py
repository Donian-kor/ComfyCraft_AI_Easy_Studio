# -*- coding: utf-8 -*-
"""P13: 4cut 방식 워크플로우 자동 생성/검증 + 프로필 목록 오염 수정 검증."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from app.core import workflow_factory as wf
from app.core.model_profiles.base import ModelProfile
from app.core.model_registry import ModelRegistry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"


def _template_dir(tmp: Path) -> Path:
    """실제 프로젝트 템플릿을 임시 폴더에 복사한다."""
    tmp.mkdir(parents=True, exist_ok=True)
    for name in wf.TEMPLATE_FILES.values():
        shutil.copy(WORKFLOWS_DIR / name, tmp / name)
    return tmp


class WorkflowFactoryTests(unittest.TestCase):
    """workflow_factory (4cut 이식본) — 원본 골격 그대로 동작하는지."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.wf_dir = _template_dir(self.tmp / "workflows")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_from_template_injects_checkpoint(self):
        path = wf.build_from_template("my-model.safetensors", "My Model",
                                     self.wf_dir, "checkpoint")
        self.assertEqual(path.name, "my_model.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        ckpts = [n["inputs"]["ckpt_name"] for n in data.values()
                 if n.get("class_type") == wf.CHECKPOINT_NODE_TYPE]
        self.assertEqual(ckpts, ["my-model.safetensors"])

    def test_build_from_template_does_not_touch_source(self):
        wf.build_from_template("mine.safetensors", "m", self.wf_dir, "checkpoint")
        source = json.loads((self.wf_dir / "checkpoint.json").read_text(encoding="utf-8"))
        ckpts = [n["inputs"]["ckpt_name"] for n in source.values()
                 if n.get("class_type") == wf.CHECKPOINT_NODE_TYPE]
        self.assertNotEqual(ckpts, ["mine.safetensors"],
                            "원본 템플릿이 수정되면 안 됨")

    def test_build_from_template_validates(self):
        path = wf.build_from_template("my-model.safetensors", "m",
                                     self.wf_dir, "checkpoint")
        self.assertEqual(
            wf.validate_workflow(path, model_file="my-model.safetensors",
                                 wf_type="checkpoint"), [])

    def test_all_template_types_build(self):
        """모든 워크플로우 종류에 대해 자동 생성 + 검사가 통과해야 한다."""
        for wf_type in wf.TEMPLATE_FILES:
            with self.subTest(wf_type=wf_type):
                model_file = f"m-{wf_type}.safetensors"
                path = wf.build_from_template(model_file, "m", self.wf_dir, wf_type)
                self.assertTrue(path.is_file())
                errors = wf.validate_workflow(path, model_file=model_file,
                                              wf_type=wf_type)
                self.assertEqual(errors, [], f"{wf_type} 검사 실패")

    def test_workflow_file_name_follows_model_file(self):
        self.assertEqual(
            wf.workflow_stem("models/ERNIE-AIO-Turbo-fp8.safetensors", "x"),
            "ernie_aio_turbo_fp8")

    def test_slugify_falls_back(self):
        self.assertEqual(wf.slugify(""), "custom_model")

    def test_missing_template_raises(self):
        with self.assertRaises(FileNotFoundError):
            wf.build_from_template("m.safetensors", "m", self.tmp / "nope")

    def test_empty_model_file_raises(self):
        with self.assertRaises(ValueError):
            wf.build_from_template("", "m", self.wf_dir)

    def test_validate_detects_missing_nodes(self):
        path = self.wf_dir / "broken.json"
        path.write_text(json.dumps({
            "3": {"class_type": "CheckpointLoaderSimple",
                  "inputs": {"ckpt_name": "YOUR_MODEL.safetensors"}},
        }), encoding="utf-8")
        errors = wf.validate_workflow(path)
        self.assertTrue(any("필수 노드" in e for e in errors))
        self.assertTrue(any("체크포인트" in e for e in errors))

    def test_validate_detects_checkpoint_mismatch(self):
        path = wf.build_from_template("other.safetensors", "o", self.wf_dir)
        errors = wf.validate_workflow(path, model_file="mine.safetensors")
        self.assertTrue(any("다릅니다" in e for e in errors))



class GenerateWithLlmTests(unittest.TestCase):
    """AI 폴백 경로 — 검증에 통과한 결과만 저장하는지."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.wf_dir = _template_dir(self.tmp / "workflows")
        # AI가 "정상 응답"을 돌려줄 때의 결과물: 모델 파일명이 채워진 워크플로우.
        self.template = json.loads(
            (self.wf_dir / "checkpoint.json").read_text(encoding="utf-8"))
        self.good = json.loads(json.dumps(self.template))
        for node in self.good.values():
            if isinstance(node, dict) and node.get("class_type") == "CheckpointLoaderSimple":
                node["inputs"]["ckpt_name"] = "my.safetensors"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    class _StubLLM:
        def __init__(self, results):
            self._results = list(results)
            self.calls = 0

        def chat_json(self, system_prompt, user_prompt):
            self.calls += 1
            return self._results.pop(0)

    def test_generates_and_saves_on_valid(self):
        llm = self._StubLLM([self.good])
        path = wf.generate_with_llm(llm, "my.safetensors", self.wf_dir, "m")
        self.assertTrue(path.is_file())
        self.assertEqual(llm.calls, 1)

    def test_raises_after_retries(self):
        bad = {"1": {"class_type": "SaveImage", "inputs": {}}}
        llm = self._StubLLM([bad, bad])
        with self.assertRaises(RuntimeError):
            wf.generate_with_llm(llm, "my.safetensors", self.wf_dir, "m", retries=2)

    def test_rejects_placeholder_only_result(self):
        """템플릿을 그대로 돌려주는(체크포인트 미지정) 응답은 채택하지 않는다."""
        llm = self._StubLLM([self.template, self.template])
        with self.assertRaises(RuntimeError):
            wf.generate_with_llm(llm, "my.safetensors", self.wf_dir, "m", retries=2)


class RegistryPollutionTests(unittest.TestCase):
    """P13-1: 설정/워크플로우 JSON이 프로필로 등록되지 않아야 한다."""

    def test_no_garbage_profiles(self):
        names = {p.name for p in ModelRegistry().profiles}
        for junk in ("lmstudio", "comfyui", "cache", "output", "ui", "1", "2", "3"):
            self.assertNotIn(junk, names, f"설정 파일 키 '{junk}'가 프로필로 등록됨")

    def test_real_profiles_present(self):
        names = {p.name for p in ModelRegistry().profiles}
        for expected in ("flux", "realvisxl_v5", "juggernautxl_ragnarok", "zanime_aio"):
            self.assertIn(expected, names)

    def test_schema_guard(self):
        self.assertTrue(ModelRegistry._looks_like_profile(
            {"patterns": ["x"], "workflow_type": "checkpoint"}))
        self.assertFalse(ModelRegistry._looks_like_profile({"name": "ui"}))
        self.assertFalse(ModelRegistry._looks_like_profile({"patterns": []}))

    def test_workflow_file_field_roundtrip(self):
        payload = {"m": {"name": "m", "patterns": ["m"],
                         "workflow_type": "checkpoint",
                         "workflow_file": "workflows/m.json"}}
        profiles = ModelRegistry()._profiles_from_payload(payload)
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0].workflow_file, "workflows/m.json")

    def test_default_workflow_file_is_empty(self):
        self.assertEqual(ModelProfile(name="x", family="x").workflow_file, "")


if __name__ == "__main__":
    unittest.main()

    def test_validate_missing_file(self):
        self.assertEqual(len(wf.validate_workflow(self.wf_dir / "nope.json")), 1)

    def test_check_model_file_states(self):
        class _Client:
            def __init__(self, names):
                self._names = names

            def list_checkpoints(self, timeout=5):
                return self._names

        self.assertEqual(
            wf.check_model_file(_Client(["a.safetensors"]), "a.safetensors")[0], "ok")
        self.assertEqual(
            wf.check_model_file(_Client(["b.safetensors"]), "a.safetensors")[0], "missing")
        self.assertEqual(wf.check_model_file(None, "")[0], "unknown")