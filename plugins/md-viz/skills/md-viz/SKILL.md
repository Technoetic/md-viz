---
name: md-viz
description: 외부 패키지 설치 없이 GitHub README.md를 극단적으로 선명하고 강렬하게 시각화하는 전용 스킬. GitHub 네이티브 라이브 문법(Mermaid·MathJax·GeoJSON·알림 5종·<details>·<kbd>)과 번들 Python 3 표준 라이브러리 생성기 4종(네온 SVG 배지·GitHub <img> 안전 순수 SVG 차트 10종·순수 stdlib 루프 GIF89a+PNG·실제 저장소 정렬 트리)만으로 모든 PC에서 즉시 100% 동작한다.
---

# ⚡ 무설치 GitHub README.md 전용 시각화 (`md-viz` Zero-Install)

호출 뒤에 적힌 파일 경로(기본 대상: 저장소의 `README.md`) 또는 제공된 본문을 대상으로 한다. 대상이 생략됐으면 현재 저장소의 `README.md` 또는 대화에서 명확히 가리키는 문서를 사용하고, 후보가 여럿이면 한 번만 묻는다.

> **핵심 설계 원칙 (Zero-Install GitHub `README.md` First):**
> GitHub `README.md`는 `<script>`와 외부 JS/CSS를 차단하므로, **네이티브 라이브 문법(`Mermaid`·`MathJax`·`GeoJSON`·알림 5종·구문 강조)** 과 **외부 설치 0개로 즉시 돌아가는 번들 Python 3 표준 라이브러리 생성기 4종(`badge.py` · `svg_chart.py` · `gif_anim.py` · `tree_gen.py`)** 만으로 모든 시각화를 완결한다. `npm install`·`pip install`·브라우저 캡처 없이 어떤 환경에서도 100% 재현된다.
> *(단, 사용자가 `"Mermaid만"`, `"배지만"`, `"차분하게"`처럼 범위를 좁히면 그 지시를 최우선한다.)*

## 0단계 · 무설치 스택 점검 (`check_env.py`)

작업 시작 시 번들 [환경 점검 스크립트](scripts/check_env.py)를 실행해 4개 stdlib 생성기와 GitHub 네이티브 레이어 준비 상태를 확인한다.

```sh
python scripts/check_env.py --json
```

- `zero_install_ready: true`이면 외부 설치 없이 곧바로 1·2단계를 전량 실행한다.
- 외부 패키지(`npm`, `pip`, `Rscript`, `d2`, `dot` 등)는 **설치하지 않고도** 모든 핵심 차트·배지·애니메이션·트리를 생성할 수 있다.

## 1단계 · GitHub `README.md` 네이티브 라이브 레이어 (이미지 불필요, GitHub 직접 렌더링)

복사 가능한 완성 문법은 [GitHub 표현 패턴집](references/markdown-patterns.md)을 따른다.

