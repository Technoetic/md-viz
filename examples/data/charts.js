const bg = "#101425", fg = "#E9EDFF", grid = "#343B53";
const cyan = "#71E7E1", pink = "#FE72B7", lime = "#DAF777", blue = "#7A94F7";
const specs = {
  "vega-lite":["ADMISSIONS","Vega-Lite","관객은 몇 시에 몰렸을까?","18시 20분과 30분에 기록한 입장객은 각각 270명과 274명입니다.",cyan],
  matplotlib:["LIGHTING","Matplotlib","두 조명의 빛이 어디에서 가장 강할까?","정면을 0°로 두면 청록은 왼쪽 15°, 호박색은 오른쪽 30°에서 가장 밝습니다.",lime],
  seaborn:["AUDIENCE","seaborn","어느 곡에 관객 반응이 가장 컸을까?","앙코르에서 네 구역 모두 반응 지수 90을 넘거나 90에 도달합니다.",pink],
  altair:["SOUNDCHECK","Altair","어떤 악기의 점검이 계획보다 길었을까?","보컬과 신시사이저는 계획보다 각각 3분 더 걸렸습니다.",cyan],
  ggplot2:["QUEUES","ggplot2","어느 입구에서 더 오래 기다렸을까?","입구마다 8명을 관찰한 예시입니다. 동쪽 입구의 중앙값은 8.5분입니다.",pink],
  chartjs:["ENERGY","Chart.js","공연 전력량 100 kWh는 어디로 갔을까?","조명에 48 kWh, 음향에 32 kWh를 사용했습니다.",lime],
  observable:["MERCH","Observable Plot","관객이 가장 많이 산 기념품은?","포스터 88장과 핀 27개가 팔렸습니다. 판매량 차이는 61개입니다.",cyan],
  plotly:["BOX OFFICE","Plotly","좌석을 조정하자 판매 가능 수가 어떻게 바뀌었을까?","2,400석에서 시작해 100석을 열고 200석을 제외하면 2,300석이 남습니다.",pink],
  echarts:["WALK FLOW","Apache ECharts","어느 입구에서 어느 객석으로 이동했을까?","관객 300명 중 210명은 플로어로, 90명은 발코니로 향했습니다.",cyan],
  d3:["CUE CLOCK","D3","8마디 동안 어느 조명이 켜질까?","바깥부터 Wash, Beam, Flash입니다. 밝은 칸은 켜짐, 한 칸은 한 박입니다.",lime],
  cytoscape:["SIGNAL","Cytoscape.js","보컬 신호는 어디서 공연용과 녹음용으로 갈릴까?","스플리터에서 갈라진 신호가 각각 공연 믹서와 녹음 믹서로 갑니다.",pink],
  leaflet:["FIELD MAP","Leaflet","집결점·환승점·무대는 어느 방향에 있을까?","점은 서울 도심의 예시 좌표입니다. 선은 지점 순서를 연결합니다.",cyan]
};

const deps = {
  chartjs:["chart.umd.min.js"], observable:["d3.min.js","plot.umd.min.js"],
  plotly:["plotly.min.js"], echarts:["echarts.min.js"], d3:["d3.min.js"],
  cytoscape:["cytoscape.min.js"], leaflet:["leaflet.js"]
};
function load(name) {
  return new Promise((resolve,reject) => {
    const script=document.createElement("script");
    script.onload=resolve;script.onerror=()=>reject(Error("Cannot load " + name));
    script.src="vendor/"+name;document.head.append(script);
  });
}
const w=808, h=280, host=document.querySelector("#chart");

