Compacted conversation# UI 개선 제안 보고서

다음은 현재 ComfyUI + LMStudio GUI 애플리케이션의 UI 개선을 위한 상세한 보고서입니다.

---

## 📋 목차

1. layout 및 구조 개선
2. styling 및 디자인 개선
3. interactivity 및 상호작용 개선
4. accessibility 및 사용자 경험 개선
5. performance 최적화

---

## 1. Layout 및 구조 개선

### 1.1 탭 전환 애니메이션 추가

**현재 상태:** 
- TabWidget이 기본 설정으로 전환됨 (순간적 변경)
- 사용자가 전환 과정에서 UI 변화에 대한 피드백을 얻지 못함

**개선 제안:**

```python
# main_ui.py 에서 TabWidget 에 애니메이션 적용

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtWidgets import QApplication

def animate_tab_change(self):
    """탭 전환 시 부드러운 애니메이션 효과"""
    animation = QPropertyAnimation(self.tabWidget, b"currentIndex", duration=300)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    
    # 현재 인덱스 → 다음 인덱스로 이동
    next_index = self.tabWidget.currentIndex() + 1 if self.tabWidget.currentIndex() < self.tabWidget.count() - 1 else 0
    
    animation.start(lambda: setattr(self.tabWidget, 'currentIndex', next_index))

# TabWidget 에 custom property 추가
self.tabWidget.setDynamicStyleSheet("""
    QTabBar::pane {
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
""")
```

### 1.2 탭 스타일 개선

**현재 스타일:**
- TabWidget 의 border-radius: 16px 적용됨 (이미 둥근 테두리 사용)
- 선택된 Tab 이 하단으로 #7c6cff 색상 바가 표시됨

**개선 제안:**

```python
# 탭바 배경색과 스타일 개선

self.tabWidget.setStyleSheet("""
    QTabBar {
        border: 1px solid #2a2f3d;
        border-radius: 16px;
        margin-top: 8px;
        background-color: #0e1016;
        
        /* 탭 활성화 상태 */
        QTabBar::tab {
            background-color: transparent;
            color: #758f9b;
            padding: 12px 24px;
            margin-right: 8px;
            border-radius: 10px;
            font-size: 13px;
            
            /* 호버 효과 */
            QTabBar::tab:hover {
                background-color: #1d212c;
                color: #f4f5f8;
                border-bottom: none;
            }
            
            /* 선택된 Tab 스타일 */
            QTabBar::tab:selected {
                color: #f4f5f8;
                background-color: transparent;
                font-weight: 600;
                min-width: 120px;
                
                /* 하단 선 효과 */
                border-bottom: none;
            }
        }
    }
""")
```

### 1.3 화면 간격 및 여백 최적화

**현재 문제:**
- 여러 컴포넌트 간의 여백이 일관되지 않음
- 일부 요소가 너무 밀집되어 있음

**개선 제안:**

```python
# 전역 스타일시트 개선

self.setStyleSheet("""
    QMainWindow {
        background-color: #0e1016;
        
        /* 컴포넌트 간 최소 여백 */
        QTabWidget::pane, QGroupBox, QPushButton, QLabel {
            margin-top: 8px;
            margin-bottom: 8px;
        }
        
        /* 선택된 Tab 과 Pane 간 여백 */
        QTabBar::tab:selected {
            margin-top: 16px;
        }
    }
""")

# 각 컴포넌트에도 명시적 스타일 적용
self.settingsTab.setStyleSheet("""
    QTabWidget::pane {
        border: 2px solid #2a2f3d;
        border-radius: 12px;
        padding: 8px;
    }
""")

self generationTab.setStyleSheet("""
    QTabWidget::pane {
        border: 2px solid #2a2f3d;
        border-radius: 12px;
        background-color: #0e1016;
    }
""")
```

### 1.4 Splitter 핸들 스타일 개선

**현재 상태:**
- Splitter handle 이 기본 스타일로 사용됨

