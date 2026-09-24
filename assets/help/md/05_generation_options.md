# 이미지 생성 옵션

생성 품질과 속도를 결정하는 핵심 파라미터들을 설명합니다. 모델 프로파일로 자동 적용되지만, 이해하고 직접 조정하면 더 좋은 결과를 얻을 수 있습니다.

## 핵심 파라미터

### Steps (샘플링 스텝)
| 값 | 효과 | 추천 |
|----|------|------|
| 10~15 | 빠름, 거친 결과 | 테스트용 |
| **20~30** | **균형 (기본)** | **대부분 상황** |
| 40~50 | 느림, 매우 정교 | 최종 고품질 생성 |
| 50+ | 매우 느림, 한계효과 | 특수 목적 |

**모델별 기본값**: FLUX=20, SDXL=25, Z-ANIME=20, ZImage=15~20

### CFG Scale (Classifier-Free Guidance)
프롬프트를 얼마나 강하게 따를지 제어

| 값 | 효과 | 추천 |
|----|------|------|
| 1.0~2.0 | 프롬프트 느슨함, 창의적 | FLUX 계열 |
| **3.5~7.0** | **균형 (기본)** | **SDXL, Z-ANIME** |
| 7.0~12.0 | 프롬프트 엄격, 인위적 가능 | 강한 스타일 강요 시 |
| 12+ | 과도, 아티팩트 발생 | 비추천 |

**모델별 기본값**: FLUX=1.0, SDXL=7.0, Z-ANIME=4.0~5.0, ZImage=3.5

### Sampler (샘플러)
노이즈에서 이미지를 복원하는 알고리즘

| 샘플러 | 특징 | 추천 모델 |
|--------|------|-----------|
| **DPM++ 2M** | 빠름, 안정적, 범용 | 거의 모든 모델 |
| **DPM++ 2M Karras** | Karras 노이즈 스케줄, 품질↑ | SDXL, SD1.5 |
| **Euler a** | 빠름, 확률적, 다양성 | SD1.5, 애니메이션 |
| **Euler** | 결정론적, 재현성 좋음 | 테스트/비교 |
| **DDIM** | 결정론적, img2img 적합 | img2img, 인페인팅 |
| **UniPC** | 매우 빠름, 적은 스텝 | FLUX, 빠른 생성 |

### Scheduler (노이즈 스케줄러)
스텝별 노이즈 감소 곡선

| 스케줄러 | 특징 |
|----------|------|
| **normal** | 표준, 범용 |
| **karras** | 후반부 노이즈 더 정교, 품질↑ (추천) |
| **exponential** | 지수적 감소 |
| **sgm_uniform** | SDXL 공식 권장 |
| **ddim_uniform** | DDIM 샘플러용 |

---

## 해상도와 비율

### 권장 해상도 (모델별)

| 모델 | 기본 | 최대 | 배수 |
|------|------|------|------|
| **FLUX** | 1024×1024 | 1536×1536 | 64 |
| **SDXL** | 1024×1024 | 2048×2048 | 64 |
| **Z-ANIME** | 896×1152 | 1152×1536 | 64 |
| **ZImage** | 1024×1024 | 1536×1536 | 64 |
| **SD 1.5** | 512×512 | 768×768 | 64 |

**중요**: 가로/세로는 **64의 배수**여야 합니다 (VAE 압축 단위).

### 프리셋 비율
```
□ 정사각 (1:1)     1024×1024  - 프로필, 썸네일, 정방형 구성
▯ 세로형 (9:16) ★  896×1152   - 모바일 배경, 세로 일러스트, 만화 컷
▭ 와이드 (16:9)    1152×896   - 모니터 배경, 풍경, 시네마틱
```

---

## 고급 설정

### Seed (시드)
- **-1**: 완전 랜덤 (매번 다른 결과)
- **고정값**: 같은 프롬프트/설정으로 **동일 결과 재현**
- **🔒 고정 토글**: 시드값 잠금 (다음 생성에도 유지)
- **활용**: 캐릭터/구도 고정하며 프롬프트만 수정할 때

### Denoise Strength (디노이즈)
img2img / 인페인팅 시 원본 이미지 유지 비율

| 값 | 효과 |
|----|------|
| **1.0** | 완전 새로 생성 (txt2img 동일) |
| 0.7~0.9 | 원본 구조 유지하며 디테일 변경 |
| 0.4~0.6 | 원본 강하게 유지, 스타일만 변경 |
| 0.1~0.3 | 미세 보정만 |

---

## 모델별 추천 설정 요약

