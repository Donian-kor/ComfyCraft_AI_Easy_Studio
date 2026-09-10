
from pathlib import Path

path = Path('app/gui/split_text_button.py')
content = p.read_text(encoding='utf-8')

old = 'self._icon_gap_px = 8  # space between icon and text

        self.setFont(self._make_font())'
new = 