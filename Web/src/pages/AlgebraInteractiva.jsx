import { useEffect, useRef, useState } from "react";
import { Download, RotateCcw } from "lucide-react";

// Quatre applets de GeoGebra per a MA_01 (2-nov-2026). Es construeixen amb ordres
// des de l'API oficial (deployggb.js): no depenen de cap fitxer pujat a geogebra.org.

const GGB_SCRIPT = "https://www.geogebra.org/apps/deployggb.js";
let promesaScript = null;

function carregaGeoGebra() {
  if (window.GGBApplet) return Promise.resolve();
  if (!promesaScript) {
    promesaScript = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = GGB_SCRIPT;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }
  return promesaScript;
}

// Punts del pètal (llargada, amplada) de 8 versicolor i 8 virgíniques reals d'Iris.
const VERSICOLOR = [[4.7, 1.4], [4.5, 1.5], [4.9, 1.5], [4.0, 1.3], [4.6, 1.5], [4.5, 1.3], [4.7, 1.6], [5.0, 1.7]];
const VIRGINICA = [[6.0, 2.5], [5.1, 1.9], [5.9, 2.1], [5.6, 1.8], [5.8, 2.2], [6.6, 2.1], [4.5, 1.7], [4.9, 1.8]];

function ordresFrontera() {
  const o = [
    "Q=(5,1.7)",
    "T=(5.6,2.3)",
    "w=Vector(Q,T)",
    "f=PerpendicularLine(Q,w)",
    "zona=(x(T)-x(Q))*(x-x(Q))+(y(T)-y(Q))*(y-y(Q))>0",
  ];
  const errors = [];
  VERSICOLOR.forEach(([px, py], i) => {
    o.push(`N_{${i + 1}}=(${px},${py})`);
    errors.push(`If(Dot(w,N_{${i + 1}}-Q)>0,1,0)`);
  });
  VIRGINICA.forEach(([px, py], i) => {
    o.push(`V_{${i + 1}}=(${px},${py})`);
    errors.push(`If(Dot(w,V_{${i + 1}}-Q)<0,1,0)`);
  });
  o.push(`errs=Sum({${errors.join(",")}})`);
  o.push("bb=-Dot(w,Q)");
  o.push(
    'txt=Text("w = ("+x(w)+", "+y(w)+")    b = "+bb+"\\nerrors: "+errs+" de 16", Corner(4)+(0.15,-0.25), true)'
  );
  // estil
  o.push('SetColor(zona,"#e11d48")', "SetFilling(zona,0.12)", "ShowLabel(zona,false)");
  o.push('SetColor(f,"black")', "SetLineThickness(f,7)", "ShowLabel(f,false)");
  o.push('SetColor(w,"black")', "SetLineThickness(w,8)", 'SetCaption(w,"w")');
  o.push('SetColor(Q,"black")', 'SetCaption(Q,"mou la frontera")', 'SetCaption(T,"gira w")');
  VERSICOLOR.forEach((_, i) => o.push(`SetColor(N_{${i + 1}},"#2563eb")`, `SetFixed(N_{${i + 1}},true)`, `ShowLabel(N_{${i + 1}},false)`));
  VIRGINICA.forEach((_, i) => o.push(`SetColor(V_{${i + 1}},"#ea580c")`, `SetFixed(V_{${i + 1}},true)`, `ShowLabel(V_{${i + 1}},false)`));
  o.push("ShowLabel(errs,false)", "ShowLabel(bb,false)");
  return o;
}

