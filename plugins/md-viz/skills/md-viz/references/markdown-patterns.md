# Markdown 표현 작성 예시

아래는 공연 리허설 안내서를 가정한 시연용 예시다. 작성 중인 문서에 붙일 때는 이름·좌표·상태를 원자료에서 가져오고, 이미지와 링크는 그 문서를 기준으로 실제 존재하는 경로에 맞춘다.

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

릴리스 버전은 해당 릴리스에, 라이선스는 라이선스 파일에 연결한다. 자주 바뀌는 CI 상태에는 실제 워크플로의 상태 배지를 사용한다. 공연 안내서에서는 박자를 확인할 수 있게 템포 배지를 입력 데이터에 연결한다.

문서 전체에 해당하는 버전·지원 환경은 제목 아래 배지로 모은다. 각 절에서는 새로 등장한 사실도 살핀다. 공연 안내서라면 음악 절의 120 BPM과 교통 절의 셔틀 경유지 3곳을 각각 배지로 만들 수 있다.

```markdown
[![시연곡 템포 120 BPM](assets/tempo.svg)](show.json)
```

이미지를 표시하지 않는 문서에는 `[공연 템포 120 BPM](show.json)`으로 값과 근거를 함께 남긴다.

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

문서가 가리키는 경로를 기준으로 독자에게 필요한 가지를 뽑는다. 아래에서는 실행할 파일과 교체할 이미지를 찾을 수 있다.

````markdown
```text
rehearsal/
├── README.md
├── assets/
│   ├── cue-change.gif
│   └── cue-change.png
└── player.py
```
````

고정폭 글꼴을 지원하지 않는 매체에는 `rehearsal/player.py`처럼 전체 상대 경로를 목록으로 적는다.

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
