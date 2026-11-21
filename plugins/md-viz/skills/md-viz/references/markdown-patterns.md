# Markdown 표현 작성 예시

공연 리허설은 시연용 예시다. README 배지와 디렉터리 트리는 md-viz 저장소의 실제 파일을 사용한다. 다른 문서에 옮길 때는 대상 자료에서 이름·값·경로를 확인한다.

## 지리 지도

GitHub에서 다음 블록은 한 지점을 표시한다. GeoJSON의 점 좌표는 경도, 위도 순서다. 본문에도 지명과 좌표를 적으면 인쇄물이나 지도 뷰어가 없는 환경에서 위치를 읽을 수 있다.

````markdown
리허설 집결 지점 A는 동경 127.0°, 북위 37.5°에 있다(시연용 좌표).

```geojson
{
  "type": "Feature",
  "properties": { "name": "집결 지점 A" },
  "geometry": { "type": "Point", "coordinates": [127.0, 37.5] }
}
```
````

원자료가 TopoJSON이면 `topojson` 블록에 `type`이 `Topology`인 유효한 객체를 넣는다. 두 형식은 데이터 구조가 다르다. 장소만 알고 좌표를 확인할 수 없으면 원문에 있는 지명 목록을 사용한다. [GitHub 지도 구문](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-geojson-and-topojson-maps)

## 배지

아래 블록을 md-viz 저장소 루트 README의 제목 아래에 붙이면 첫 줄에서는 설치 환경과 지원 범위를, 둘째 줄에서는 각 도감에 담긴 도구 수를 읽을 수 있다. 배지 하나를 누르면 해당 근거가 열린다. 링크 사이의 줄바꿈은 HTML에서 공백이 되어 좁은 화면에서 배지 단위로 줄이 바뀐다.

```html
<div align="center">
  <a href="#설치하기"><img src="docs/art/elements/hosts.svg" alt="설치 환경 3종"></a>
  <a href="#25종-시각화-도감"><img src="docs/art/elements/renderers.svg" alt="시각화 도구 25종"></a>
  <a href="docs/github-elements.md"><img src="docs/art/elements/markdown.svg" alt="GitHub 문서 표현 6종"></a>
</div>
<div align="center">
  <a href="docs/structure.md"><img src="docs/art/elements/structure.svg" alt="무대 구조와 신호 도구 9종"></a>
  <a href="docs/data.md"><img src="docs/art/elements/data.svg" alt="공연 데이터 도구 12종"></a>
  <a href="docs/notation.md"><img src="docs/art/elements/notation.svg" alt="코드와 수식 도구 4종"></a>
</div>
```

새 배지도 예제 SVG처럼 같은 높이의 직사각형 두 칸으로 만든다. 왼쪽에는 짙은 회색 바탕에 짧은 이름(예: `DATA`, `설치 환경`), 오른쪽에는 항목별 강조색에 값(예: `12 TOOLS`, `3종`)을 적는다. 릴리스·라이선스·CI를 표시할 때는 각각 해당 릴리스, 라이선스 파일, 실제 워크플로에 연결한다.

스킬 폴더에서 다음 명령을 실행하면 현재 폴더에 높이 28px인 `data-tools.svg`가 생긴다. README에 쓸 때는 `data-tools.svg` 자리에 대상 저장소의 SVG 출력 경로를 넣는다. 생성기는 값 칸의 색에 맞춰 읽기 쉬운 글자색을 고른다. [배지 생성기](../scripts/badge.py)

```sh
python scripts/badge.py DATA "12 TOOLS" data-tools.svg --color "#19C6A3"
```

해당 절에서 처음 쓰는 배지는 근거 옆에 둔다. 아래 Markdown을 같은 README의 공연 예제 절에 붙이면 시연곡의 템포에서 원본 데이터로 이동한다. 이미지를 표시할 수 없는 매체에는 `[공연 템포 120 BPM](examples/data/show.json)`으로 옮긴다.

```markdown
[![공연 템포 120 BPM](docs/art/elements/tempo.svg)](examples/data/show.json)
```

## 이모지