function chartjs(data) {
  host.style.display="grid";host.style.gridTemplateColumns="1fr 1fr";host.style.alignItems="center";
  const wrap=document.createElement("div");wrap.style="height:265px;width:345px;position:relative;justify-self:end";
  const canvas=document.createElement("canvas");wrap.append(canvas);host.append(wrap);
  const values=Object.values(data.power), names=Object.keys(data.power), colors=[lime,cyan,pink,blue];
  new Chart(canvas,{type:"doughnut",data:{labels:names,datasets:[{data:values,backgroundColor:colors,borderColor:bg,borderWidth:4}]},
    options:{animation:false,maintainAspectRatio:false,cutout:"73%",plugins:{legend:{display:false}}},
    plugins:[{id:"total",afterDraw(chart){const area=chart.chartArea,ctx=chart.ctx,x=(area.left+area.right)/2,y=(area.top+area.bottom)/2;
      ctx.save();ctx.textAlign="center";ctx.fillStyle=fg;ctx.font="bold 38px Arial";ctx.fillText("100",x,y+6);
      ctx.fillStyle="#aeb9d3";ctx.font="15px Arial";ctx.fillText("kWh",x,y+27);ctx.restore();}}]});
  const legend=document.createElement("div");legend.style="margin:0 30px;width:245px";
  for (let i=0;i<names.length;i++){const row=document.createElement("div");row.style="display:flex;justify-content:space-between;border-bottom:1px solid #343b53;padding:9px 1px;font:600 20px Arial";
    const label=document.createElement("span");label.textContent=names[i];label.style.color=colors[i];
    const value=document.createElement("span");value.textContent=values[i]+"%";row.append(label,value);legend.append(row);}
  host.append(legend);
}
function observable(data) {
  const rows=Object.entries(data.merch).map(([name,qty])=>({name,qty}));
  const svg=Plot.plot({width:w,height:h,marginLeft:91,marginRight:56,marginBottom:45,style:{background:bg,color:fg,fontSize:"16px",fontFamily:"Arial"},
    x:{label:"Units sold",domain:[0,95],grid:true},y:{label:null,domain:rows.map(d=>d.name)},marks:[
      Plot.ruleY(rows,{y:"name",x1:0,x2:"qty",stroke:"#4D627D",strokeWidth:4}),
      Plot.dot(rows,{y:"name",x:"qty",r:9,fill:cyan}),Plot.text(rows,{y:"name",x:"qty",text:"qty",dx:16,textAnchor:"start",fill:lime,fontWeight:700})]});
  host.append(svg);
}
async function plotly(data) {
  const t=data.tickets;
  await Plotly.newPlot(host,[{type:"waterfall",measure:["absolute","relative","relative","relative","total"],
    x:["Initial","Released","Sightline hold","Reserved","For sale"],y:[t.start,t.released,-t.sightline,-t.reserved,0],
    text:[String(t.start),"+"+t.released,"−"+t.sightline,"−"+t.reserved,String(t.start+t.released-t.sightline-t.reserved)],
    textposition:"outside",cliponaxis:false,connector:{line:{color:"#8792ad",dash:"dot"}},increasing:{marker:{color:lime}},decreasing:{marker:{color:pink}},totals:{marker:{color:cyan}}}],
  {width:w,height:h,paper_bgcolor:bg,plot_bgcolor:bg,showlegend:false,font:{family:"Arial",size:15,color:fg},
   margin:{t:24,r:18,b:40,l:69},yaxis:{range:[0,2850],title:"Seats",gridcolor:grid,zeroline:false},
   xaxis:{tickfont:{size:14}},waterfallgap:.36}, {staticPlot:true,displayModeBar:false});
}
function drawEcharts(data) {
  const chart=window.echarts.init(host,null,{renderer:"svg",width:w,height:h});
  const colors={North:cyan,East:blue,West:pink,Floor:lime,Balcony:"#CC86FF"};
  chart.setOption({animation:false,series:[{type:"sankey",left:112,right:132,top:16,bottom:12,nodeWidth:20,nodeGap:17,
    data:Object.keys(colors).map(name=>({name,itemStyle:{color:colors[name]},label:{position:["Floor","Balcony"].includes(name)?"right":"left"}})),
    links:data.walks.map(([source,target,value])=>({source,target,value})),lineStyle:{color:"gradient",opacity:.43,curveness:.55},
    label:{color:fg,fontFamily:"Arial",fontSize:17,formatter:p=>p.name+"  "+p.value}}]});
}
function drawD3(data) {
  const cue=data.cues,channels=["Wash","Beam","Flash"],colors=[cyan,pink,lime];
  const svg=d3.select(host).append("svg").attr("viewBox","0 0 808 280");
  const face=svg.append("g").attr("transform","translate(240 140)");
  const step=2*Math.PI/cue.Wash.length;
  channels.forEach((name,row)=>{const r=98-row*18;
    const arc=d3.arc().innerRadius(r-13).outerRadius(r).padAngle(.011).cornerRadius(1.6);
    face.selectAll(".r"+row).data(cue[name]).join("path").attr("d",(v,i)=>arc({startAngle:i*step,endAngle:(i+1)*step})).attr("fill",v=>v?colors[row]:"#2a3248");});
  for(let b=0;b<8;b++){const angle=(b*4+2)*step-Math.PI/2;
    face.append("text").attr("x",Math.cos(angle)*120).attr("y",Math.sin(angle)*120+4).attr("text-anchor","middle").attr("fill",fg).attr("font-size",13).text("B"+(b+1));}
  face.append("text").attr("text-anchor","middle").attr("fill",fg).attr("y",3).attr("font-size",22).attr("font-weight",700).text("16 s");
  const legend=svg.append("g").attr("transform","translate(478 56)");
  legend.append("text").attr("fill",fg).attr("font-size",20).attr("font-weight",700).text("120 BPM   /   4/4");
  channels.forEach((name,i)=>{const y=47+i*40;legend.append("rect").attr("x",0).attr("y",y-13).attr("width",18).attr("height",14).attr("rx",3).attr("fill",colors[i]);
    legend.append("text").attr("x",29).attr("y",y).attr("fill",fg).attr("font-size",18).text(name+"     "+d3.sum(cue[name])+" / 32");});
}
async function drawNetwork(data) {
  const graph=data.signal;
  const cy=cytoscape({container:host,pixelRatio:1,layout:{name:"preset",fit:true,padding:30},userZoomingEnabled:false,userPanningEnabled:false,
    elements:[...graph.nodes.map(([id,label,x,y])=>({data:{id,label},position:{x,y}})),...graph.edges.map(([source,target])=>({data:{source,target}}))],
    style:[{selector:"node",style:{shape:"round-rectangle",width:121,height:45,"background-color":"#23354c","border-color":cyan,"border-width":2,label:"data(label)",color:fg,"font-family":"Arial","font-size":16,"text-valign":"center"}},
      {selector:"edge",style:{width:3,"line-color":"#859BB9","target-arrow-color":"#859BB9","target-arrow-shape":"triangle","curve-style":"bezier"}},
      {selector:"#split",style:{"background-color":"#48344F","border-color":pink}},
      {selector:"#rec,#disk",style:{"border-color":lime}}]});
  await new Promise(resolve=>cy.ready(resolve));
}
function drawMap(data) {
  const map=L.map(host,{zoomControl:false,attributionControl:false,zoomSnap:.05,zoomAnimation:false,dragging:false,scrollWheelZoom:false});
  const points=data.shuttle.map(p=>[p.lat,p.lon]);
  map.fitBounds(points,{padding:[100,40]});
  const bounds=map.getBounds();
  const gridStyle={color:"#344462",weight:1,interactive:false};
  for(let lat=Math.ceil(bounds.getSouth()*500)/500;lat<bounds.getNorth();lat+=.002){
    L.polyline([[lat,bounds.getWest()],[lat,bounds.getEast()]],gridStyle).addTo(map);
    L.marker([lat,bounds.getWest()+.0002],{icon:L.divIcon({className:"coordinate",html:lat.toFixed(3)+"° N",iconAnchor:[0,-2]})}).addTo(map);}
  for(let lon=Math.ceil(bounds.getWest()*500)/500;lon<bounds.getEast();lon+=.002){
    L.polyline([[bounds.getSouth(),lon],[bounds.getNorth(),lon]],gridStyle).addTo(map);}
  L.polyline(points,{color:cyan,weight:3,dashArray:"8 6"}).addTo(map);
  data.shuttle.forEach((p,i)=>{
    L.circleMarker([p.lat,p.lon],{color:bg,weight:3,radius:8,fillColor:[cyan,pink,lime][i],fillOpacity:1}).addTo(map);
    L.marker([p.lat,p.lon],{icon:L.divIcon({className:"venue-label",html:p.label,iconAnchor:[-13,13]})}).addTo(map);
  });
  L.control.scale({imperial:false,maxWidth:95}).addTo(map);
}

async function render(){
  const key=new URLSearchParams(location.search).get("chart")||"d3";
  const [category,engine,title,insight,accent]=specs[key];
  document.documentElement.style.setProperty("--ac",accent);
  for (const [id,value] of Object.entries({category,engine,insight}))document.getElementById(id).textContent=value;
  document.querySelector("h1").textContent=title;
  if(deps[key]){
    for(const name of deps[key])await load(name);
    const data=await (await fetch("show.json")).json();
    const f={chartjs,observable,plotly,echarts:drawEcharts,d3:drawD3,cytoscape:drawNetwork,leaflet:drawMap}[key];
    await f(data);
  }else{
    const im=document.createElement("img");
    im.className="still";im.alt=title;im.src=key+(["matplotlib","seaborn"].includes(key)?".png":".svg");
    host.append(im);await im.decode();
  }
  await document.fonts.ready;
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  document.body.dataset.state="ready";
}
render().catch(e=>{document.body.dataset.state="error";document.body.dataset.error=String(e);});