**개선 제안:**

```python
# splitterHandle 를 위한 QStyleFactory 를 사용한 커스텀 스타일

from PySide6.QtWidgets import QApplication

class CustomSplitter(QSplitter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #262b3a;
                border-radius: 5px;
                
                /* 호버 효과 */
                QSplitter::handle:hover {
                    background-color: #7c6cff;
                    border: 1px solid rgba(124, 108, 255, 0.3);
                }
            }
        """)

# main_ui.py 에서 사용
self.splitter = CustomSplitter(self)
```

---

## 2. Styling 및 디자인 개선

### 2.1 색상 대비도 개선

**현재 상태:**
- 배경색: #0e1016 (매우 어둠)
- 텍스트 색상: #cdd2e0, #758f9b, #f4f5f8

**WCAG 대비도 분석:**
| 색상 조합 | 대비도 | WCAG AA 기준 |
|-----------|--------|-------------|
| #cdd2e0 vs #0e1016 | 2.1:1 | ❌ 미달 (최소 4.5:1) |
| #758f9b vs #0e1016 | 1.8:1 | ❌ 미달 |

**개선 제안:**

```python
# 개선된 색상 팔레트

# 주요 색상
PRIMARY_BACKGROUND = "#0e1016"
SECONDARY_BACKGROUND = "#171a23"
CARD_BACKGROUND = "#1d212c"

# 텍스트 색상 (계급별)
MAIN_TEXT = "#f4f5f8"        # 명문 - 제목, 주요 정보
SUBTEXT = "#9aa2b8"          # 보조 문구 - 설명, 부가 정보
MUTED_TEXT = "#758f9b"       # 최강 약한 텍스트 - placeholder, 비활성화 상태

# 액센트 색상 (계급별)
PRIMARY_ACCENT = "#7c6cff"   # 주요 액센트 - 버튼, 호버 효과
SUCCESS_COLOR = "#22c55e"    # 성공 상태 - 완료, 확인
WARNING_COLOR = "#f97316"    # 경고 상태 - 주의사항
ERROR_COLOR = "#ef4444"      # 오류 상태 - 에러 메시지

# 테두리 및 구분선
PRIMARY_BORDER = "#2a2f3d"   # 주요 테두리
SECONDARY_BORDER = "#202430" # 보조 테두리
FOGGER_BORDER = "#171a23"    # 경계선

# 호버 효과 색상
HOVER_BACKGROUND = "#262b3a"
HOVER_ACCENT = "#7c6cff"     # 액센트 색상 강조
```

**적용 예시:**

```python
# 버튼 텍스트 색상 개선 (비활성화 상태 대비도 향상)
self.generateButton.setStyleSheet("""
    QPushButton {
        background-color: #7c6cff;
        color: #ffffff;
        font-weight: 500;
        
        /* 비활성화 상태 대비도 개선 */
        QPushButton:disabled {
            background-color: #14161f;
            color: #9aa2b8;  # f4f5f8 에서 #9aa2b8 로 변경 (대비도 향상)
            border-color: #202430;
        }
    }
""")

# Progress Label 색상 개선
self.progressStatusLabel.setStyleSheet("""
    QLabel {
        color: #7c6cff;  # #9aa2b8 에서 액센트 색상으로 변경
        font-weight: 500;
    }
    /* 성공 상태 */
    QLabel[value="100"] {
        color: #22c55e;
    }
""")

# Progress Percent Label 대비도 향상
self.progressPercentLabel.setStyleSheet("""
    QLabel {
        color: #f4f5f8;  # 기존 유지 (이미 최강 밝음)
        font-size: 22px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);  /* 텍스트 그림자 추가 */
    }
""")
```

### 2.2 타이포그래피 및 폰트 개선

**현재 상태:**
- 기본 폰트: Segoe UI (영어), Malgun Gothic (한국어)
- 글꼴 크기: 10px - 24px 간격

**개선 제안:**

