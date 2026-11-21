// npm install, then node build.mjs [output-directory]
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve, join } from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import { codeToHtml } from "shiki";
import hljs from "highlight.js";
import katex from "katex";
import { mathjax } from "@mathjax/src/js/mathjax.js";
import { TeX } from "@mathjax/src/js/input/tex.js";
import { SVG } from "@mathjax/src/js/output/svg.js";
import { liteAdaptor } from "@mathjax/src/js/adaptors/liteAdaptor.js";
import { RegisterHTMLHandler } from "@mathjax/src/js/handlers/html.js";
import assert from "node:assert/strict";

const output = resolve(process.argv[2] ?? "output");
await mkdir(output, { recursive: true });
const require = createRequire(import.meta.url);
const katexCss = require.resolve("katex/dist/katex.min.css");
let css = await readFile(katexCss, "utf8");
for (const name of new Set(Array.from(css.matchAll(/url[(]fonts\/([^)]*)[)]/g), m => m[1]))) {
  const bytes = await readFile(new URL("./fonts/" + name, pathToFileURL(katexCss)));
  css = css.replaceAll("url(fonts/" + name + ")", "url(data:application/octet-stream;base64," + bytes.toString("base64") + ")");
}

const cue = 'const cue = {\n  bar: 1,\n  lights: "cyan"\n};';
const validate = 'def on_downbeat(beat):\n    return beat % 4 == 0';
const shiki = await codeToHtml(cue, { lang: "javascript", theme: "dracula" });
const highlighted = hljs.highlight(validate, { language: "python" }).value;
function plain(html) {
  return html.replace(/<[^>]*>/g, "").replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'")
    .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
}
assert.equal(plain(shiki), cue);
assert.equal(plain(highlighted), validate);

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const mathDocument = mathjax.document("", { InputJax: new TeX(), OutputJax: new SVG({ fontCache: "none" }) });
const beat = String.raw`t_{\mathrm{beat}} = \frac{60}{120}\,\mathrm{s} = 0.5\,\mathrm{s}`;
const duration = String.raw`8 \times 4 \times 0.5\,\mathrm{s} = 16\,\mathrm{s}`;
const mathSvg = adaptor.outerHTML(await mathDocument.convertPromise(beat, { display: false }));
const katexMath = katex.renderToString(duration, { throwOnError: true, output: "htmlAndMathml" });
assert.match(mathSvg, /data-mml-node="mfrac"/);
assert.match(katexMath, /<math\b/);
assert.match(katexMath, /<mn>16<\/mn>/);

const cards = [
  ["shiki", "Shiki", "#c2ff54", "첫 마디의 조명을 지정한다", shiki],
  ["highlight", "highlight.js", "#69f2f6", "각 마디의 첫 박을 찾는다", '<pre><code>' + highlighted + '</code></pre>'],
  ["mathjax", "MathJax", "#f49ade", "120 BPM에서 한 박은 몇 초일까?", mathSvg],
  ["katex", "KaTeX", "#ffd579", "4/4박자 여덟 마디는 얼마나 길까?", katexMath]
];
for (const [key, engine, accent, title, rendered] of cards) {
  const style = `*{box-sizing:border-box}body{margin:0;background:#10111e;color:#f2f0f7;font-family:Arial,"Malgun Gothic",sans-serif}
    article{width:760px;height:328px;padding:34px 40px;border-top:7px solid ` + accent + `;position:relative;overflow:hidden}
    header{display:flex;align-items:center;justify-content:space-between;color:` + accent + `;font:bold 20px Consolas,monospace}
    small{color:#a5a5b9;font:14px Consolas,monospace;letter-spacing:.08em}
    h1{font-size:28px;letter-spacing:-1px;margin:19px 0 14px}
    section{min-height:151px;display:flex;align-items:center;background:#191b2c;padding:15px 25px;border-radius:4px}
    pre{margin:0;font:22px/1.35 Consolas,monospace;background:transparent!important}code{font:inherit}
    .hljs-keyword{color:#ff9de3}.hljs-title{color:#8ce5ff}.hljs-number{color:#c0ff71}.hljs-params{color:#e3e1ff}
    mjx-container,.katex{font-size:35px!important}mjx-container svg{vertical-align:middle}`;
  const page = `<!doctype html><html lang="ko"><meta charset="utf-8"><title>` + engine + `</title>
    <style>` + (key === "katex" ? css : "") + style + `</style><article><header>` + engine +
    `<small>NEON ENCORE / SCORE</small></header><h1>` + title + `</h1><section>` + rendered + `</section></article></html>`;
  await writeFile(join(output, key + ".html"), page);
}
console.log("Rendered and checked " + cards.map(row => row[1]).join(", "));
