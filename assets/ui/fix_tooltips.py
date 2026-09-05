import re
from pathlib import Path
from typing import Match

# Get the project root directory (where this script is located)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Go up from assets/ui to project root
UI_FILE = PROJECT_ROOT / "assets" / "ui" / "main.ui"


def escape_html_in_tooltips(text: str) -> str:
    """Escape HTML entities in tooltip strings within XML"""
    # Replace HTML tags with escaped versions (XML entities)
    replacements = {
        '<br/>': '&lt;br/&gt;',
        '<br>': '&lt;br&gt;',
        '<b>': '&lt;b&gt;',
        '</b>': '&lt;/b&gt;',
        '<i>': '&lt;i&gt;',
        '</i>': '&lt;/i&gt;',
        '<p>': '&lt;p&gt;',
        '</p>': '&lt;/p&gt;',
        '<html>': '&lt;html&gt;',
        '</html>': '&lt;/html&gt;',
        '<head/>': '&lt;head/&gt;',
        '<body>': '&lt;body&gt;',
        '</body>': '&lt;/body&gt;',
    }
    result = text
    for html_tag, escaped in replacements.items():
        result = result.replace(html_tag, escaped)
    return result


def escape_tooltips(match: Match[str]) -> str:
    """Callback to escape tooltip content in a regex match"""
    full_match = match.group(0)
    # Find the string content
    string_match = re.search(r'<string>(.*?)</string>', full_match, re.DOTALL)
    if string_match:
        original = string_match.group(1)
        escaped = escape_html_in_tooltips(original)
        return full_match.replace(original, escaped)
    return full_match


def main() -> None:
    """Main function to fix tooltips in the UI file"""
    if not UI_FILE.exists():
        print(f"Error: UI file not found at {UI_FILE}")
        return

    # Read the file
    content = UI_FILE.read_text(encoding='utf-8')

    # Find all toolTip properties and apply escaping
    pattern = r'(<property name="toolTip">\s*<string>.*?</string>\s*</property>)'
    content = re.sub(pattern, escape_tooltips, content, flags=re.DOTALL)

    # Write back to the same file
    UI_FILE.write_text(content, encoding='utf-8')
    print(f"Done! Fixed tooltips in {UI_FILE}")


if __name__ == "__main__":
    main()