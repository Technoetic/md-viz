<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/art/cover.png">
  <img src="docs/art/cover.gif" width="1280" alt="MD-VIZ 공연 포스터. 레코드의 홈처럼 색 선이 움직인다. 도식·차트·악보 21종과 코드·수식 4종을 Antigravity, Claude Code, Codex에서 사용한다.">
</picture>

# md-viz · 마크다운 시각화 플러그인

<div align="center">
  <a href="plugins/md-viz/plugin.json"><img src="docs/art/elements/release.svg" alt="플러그인 버전 v0.2.2 · 배포 명세 열기"></a>
  <a href="#25종-시각화-도감"><img src="docs/art/elements/renderers.svg" alt="시각화 도구 25종 · 전체 도감 보기"></a>
  <a href="docs/github-elements.md"><img src="docs/art/elements/markdown.svg" alt="GitHub 마크다운 표현 6종 · 사용 예시 보기"></a>
  <a href="#설치하기"><img src="docs/art/elements/hosts.svg" alt="설치 환경 3종 · 설치 방법 보기"></a>
</div>
<div align="center">
  <a href="#antigravity-cli-agy"><img src="docs/art/elements/antigravity.svg" alt="Antigravity CLI 설치 명령"></a>
  <a href="#claude-code"><img src="docs/art/elements/claude-code.svg" alt="Claude Code 설치 명령"></a>
  <a href="#codex"><img src="docs/art/elements/codex.svg" alt="Codex 설치 명령"></a>
</div>
<div align="center">
  <a href="docs/structure.md"><img src="docs/art/elements/structure.svg" alt="구조·신호·악보 도감 9종"></a>
  <a href="docs/data.md"><img src="docs/art/elements/data.svg" alt="공연 데이터 도감 12종"></a>
  <a href="docs/notation.md"><img src="docs/art/elements/notation.svg" alt="코드·수식 도감 4종"></a>
</div>
<div align="center">
  <a href="docs/structure.md#첫-멜로디--abcjs"><img src="docs/art/elements/abcjs.svg" alt="abcjs로 그린 첫 멜로디의 악보 보기"></a>
  <a href="docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까"><img src="docs/art/elements/d3.svg" alt="D3로 그린 박자별 조명 큐 보기"></a>
  <a href="docs/github-elements.md#geojson-지도--셔틀은-어디서-갈아탈까"><img src="docs/art/elements/geojson.svg" alt="GeoJSON으로 표시한 셔틀 지도 보기"></a>
  <a href="docs/notation.md#다음-큐까지-몇-초를-셀까--katex"><img src="docs/art/elements/katex.svg" alt="KaTeX로 표시한 조명 큐 길이 계산식 보기"></a>
</div>

리허설 노트에 **“120 BPM, 4/4박자, 첫 마디는 도·레·미·솔”**이라고 적혀 있습니다. 연주자에게는 악보가, 조명 담당자에게는 어느 박에 스위치를 켤지 보여 주는 그림이 필요합니다. `md-viz`는 독자가 답을 찾을 수 있는 도구를 골라 그림을 만들고, 원문의 해당 문장 옆에 넣습니다.

README 전체를 맡기면 역할·동작을 구분하는 이모지와, 수치·상태의 출처를 열어 볼 수 있는 배지를 최대한 활용합니다. GitHub에서는 참고할 배경, 실행 요령, 필수 조건, 예상되는 오류, 손실 위험을 찾아 해당 문단에 다섯 종류의 알림을 고루 씁니다. [📖 스킬 원문](plugins/md-viz/skills/md-viz/SKILL.md)

## 여덟 음을 붙여 넣으면

> [!NOTE]
> **NEON ENCORE**는 이 도감을 위해 만든 가상 공연입니다. 악곡, 관객 수, 셔틀 경로는 모두 같은 공연을 설명하는 시연용 예시입니다.

🎵 **첫 멜로디**의 두 번째 마디에서는 첫 번째 마디의 음을 거꾸로 연주합니다.

[![공연 템포 120 BPM · 예제 데이터 열기](docs/art/elements/tempo.svg)](examples/data/show.json)

```text
X:1
T:Encore motif
M:4/4
L:1/4
Q:1/4=120
K:C
C D E G | G E D C |]
```

