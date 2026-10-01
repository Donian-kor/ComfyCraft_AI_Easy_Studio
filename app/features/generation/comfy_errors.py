"""Feature 계층 — ComfyUI 오류/상태 파싱 (순수 Python, UI 프레임워크 금지).

기존 app/sections/generation.py 의 정적 메서드들을 그대로 옮긴 것이다.
Qt Signal 이나 Controller 참조가 전혀 없으므로 단위 테스트가 가능하다.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def is_execution_finished(item: Dict[str, Any]) -> bool:
    """ComfyUI 가 이 작업을 '종료'했다고 명시했는지 판단한다.

    history 에 항목이 생겼다는 사실만으로는 끝난 게 아니다(큐에
    돌고 있는 동안에도 항목이 보일 수 있다). status.completed 나
    status_str 로 서버가 종료했음을 알려 준 경우만 참으로 본다.
    """
    if not isinstance(item, dict):
        return False
    status = item.get("status", {})
    if not isinstance(status, dict):
        return False
    if status.get("completed") is True:
        return True
    return str(status.get("status_str") or "").lower() in (
        "success", "error", "interrupted",
    )


def format_status_message(msg: Any) -> Optional[str]:
    """status.messages 원소 하나를 사람이 읽을 문장으로 바꾼다.

    ComfyUI 는 실행 로그를 2원소 리스트로 보낸다:
        ["execution_start", {...}]
        ["execution_error", {"exception_message": ..., "node_id": "3",
                              "exception_type": ..., "traceback": [...]}]
    예전 코드는 dict 와 str 만 보고 리스트 원본을 통째로 건너뛰고,
    키 이름도 error/message 만 찾았다. 그래서 진짜 OOM 같은
    execution_error 가 조용히 통과했다.
    """
    if isinstance(msg, (list, tuple)):
        if not msg:
            return None
        head = str(msg[0])
        body = msg[1] if len(msg) > 1 else None
        detail = format_status_message(body)
        if head in ("execution_error", "execution_interrupted"):
            where = ""
            if isinstance(body, dict):
                node_id = body.get("node_id")
                node_type = body.get("node_type")
                if node_id is not None:
                    where = f" (노드 {node_id}"
                    if node_type:
                        where += f"/{node_type}"
                    where += ")"
            suffix = f": {detail}" if detail else ""
            if head == "execution_interrupted":
                return f"생성이 중단되었습니다{where}{suffix}"
            return f"ComfyUI 노드 실행 오류{where}{suffix}"
        return detail

    if isinstance(msg, str):
        return msg or None

    if isinstance(msg, dict):
        # 1) 명시적 오류 키가 있으면 그 값을 쓴다.
        for key in ("exception_message", "error", "message"):
            value = msg.get(key)
            if value:
                return str(value)
        # 2) 예외 유형만 있으면 그것도 알린다.
        exc_type = msg.get("exception_type")
        if exc_type:
            return str(exc_type)
        return None

    return None



def extract_comfyui_error(item: Dict[str, Any]) -> Optional[str]:
    """history 항목에서 사람이 읽을 수 있는 오류 문장을 뽑아낸다.

    ComfyUI 는 status_str 로 요약만 보내고 진짜 원인은 messages 안의
    ["execution_error", {"exception_message": ...}] 에 넣는다.
    """
    if not isinstance(item, dict):
        return None

    direct_error = item.get("error")
    if direct_error:
        return str(direct_error)

    status = item.get("status", {})
    if isinstance(status, dict):
        error = status.get("error")
        if error:
            return str(error)

        messages = status.get("messages")
        saw_failure = False
        if isinstance(messages, list):
            for msg in messages:
                if (isinstance(msg, (list, tuple)) and msg
                        and str(msg[0]) in ("execution_error",
                                            "execution_interrupted")):
                    saw_failure = True
                text = format_status_message(msg)
                if text and saw_failure:
                    return text

        # messages 가 실패 신호를 안 준 경우에만 상태 문자열로 대체한다.
        # "running" 처럼 status_str 이 정상인데 messages 가 비어 있는
        # 정상 진행 중 케이스를 오탐하면 안 된다.
        status_str = str(status.get("status_str") or "")
        if status_str in ("error", "interrupted") and not saw_failure:
            return ("생성이 중단되었습니다"
                    if status_str == "interrupted"
                    else "ComfyUI 가 오류로 종료했습니다 (상세 내용 없음)")

    for node_output in item.get("outputs", {}).values():
        if not isinstance(node_output, dict):
            continue
        node_status = node_output.get("status", {})
        if isinstance(node_status, dict):
            error = node_status.get("error")
            if error:
                return str(error)
            messages = node_status.get("messages")
            if isinstance(messages, list):
                for msg in messages:
                    text = format_status_message(msg)
                    if text:
                        return text

    return None
