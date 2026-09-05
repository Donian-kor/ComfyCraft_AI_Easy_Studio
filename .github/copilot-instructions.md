# GitHub Copilot Instructions

## Response Language

- Always respond in Korean (한국어), regardless of the language used by the user.
- If the user asks in English, always answer in Korean.
- If the user asks in Japanese, Chinese, or any other language, always answer in Korean.
- Never switch the response language based on the language of the user's question.
- Technical terms may be written in English when appropriate, but explanations must be in Korean.

## Coding Rules

- Explain code and technical concepts in clear Korean.
- Keep programming language syntax unchanged.
- Keep Python, PySide6, PyQt, Qt, API, library, class, function, variable, and file names in their original form.
- Keep error messages and terminal output in their original form when quoting them.
- Write new code comments in Korean unless English is required.
- When modifying existing code, preserve the existing code structure and style whenever possible.
- Do not unnecessarily rewrite large portions of existing code.
- Clearly explain what was changed and why in Korean.

## UI & PySide6 Architecture Rules

- Always strictly separate the UI design code from the functional logic code.
- When creating a new program, structure it into two distinct parts:
  1. **UI Component (e.g., `ui_main.py`):** Base UI class generated/structured to match Qt Designer specifications (mimicking `pyside6-uic` output structure).
  2. **Logic Component (e.g., `main.py`):** A separate functional class that instantiates the UI class (prefer composition/composition structure like `self.ui = Ui_MainWindow()`) to handle events, signals, and slots.
- Ensure that the UI design remains fully editable in Qt Designer (Widget-based layout) without affecting or overwriting the functional logic code.
- Always use the latest **PySide6** version syntax and conventions. Never mix with PyQt5 or PyQt6 syntax.
  - Use `from PySide6.QtCore import Slot, Signal` instead of `@pyqtSlot` or `pyqtSignal`.
- **Thread Safety:** For any long-running, blocking, or heavy background tasks, always implement them using `QThread` and `QObject` (Worker pattern) to prevent the main UI thread from freezing.
- **Resource Management:** Ensure asset paths (images, icons, etc.) are handled robustly using dynamic path resolution (`pathlib` or `os.path`) or the Qt Resource System (`.qrc`) so that layouts do not break across different environment paths.