목차, 절 제목, 작업 순서와 상태 표에도 의미가 통하는 이모지를 최대한 배치한다. 같은 동작의 레이블은 짧게 통일한다. 아래 문장은 기호를 보지 못해도 리허설 결과를 읽을 수 있다.

```markdown
- ✅ 완료 — 마이크 점검
- ⏳ 대기 — 무대 조명 점검
```

GitHub에서는 `:white_check_mark:` 같은 단축 코드도 쓸 수 있다. 다른 뷰어에 옮길 때는 `✅ 완료` 또는 `완료`로 적는다.

## 애니메이션 GIF

변화를 확인하려는 독자가 재생을 선택하게 하려면 정지 이미지에서 GIF로 연결한다. 아래는 HTML 없이 동작하며, 인쇄 시에도 두 큐의 순서가 문장으로 남는다.

```markdown
[![두 번째 조명 큐가 선택된 화면. 누르면 전환 과정이 재생된다.](assets/cue-change.png)](assets/cue-change.gif)

재생을 누르면 첫 번째 큐가 끝나고 두 번째 큐에 불이 들어온다.
```

문서 안에서 바로 움직여야 하면 `![첫 번째 큐에서 두 번째 큐로 넘어가는 모습](assets/cue-change.gif)`로 삽입한다. 바로 아래에 같은 과정의 정지 화면이나 단계 설명을 두고, 완성된 문서에서 GIF의 프레임 전환을 확인한다.

## 디렉터리 트리

저장소 루트에서 `git ls-files -- examples/data/show.json examples/cue_player.py docs/art/cue-player.gif docs/art/cue-player.png`을 실행하면 아래 예제의 네 파일을 확인할 수 있다. 트리는 같은 루트를 `.`으로 표시한다. 코드 블록 전체를 복사하면 입력, 생성 코드, 결과 파일의 역할이 경로 옆에 남는다.

````markdown
```text
.                           ← 저장소 루트
├── examples/               ← 공연 예제의 입력과 코드
│   ├── data/               ← 공연 데이터
│   │   └── show.json       ← 조명 큐와 템포의 원본
│   └── cue_player.py       ← 조명 큐 애니메이션 생성
└── docs/                   ← 시각화 도감
    └── art/                ← 도감에 쓰는 그림
        ├── cue-player.gif  ← 재생 중인 조명 큐
        └── cue-player.png  ← 첫 박의 정지 화면
```
````

폴더 이름에는 `/`를 붙이고, 공백은 트리 기호와 가장 긴 파일 이름을 포함한 표시 폭을 기준으로 채운다. 한글 경로가 있으면 완성된 고정폭 블록에서 화살표 열을 확인한다. 고정폭 글꼴을 지원하지 않는 매체에는 `examples/data/show.json — 조명 큐와 템포의 원본`처럼 전체 상대 경로와 역할을 한 줄에 쓴다.

## GitHub 알림 5종

다섯 유형 모두 들어갈 자리를 찾는다. 예를 들어 배경은 리허설 소개에, 요령은 재생 방법에, 필수 설정은 자동 전환 설명에 둔다. 장비 연결과 초기화에는 각각 해당 동작의 결과를 적는다. 각 알림은 독립된 인용 블록에서 표식으로 시작하고, 다음 인용 줄에 메시지를 쓴다. 실제 원고에 적용할 때는 근거가 있는 블록을 해당 절로 옮긴다.

```markdown
> [!NOTE]
> 리허설 녹음은 첫 번째 큐부터 시작한다.

> [!TIP]
> 스페이스 키로 선택한 큐를 다시 재생할 수 있다.

> [!IMPORTANT]
> 자동 전환을 쓰려면 각 큐에 재생 시간을 입력해야 한다.

> [!WARNING]
> 장비 연결을 바꾸기 전에 재생을 멈춰 다음 큐의 오작동을 피한다.

> [!CAUTION]
> 초기화하면 저장하지 않은 큐 편집 내용이 사라진다.
```

알림을 지원하지 않는 Markdown에는 `> **주의** — 초기화하면 저장하지 않은 큐 편집 내용이 사라진다.`처럼 쓴다. [GitHub 알림 구문](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts)
