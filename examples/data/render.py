"""Render the twelve sample cards using local engines and an Aside browser."""
import argparse
import base64
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from threading import Thread

HERE = Path(__file__).resolve().parent
CARDS = ["vega-lite","matplotlib","seaborn","altair","ggplot2","chartjs","observable","plotly",
         "echarts","d3","cytoscape","leaflet"]
BUNDLES = [
    "chart.js/dist/chart.umd.min.js", "@observablehq/plot/dist/plot.umd.min.js",
    "d3/dist/d3.min.js", "echarts/dist/echarts.min.js", "cytoscape/dist/cytoscape.min.js",
    "leaflet/dist/leaflet.js", "leaflet/dist/leaflet.css",
]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def capture(port, names, output):
    code = r"""
const cardNames=__NAMES__, result={};
const tab=await openTab('about:blank');
try {
 for(const key of cardNames){
   await tab.goto('http://127.0.0.1:__PORT__/card.html?chart='+key);
   for(let i=0;i<100;i++){if(await tab.evaluate(()=>document.body.dataset.state)) break;
       await new Promise(r=>setTimeout(r,100));}
   const status=await tab.evaluate(()=>({state:document.body.dataset.state,error:document.body.dataset.error,
      width:document.querySelector('article').offsetWidth,height:document.querySelector('article').offsetHeight}));
   if(status.state!=='ready')throw Error(key+' '+JSON.stringify(status));
   // Warm up the webview compositor before asking it to crop the capture.
   await tab.screenshot({timeout:100}).catch(()=>{});
   let shot;
   for(let attempt=0;attempt<3;attempt++){
     try{shot=await tab.screenshot({clip:{x:0,y:0,width:status.width,height:status.height},type:'png',timeout:8000});break;}
     catch(error){if(attempt===2)throw error;}
   }
   result[key]=Buffer.from(shot).toString('base64');
 }
} finally {await closeTab(tab);}
console.log(JSON.stringify(result));
""".replace("__PORT__", str(port)).replace("__NAMES__", json.dumps(names))
    # Aside accepts a multiline script as one argument. Keep the output local.
    with tempfile.TemporaryDirectory() as td:
        script = Path(td, "capture.js")
        script.write_text(code, encoding="utf-8")
        result = subprocess.run(["aside","repl",script.read_text(encoding="utf-8")], capture_output=True,
                                timeout=120)
    if result.returncode:
        raise RuntimeError((result.stderr + result.stdout[:1000]).decode("utf-8", errors="replace"))
    lines = result.stdout.decode("utf-8").splitlines()
    images = next((json.loads(line) for line in lines if line.startswith('{"'+names[0]+'"')),None)
    if not images or set(images) != set(names):
        raise RuntimeError("Missing capture. Aside output: " + str(lines)[:500])
    for key, encoded in images.items():
        contents = base64.b64decode(encoded, validate=True)
        if not contents.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Invalid screenshot for " + key)
        (output / (key + ".png")).write_bytes(contents)
        print(key, len(contents), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-modules",type=Path,default=HERE / "node_modules")
    parser.add_argument("--plotly-bundle",type=Path,help="Optional path to plotly.min.js")
    parser.add_argument("--rscript",default="Rscript")
    parser.add_argument("--output",type=Path,default=HERE.parents[1] / "docs/art/data")
    parser.add_argument("--cards",nargs="+",choices=CARDS,default=CARDS)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="md-viz-preview-") as td:
        page = Path(td)
        vendor = page / "vendor"
        vendor.mkdir()
        for relative in BUNDLES:
            shutil.copyfile(args.node_modules / relative, vendor / Path(relative).name)
        plotly = args.plotly_bundle or args.node_modules / "plotly.js-dist-min/plotly.min.js"
        shutil.copyfile(plotly, vendor / "plotly.min.js")
        for file in ["card.html","charts.js","show.json"]:
            shutil.copyfile(HERE / file,page / file)
        subprocess.run([sys.executable,HERE / "python_charts.py",page],check=True)
        subprocess.run([args.rscript,"--vanilla",HERE / "ggplot.R",page / "show.json",page / "ggplot2.svg"],check=True)
        with ThreadingHTTPServer(("127.0.0.1",0), partial(QuietHandler,directory=page)) as server:
            Thread(target=server.serve_forever,daemon=True).start()
            try:
                for start in range(0,len(args.cards),3):
                    capture(server.server_port, args.cards[start:start+3], args.output)
            finally:
                server.shutdown()


if __name__ == "__main__":
    main()
