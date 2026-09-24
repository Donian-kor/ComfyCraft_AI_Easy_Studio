# 모델 설정

ComfyCraft AI Easy Studio는 **모델 프로파일 시스템**을 통해 선택한 모델에 최적화된 생성 파라미터를 자동으로 적용합니다.

---

## 모델 프로파일이란?

각 모델마다 최적의 생성 설정(Steps, CFG, Sampler, Scheduler, VAE, CLIP 등)이 다릅니다. 이 프로그램은 모델 이름을 분석해 자동으로 적절한 프로파일을 매칭하고 설정을 적용합니다.

### 지원 모델 패밀리

| 패밀리 | 대표 모델 | 특징 | 워크플로우 |
|--------|-----------|------|------------|
| **FLUX** | flux1-dev, flux1-schnell | 자연스러운 실사, 텍스트 렌더링 우수 | flux_gguf |
| **ZImage** | zimage_turbo, zimage_base | 고속 생성, 실사/일러스트 모두 강함 | zimage |
| **Z-ANIME** | z_anime_base, zanime_aio | 애니메이션/웹툰 특화 | zanime / anime_aio |
| **SDXL** | juggernaut_xl, dreamshaper_xl | 범용 고품질, 실사/일러스트 | sdxl |
| **GGUF** | *-Q4_K_S, *-Q8_0 등 | 양자화 모델, VRAM 절약 | gguf |

### 프로파일 자동 적용 확인

모델 선택 시 하단에 배지로 표시됨:
```
✓ FLUX_GGUF 최적 설정 적용됨 (CFG 1.0 / 20스텝)
```

상세 정보는 로그 창에서 확인:
```
모델 프로파일 로드: [FLUX_GGUF] flux1-dev-Q4_K_S
  └─ VAE: ae.safetensors
  └─ CLIP: t5xxl_fp16.safetensors, clip_l.safetensors
```

---

## 모델 선택 UI

### ComfyUI 모델 (생성용)
- 드롭다운: `생성 모델 (AI 엔진)`
- ComfyUI 서버에서 로드된 모델 목록 자동 동기화
- 모델 폴더 경로 설정 필요 (설정 대화상자에서)

### LM Studio 모델 (프롬프트용)
- 드롭다운: `언어 모델 (LM Studio AI)`
- LM Studio Local Server에서 로드된 모델 목록 자동 동기화
- 프롬프트 확장 품질에 영향 (큰 모델일수록 더 상세한 프롬프트 생성)

---

## 모델 폴더 설정

ComfyUI 모델을 인식하려면 **모델 폴더 경로**를 정확히 지정해야 합니다.

### 설정 방법
1. 헤더 `⚙️ 설정` 클릭 또는 ComfyUI 상태 버튼 클릭
2. `모델 폴더` 입력란에 ComfyUI `models` 폴더 경로 입력
   - 예: `C:\ComfyUI\models` 또는 `/home/user/ComfyUI/models`
3. `찾아보기` 버튼으로 폴더 선택 가능
4. `연결 확인`으로 모델 로드 테스트

### 폴더 구조 요구사항
```
models/
├── checkpoints/       # 메인 모델 (.safetensors, .gguf)
├── unet/              # FLUX 등 UNet 모델
├── diffusion_models/  # SD3, FLUX 등
├── vae/               # VAE 모델
├── clip/              # CLIP 텍스트 인코더
├── loras/             # LoRA 파일
├── sams/              # SAM 모델 (FaceDetailer용)
│   └── sam_vit_b_01ec64.pth
└── ultralytics/       # YOLO 모델 (FaceDetailer용)
    └── bbox/face_yolov8m.pt
```

**중요**: `checkpoints` 또는 `unet` / `diffusion_models` 폴더가 있어야 모델을 인식합니다.

---

## 📦 모델 파일 다운로드 가이드

### HuggingFace에서 다운로드 (권장)

