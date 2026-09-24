#!/usr/bin/env python3
"""마크다운 → HTML 변환 빌드 스크립트"""
import markdown
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MD_DIR = BASE_DIR / "assets" / "help" / "md"
HTML_DIR = BASE_DIR / "assets" / "help" / "html"

HTML_DIR.mkdir(parents=True, exist_ok=True)

COMMON_CSS = """
<style>
:root { 
    --text: #1a1a1a; 
    --text-muted: #555; 
    --primary: #0078d4; 
    --bg: #ffffff; 
    --code-bg: #f4f4f4; 
    --border: #e0e0e0; 
    --header-border: #e0e0e0;
}
[data-theme="dark"] { 
    --text: #e0e0e0; 
    --text-muted: #aaa; 
    --primary: #60a5fa;
    --bg: #1e1e1e; 
    --code-bg: #2d2d2d; 
    --border: #333; 
    --header-border: #333;
}
body { 
    font-family: 'Pretendard', 'Noto Sans KR', system-ui; 
    font-size: 14px; 
    line-height: 1.6; 
    color: var(--text); 
    background: var(--bg); 
    padding: 24px; 
    max-width: 720px; 
    margin: 0 auto; 
}
h1 { 
    font-size: 24px; 
    font-weight: 700; 
    margin: 0 0 16px; 
    padding-bottom: 8px; 
    border-bottom: 1px solid var(--header-border); 
}
h2 { 
    font-size: 20px; 
    font-weight: 700; 
    margin: 24px 0 12px; 
    color: var(--primary); 
}
h3 { 
    font-size: 16px; 
    font-weight: 600; 
    margin: 18px 0 8px; 
}
p { 
    margin: 0 0 12px; 
}
code { 
    background: var(--code-bg); 
    padding: 2px 6px; 
    border-radius: 4px; 
    font-family: 'JetBrains Mono', 'Consolas', monospace; 
    font-size: 13px; 
}
pre { 
    background: var(--code-bg); 
    padding: 12px; 
    border-radius: 6px; 
    overflow-x: auto; 
    margin: 16px 0; 
}
pre code { 
    background: none; 
    padding: 0; 
}
table { 
    border-collapse: collapse; 
    width: 100%; 
    margin: 16px 0; 
}
th, td { 
    border: 1px solid var(--border); 
    padding: 8px 12px; 
    text-align: left; 
}
th { 
    background: var(--code-bg); 
    font-weight: 600; 
}
a { 
    color: var(--primary); 
    text-decoration: none; 
}
a:hover { 
    text-decoration: underline; 
}
img { 
    max-width: 100%; 
    height: auto; 
    border-radius: 4px; 
    display: block; 
    margin: 16px auto; 
}
ul, ol { 
    padding-left: 24px; 
    margin: 8px 0; 
}
li { 
    margin: 4px 0; 
}
hr { 
    border: none; 
    border-top: 1px solid var(--border); 
    margin: 24px 0; 
}
blockquote { 
    border-left: 3px solid var(--primary); 
    padding-left: 16px; 
    margin: 16px 0; 
    color: var(--text-muted); 
}
.toc {
    background: var(--code-bg);
    padding: 16px;
    border-radius: 6px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
}
.toc ul {
    list-style: none;
    padding-left: 0;
}
.toc li {
    margin: 4px 0;
}
.toc a {
    text-decoration: none;
    color: var(--text);
}
.toc a:hover {
    color: var(--primary);
}
</style>
"""

MD_EXTENSIONS = [
    'tables', 'fenced_code', 'toc', 'codehilite',
    'attr_list', 'def_list', 'footnotes', 'md_in_html'
]

HELP_SECTIONS = [
    {"id": "getting_started", "title": "시작하기", "icon": "play-circle", "file": "01_getting_started.html", "md": "01_getting_started.md"},
    {"id": "basic_usage", "title": "기본 워크플로우", "icon": "book-open", "file": "02_basic_usage.html", "md": "02_basic_usage.md"},
    {"id": "model_settings", "title": "모델 설정", "icon": "cpu", "file": "03_model_settings.html", "md": "03_model_settings.md"},
    {"id": "prompt_writing", "title": "프롬프트 작성 가이드", "icon": "edit-3", "file": "04_prompt_writing.html", "md": "04_prompt_writing.md"},
    {"id": "generation_options", "title": "생성 옵션 상세", "icon": "sliders", "file": "05_generation_options.html", "md": "05_generation_options.md"},
    {"id": "facedetailer", "title": "FaceDetailer 얼굴 보정", "icon": "user", "file": "06_facedetailer.html", "md": "06_facedetailer.md"},
    {"id": "history_shortcuts", "title": "히스토리 & 단축키", "icon": "image", "file": "07_history_shortcuts.html", "md": "07_history_shortcuts.md"},
    {"id": "faq", "title": "문제해결 (FAQ)", "icon": "help-circle", "file": "08_faq.html", "md": "08_faq.md"},
]

def convert_md_to_html(md_path: Path, html_path: Path, title: str):
    md_text = md_path.read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs={
        'codehilite': {'css_class': 'highlight', 'use_pygments': False},
        'toc': {'anchorlink': True, 'permalink': True, 'baselevel': 2},
    })
    html_body = md.convert(md_text)
    toc = md.toc if hasattr(md, 'toc') and md.toc else ''
    
    toc_html = f'<div class="toc">{toc}</div>' if toc else ''
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {COMMON_CSS}
</head>
<body>
    {toc_html}
    {html_body}
</body>
</html>"""
    html_path.write_text(html, encoding='utf-8')
    print(f"[OK] Generated: {html_path.name}")

def main():
    print("=" * 50)
    print("도움말 HTML 빌드 시작")
    print("=" * 50)
    
    for section in HELP_SECTIONS:
        md_path = MD_DIR / section["md"]
        html_path = HTML_DIR / section["file"]
        
        if md_path.exists():
            convert_md_to_html(md_path, html_path, section["title"])
        else:
            print("[WARN] Source file missing:", md_path.name)
    
    print("=" * 50)
    print("빌드 완료")
    print("=" * 50)

if __name__ == "__main__":
    main()