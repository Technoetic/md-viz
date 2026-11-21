# NEON ENCORE 입력으로 다시 그리기

이 폴더를 **별도 작업 폴더에 복사**하고 그 안에서 아래 명령을 실행하세요. 예제에는 가상의 공연 데이터만 들어 있습니다. 웹 라이브러리는 처음 설치할 때 다운로드하며, 예제 화면은 로컬에서 엽니다.

## 브라우저에서 세 그림 보기

Node.js와 Python 3가 필요합니다. 세 라이브러리와 이 예제에 사용한 브라우저 의존성을 설치하세요.

```sh
npm install --no-save --package-lock=false abcjs@6.7.2 @excalidraw/excalidraw@0.17.6 react@18.3.1 react-dom@18.3.1 markmap-lib@0.18.13 markmap-view@0.18.13 d3@7.9.2
```

markmap이 읽을 트리를 생성하고 로컬 서버를 시작하세요. Windows에서 Python 명령이 `py`라면 마지막 줄의 `python`을 `py`로 바꿉니다.

```sh
node -e "const fs=require('node:fs'),{Transformer}=require('markmap-lib'); const {root}=new Transformer().transform(fs.readFileSync('set-notes.md','utf8')); fs.writeFileSync('set-notes.json',JSON.stringify(root));"
python -m http.server 8000 --bind 127.0.0.1
```

브라우저 주소창에 `http://127.0.0.1:8000/browser-demo.html`을 입력합니다. [브라우저 예제](browser-demo.html)에서 아래 세 변환을 실행합니다.

| 그림 | 원본 → 중간 결과 → 화면 |
|---|---|
| 무대 배치 | `stage-plot.js`의 `encoreStage()`가 좌표와 도형 배열을 반환합니다. `convertToExcalidrawElements()`로 장면 요소를 만들고 `exportToSvg()`로 그립니다. |
| 리허설 노트 | 위 Node 명령이 `set-notes.md`의 제목과 목록을 `set-notes.json` 트리로 변환합니다. 화면에서 `Markmap.create()`가 가지를 펼칩니다. |
| 첫 멜로디 | `encore.abc`를 문자열로 읽어 `ABCJS.renderAbc()`에 넘기면 두 마디의 오선보가 그려집니다. |

좌표나 악보를 바꾸면 화면을 새로 고치세요. 리허설 노트를 바꿨다면 위 Node 명령으로 JSON을 갱신합니다. 작업을 마쳤으면 터미널에서 `Ctrl+C`로 서버를 종료하세요.

## 나머지 입력

| 입력 | 렌더링 방법 |
|---|---|
| `cue-gate.mmd` | Mermaid CLI에서 `mmdc -i cue-gate.mmd -o cue-gate.svg` |
| `standby.puml` | PlantUML JAR가 있는 환경에서 `java -jar plantuml.jar -charset UTF-8 -tsvg standby.puml` |
| `signal-path.dot` | Graphviz에서 `dot -Tsvg signal-path.dot -o signal-path.svg` |
| `patch-bays.d2` | D2에서 `d2 patch-bays.d2 patch-bays.svg` |
| `cue-desk.dsl` | Structurizr CLI의 `export -workspace cue-desk.dsl -format dot -output out`을 실행하고, `dot -Tsvg out/structurizr-EncoreContext.dot -o cue-desk.svg`로 렌더링합니다. |
| `count-in.json` | Node용 WaveDrom 3.5.0에서 아래 명령으로 SVG를 씁니다. |

```sh
npm install --no-save --package-lock=false wavedrom@3.5.0
node -e "const fs=require('node:fs'),w=require('wavedrom'); const input=JSON.parse(fs.readFileSync('count-in.json','utf8')); fs.writeFileSync('count-in.svg',w.onml.stringify(w.renderAny(0,input,w.waveSkin)));"
```

WaveDrom 실습은 별도 복사본에서 실행하면 앞서 설치한 브라우저 예제 라이브러리도 계속 사용할 수 있습니다. [완성된 PNG 도감](../../docs/structure.md)