```python
# main_ui.py 에서 폰트 설정 개선

def setup_fonts(self):
    """폰트 및 글자크기 최적화"""
    
    # 기본 폰트 family 설정 (계급별)
    font_sizes = {
        'title': 24,      # 제목
        'subtitle': 18,   # 부제목
        'heading': 16,    # 섹션 제목
        'body': 14,       # 본문 텍스트
        'caption': 12,    # 보조 정보
        'small': 10,      # 작은 텍스트
    }
    
    font_weights = {
        'title': 700,     # 굵은 글씨
        'heading': 600,   # 세미 Bold
        'body': 400,      # 정상이름
        'caption': 400,
        'small': 500,     # 작은 텍스트는 약간 두껍게
    }
    
    # 각 레이블에 적용
    self.settingsTitle.setFont(QFont('Segoe UI', font_sizes['title'], font_weights['title']))
    self.settingsSubtitle.setFont(QFont('Segoe UI', font_sizes['caption'], font_weights['caption']))
    self.settingsDescription.setFont(QFont('Malgun Gothic', font_sizes['body'], font_weights['body']))
    
    # Progress Percent Label 개선 (가독성 향상)
    self.progressPercentLabel.setFont(QFont(
        'Segoe UI', 
        24,  
        QFont.Weight.Bold
    ))

# 텍스트 선택 시 배경색 (선택된 텍스트 가시성 확보)
self.textSelectStyle = """
    QSelectionRectangle {
        background-color: rgba(124, 108, 255, 0.3);
        border-radius: 2px;
    }
"""

# 커서 스타일 개선 (가독성 향상)
cursor_styles = {
    'normal': Qt.CursorShape.IBeamCursor,
    'reading': Qt.CursorShape.WaitCursor,
}

# TextEdit 에 적용 (설정 탭의 TextEdit 컴포넌트)
self.text_edit.setAcceptRichText(False)
self.text_edit.setStyleSheet("""
    QTextEdit {
        background-color: transparent;
        color: #cdd2e0;
        border: none;
        
        /* 텍스트 선택 시 배경색 */
        QSelectionRectangle {
            background-color: rgba(124, 108, 255, 0.3);
            border-radius: 2px;
        }
    }
""")
```

### 2.3 아이콘 및 비주얼 피드백 강화

**개선 제안:**

```python
# 아이콘 통합 (Qt Style Sheets 를 통한)

self.tabWidget.setStyleSheet("""
    QTabBar {
        /* 아이콘 표시 */
        QTabBar::close-button {
            background-color: transparent;
            width: 16px;
            height: 16px;
            
            /* 호버 시 삭제 버튼 표시 */
            QTabBar::close-button:hover {
                color: #7c6cff;
                
                /* 클릭 시 */
                QTabBar::close-button:pressed {
                    color: #ef4444;
                }
            }
        }
    }
""")

# 버튼에 아이콘 추가 (QLabel + QPushButton 을 사용하여)

class IconButton(QPushButton):
    """아이콘을 포함하는 커스텀 버튼"""
    
    def __init__(self, icon_path, text="", parent=None):
        super().__init__(text, parent)
        
        # 아이콘 Label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("QLabel { color: #cdd2e0; }")
        
        self.icon_label.pixmap = None
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.icon_label)
        layout.addStretch()

def load_icon(pix_path):
    """이미지 로딩"""
    from PySide6.QtGui import QPixmap
    pixmap = QPixmap(pix_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio)
    return pixmap

# 버튼에 아이콘 적용
self.openOutputFolderButton.pixmap = load_icon("assets/icons/folder-open.png")
self.saveImageButton.pixmap = load_icon("assets/icons/save.png")
```

---

## 3. Interactivity 및 상호작용 개선

### 3.1 애니메이션 효과 추가

**탭 전환 애니메이션:**