[![abcjs로 렌더링한 악보. 도·레·미·솔 다음에 솔·미·레·도가 이어진다.](docs/art/structure/encore.png)](docs/structure.md#첫-멜로디--abcjs)

120 BPM에서는 한 박이 0.5초이므로 이 악보는 4초입니다. 같은 템포에서 조명 여덟 마디를 프로그래밍하려면 16초가 필요합니다. 아래 두 그림을 열면 **몇 번째 박**과 **몇 초 뒤**라는 질문에 각각 답할 수 있습니다.

| 💡 조명의 스위치는 어느 박에 바뀔까? | ⏱️ 여덟 마디가 끝나는 시각은? |
|---|---|
| [![WaveDrom으로 그린 클릭·반주·조명의 여덟 박 신호](docs/art/structure/count-in.png)](docs/structure.md#박자에-맞춘-스위치--wavedrom) | [![KaTeX가 표시한 식. 8마디 × 4박 × 0.5초 = 16초](docs/art/notation/katex.png)](docs/notation.md#다음-큐까지-몇-초를-셀까--katex) |

## 설치하기

🔌 **설치할 환경**을 골라 터미널에서 해당 명령을 실행하세요. 새 대화를 열면 예시처럼 호출할 수 있습니다. 세 환경에서 같은 스킬 본문을 읽습니다.

### Antigravity CLI (agy)

```sh
agy plugin install https://github.com/Technoetic/md-viz/tree/main/plugins/md-viz
```

> `/md-viz README.md의 설치 순서를 처음 쓰는 사람이 따라갈 수 있게 그림으로 보여 줘.`

### Claude Code

```sh
claude plugin marketplace add Technoetic/md-viz
claude plugin install md-viz@technoetic-md-viz
```

> `/md-viz:md-viz 리허설 노트에서 조명팀과 음향팀이 신호를 주고받는 순서를 그려 줘.`

### Codex

```sh
codex plugin marketplace add Technoetic/md-viz
codex plugin add md-viz@technoetic-md-viz
```

> `$md-viz:md-viz README.md의 표를 그래프로 바꾸고, 원본 값과 단위가 일치하는지 확인해 줘.`

> [!IMPORTANT]
> 플러그인은 시각화 지침을 설치합니다. 새 그림을 만들 때는 선택한 렌더러도 준비하세요. 이 저장소의 완성된 그림은 GitHub와 오프라인에서 바로 볼 수 있습니다. [데이터 도감 재현에 필요한 도구](examples/data/README.md#준비)

## 저장소 구조

스킬의 도구 선택 기준은 `SKILL.md`에서, 그림을 다시 만드는 코드는 `examples/`에서 찾을 수 있습니다.

```text
md-viz/                     ← 저장소 루트
├── plugins/md-viz/         ← 설치되는 플러그인
│   ├── plugin.json         ← Antigravity 설치 정보
│   └── skills/md-viz/      ← 스킬 본문과 참고 자료
│       ├── SKILL.md        ← 시각화 도구 선택 기준
│       └── scripts/        ← 설치에 포함되는 도구
│           └── badge.py    ← 두 색의 SVG 배지 한 개 생성
├── docs/                   ← 그림과 해설
│   ├── github-elements.md  ← GitHub 문법 예제
│   └── art/                ← 도감에 실린 그림
├── examples/               ← 예제 코드와 데이터
│   ├── badges.py           ← README 상단 배지 전체 생성
│   └── data/               ← 공연 데이터와 차트 원본
└── tests/                  ← 도감과 플러그인 검사
```

상단 배지를 다시 만들려면 저장소 루트에서 `python examples/badges.py`를 실행하세요. 다른 프로젝트용 배지 한 개를 만드는 명령은 [배지 작성 예시](plugins/md-viz/skills/md-viz/references/markdown-patterns.md#배지)에 있습니다.

## 25종 시각화 도감

**25개 도구가 같은 가상 공연을 서로 다른 자리에서 봅니다.** 무대감독은 시작 신호를 따라가고, 객석 담당자는 입장 흐름을 읽고, 조명 담당자는 박자를 시간으로 바꿉니다. 각 도감에는 그림, 해설, 입력 원본이 함께 있습니다.

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/art/cue-player.png">
  <img src="docs/art/cue-player.gif" width="1080" alt="세 줄의 색 칸은 Wash, Beam, Flash 조명이 켜질 박이다. 재생 위치가 0.5초마다 한 칸씩 이동해 32박을 16초에 돈다.">
</picture>

밝은 칸이 켜질 박입니다. 세로로 읽으면 그 순간에 함께 켜질 조명이 보입니다. 같은 32박을 원형으로 펼친 D3 그림과 비교해 보세요. [원형 조명 큐 보기](docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까)

![도구 이름과 실제 렌더링을 다섯 줄에 배열한 25종 시각 색인. 아래 세 도감에서 각 그림을 크게 볼 수 있다.](docs/art/contact-sheet.png)

| 도감 | 들어 있는 도구 |
|---|---|
| [🎭 **무대 뒤의 아홉 장면** · 9종](docs/structure.md) | Mermaid · PlantUML · Graphviz · D2 · Structurizr · markmap · Excalidraw · WaveDrom · abcjs |
| [📊 **입장부터 앙코르까지, 공연 데이터** · 12종](docs/data.md) | Vega-Lite · Matplotlib · seaborn · Altair · ggplot2 · Chart.js · Observable Plot · Plotly · Apache ECharts · D3 · Cytoscape.js · Leaflet |
| [🧮 **공연 기술 노트의 코드와 수식** · 4종](docs/notation.md) | Shiki · highlight.js · MathJax · KaTeX |

> [!CAUTION]
> 데이터 도감을 다시 그리면 기본 경로 `docs/art/data/`의 기존 PNG가 덮어써집니다. 원본과 비교하려면 `examples/data/`에서 `python render.py --output preview`로 새 그림을 별도 폴더에 저장하세요. [도감 재현 방법](examples/data/README.md#출력)

## GitHub 문서 표현 6가지

📍 **셔틀은 어디에서 갈아탈까?** 예제 지도에서 집결지 A, 환승지 B, 무대 C의 위치를 볼 수 있습니다. 🎵 **조명 큐는 얼마나 빠를까?** 템포 배지를 누르면 원본 값이, GIF를 열면 그 박자에 맞춰 켜지는 조명이 보입니다.

> [!WARNING]
> 셔틀 지도를 내 좌표로 바꿀 때는 경도, 위도 순서로 입력하세요. 서울 예제의 첫 경도 `126.9754`를 위도 자리에 넣으면 유효 범위를 벗어납니다. [예제 좌표 확인](docs/art/elements/shuttle.geojson)

[![GitHub 알림 5종 · 공연 안내서의 알림 예시 보기](docs/art/elements/alerts.svg)](docs/github-elements.md#알림-블록--공연-노트에서-무엇을-강조할까)

예제에는 지도·배지·이모지·GIF를 넣는 구문과 실제 파일을 찾을 수 있는 디렉터리 트리가 있습니다. 알림 다섯 종류도 완성된 모습과 복사할 문법을 함께 실었습니다. [공연 안내서로 여섯 기법 보기](docs/github-elements.md)

> [!TIP]
> 한 기법만 요청해도 됩니다. 예를 들어 “처음 온 기여자가 예제를 찾을 수 있게 실제 파일로 디렉터리 트리를 만들고, 실행할 파일에 설명을 붙여 줘”라고 해 보세요.

### 내 문서에 적용하기

- 🖼️ **그림 한 장이 필요할 때** — “이 장애 대응 절차의 분기만 Mermaid 한 장으로 그려 줘.”
- 📖 **기존 README 전체를 바꿀 때** — “25종을 검토해서 이 원고에 맞는 도구를 최대한 활용해 줘. 코드는 복사할 수 있게 두고, 그림에는 대체 텍스트를 붙여 줘.”
- ✍️ **블로그에 옮길 때** — “네이버 블로그에 붙여 넣을 글이야. 그림은 PNG로 내보내고 식은 글로도 읽을 수 있게 해 줘.”

도구 선택 기준과 게시 환경별 출력 방식은 [스킬 원문](plugins/md-viz/skills/md-viz/SKILL.md)에, 이 README의 그림에 사용한 코드는 [예제 폴더](examples)에 있습니다.
