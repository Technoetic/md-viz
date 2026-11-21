# 공연 데이터 카드 재현하기

입력 표는 [show.json](show.json)에 들어 있습니다. 모든 데이터는 가상 공연의 시연용 예시입니다. [완성된 12종 도감](../../docs/data.md)은 GitHub에서 이미지로 바로 볼 수 있습니다.

## 준비

Python 3, Node.js와 npm, R, 그리고 브라우저 캡처 도구(기본 스크립트는 Chromium 기반 **Aside** 브라우저의 `aside` CLI 사용 — Aside 환경이 없는 외부 기여자는 로컬 HTTP 미리보기 `card.html?chart=<이름>`을 일반 Chromium/Playwright/브라우저로 열어 `article` 요소를 캡처할 수 있습니다)를 사용합니다. 한글을 표시할 수 있는 시스템 글꼴이 필요합니다. 이 폴더에서 다음 명령을 실행하세요.

```sh
npm install
python -m pip install altair==5.5.0 vl-convert-python==1.9.0.post1 matplotlib==3.10.8 seaborn==0.13.2 pandas numpy
Rscript -e "install.packages(c('ggplot2', 'jsonlite', 'svglite'), repos='https://cloud.r-project.org')"
```

## 출력

Aside 브라우저를 열고 실행합니다.

```sh
python render.py
```

[Python](python_charts.py)은 Vega-Lite·Matplotlib·seaborn·Altair로, [R](ggplot.R)은 ggplot2로 원본 그림을 생성합니다. [웹 예제](charts.js)는 로컬에 설치된 일곱 JavaScript 라이브러리를 실제로 구동합니다. 실행기는 루프백 주소로만 임시 미리보기를 열고 각 엔진의 렌더링이 끝난 카드 12장을 `docs/art/data/`에 PNG로 저장합니다. 스크립트가 연 탭은 캡처 후 닫힙니다.

다른 출력 경로를 쓰려면 `--output`, 별도 패키지 설치 폴더는 `--node-modules`, R 실행 파일은 `--rscript`를 지정하세요. 이 의존성은 도감 재생성에 사용합니다. 플러그인의 스킬 설치에는 필요하지 않습니다.