const APPLETS = [
  {
    id: "ggbEscalar",
    titol: "1. El signe del producte escalar",
    seccio: "Apartat 4 del quadern",
    text: "Arrossega el punt B. La norma de les fletxes canvia, però el que decideix el signe de a · b és l'angle: agut, positiu; recte, zero; obtús, negatiu.",
    repte: "Troba dues posicions de B on a · b valgui exactament 0. Què tenen en comú?",
    vista: [-4, 5, -2, 4],
    ordres: [
      "A=(3,1)",
      "B=(1,3)",
      "a=Vector(A)",
      "b=Vector(B)",
      "p=Dot(a,b)",
      "th=acos(p/(Length(a)*Length(b)))*180/pi",
      'sig=If(p>0.05,"positiu (angle agut)",If(p<-0.05,"negatiu (angle obtús)","zero (90 graus)"))',
      'txt=Text("a · b = "+p+"\\nangle = "+th+" graus\\n"+sig, Corner(4)+(0.2,-0.3), true)',
      'SetColor(a,"#2563eb")',
      'SetColor(b,"#ea580c")',
      "SetLineThickness(a,8)",
      "SetLineThickness(b,8)",
      'SetColor(A,"#2563eb")',
      'SetColor(B,"#ea580c")',
      "SetFixed(A,true)",
      "ShowLabel(p,false)",
      "ShowLabel(th,false)",
      "ShowLabel(sig,false)",
    ],
  },
  {
    id: "ggbProjeccio",
    titol: "2. La projecció: l'ombra d'una fletxa",
    seccio: "Apartat 5 del quadern",
    text: "Arrossega A o B. La fletxa verda és l'ombra de a sobre la recta de b, i la línia discontínua sempre fa 90 graus amb b.",
    repte: "Quan és negativa la projecció escalar? I quan l'ombra és més llarga que b?",
    vista: [-2, 6.5, -1.5, 4],
    ordres: [
      "A=(1.5,3)",
      "B=(5,1)",
      "a=Vector(A)",
      "b=Vector(B)",
      "r=Line((0,0),B)",
      "P=(Dot(a,b)/Dot(b,b))*B",
      "ombra=Vector(P)",
      "s=Segment(A,P)",
      "pesc=Dot(a,b)/Length(b)",
      'txt=Text("projecció escalar = (a · b) / ‖b‖ = "+pesc, Corner(4)+(0.2,-0.3), true)',
      'SetColor(a,"#2563eb")',
      'SetColor(b,"#ea580c")',
      'SetColor(ombra,"#16a34a")',
      "SetLineThickness(a,8)",
      "SetLineThickness(b,8)",
      "SetLineThickness(ombra,10)",
      'SetColor(r,"gray")',
      "SetLineStyle(r,2)",
      "SetLineStyle(s,1)",
      'SetColor(s,"black")',
      "ShowLabel(r,false)",
      "ShowLabel(s,false)",
      "ShowLabel(P,false)",
      'SetColor(P,"#16a34a")',
      "ShowLabel(pesc,false)",
      'SetCaption(ombra,"ombra")',
    ],
  },
  {
    id: "ggbMatriu",
    titol: "3. Una matriu és una transformació",
    seccio: "Apartat 6 del quadern",
    text: "Els punts U i V són les dues columnes de la matriu: on van a parar (1, 0) i (0, 1). Arrossega'ls i mira com es deforma tot el pla. El punt P és un vector qualsevol, i AP la seva imatge.",
    repte: "Aconsegueix un gir, una ampliació i un cisallament. Què passa amb el quadrat quan U i V queden sobre la mateixa recta? Mira el determinant.",
    vista: [-3.5, 4.5, -2.5, 3.5],
    ordres: [
      "U=(1,0)",
      "V=(0,1)",
      "P=(1,0.5)",
      "sq0=Polygon((0,0),(1,0),(1,1),(0,1))",
      "sq=Polygon((0,0),U,U+V,V)",
      "gx=Sequence(Segment(k*U-4*V,k*U+4*V),k,-4,4)",
      "gy=Sequence(Segment(-4*U+k*V,4*U+k*V),k,-4,4)",
      "AP=x(P)*U+y(P)*V",
      "vp=Vector(P)",
      "vap=Vector(AP)",
      "det=x(U)*y(V)-x(V)*y(U)",
      'txt=Text("A = [ "+x(U)+"   "+x(V)+" ]\\n      [ "+y(U)+"   "+y(V)+" ]\\ndet(A) = "+det, Corner(4)+(0.2,-0.3), true)',
      'SetColor(gx,"#93c5fd")',
      'SetColor(gy,"#93c5fd")',
      "SetLineThickness(gx,2)",
      "SetLineThickness(gy,2)",
      'SetColor(sq0,"gray")',
      "SetFilling(sq0,0.15)",
      'SetColor(sq,"#2563eb")',
      "SetFilling(sq,0.3)",
      'SetColor(U,"#dc2626")',
      'SetColor(V,"#16a34a")',
      'SetCaption(U,"U = columna 1")',
      'SetCaption(V,"V = columna 2")',
      'SetColor(vp,"gray")',
      'SetColor(vap,"#2563eb")',
      "SetLineThickness(vap,8)",
      'SetCaption(vap,"AP")',
      'SetCaption(vp,"P")',
      "ShowLabel(P,false)",
      "ShowLabel(AP,false)",
      "ShowLabel(sq0,false)",
      "ShowLabel(sq,false)",
      "ShowLabel(det,false)",
    ],
  },
  {
    id: "ggbFrontera",
    titol: "4. La frontera de decisió i el vector w",
    seccio: "Apartat 7 del quadern",
    text: "Són 16 flors reals d'Iris, mesures del pètal: blaves versicolor, taronges virgíniques. La recta és z = w · x + b = 0, i w hi és sempre perpendicular. La zona vermella és on z > 0: el model hi diu «virgínica».",
    repte: "Mou Q i T fins a deixar el mínim d'errors que puguis. Ho pots fer amb zero? Això és, a mà, el que fa l'entrenament.",
    vista: [3.5, 7, 0.9, 2.8],
    ordres: ordresFrontera(),
  },
];