| # | GitHub 네이티브 기법 | 배치 원칙 |
|---|---|---|
| 1 | 🌊 **라이브 네온 `mermaid` 블록** | 아키텍처·파이프라인·시퀀스·상태·간트·마인드맵을 ` ```mermaid ` + 고대비 다크-네온 `classDef`(시안 `#00F5D4` · 마젠타 `#FF2E93` · 라임 `#C8FF00` · 앰버 `#FFBB54` · 바이올렛 `#C084FC`)로 작성한다. |
| 2 | 🧮 **라이브 `MathJax` 수식** | 핵심 공식·복잡도·성능 계산은 GitHub 공식 내장 수식 렌더러인 `$...$`, `$$...$$`, ` ```math ` 블록으로 직접 표기한다. |
| 3 | 🗺️ **라이브 `geojson`/`topojson` 지도** | 실제 위경도·경로·거점이 있으면 `[경도, 위도]` 순서의 ` ```geojson ` 블록(`marker-color`, `stroke` 포함)을 삽입한다. |
| 4 | 📣 **GitHub 알림 5종 전량 (`5/5`)** | 문서 전체에서 `[!NOTE]`(맥락), `[!TIP]`(요령), `[!IMPORTANT]`(전제), `[!WARNING]`(함정), `[!CAUTION]`(파괴적 위험)을 근거 있는 위치에 고루 배치한다(근거가 없으면 날조하지 않고 생략 사유를 적는다). |
| 5 | 💻 **네이티브 구문 강조 & `<kbd>` 키캡** | 언어 식별자를 명시한 ` ```sh `, ` ```python `, ` ```json ` 코드 블록과 `<kbd>/md-viz</kbd>` 명령·단축키 필로 스캔 속도를 높인다. |
| 6 | 🖼️ **멀티컬럼 갤러리 월 & 이모지 리듬** | 생성한 SVG/GIF 자산을 2~3열 Markdown 표 + `<details open>`으로 묶어 한 화면에서 조망하게 하고, 모든 `H2`/`H3` 제목과 상태 항목에 의미가 통일된 이모지 + 텍스트 레이블을 짝짓는다. |

## 2단계 · 무설치 Python 표준 라이브러리 생성기 4종 (0 외부 패키지)

GitHub `README.md`에서 직접 실행할 수 없는 차트·히어로 배너·배지·애니메이션·트리는 **모두 번들 Python 3 stdlib 스크립트**로 로컬 파일(`docs/art/` 등)을 생성해 상대 경로로 삽입한다.

### 1) 🏷️ 2톤 네온 SVG 배지 월 — [`scripts/badge.py`](scripts/badge.py)

`H1` 제목 바로 아래 `<div align="center">` 2~3행으로 버전·라이선스·CI·핵심 지표·바로가기 배지를 배치한다(WCAG 자동 대비, 6자리 hex 검증, XML 이스케이프).

```sh
python scripts/badge.py ZERO-DEPS "PYTHON STDLIB" docs/art/zero-deps.svg --color "#00F5D4"
```

### 2) 📊 GitHub `<img>`-안전 순수 SVG 시각화 10종 — [`scripts/svg_chart.py`](scripts/svg_chart.py)

`<script>`·`<foreignObject>`·외부 URL을 원천 차단하고 내장 XML 보안 검증을 통과한 순수 `<svg>`만 출력한다. `--readme README.md --slot <id>`를 주면 `<!-- md-viz:start:<id> -->` 블록으로 상대 경로를 멱등 삽입·갱신한다.

| `--type` | 최적 용도 |
|---|---|
| `hero` | 저장소 최상단 다크-네온 히어로 배너(제목·태그라인·메타 필·기하학 링) |
| `kpi` | 핵심 지표 2~6종 카드 스트립(수치·증감 델타 배지·보조 설명) |
| `bar` | 수평(`horizontal`) 또는 수직(`vertical`) 항목 비교 막대 + 끝점 수치 라벨 |
| `line` | 다중 시계열 추세선 + 반투명 네온 영역 채움 + 범례 |
| `donut` | 구성비 도넛 링 + 중앙 합계 KPI + 우측 백분율 범례 |
| `heatmap` | 행×열 강도 매트릭스 + 자동 대비 수치 라벨 |
| `waterfall` | 시작→증감(+라임/-마젠타)→최종 합계 폭포 분해 차트 |
| `radar` | 다축 역량·벤치마크 거미줄 비교 |
| `sankey` | 2열 유입→분배 비례 리본 흐름도 |
| `timeline` | 다중 트랙 단계·마일스톤·박자 매트릭스 |

```sh
python scripts/svg_chart.py --type kpi --spec kpi.json --out docs/art/kpi.svg --readme README.md --slot kpi --alt "핵심 지표 요약"
```

### 3) 🎬 순수 stdlib 루프 GIF89a + 정지 PNG (`<picture>`) — [`scripts/gif_anim.py`](scripts/gif_anim.py)

Pillow 없이 Python 표준 라이브러리(`struct`·`zlib`·LZW)만으로 루프 애니메이션 `.gif`와 동일 해상도 정지 `.png`를 함께 생성하고, `prefers-reduced-motion: reduce` 대응 `<picture>` 태그를 바로 출력·삽입한다.

```sh
python scripts/gif_anim.py --spec loop.json --out docs/art/pipeline-loop.gif --readme README.md --slot loop --alt "파이프라인 단계 루프"
```

### 4) 🗂️ 실제 저장소 열 정렬 디렉터리 트리 — [`scripts/tree_gen.py`](scripts/tree_gen.py)

실제 디스크의 파일·폴더만 읽어 `.git`/`node_modules`/`__pycache__`를 제외하고, 동아시아 전각 폭 기준으로 `← 역할 설명` 화살표 열을 1칸 오차 없이 정렬한다.

```sh
python scripts/tree_gen.py --root . --max-depth 3 --roles roles.json --readme README.md --slot repo-tree
```

## 3단계 · 고대비 비주얼 규격 & 사실 정직성 철칙

1. **다크-네온 팔레트:** 옵시디언 캔버스(`#0B0F1A` / `#131621`) + 고채도 네온 시그널(`#00F5D4` 시안 · `#FF2E93` 마젠타 · `#C8FF00` 라임 · `#FFBB54` 앰버 · `#C084FC` 바이올렛 · `#38BDF8` 스카이)로 GitHub 라이트/다크 모드 양쪽에서 또렷한 대비를 확보한다.
2. **사실 날조 0%:** 원문이나 실제 코드베이스에 없는 수치·성능·경로·버전을 절대 지어내지 않는다. 시연용 예시가 꼭 필요하면 캡션과 본문에 **`시연용 예시` / `Illustrative Example`** 표식을 명시한다.
3. **기존 내용 보존:** 원고의 핵심 설명, 복사 가능한 코드, 기존 링크와 작성자 이미지를 지우지 않고 시각 자산을 덧붙인다.
4. **신뢰 경계:** 모든 자산 생성은 로컬에서 완결하며, 외부 이미지 호스팅·원격 API 전송·무단 원격 push를 수행하지 않는다.

## 4단계 · 선택적 외부 렌더러 (명시 요청 시에만)

사용자가 `PlantUML`, `D2`, `Graphviz`, `Matplotlib`, `ECharts`, `abcjs` 등 특정 외부 라이브러리를 **명시적으로 지정**하고 `check_env.py`에서 해당 로컬 엔진이 `ready`로 확인된 경우에만 보조 사전 렌더링(PNG/SVG 상대 경로 삽입)으로 확장한다. 기본 호출에서는 외부 엔진 설치를 요구하거나 기다리지 않는다.

## 5단계 · 최종 검수 및 의무 4줄 스코어보드

생성된 `README.md`와 모든 `docs/art/` 자산을 직접 검증(상대 경로 실재, SVG XML 파싱 및 `<script>`/`<foreignObject>` 0건, GIF/PNG 헤더 및 동일 해상도, 내부 제목 앵커 실재, 알림 5종, 디렉터리 트리 열 정렬)한 뒤 결과 끝에 아래 4줄을 보고한다:

1. **GitHub 네이티브 레이어:** `N / 6` (적용 항목 목록)
2. **무설치 stdlib 생성기:** `M / 4` (`badge.py` · `svg_chart.py`[유형 목록] · `gif_anim.py` · `tree_gen.py`)
3. **적용한 GitHub 알림 유형:** `A / 5` (코드 블록 안 예시 제외)
4. **생성 자산 & 검증 요약:** 저장 경로 목록, SVG/GIF/PNG 헤더 검증 결과, 생략 항목 사유
