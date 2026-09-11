# -*- coding: utf-8 -*-
from pathlib import Path

path = Path('코드리뷰.md')
content = path.read_text(encoding='utf-8-sig')

# 1. 제목과 개요 업데이트
old_header = """# 🔍 ComfyCraft AI Easy Studio v0.3 — 코드 리뷰 보고서

> **분석 대상**: 프로젝트 전체 (약 30개 소스 파일, 10개 JSON 설정, 113KB UI 파일)
> **분석 일시**: 2026-09-10

---

## 📁 프로젝트 구조 개요

```mermaid
flowchart TD
    main["main.py (2,139줄)\\n메인 컨트롤러"]
    
    subgraph app["app 패키지"]
        init["__init__.py\\n(전체 API 중앙 export)"]
        
        subgraph core["core 모듈"]
            api["api_client.py\\nHTTP/WS 클라이언트"]
            cfg["config_manager.py\\n설정 로드/저장"]
            pool["connection_pool.py\\n연결 풀"]
            fetch["model_fetcher.py\\n모델 목록 조회"]
            reg["model_registry.py\\n모델 프로파일 매칭"]
            mss["model_status_service.py\\n연결 상태 서비스"]
            wm["workflow_manager.py\\n워크플로우 렌더링"]
        end

        subgraph gui["gui 모듈"]
            psb["play_stop_button.py\\n커스텀 생성/정지 버튼"]
            stb["split_text_button.py\\n분할 텍스트 버튼"]
            tm["theme_manager.py\\n테마 관리"]
            ul["ui_loader.py\\nUI 파일 로더"]
        end

        subgraph sections["sections 모듈"]
            conn["connection.py\\n연결 확인"]
            exec["execution.py\\n진행 상황/타이머"]
            gen["generation.py\\n이미지 생성 워커"]
            prom["prompt.py\\n프롬프트 처리"]
            res["result.py\\n결과 이미지 관리"]
        end
    end

    main --> init
    init --> core
    init --> sections
    main --> gui
    gen --> api
    gen --> wm
    gen --> reg
```

전체적으로 **모듈 분리가 잘 되어 있고**, 기능별로 역할이 명확하게 나뉘어 있습니다."""

new_header = """# 🔍 ComfyCraft AI Easy Studio v0.3 — 코드 리뷰 보고서

> **분석 대상**: 프로젝트 전체 (약 30개 소스 파일, 10개 JSON 설정, 113KB UI 파일)
> **분석 일시**: 2026-09-10
> **업데이트**: 2026-09-10 (테마 시스템 개선 반영)

---

## 📁 프로젝트 구조 개요

```mermaid
flowchart TD
    main["main.py\\n메인 컨트롤러"]
    
    subgraph app["app 패키지"]
        init["__init__.py\\n(전체 API 중앙 export)"]
        
        subgraph core["core 모듈"]
            api["api_client.py\\nHTTP/WS 클라이언트"]
            cfg["config_manager.py\\n설정 로드/저장"]
            pool["connection_pool.py\\n연결 풀"]
            fetch["model_fetcher.py\\n모델 목록 조회"]
            reg["model_registry.py\\n모델 프로파일 매칭"]
            mss["model_status_service.py\\n연결 상태 서비스"]
            wm["workflow_manager.py\\n워크플로우 렌더링"]
        end

        subgraph gui["gui 모듈"]
            psb["play_stop_button.py\\n커스텀 생성/정지 버튼\\n+ 테마 색상 지원"]
            stb["split_text_button.py\\n분할 텍스트 버튼\\n+ 테마 색상 지원"]
            tm["theme_manager.py\\n테마 관리\\n+ 버튼 색상 테이블"]
            ul["ui_loader.py\\nUI 파일 로더"]
        end

        subgraph sections["sections 모듈"]
            conn["connection.py\\n연결 확인"]
            exec["execution.py\\n진행 상황/타이머"]
            gen["generation.py\\n이미지 생성 워커"]
            prom["prompt.py\\n프롬프트 처리"]
            res["result.py\\n결과 이미지 관리"]
        end
    end

    main --> init
    init --> core
    init --> sections
    main --> gui
    gen --> api
    gen --> wm
    gen --> reg
    stb --> tm
    psb --> tm
```

전체적으로 **모듈 분리가 잘 되어 있고**, 기능별로 역할이 명확하게 나뉘어 있습니다. **테마 시스템**이 개선되어 커스텀 버튼들도 테마 변경 시 자동으로 색상이 변경됩니다."""

content = content.replace(old_header, new_header)

# 2. 잘 된 점 테이블 업데이트
old_good = """| 영역 | 평가 |
|---|---|
| **모듈 분리** | core/gui/sections 3계층으로 잘 나뉨 |
| **설정 관리** | dataclass 기반 AppConfig로 타입 안전한 설정 |
| **모델 프로파일** | 자동 감지 + JSON 기반 확장 가능한 구조 |
| **워크플로우 템플릿** | 플레이스홀더 기반 렌더링으로 유연한 워크플로우 |
| **테마 시스템** | 9개 테마, QSS 기반, 설정 저장 |
| **API 클라이언트** | 자동 재시도, 세션 관리 포함 |
| **캐싱** | TTL 기반 모델 목록 캐시 (model_fetcher) |
| **UI 로더** | 커스텀 위젯 자동 교체 (PlayStopButton, SplitTextButton) |
| **한국어 UX** | 모든 UI 텍스트와 오류 메시지가 한국어 |"""

new_good = """| 영역 | 평가 |
|---|---|
| **모듈 분리** | core/gui/sections 3계층으로 잘 나뉨 |
| **설정 관리** | dataclass 기반 AppConfig로 타입 안전한 설정 |
| **모델 프로파일** | 자동 감지 + JSON 기반 확장 가능한 구조 |
| **워크플로우 템플릿** | 플레이스홀더 기반 렌더링으로 유연한 워크플로우 |
| **테마 시스템** | 9개 테마, QSS 기반, 설정 저장, 커스텀 버튼 색상 자동 변경 |
| **API 클라이언트** | 자동 재시도, 세션 관리 포함 |
| **캐싱** | TTL 기반 모델 목록 캐시 (model_fetcher) |
| **UI 로더** | 커스텀 위젯 자동 교체 (PlayStopButton, SplitTextButton) |
| **한국어 UX** | 모든 UI 텍스트와 오류 메시지가 한국어 |
| **버튼 테마 연동** | SplitTextButton/PlayStopButton에 `updateThemeColors()` 클래스 메서드로 테마 변경 시 색상 자동 갱신 |"""

content = content.replace(old_good, new_good)

path.write_text(content, encoding='utf-8')
print('1단계 완료: 구조도 및 잘 된 점 업데이트')
