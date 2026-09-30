"""창 위치/크기 기억.

왜 필요한가: Flet 은 창 위치/크기를 저장하지 않는다. 그래서 앱을 껐다 켜면
1440x900 에 왼쪽 위에 딱 붙어 나온다. 사용자가 잡아 둔 배치를 매번 다시
맞추게 되는 셈이라 '창이 시작될때 사용자가 종료한 위치에서 시작' 요구로
구현한다.

설계:
  - 저장: app/ui/flet/window_state.py
  - 읽기/쓰기만 맡는다. Flet 을 직접 다루지 않아 테스트가 쉽다.

주의: Flet 의 Page.window 은 dataclass 필드라 getattr/setattr 이
작동한다. 과거 Qt app 의 setAttribute/setProperty 는 쓰지 않는다.
"""

from __future__ import annotations

from typing import Any, Optional

# 창을 화면 어디에도 못 뜨는 상태를 막는 안전장치.
# 모니터를 분리해서 왼쪽/위쪽 화면이 사라졌을 때 창이 보이지 않는
# 최악의 상황을 막는다. (좌표는 OS 가 주는 '가상 화면' 기준)
MIN_VISIBLE = 40
MIN_WIDTH = 840
MIN_HEIGHT = 560

# 기본 창 크기. app.py 의 WINDOW_WIDTH/HEIGHT 와 같아야 한다.
# (기존 UIConfig.window_width=960 은 아무 코드도 읽지 않는 죽은 값이었다.
#  실제로 쓰던 값은 app.py 의 1440x900 이라 여기를 기준으로 삼는다.)
DEFAULTS = {"width": 1440, "height": 900, "left": None, "top": None}


def _int_or_none(value: Any) -> Optional[int]:
    """숫자로 바꿀 수 있으면 int 로 돌려주고, 아니면 None.

    설정 파일이 손상되었을 때 '' 나 'abc' 로 크기가 들어올 수 있다.
    그대로 넣으면 Flet 이 예외를 내거나 창이 0 크기로 뜬다.
    """
    try:
        if value is None or isinstance(value, bool):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def sanitize(geometry: dict, *,
             min_width: int = MIN_WIDTH,
             min_height: int = MIN_HEIGHT) -> dict:
    """저장된 값을 그대로 쓸 수 있게 안전하게 손본다.

    - 크기는 최소값 이상으로 올린다 (0 이나 음수가 되면 창이 사라짐)
    - 위치는 음수여도 되지만, 화면 가장자리에서 최소 MIN_VISIBLE 만큼은
      보여야 한다. 안 그러면 창을 화면 밖에 두어 못 찾는 일이 생긴다.
    - 하나라도 유효하지 않으면 그 항목만 기본값/이전값으로 되돌린다.
    """
    incoming = geometry or {}
    out = dict(DEFAULTS)
    # 크기부터 확정한다. 위치 판정(화면 밖인지) 에 창 크기가 쓰이므로
    # 반드시 먼저 정리해야 한다.
    #
    # 회귀 근거: 예전에는 out.update(geometry) 로 값부터 덮어쓴 뒤
    # '유효할 때만' 다시 대입했는데, 그래서 0 이나 'abc' 가 그대로
    # 남았다. 창이 0 크기로 뜨는 버그. 이제 유효하지 않으면 기본값을 쓴다.
    width = _int_or_none(incoming.get("width"))
    height = _int_or_none(incoming.get("height"))
    out["width"] = width if (width and width >= min_width) else DEFAULTS["width"]
    out["height"] = height if (height and height >= min_height) else DEFAULTS["height"]

    for key in ("left", "top"):
        value = _int_or_none(incoming.get(key))
        if value is None:
            out[key] = None
            continue
        # 창의 왼쪽/위쪽 변이 화면에서 너무 멀리 나가면 가운데로 되돌린다.
        # 완전 offscreen 판정은 창 크기를 모르니 '살아 있는 최소 부분'만 본다.
        if key == "left" and value + out["width"] < MIN_VISIBLE:
            out[key] = None
        elif key == "top" and value + out["height"] < MIN_VISIBLE:
            out[key] = None
        else:
            out[key] = value
    return out


def load(config_manager: Any) -> dict:
    """설정에서 저장된 창 정보를 읽는다. 없으면 기본값(1440x900)."""
    try:
        ui = config_manager.get().ui
    except Exception:
        return dict(DEFAULTS)
    # 창 위치를 한 번도 저장하지 않았다면 = 아직 사용자가 잡지 않았다.
    # 이때는 설정 파일에 남아 있는 옛 기본값(960x780)을 따르지 말고
    # 앱 기본 크기를 쓴다. 첫 실행에서 갑자기 창이 작아지는 걸 막는다.
    if getattr(ui, "window_left", None) is None \
            and getattr(ui, "window_top", None) is None:
        return dict(DEFAULTS)
    return sanitize({
        "width": getattr(ui, "window_width", None),
        "height": getattr(ui, "window_height", None),
        "left": getattr(ui, "window_left", None),
        "top": getattr(ui, "window_top", None),
    })


def apply(page: Any, config_manager: Any) -> dict:
    """page.window 에 저장된 위치/크기를 적용한다. 적용값을 돌려준다.

    최소 크기(min_width/min_height) 는 항상 덮어쓴다. 사용자가 라이트 모드
    처럼 '좁은 창' 상태로 저장돼 있어도 앱 UI 가 깨지지 않도록.
    """
    geometry = load(config_manager)
    window = getattr(page, "window", None)
    if window is None:
        return geometry
    window.width = geometry["width"]
    window.height = geometry["height"]
    window.min_width = MIN_WIDTH
    window.min_height = MIN_HEIGHT
    # 위치는 None 이면 OS 기본(대체로 가운데) 이다. 직접 지정하지 않는다.
    if geometry["left"] is not None:
        window.left = geometry["left"]
    if geometry["top"] is not None:
        window.top = geometry["top"]
    return geometry