| 모델 패밀리 | 추천 저장소 | 주요 파일 예시 |
|------------|-------------|----------------|
| **FLUX GGUF** | [city96/FLUX.1-dev-gguf](https://huggingface.co/city96/FLUX.1-dev-gguf) | `flux1-dev-Q4_K_S.gguf`, `flux1-dev-Q8_0.gguf` |
| **FLUX (원본)** | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | `flux1-dev.safetensors` |
| **ZImage Turbo** | [lllyasviel/zimage_turbo](https://huggingface.co/lllyasviel/zimage_turbo) | `zimage_turbo-Q4_K_S.gguf` |
| **Z-ANIME** | [z-animator/z_anime_base](https://huggingface.co/z-animator/z_anime_base) | `z_anime_base.safetensors` |
| **SDXL (Juggernaut)** | [RunDiffusion/Juggernaut-XL-v10](https://huggingface.co/RunDiffusion/Juggernaut-XL-v10) | `juggernaut_xl_v10.safetensors` |
| **SDXL (RealVis)** | [SG161222/RealVisXL_V5.0](https://huggingface.co/SG161222/RealVisXL_V5.0) | `realvisxl_v5.safetensors` |
| **VAE (FLUX)** | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | `ae.safetensors` (vae/ 폴더에) |
| **CLIP (FLUX)** | [comfyanonymous/flux_text_encoders](https://huggingface.co/comfyanonymous/flux_text_encoders) | `clip_l.safetensors`, `t5xxl_fp16.safetensors` (clip/ 폴더에) |

**다운로드 단계**:
1. 위 링크 클릭 → **Files and versions** 탭
2. 원하는 양자화 버전(Q4_K_S, Q8_0 등) 클릭
3. **Download** 버튼으로 파일 저장
4. 위 폴더 구조에 맞게 해당 폴더(`checkpoints`, `unet`, `vae`, `clip` 등)에 이동

### Civitai에서 다운로드 (대안)
- [Civitai 모델 검색](https://civitai.com/models) → 모델명 검색 → **Download** 버튼
- `.safetensors` 파일 우선 권장 (보안/호환성)
- 다운로드 후 `models/checkpoints/` 폴더에 배치

---

## ⚙️ GGUF 양자화 모델 선택 가이드

이 프로그램은 **GGUF 양자화 모델**을 적극 권장합니다 (VRAM 절약, 로딩 속도 향상).

| 양자화 버전 | VRAM 사용량 | 품질 | 추천 대상 |
|------------|-------------|------|-----------|
| **Q4_K_S** | ~6-8 GB | ★★★★☆ | **최적 균형** (기본 추천) |
| **Q4_K_M** | ~8-10 GB | ★★★★★ | 품질 중시, VRAM 10GB+ |
| **Q5_K_S** | ~8-10 GB | ★★★★★ | 고품질, VRAM 10GB+ |
| **Q8_0** | ~12-16 GB | ★★★★★ | 최고 품질, VRAM 16GB+ |
| **FP16 (원본)** | ~24 GB+ | ★★★★★ | RTX 4090 등 고사양만 |

> **초보자 팁**: `Q4_K_S` 버전부터 시작하세요. 대부분의 모델에서 품질 저하 체감 없이 VRAM을 절반 이하로 줄일 수 있습니다.

---

## 모델 패밀리별 필수 보조 파일

| 모델 패밀리 | 필수 보조 파일 | 저장 위치 |
|------------|----------------|-----------|
| **FLUX GGUF** | `clip_l.safetensors`, `t5xxl_fp16.safetensors` (또는 `t5-v1_1-xxl-encoder-Q4_K_M.gguf`), `ae.safetensors` | `clip/`, `vae/` |
| **ZImage** | `Z-Image-Engineer-V6-Q5_K_M.gguf` (CLIP), `ae.safetensors` (VAE) | `clip/`, `vae/` |
| **Z-ANIME** | (내장됨, 별도 CLIP/VAE 불필요) | - |
| **SDXL (Juggernaut/RealVis)** | `sdxl_vae.safetensors` (VAE) | `vae/` |

> **자동 적용**: 모델 선택 시 프로그램이 패밀리를 감지해 **최적 Steps/CFG/Sampler/VAE/CLIP을 자동 설정**합니다. (로그 창에서 `모델 프로파일 로드: [FAMILY] name` 확인)

---

## Z-ANIME 스타일 선택 (필수)

Z-ANIME 계열 모델(z_anime_base, zanime_aio 등) 선택 시 **스타일 선택 영역이 자동 표시**됩니다.

| 스타일 | 설명 | 추천 용도 |
|--------|------|-----------|
| 🇰🇷 **웹툰** | 한국 웹툰 스타일, 선명한 선화 | 웹툰, 만화, 캐릭터 |
| 🇯🇵 **일본애니** | 일본 애니메이션 스타일, 부드러운 채색 | 애니메이션, 일러스트 |
| ✨ **기본** | 중립적 베이스 스타일 | 자유로운 커스터마이징 |

**필수**: 생성 전 스타일 버튼 중 하나를 **반드시 선택**해야 합니다. (기본값 없음)

---

## 네거티브 프롬프트 자동 제어

모델에 따라 네거티브 프롬프트 입력란 표시 여부 자동 전환:

| 모델 유형 | 네거티브 프롬프트 | 이유 |
|-----------|-------------------|------|
| FLUX, ZImage | **숨김** | 자체 품질 제어, 부정 프롬프트 불필요 |
| SDXL, SD 1.5 | **표시** | 품질 저하 방지용 부정 키워드 필요 |

---

## 시드(Seed) 관리

| 설정 | 설명 |
|------|------|
| **-1 (기본)** | 매번 완전 랜덤 시드 |
| **고정 숫자** | 같은 프롬프트/설정으로 동일한 결과 재현 |
| **🔒 고정 토글** | 시드값 잠금 (다음 생성에도 유지) |
| **🎲 랜덤 버튼** | 새 랜덤 시드 생성 |

**활용**: 캐릭터 고정하며 포즈/배경만 바꿀 때 시드 고정 + 프롬프트 부분 수정

---

## 문제 해결

### "로드된 모델 없음" 표시
1. ComfyUI 서버가 실행 중인지 확인 (포트 8188)
2. 모델 폴더 경로가 올바른지 설정에서 확인
3. ComfyUI 웹 UI에서 모델이 로드되어 있는지 확인
4. 프로그램 재시작 후 `모델 새로고침`

### 모델 변경해도 설정 안 바뀜
- 모델 이름이 프로파일 매칭 패턴과 다를 수 있음
- 로그 창에서 `모델 프로파일 로드: [FAMILY] name` 확인
- 수동으로 Steps/CFG/Sampler 조정 후 사용

### VRAM 부족 (OOM)
- GGUF 양자화 모델 사용 (Q4_K_S 권장)
- 해상도 낮추기 (512×512 → 1024×1024 단계적 증가)
- Steps 줄이기 (20 이하)
- FaceDetailer 끄기

---

## 다음 단계

- [프롬프트 작성 가이드](04_prompt_writing.html) - 모델별 효과적인 프롬프트
- [생성 옵션 상세](05_generation_options.html) - 세부 파라미터 튜닝
- [FaceDetailer 얼굴 보정](06_facedetailer.html) - 얼굴 보정 옵션 및 활용