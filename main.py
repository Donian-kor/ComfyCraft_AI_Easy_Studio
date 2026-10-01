"""ComfyCraft AI Easy Studio — 애플리케이션 진입점 (Flet Edition).

REFACTOR_PLAN_FLET.md 에 따라 PySide6 UI 를 Flet + Material 3 로 전환했다.

계층 구조:
    main.py
      └─ app/ui/flet/          (Flet UI — 이 계층만 flet 를 import)
           └─ app/application/ (JobManager / GenerationService)
                └─ app/features/ , app/core/ , app/models/

실행:
    python main.py
"""

from __future__ import annotations

from app.paths import BASE_DIR  # noqa: F401  (외부 코드 호환 재수출)
from app.ui.flet.app import main, run  # noqa: F401


if __name__ == "__main__":
    run()
