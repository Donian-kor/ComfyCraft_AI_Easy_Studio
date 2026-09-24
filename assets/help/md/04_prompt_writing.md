# 프롬프트 작성 가이드

좋은 이미지의 핵심은 **좋은 프롬프트**입니다. 이 프로그램은 한국어 아이디어를 AI가 영문 최적 프롬프트로 변환해 주지만, 원리를 알면 더 좋은 결과를 얻을 수 있습니다.

---

## 프롬프트 구조

### 기본 공식
```
[무엇을 그릴지] + [어떤 스타일로] + [분위기/조명/구도/품질 키워드]
```

### 구성 요소별 예시

| 요소 | 키워드 예시 | 설명 |
|------|-------------|------|
| **주제** | `beautiful woman`, `cyberpunk city`, `cute cat` | 핵심 피사체 |
| **스타일** | `anime style`, `oil painting`, `photorealistic`, `webtoon` | 화풍 |
| **분위기** | `cinematic lighting`, `dark atmosphere`, `golden hour` | 무드/조명 |
| **구도** | `close up`, `wide angle`, `depth of field`, `rule of thirds` | 카메라 앵글 |
| **품질** | `8k`, `masterpiece`, `highly detailed`, `sharp focus` | 해상도/디테일 |
| **기술적** | `ray tracing`, `octane render`, `unreal engine 5` | 렌더링 힌트 |

---

## 한국어 입력 팁

### 잘 되는 입력 패턴
```
✅ "비 오는 날 네온사인 빛나는 사이버펑크 도시, 창가에 앉은 은발 소녀, 영화 같은 조명, 8k"
✅ "따뜻한 오후 햇살 받는 나무 아래 낮잠 자는 고양이, 부드러운 보카시, 지브리 스타일"
✅ "전투 중인 판타지 기사, 반짝이는 갑옷, 역동적인 포즈, 에픽한 분위기, 마스터피스"
```

### 피해야 할 패턴
```
❌ "예쁜 그림 그려줘" (너무 모호)
❌ "고양이" (스타일/분위기/구도 정보 없음)
❌ "이쁘게 해줘" (구체적 키워드 없음)
```

**핵심**: **구체적 명사 + 형용사 + 스타일/분위기 키워드** 조합

---

## AI 프롬프트 마법사 활용

### 기본 동작
1. 한국어 입력 → `✨ AI 프롬프트 마법사` 클릭
2. LM Studio 언어 모델이 분석 → 영문 프롬프트 생성
3. 하단 `생성된 영문 프롬프트` 에디터에 결과 표시

### 생성된 프롬프트 수정
- 에디터에서 **직접 수정 가능** (추가/삭제/순서 변경)
- 수정한 내용으로 생성 진행
- `📋 복사` 버튼으로 다른 곳에 재사용 가능

### 모델별 프롬프트 특성

| 모델 | 프롬프트 스타일 | 팁 |
|------|----------------|-----|
| **FLUX** | 자연어 문장형 | "A beautiful woman standing in..." 처럼 문장으로 |
| **SDXL** | 태그형/키워드형 | "beautiful woman, cyberpunk, neon lights, 8k..." 콤마 구분 |
| **Z-ANIME** | 태그형 + 스타일 태그 | "webtoon style", "japanime style" 등 스타일 태그 필수 |
| **ZImage** | 혼합형 | 자연어 + 중요 키워드 콤마 구분 |

> **자세한 모델별 특성**: [모델 설정](03_model_settings.html) 참조

---

## 고급 프롬프트 기법

### 가중치 조절 (SDXL 계열)
```
(주제:1.3), (스타일:1.2), 품질태그, 조명태그
```
- `(keyword:weight)` 형식으로 강조/억제
- 1.0 = 기본, >1.0 = 강조, <1.0 = 억제

### 부정 프롬프트 (SDXL 필수)
```
저품질 키워드:
ugly, deformed, blurry, low quality, bad anatomy, 
extra limbs, missing fingers, watermark, text, signature,
cropped, jpeg artifacts, noise, grain
```

> **참고**: FLUX, ZImage 계열은 부정 프롬프트 입력란이 자동 숨김 처리됩니다. ([모델 설정](03_model_settings.html)의 "네거티브 프롬프트 자동 제어" 참조)

### 프롬프트 템플릿 저장
자주 쓰는 조합은 외부 프롬프트 파일(`prompts.json`)에 저장해 두고 불러오기 가능

---

## 모델별 추천 프롬프트 패턴

### FLUX / ZImage (자연어 친화적)
```
"A stunning cyberpunk cityscape at night, neon signs reflecting on wet streets, 
a silver-haired android girl sitting by the window, cinematic volumetric lighting, 
hyperrealistic, 8k resolution, masterpiece, sharp focus, ray tracing"
```

### Z-ANIME 웹툰 스타일
```
webtoon style, beautiful korean webtoon character, silver hair, 
cyberpunk city background, neon lights, rain, cinematic lighting, 
clean lineart, flat shading, vibrant colors, masterpiece, 8k
```

### Z-ANIME 일본애니 스타일
```
japanime style, anime key visual, beautiful anime girl, silver hair, 
cyberpunk cityscape, neon signs, rain, dramatic lighting, 
cel shading, detailed background, 8k, masterpiece, high quality
```

### SDXL (태그형)
```
masterpiece, best quality, ultra high res, 8k, photorealistic,
beautiful woman, silver hair, cyberpunk city, neon lights, rain,
cinematic lighting, volumetric fog, ray tracing, sharp focus,
detailed skin texture, depth of field
```

---

## 프롬프트 엔지니어링 체크리스트

생성 전 확인사항:
- [ ] 주제가 명확한가? (무엇을 그릴지)
- [ ] 스타일이 지정되었나? (웹툰/애니/실사/유화 등)
- [ ] 분위기/조명 키워드가 있는가? (시네마틱/따뜻한/어두운/밝은)
- [ ] 구도 키워드가 있는가? (클로즈업/전신/풍경/앵글)
- [ ] 품질 태그가 있는가? (8k, 마스터피스, 샤프포커스 등)
- [ ] 부정 프롬프트가 필요한 모델인가? (SDXL 계열)

---

## 자주 하는 실수

| 실수 | 해결 |
|------|------|
| 한국어를 영문으로 직역 | AI 마법사 믿고 맡기기, 필요시만 수정 |
| 품질 태그 생략 | `masterpiece, best quality, 8k` 필수 추가 |
| 부정 프롬프트 안 씀 (SDXL) | 기본 부정 프롬프트라도 꼭 넣기 |
| 너무 많은 키워드 나열 | 핵심 10~15개 내외로 정리 |
| 모델 특성 무시 | 모델별 권장 프롬프트 형식 따르기 |

---

## 다음 단계

- [기본 워크플로우](02_basic_usage.html) - 3단계 전체 플로우에서 프롬프트 단계 복습
- [생성 옵션 상세](05_generation_options.html) - 파라미터로 품질 제어
- [FaceDetailer 얼굴 보정](06_facedetailer.html) - 얼굴 디테일 살리기
- [모델 설정](03_model_settings.html) - 모델별 특성 이해