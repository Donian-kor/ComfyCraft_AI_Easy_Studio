"""Flet UI 스레드로 작업을 넘기는 통로.

JobManager / 모델 조회 같은 작업은 threading.Thread 에서 도는데, Flet
컨트롤은 UI 스레드에서만 갱신할 수 있다. 다른 스레드에서 update() 를
부르면 RuntimeError 로 조용히 실패한다(예전 safe_update 가 그 오류를
삼켜서 '모델을 바꿔도 아무 반응이 없다' 는 증상이 났다).

그래서 루프 기억과 넘기는 동작을 한 곳에 모은다. common.safe_update() 와
app_state 가 둘 다 이 모듈을 쓴다(서로 순환 참조를 피하기 위함).
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any, Callable, Optional

_ui_loop: Optional[asyncio.AbstractEventLoop] = None
_ui_thread_id: Optional[int] = None


def set_ui_loop(loop: Optional[asyncio.AbstractEventLoop]) -> None:
    """Flet 이 만든 이벤트 루프를 기억한다 (앱 시작 시 1회 호출).

    루프를 등록한 이 호출 자체가 UI 스레드에서 일어나므로, 그때의 스레드
    번호도 함께 기억한다. '지금 UI 스레드인가?' 를 판정할 때 쓴다.
    """
    global _ui_loop, _ui_thread_id
    _ui_loop = loop
    _ui_thread_id = threading.get_ident() if loop is not None else None


def is_ui_thread() -> bool:
    """지금 UI 스레드에서 돌고 있으면 True.

    'asyncio 루프가 돌고 있는가' 로 판정하면 안 된다. Job 스레드에도
    asyncio 루프가 없기 때문에 둘을 구분할 수 없다(그게 이전 판정의
    버그였다). set_ui_loop() 이 기억한 스레드 번호로 판정한다.
    루프를 한 번도 등록하지 않았으면(헤드리스 테스트) 그냥 True 다.
    """
    if _ui_loop is None:
        return True
    return threading.get_ident() == _ui_thread_id
def run_on_ui(fn: Callable[[], Any]) -> None:
    """백그라운드 스레드의 갱신을 UI 스레드로 넘긴다.

    루프가 아직 없으면(테스트/초기화) 조용히 건너뛴다.
    """
    loop = _ui_loop
    if loop is None or loop.is_closed():
        return
    try:
        asyncio.run_coroutine_threadsafe(_call(fn), loop)
    except RuntimeError:
        # 루프가 종료되는 타이밍에 겹친 경우. 앱 종료를 막지 않는다.
        pass


async def _call(fn: Callable[[], Any]) -> None:
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            await result
    except Exception:
        # UI 갱신 실패가 Job 이나 앱 전체를 죽이면 안 된다
        pass