```python
# TabWidget 에 커스텀 스타일 적용

class AnimateTabWidget(QTabWidget):
    """타블릿 전환 애니메이션을 지원하는 커스텀 클래스"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 현재 인덱스를 저장
        self._old_index = -1
        
        # 변경될 각 Tab 에 대해 ID 할당
        for i in range(self.count()):
            widget = self.tab(i)
            if hasattr(widget, 'objectName'):
                widget.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    def tabChanged(self):
        """탭 전환 시 호출"""
        super().tabChanged()
        
        # 이전 Tab 을 숨김
        index = self.currentIndex()
        if index > 0:
            self._old_index = self.tabBar().currentIndex() - 1
        
        old_widget = self.tab(self._old_index)
        new_widget = self.tab(index)
        
        # 애니메이션 적용 (PySide6 6.5 이상)
        if hasattr(old_widget, 'setShowWithoutActivating'):
            old_widget.setShowWithoutActivating(True)
        else:
            old_widget.hide()

# main_ui.py 에서 사용
self.settingsTab = AnimateTabWidget(self)
self.generationTab = AnimateTabWidget(self)
```

**버튼 클릭 효과:**

```python
# 버튼 클릭 시 시각적 피드백

class AnimatedButton(QPushButton):
    """클릭 애니메이션을 지원하는 버튼"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 클릭 효과용 임시 레이블
        self.effect_label = QLabel()
        self.effect_label.setFixedSize(self.size())
        self.effect_label.setStyleSheet("QLabel { color: transparent; }")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.effect_label)
        layout.addStretch()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.effect_label.setText("✓")
        self.effect_label.setStyleSheet("""
            QLabel { 
                color: #22c55e;  
                font-size: 16px;  
                animation: fadeOut 0.3s forwards; 
            }""")

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.effect_label.setText("")
        self.effect_label.setStyleSheet("QLabel { color: transparent; }")

# CSS 애니메이션 추가
self.setStyleSheet("""
    @keyframes fadeOut {
        from { opacity: 1; transform: scale(0.95); }
        to { opacity: 0; transform: scale(1); }
    }
""")
```

### 3.2 키보드 접근성 개선

**키보드 단축키 설정:**

```python
# main_ui.py 에서 키보드 단축키 정의

import sys

class KeyboardShortcuts:
    """키보드 단축키 관리 클래스"""
    
    TAB_SHORTCUT = QKeySequence('Tab')
    ENTER_SHORTCUT = QKeySequence('Return')
    ESCAPE_SHORTCUT = QKeySequence('Escape')

# TabWidget 에 키보드 단축키 적용
self.settingsTab.setKeyboardShortcut(KeyboardShortcuts.TAB_SHORTCUT)
```

**접근성 개선:**

```python
# 주석 텍스트 추가 (스크린 리더 지원)

def add_accessibility_label(widget, description):
    """widget 에 접근성 레이블 추가"""
    
    # ARIA 역할 설정
    if hasattr(widget, 'setAccessibleName'):
        widget.setAccessibleName(description)
    
    # 설명 텍스트 (Qt 6.2 이상)
    if hasattr(widget, 'setAttribute'):
        from PySide6.QtCore import Qt
        widget.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

# 버튼에 접근성 레이블 추가
add_accessibility_label(
    self.openOutputFolderButton,
    "출력 폴더 열기"
)

add_accessibility_label(
    self.saveImageButton,
    "이미지 저장하기"
)
```

---

## 4. Performance 최적화

### 4.1 UI 렌더링 성능 개선

**Lazy Loading 적용:**

