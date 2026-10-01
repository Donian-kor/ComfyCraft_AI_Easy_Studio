"""세션/카드 액션 모음 (AppState 에서 분리).

이 모듈은 UI 와 직접 관계된 동작만 담당한다. AppState 의 줄 수를
600줄 이하로 유지하기 위해 분리했다.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import flet as ft

from app.models.chat import ChatMessageData
from app.ui.flet.shell import AppShell


def make_save_image_action(
    services,
    shell_getter: Callable[[], Optional[AppShell]],
) -> Callable[[str], None]:
    """이미지 '다른 이름으로 저장' 액션을 만든다.

    `shell_getter` 는 `lambda: state.shell` 처럼 최신 쉘을 돌려주는
    함수여야 한다(생성 시점에 shell 이 None 일 수 있으므로).
    """
    def action(image_path: str) -> None:
        if not image_path:
            return
        shell = shell_getter()
        if shell is None:
            return
        file_name = Path(image_path).name
        output_dir = str(services.output_dir)

        def on_result(target_path: Optional[str]) -> None:
            if target_path is None:
                return
            try:
                from app.features.generation.output_files import copy_image
                saved = copy_image(image_path, target_path)
                shell = shell_getter()
                if shell is not None:
                    shell.set_status(
                        f"저장했습니다: {saved}" if saved else "저장에 실패했습니다.",
                        "done" if saved else "error")
            except Exception as exc:
                shell = shell_getter()
                if shell is not None:
                    shell.set_status(f"저장 실패: {exc}", "error")

        shell.show_save_dialog(file_name, output_dir, on_result)
    return action


def make_reuse_settings_action(
    studio_getter: Callable[[], Optional],
    shell_getter: Callable[[], Optional[AppShell]],
) -> Callable[[ChatMessageData], None]:
    """이미지 카드의 '이 설정으로' — 지난 옵션을 좌측 패널에 되돌린다."""
    def action(message: ChatMessageData) -> None:
        studio = studio_getter()
        if studio is None:
            return
        snapshot = message.metadata.get("snapshot") or {}
        if not snapshot:
            return
        studio.options.apply_snapshot(snapshot)
        shell = shell_getter()
        if shell is not None:
            shell.set_status("지난 생성 설정을 불러왔습니다.", "done")
    return action


def make_open_image_action(
    shell_getter: Callable[[], Optional[AppShell]],
    messages_getter: Callable[[], List[ChatMessageData]],
) -> Callable[[ChatMessageData], None]:
    """이미지를 크게 보는 미리보기 모달을 연다 (줌/팬/회전/이전·다음).

    `messages_getter`는 현재 채팅의 전체 메시지 리스트를 돌려주는 함수여야 한다.
    이미지 메시지들만 필터링해 paths 리스트를 만든다.
    """
    def action(message: ChatMessageData) -> None:
        path = str(message.metadata.get("image_path", "") or "")
        if not path:
            return
        shell = shell_getter()
        if shell is None:
            return

        # 현재 채팅의 모든 이미지 메시지에서 경로 수집
        all_messages = messages_getter()
        image_paths = [
            str(m.metadata.get("image_path", "") or "")
            for m in all_messages
            if m.kind == "image" and m.metadata.get("image_path")
        ]
        # 현재 이미지의 인덱스 찾기
        try:
            index = image_paths.index(path)
        except ValueError:
            index = 0

        shell.show_image_preview_modal(
            image_paths,
            index=index,
            return_focus_widget=shell._new_chat_button if hasattr(shell, '_new_chat_button') else None,
            on_save=lambda p: shell.set_status(f"저장 요청: {p}", "done"),
        )
    return action


def make_open_output_folder_action(
    services,
    shell_getter: Callable[[], Optional[AppShell]],
) -> Callable[[], None]:
    """출력 폴더를 파일 관리자로 연다."""
    def action() -> None:
        shell = shell_getter()
        if shell is None:
            return
        from app.features.generation.output_files import open_output_folder
        ok = open_output_folder(Path(services.output_dir))
        shell.set_status(
            "출력 폴더를 열었습니다." if ok else "폴더를 열 수 없습니다.",
            "done" if ok else "error")
    return action


def make_rewrite_action(
    studio_getter: Callable[[], Optional],
    shell_getter: Callable[[], Optional[AppShell]],
) -> Callable[[ChatMessageData], None]:
    """이미지 카드의 '프롬프트 재작성' — 스냅샷 복원 후 프롬프트 입력창을 편집 상태로 둔다.

    - 스냅샷의 enhanced_prompt를 입력창에 채워 재향상(LLM 프롬프트 향상)을 건너뛴다.
    - 사용자가 수정 후 전송하면 handle_prompt가 새 프롬프트로 생성 시작.
    """
    def action(message: ChatMessageData) -> None:
        studio = studio_getter()
        if studio is None:
            return
        snapshot = message.metadata.get("snapshot") or {}
        if not snapshot:
            shell = shell_getter()
            if shell is not None:
                shell.set_status("이 이미지의 설정을 찾을 수 없습니다.", "error")
            return
        # 스냅샷 복원 (옵션 패널에 값 되돌리기)
        studio.options.apply_snapshot(snapshot)
        # 프롬프트 입력창에 enhanced_prompt 또는 prompt 채우기 (재향상 방지)
        enhanced = snapshot.get("enhanced_prompt") or snapshot.get("prompt", "")
        if enhanced and hasattr(studio, "set_prompt_input"):
            studio.set_prompt_input(enhanced)
        # 포커스를 입력창으로 이동
        if hasattr(studio, "focus_prompt_input"):
            studio.focus_prompt_input()
        shell = shell_getter()
        if shell is not None:
            shell.set_status("프롬프트를 불러왔습니다. 수정 후 전송하세요.", "done")
    return action


def make_regenerate_action(
    studio_getter: Callable[[], Optional],
    shell_getter: Callable[[], Optional[AppShell]],
    app_state_getter: Callable[[], Optional],
) -> Callable[[ChatMessageData], None]:
    """이미지 카드의 '다시 만들기' — 스냅샷 복원 후 즉시 재생성.

    - enhanced_prompt를 재활용해 재향상(LLM 프롬프트 향상)을 건너뛴다.
    - 생성 중이면 무시.
    """
    def action(message: ChatMessageData) -> None:
        studio = studio_getter()
        app_state = app_state_getter()
        if studio is None or app_state is None:
            return
        snapshot = message.metadata.get("snapshot") or {}
        if not snapshot:
            shell = shell_getter()
            if shell is not None:
                shell.set_status("이 이미지의 설정을 찾을 수 없습니다.", "error")
            return
        # 생성 중이면 차단
        if getattr(app_state.jobs, "is_busy", False):
            shell = shell_getter()
            if shell is not None:
                shell.set_status("생성 중에는 다시 만들 수 없습니다.", "error")
            return
        # 스냅샷 복원
        studio.options.apply_snapshot(snapshot)
        # enhanced_prompt가 있으면 입력창에 채워 재향상 건너뛰기 준비
        enhanced = snapshot.get("enhanced_prompt") or snapshot.get("prompt", "")
        if enhanced and hasattr(studio, "set_prompt_input"):
            studio.set_prompt_input(enhanced)
        # 즉시 생성 시작 (AppState.start_generation이 enhanced_prompt를 읽어서 재향상 건너뜀)
        app_state.start_generation(enhanced)
        shell = shell_getter()
        if shell is not None:
            shell.set_status("다시 만들기를 시작했습니다.", "done")
    return action