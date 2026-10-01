# -*- coding: utf-8 -*-
"""P6: 대화 세션 저장/복원 (session.json + 중앙 인덱스).

- base/.sessions/sessions.json: 중앙 인덱스 [{id, title, updated_at, model}]
- base/.sessions/<id>/session.json: 전체 세션 (메시지 + 스냅샷)
- 이미지 파일은 출력 폴더에 유지, 경로만 기록한다.
"""
from __future__ import annotations

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _new_id() -> str:
    return f"{int(time.time() * 1000):x}-{uuid.uuid4().hex[:6]}"


class SessionManager:
    """세션 CRUD + 인덱스 관리. 파일 I/O만 담당한다."""

    def __init__(self, sessions_dir: Path | str):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.sessions_dir / "sessions.json"

    # -- index -----------------------------------------------------------
    def _read_index(self) -> List[Dict[str, Any]]:
        try:
            if not self.index_path.exists():
                return []
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            entries = data.get("sessions", []) if isinstance(data, dict) else []
            return [e for e in entries if isinstance(e, dict) and e.get("id")]
        except Exception:
            return []

    def _write_index(self, entries: List[Dict[str, Any]]) -> None:
        tmp = self.index_path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps({"sessions": entries}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.index_path)

    def list_sessions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """(updated_at, seq) 내림차순. limit이 있으면 상위 N개만."""
        entries = sorted(
            self._read_index(),
            key=lambda e: (str(e.get("updated_at", "")),
                           int(e.get("seq", 0))),
            reverse=True,
        )
        if limit is not None:
            entries = entries[: max(0, limit)]
        return entries

    # -- sessions --------------------------------------------------------
    def _session_path(self, session_id: str) -> Path:
        return self.sessions_dir / session_id / "session.json"

    def new_session(self, title: str = "새 대화",
                    model: str = "") -> Dict[str, Any]:
        now = _now_iso()
        return {
            "session_id": _new_id(),
            "title": title or "새 대화",
            "type": "single",
            "created_at": now,
            "updated_at": now,
            "model": model or "",
            "messages": [],
            "last_snapshot": {},
        }

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        try:
            path = self._session_path(session_id)
            if not path.exists():
                return None
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not data.get("session_id"):
                return None
            data.setdefault("messages", [])
            data.setdefault("last_snapshot", {})
            data.setdefault("type", "single")
            return data
        except Exception:
            return None

    def save_session(self, session: Dict[str, Any]) -> bool:
        """세션 파일 + 인덱스 갱신. 성공 시 True."""
        try:
            sid = session.get("session_id")
            if not sid:
                return False
            session["updated_at"] = _now_iso()
            session_dir = self.sessions_dir / sid
            session_dir.mkdir(parents=True, exist_ok=True)
            tmp = session_dir / "session.tmp"
            tmp.write_text(
                json.dumps(session, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            tmp.replace(self._session_path(sid))
            entries = [e for e in self._read_index() if e.get("id") != sid]
            top_seq = 0
            for entry in entries:
                try:
                    top_seq = max(top_seq, int(entry.get("seq", 0)))
                except (TypeError, ValueError):
                    pass
            entries.append({
                "id": sid,
                "title": session.get("title", "새 대화"),
                "updated_at": session["updated_at"],
                "model": session.get("model", ""),
                "seq": top_seq + 1,
            })
            self._write_index(entries)
            return True
        except Exception:
            return False

    def rename_session(self, session_id: str, title: str) -> bool:
        session = self.load_session(session_id)
        if session is None or not (title or "").strip():
            return False
        session["title"] = title.strip()[:60]
        return self.save_session(session)

    def delete_session(self, session_id: str) -> bool:
        """기록만 삭제한다. 이미지 파일은 출력 폴더에 유지된다."""
        try:
            entries = [e for e in self._read_index()
                       if e.get("id") != session_id]
            self._write_index(entries)
            session_dir = self.sessions_dir / session_id
            if session_dir.exists():
                import shutil
                shutil.rmtree(session_dir, ignore_errors=True)
            return True
        except Exception:
            return False