### FLUX (GGUF 포함)
```
Steps: 20~25
CFG: 1.0~3.5 (낮게!)
Sampler: DPM++ 2M / UniPC
Scheduler: normal / sgm_uniform
Denoise: 1.0
해상도: 1024×1024 ~ 1536×1536
```
**특징**: CFG 낮게, 자연어 프롬프트, 네거티브 불필요

### Z-ANIME (웹툰/일본애니)
```
Steps: 20~25
CFG: 4.0~5.0
Sampler: DPM++ 2M Karras / Euler a
Scheduler: karras
Denoise: 1.0
해상도: 896×1152 (세로) / 1152×896 (가로)
스타일: 웹툰/일본애니/기본 필수 선택
```
**특징**: 스타일 버튼 선택 필수, CFG 중간

### ZImage (Turbo/Base)
```
Steps: 15~20 (Turbo는 더 적게)
CFG: 3.5~4.5
Sampler: DPM++ 2M / UniPC
Scheduler: normal
Denoise: 1.0
해상도: 1024×1024 ~ 1536×1536
```
**특징**: 고속 생성, FLUX 계열과 유사

### SDXL
```
Steps: 25~30
CFG: 6.0~7.5
Sampler: DPM++ 2M Karras / DPM++ 3M SDE
Scheduler: karras / sgm_uniform
Denoise: 1.0
해상도: 1024×1024 ~ 2048×2048
부정 프롬프트: 필수
```
**특징**: CFG 높게, 부정 프롬프트 필수, Karras 스케줄러 권장

### SD 1.5
```
Steps: 20~30
CFG: 7.0~8.0
Sampler: DPM++ 2M Karras / Euler a
Scheduler: karras
Denoise: 1.0
해상도: 512×512 ~ 768×768
```
**특징**: 저해상도, 하이레즈 픽스 별도 필요

---

## 성능 vs 품질 트레이드오프

### 빠르게 테스트하려면
- Steps: 15~20
- 해상도: 512×512 또는 768×768
- FaceDetailer: OFF
- Sampler: Euler a / UniPC

### 최고 품질로 뽑으려면
- Steps: 40~50
- 해상도: 모델 최대 지원 해상도
- FaceDetailer: ON (얼굴 있는 경우)
- Sampler: DPM++ 2M Karras / DPM++ 3M SDE
- Scheduler: karras

### VRAM 절약하려면
- GGUF 양자화 모델 사용 (Q4_K_S)
- 해상도 낮추기
- Steps 줄이기
- FaceDetailer 끄기
- xformers / SDP 어텐션 활성화 (ComfyUI 설정)

---

## 파라미터 조합 예시

### 일러스트/캐릭터 (Z-ANIME 웹툰)
```
모델: z_anime_base
스타일: 웹툰
Steps: 25
CFG: 4.5
Sampler: DPM++ 2M Karras
Scheduler: karras
해상도: 896×1152
FaceDetailer: ON (기본값)
```

### 실사/포토리얼 (FLUX)
```
모델: flux1-dev-Q4_K_S
Steps: 20
CFG: 2.5
Sampler: UniPC
Scheduler: normal
해상도: 1024×1024
FaceDetailer: ON (Denoise 0.3~0.4)
```

### 애니메이션/일러스트 (SDXL)
```
모델: animagineXL
Steps: 30
CFG: 7.0
Sampler: DPM++ 2M Karras
Scheduler: karras
해상도: 896×1152
부정 프롬프트: (기본 품질 저하 키워드)
FaceDetailer: ON
```

---

## 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| 이미지 깨짐/노이즈 | Steps 부족 / CFG 과도 | Steps↑, CFG↓ |
| 프롬프트 무시됨 | CFG 너무 낮음 | CFG↑ (모델 권장값으로) |
| 기괴한 얼굴/손 | 모델 한계 / Steps 부족 | FaceDetailer ON, Steps↑ |
| 너무 느림 | 해상도 높음 / Steps 과다 | 해상도↓, Steps↓, GGUF 모델 |
| VRAM OOM | 해상도/배치/모델 크기 | 해상도↓, GGUF, FaceDetailer OFF |
| 같은 시드인데 결과 다름 | 설정 변경됨 / 비결정론적 샘플러 | Euler/DDIM 사용, 설정 고정 확인 |

---

## 다음 단계

- [FaceDetailer 얼굴 보정](06_facedetailer.html) - 얼굴 디테일 전문 보정
- [모델 설정](03_model_settings.html) - 모델별 프로파일 상세
- [프롬프트 작성 가이드](04_prompt_writing.html) - 프롬프트로 품질 제어
- [기본 워크플로우](02_basic_usage.html) - 3단계 전체 플로우에서 옵션 설정 복습