function Applet({ config }) {
  const contenidor = useRef(null);
  const api = useRef(null);
  const [error, setError] = useState(false);

  const munta = () => {
    const amplada = contenidor.current?.clientWidth || 700;
    const params = {
      id: config.id,
      appName: "classic",
      perspective: "G",
      width: amplada,
      height: Math.max(320, Math.min(460, Math.round(amplada * 0.62))),
      showToolBar: false,
      showAlgebraInput: false,
      showMenuBar: false,
      showResetIcon: false,
      enableShiftDragZoom: false,
      enableRightClick: false,
      showZoomButtons: false,
      language: "ca",
      borderColor: "#e5e7eb",
      appletOnLoad: (a) => {
        api.current = a;
        a.setGridVisible(true);
        a.setCoordSystem(...config.vista);
        config.ordres.forEach((c) => a.evalCommand(c));
      },
    };
    new window.GGBApplet(params, true).inject(config.id);
  };

  useEffect(() => {
    carregaGeoGebra().then(munta).catch(() => setError(true));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const reinicia = () => {
    if (!api.current) return;
    api.current.newConstruction();
    api.current.setGridVisible(true);
    api.current.setCoordSystem(...config.vista);
    config.ordres.forEach((c) => api.current.evalCommand(c));
  };

  const descarrega = () => {
    if (!api.current) return;
    const b64 = api.current.getBase64();
    const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    const url = URL.createObjectURL(new Blob([bytes], { type: "application/vnd.geogebra.file" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `MA01_${config.id.replace("ggb", "").toLowerCase()}.ggb`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="bg-white rounded-xl p-5 sm:p-6 shadow-sm border border-gray-100">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-2">
        <h2 className="text-xl font-bold text-gray-900">{config.titol}</h2>
        <span className="text-xs text-gray-500">{config.seccio}</span>
      </div>
      <p className="text-gray-700 mb-2 leading-relaxed">{config.text}</p>
      <p className="text-sm text-indigo-800 bg-indigo-50 rounded-lg px-3 py-2 mb-4">
        <strong>Prova:</strong> {config.repte}
      </p>
      <div ref={contenidor} className="w-full overflow-hidden rounded-lg">
        {error ? (
          <p className="text-sm text-red-700">No s'ha pogut carregar GeoGebra. Comprova la connexió.</p>
        ) : (
          <div id={config.id} />
        )}
      </div>
      <div className="flex gap-3 mt-3">
        <button onClick={reinicia} className="inline-flex items-center gap-1.5 text-sm text-gray-700 hover:text-gray-900">
          <RotateCcw className="w-4 h-4" /> Torna a començar
        </button>
        <button onClick={descarrega} className="inline-flex items-center gap-1.5 text-sm text-gray-700 hover:text-gray-900">
          <Download className="w-4 h-4" /> Descarrega el .ggb
        </button>
      </div>
    </section>
  );
}

export default function AlgebraInteractiva() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl p-6 sm:p-8 shadow-sm border border-gray-100">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Àlgebra lineal interactiva</h1>
        <p className="text-gray-700 leading-relaxed">
          Quatre dibuixos del quadern <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm">MA_01_algebra_lineal</code>{" "}
          que es poden moure. Els punts grossos s'arrosseguen amb el ratolí. No substitueixen el quadern: els números
          exactes i les comprovacions hi són allà; aquí es tracta de veure què passa quan canvies una cosa.
        </p>
      </div>
      {APPLETS.map((c) => (
        <Applet key={c.id} config={c} />
      ))}
    </div>
  );
}