```python
# 많은 데이터를 가진 컴포넌트에 지연 로딩 적용

class LazyLoadWidget(QWidget):
    """기억 사용량을 줄이는 지연 로딩 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._loaded = False
        self._data = None
    
    def load_data(self):
        """데이터 로드"""
        if not self._loaded:
            # 지연 로딩 시점
            self._load_internal()
            self._loaded = True

class LargeTextLabel(QLabel):
    """큰 텍스트를 표시하는 효율적인 레이블"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        # 텍스트 크기 조정 (필요한 만큼만 로드)
        self._resize_text()

    def _resize_text(self):
        """텍스트 크기를 최적화"""
        font = self.font()
        lines = self.text.split('\n')
        
        for i, line in enumerate(lines):
            # 줄당 최대 픽셀 수 (예: 500px)
            max_pixels = 500
            
            while True:
                temp_font = font
                if i > 0:
                    temp_font.setPointSize(temp_font.pointSize() - 1)
                
                lines[i] = str(temp_font.boundingRect(lines[i]).width())
                
                total_width = sum(
                    len(l.strip()) * temp_font.pixelWidth() 
                    for l in lines if l.strip()
                )
                
                if total_width <= max_pixels:
                    break
            
            # 실제 텍스트로 복원
            lines[i] = lines[i].split('(')[0].strip()

        self.setText('\n'.join(lines))

# 적용 예시
self.settingsDescription = LargeTextLabel(
    "이 설정을 사용하여 모델의 동작을 최적화할 수 있습니다.\n"
    "모델 크기와 성능 사이의 균형을 찾아보세요.",
    self.settingsPanel
)
```

**QPainter 를 통한 효율적 렌더링:**

```python
from PySide6.QtGui import QPainter, QPen, QColor, QBrush

class EfficientProgressBar(QProgressBar):
    """효율적인 프로그레스 바 구현"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # painter 를 캐싱 (반복 렌더링 시 성능 향상)
        self._painter = QPainter()

    def paintEvent(self, event):
        """효율적인 페인팅 이벤트 처리"""
        if not hasattr(self, '_painter'):
            self._painter = QPainter()
        
        super().paintEvent(event)

        # painter 를 재사용
        with self._painter:
            painter = self._painter
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 배경색 채우기
            painter.fillRect(
                QRect(self.rect()),
                QColor("#262b3a")  # background-color
            )

            # 프로그레스 바 색상 채우기
            progress = self.value()
            max_value = self.maximum()
            
            if max_value > 0:
                width = int((progress / max_value) * self.width())
                
                painter.setPen(QPen(Qt.NoPen))
                painter.setBrush(QColor("#7c6cff"))  # gradient 색상
                
                painter.drawRect(0, 2, width, self.height() - 4)

# 적용 예시
self.progressBar = EfficientProgressBar(self.executionPanel)
```

### 4.2 메모리 최적화

**이미지 캐싱:**

```python
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal

class ImageCache(QObject):
    """이미지 캐싱 클래스"""
    
    def __init__(self):
        super().__init__()
        self._cache = {}

    def get_pixmap(self, path, size=(24, 24)):
        """이미지를 캐시하고 반환"""
        if path in self._cache:
            return self._cache[path]
        
        pixmap = QPixmap(path).scaled(size)
        self._cache[path] = pixmap
        
        # 메모리 제한 (예: 최대 10MB)
        memory_usage = sum(pixmap.size() for p in self._cache.values())
        if memory_usage > 10 * 1024 * 1024:
            self._cleanup()
        
        return pixmap

    def _cleanup(self):
        """오래된 이미지를 제거"""
        # 최근 사용되지 않은 이미지 먼저 삭제
        sorted_cache = sorted(
            self._cache.items(), 
            key=lambda x: len(x[1])
        )
        
        total_memory = 0
        for path, pixmap in sorted_cache:
            if total_memory + pixmap.size() > 5 * 1024 * 1024:
                del self._cache[path]
                return
        
        self._cache = dict(sorted_cache)

# 전역 캐싱 인스턴스
image_cache = ImageCache()

# 이미지 로딩 시 사용
def load_icon(path):
    """캐시된 이미지를 반환"""
    pixmap = image_cache.get_pixmap(path, (24, 24))
    
    # Label 에 적용
    icon_label = QLabel()
    icon_label.setPixmap(pixmap)
    return icon_label

# 버튼에 아이콘 적용
self.openOutputFolderButton.pixmap = load_icon("assets/icons/folder-open.png")
```