def snapshot(page: Any) -> dict:
    """지금 창 상태를 읽어 딕셔너리로 만든다.

    Flet 은 getattr 로 None 을 주기도 하므로 _int_or_none 으로 걸러낸다.
    """
    window = getattr(page, "window", None)
    if window is None:
        return dict(DEFAULTS)
    return sanitize({
        "width": getattr(window, "width", None),
        "height": getattr(window, "height", None),
        "left": getattr(window, "left", None),
        "top": getattr(window, "top", None),
    })


# --- 실제 창 크기 추적 ------------------------------------------------
# 회귀 근거: Flet 의 Page.window.width/height 는 *우리가 넣은 값*일 뿐이다.
# 사용자가 창을 리사이즈해도 Flet 이 이 필드를 갱신해 주지 않는다. 그래서
# 저장하니 항상 처음 크기(1440x900)가 그대로 저장됐다.
# 실제로 변하는 값은 PageResizeEvent 의 width/height 이므로 그걸 받아서
# '지금 창이 얼마나 큰지' 를 따로 기억해 둔다.

class SizeTracker:
    """on_resize 로 실제 창 크기를 기억한다.

    page.window.width 는 리사이즈를 반영하지 않으므로, 이 값을 근거로
    snapshot 을 고쳐 쓴다.

    단, on_resize 는 *페이지* 크기(제목창/테두리 제외)를 준다. 설정에
    저장하는 건 *창* 크기이므로, 처음 재울 때 '설정한 창 크기 - 실제
    페이지 크기' 만큼의 차이를 재고 뒤에 더해 준다. (제목창 높이 등)
    """

    def __init__(self) -> None:
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        # 창 크기와 페이지 크기의 차이(제목창+테두리). 첫 resize 에서 학습.
        self.chrome_w: int = 0
        self.chrome_h: int = 0
        self._learned = False

    def learn_chrome(self, window_w, window_h, page_w, page_h) -> None:
        """설정한 창 크기와 실제 페이지 크기 차이를 한 번만 학습한다.

        첫 resize 는 '창을 처음 크기에서 살짝이라도 바꾼' 시점이라,
        이때 측정한 차이가 가장 정확하다. (클라이언트가 첫 레이아웃
        크기를 알려주므로 창 테두리/제목창만큼의 차이가 반드시 난다)

        창이 더 커진 경우(페이지 > 설정값)에는 차이를 잴 수 없으므로
        그대로 둔다. 음수가 되게 만드는 것보다 0 이 안전하다.
        """
        if self._learned:
            return
        w = _int_or_none(window_w)
        h = _int_or_none(window_h)
        pw = _int_or_none(page_w)
        ph = _int_or_none(page_h)
        learned = False
        if w and pw and w > pw:
            self.chrome_w = w - pw
            learned = True
        if h and ph and h > ph:
            self.chrome_h = h - ph
            learned = True
        if pw and ph:
            self._learned = learned or self._learned

    def observe(self, event: Any) -> None:
        """PageResizeEvent 를 받아 실제 크기를 기록한다."""
        width = _int_or_none(getattr(event, "width", None))
        height = _int_or_none(getattr(event, "height", None))
        if width and width > 0:
            self.width = width
        if height and height > 0:
            self.height = height
        # 첫 리사이즈 시점에 창(설정값)과 페이지(실제) 크기를 비교해
        # 제목창 높이를 학습한다.
        #
        # 회귀 근거: PageResizeEvent.control 는 '창'이 아니라 Page 다.
        # 그래서 page.window 로 가야 한다. 예전 코드는 control.window 를
        # 봤는데 None 이라 학습이 영영 안 됐다(제목창 높이가 안 붙음).
        control = getattr(event, "control", None)
        window = getattr(control, "window", None)
        if window is not None:
            self.learn_chrome(getattr(window, "width", None),
                              getattr(window, "height", None),
                              width, height)

    def geometry(self, page: Any) -> dict:
        """저장 직전 상태를 만든다. 추적한 크기가 있으면 우선 쓴다.

        추적 값은 페이지 크기라 제목창 높이(chrome_h)를 더해 준다.
        """
        geometry = snapshot(page)
        if self.width:
            geometry["width"] = self.width + self.chrome_w
        if self.height:
            geometry["height"] = self.height + self.chrome_h
        return sanitize(geometry)


def save(page: Any, services: Any, tracker: Any = None) -> bool:
    """현재 창 위치/크기를 설정에 저장한다. 성공 여부를 돌려준다.

    tracker 가 있으면 그쪽의 실제 크기를 우선한다. (page.window.width 는
    리사이즈를 반영하지 않으므로)

    저장은 부가 기능이므로 실패해도 앱은 계속 돌아가야 한다.
    """
    try:
        geometry = (tracker.geometry(page) if tracker is not None
                    else snapshot(page))
        ui = services.config.ui
        ui.window_width = geometry["width"]
        ui.window_height = geometry["height"]
        ui.window_left = geometry["left"]
        ui.window_top = geometry["top"]
        return bool(services.config_manager.save(services.config))
    except Exception:
        return False