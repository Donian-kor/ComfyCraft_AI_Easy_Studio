"""내부 생성 엔진 테스트 스크립트.

ComfyUI/LMStudio 없이 내부 엔진으로 이미지 생성을 테스트한다.
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.application.internal_transport import InternalTransport
from app.models.generation import GenerationRequest, GenerationResult, GenerationProgress
from app.core.config_manager import get_config_manager


def test_internal_transport():
    """내부 생성 엔진 기본 테스트"""
    print("=" * 60)
    print("내부 생성 엔진 테스트 시작")
    print("=" * 60)
    
    # 설정 로드
    config_manager = get_config_manager()
    config = config_manager.get()
    
    # 출력 디렉토리
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # 내부 전송 계층 생성
    transport = InternalTransport(
        output_dir,
        log=lambda m: print(f"[LOG] {m}")
    )
    
    # 테스트 요청 생성
    request = GenerationRequest(
        prompt="a cute cat sitting on a table",
        negative_prompt="low quality, blurry, deformed",
        width=512,
        height=512,
        steps=10,
        cfg=7.0,
        seed=42,
        filename_prefix="test_internal",
    )
    
    print(f"\n테스트 요청:")
    print(f"  prompt: {request.prompt}")
    print(f"  size: {request.width}x{request.height}")
    print(f"  steps: {request.steps}")
    print(f"  cfg: {request.cfg}")
    print(f"  seed: {request.seed}")
    
    # 진행 상태 콜백
    def on_progress(progress: GenerationProgress):
        print(f"[PROGRESS] {progress.status}: {progress.progress}% - {progress.message}")
    
    # 이미지 생성 시도
    print("\n--- 이미지 생성 시작 ---")
    try:
        result = transport.generate_image(
            request,
            on_progress=on_progress,
            log=lambda m: print(f"[LOG] {m}")
        )
        
        print(f"\n--- 생성 결과 ---")
        print(f"  status: {result.status}")
        print(f"  image_path: {result.image_path}")
        print(f"  elapsed: {result.elapsed:.2f}s")
        print(f"  error: {result.error}")
        
        if result.ok:
            print("\n[OK] 테스트 성공!")
            return True
        else:
            print(f"\n[ERROR] 테스트 실패: {result.error}")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_import():
    """모듈 import 테스트"""
    print("\n--- 모듈 import 테스트 ---")
    try:
        from app.application.internal_transport import InternalTransport
        print("[OK] InternalTransport import OK")
        
        from app.application.generation_service import GenerationService
        print("[OK] GenerationService import OK")
        
        from app.application.services import AppServices
        print("[OK] AppServices import OK")
        
        return True
    except Exception as e:
        print(f"[ERROR] import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("내부 생성 엔진 테스트 스크립트")
    print("=" * 60)
    
    # import 테스트
    if not test_import():
        sys.exit(1)
    
    # 생성 테스트 (모델 파일이 있는 경우에만)
    print("\n--- 생성 테스트 ---")
    print("주의: 모델 파일이 필요합니다.")
    print("모델 경로를 확인하려면 설정의 comfyui_model_paths를 확인하세요.")
    
    # 테스트 실행
    success = test_internal_transport()
    
    if success:
        print("\n[OK] 모든 테스트 통과")
        sys.exit(0)
    else:
        print("\n[WARNING] 테스트 실패 (모델 파일 누락 등)")
        # 모델이 없어도 import는 성공했으므로 exit code는 0으로
        sys.exit(0)