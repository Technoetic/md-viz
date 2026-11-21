/* Input to ExcalidrawLib.convertToExcalidrawElements(), in audience view. */
function encoreStage() {
  const shapes = [];
  function box(x, y, width, height, fill, stroke) {
    shapes.push({type: "rectangle", x, y, width, height, fillStyle: "solid",
      backgroundColor: fill, strokeColor: stroke, strokeWidth: 2, roughness: 0.8});
  }
  function label(x, y, text, size = 23, color = "#f0f2ff") {
    shapes.push({type: "text", x, y, text, fontSize: size, fontFamily: 2, strokeColor: color});
  }
  function circle(x, y, diameter, fill, stroke) {
    shapes.push({type: "ellipse", x, y, width: diameter, height: diameter,
      backgroundColor: fill, fillStyle: "solid", strokeColor: stroke, roughness: 1});
  }
  box(0, 0, 660, 270, "#202439", "#9b98d0");
  label(20, 16, "UPSTAGE", 14, "#cad0ee");
  box(290, 18, 145, 82, "#173e3b", "#65e4cd");
  circle(308, 34, 36, "#216456", "#8afbd8");
  circle(347, 38, 30, "#216456", "#8afbd8");
  circle(387, 33, 27, "#216456", "#8afbd8");
  label(328, 72, "DRUMS", 15);
  box(38, 107, 153, 50, "#263f57", "#81bafa");
  label(77, 117, "SYNTH", 21);
  circle(303, 155, 58, "#5c2951", "#ff8ec8");
  label(289, 219, "VOCALS", 21);
  box(485, 176, 133, 48, "#272844", "#a69bdd");
  label(508, 185, "MONITOR", 18);
  label(246, 295, "↓   AUDIENCE   ↓", 23, "#f3a6d3");
  return shapes;
}
