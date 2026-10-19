import { Link } from "react-router-dom";
import {
  CalendarRange,
  Table2,
  Brain,
  Layers,
  Gamepad2,
  Sigma,
  Wrench,
  ArrowRight,
  Target,
  Users,
  Clock,
  User,
  Mountain,
  Cloud,
  CheckCircle2,
} from "lucide-react";
import MermaidDiagram from "../components/MermaidDiagram";
import { QuanCridar } from "../components/Bloc";
import { DADES_CURS } from "../data/curs";

const seccions = [
  { name: "Calendari i avaluació", description: "Les 34 sessions, les proves i com es calcula la nota", href: "/calendari", icon: CalendarRange, color: "bg-blue-600" },
  { name: "1 · Dades", description: "Objectes de Python, NumPy i Pandas", href: "/dades", icon: Table2, color: "bg-emerald-600" },
  { name: "2 · Supervisat", description: "k-NN, arbres, boscos, regressió logística i SVM, amb la matemàtica de sota", href: "/supervisat", icon: Brain, color: "bg-sky-600" },
  { name: "3 · Dades brutes i no supervisat", description: "Pipelines sense fuites, PCA i k-means", href: "/no-supervisat", icon: Layers, color: "bg-teal-600" },
  { name: "4 · Xarxes i RL", description: "PyTorch, agents que aprenen jugant i el concurs", href: "/xarxes-i-rl", icon: Gamepad2, color: "bg-rose-600" },
  { name: "Recursos", description: "Caixa d'eines, catàleg de datasets, eines i vídeos", href: "/recursos", icon: Wrench, color: "bg-amber-600" },
];

const recorregut = `
flowchart LR
    B1["1 · Dades<br/>NumPy i Pandas"] --> B2["2 · Supervisat<br/>models que prediuen"]
    B2 --> B3["3 · Dades brutes<br/>i no supervisat"]
    B3 --> B4["4 · Xarxes i RL<br/>agents que juguen"]
    MA["Matematiques<br/>dins de cada bloc"] -.cada formula, la seva linia de codi.-> B1
    MA -.-> B2
    MA -.-> B3

    style B1 fill:#d1fae5
    style B2 fill:#e0f2fe
    style B3 fill:#ccfbf1
    style B4 fill:#ffe4e6
    style MA fill:#ede9fe,stroke:#7c3aed,stroke-width:2px
`;

export default function Home() {
  return (
    <div className="space-y-10">
      {/* Com es treballa */}
      <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm border border-gray-100">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Com es treballa</h2>
        <p className="text-gray-600 mb-5 max-w-3xl">
          Treballes tu, al teu ritme dins de cada sessió. En Xavi és a l'aula com a expert: el crides
          quan necessites criteri, no perquè et dicti els passos.
        </p>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
            <User className="w-5 h-5 text-emerald-700 mb-2" />
            <h3 className="font-semibold text-emerald-900 mb-1">Cada bloc, quatre passos</h3>
            <p className="text-sm text-gray-700">
              <strong>Aprèn</strong> amb els quaderns de teoria, mira els <strong>exemples</strong>{" "}
              resolts, enfronta't als <strong>reptes</strong> i arriba a la <strong>prova</strong>.
              La pàgina de cada bloc segueix aquest ordre.
            </p>
          </div>
          <div className="p-4 bg-sky-50 border border-sky-200 rounded-lg">
            <Mountain className="w-5 h-5 text-sky-700 mb-2" />
            <h3 className="font-semibold text-sky-900 mb-1">Els reptes són el centre</h3>
            <p className="text-sm text-gray-700">
              Dades reals que no has vist mai i una pregunta per respondre. No hi ha passos escrits:
              tens els exemples resolts i la caixa d'eines. Que alguna cosa surti malament forma part
              de la feina.
            </p>
          </div>
          <div className="p-4 bg-violet-50 border border-violet-200 rounded-lg">
            <CheckCircle2 className="w-5 h-5 text-violet-700 mb-2" />
            <h3 className="font-semibold text-violet-900 mb-1">Comprovacions a cada pas</h3>
            <p className="text-sm text-gray-700">
              Cada tasca et diu si el procediment és correcte, no quin número t'ha de sortir. Cada
              fórmula va seguida de la línia de NumPy que la calcula.
            </p>
          </div>
          <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <Cloud className="w-5 h-5 text-amber-700 mb-2" />
            <h3 className="font-semibold text-amber-900 mb-1">Sense instal·lar res</h3>
            <p className="text-sm text-gray-700">
              Tot s'obre a Google Colab des del navegador. Desa una còpia al teu Drive just en obrir
              cada quadern.
            </p>
          </div>
        </div>
        <QuanCridar color="indigo" />
      </div>

      {/* Seccions */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {seccions.map((s) => (
          <Link key={s.name} to={s.href} className="bg-white rounded-xl p-6 shadow-sm card-hover border border-gray-100">
            <div className={`${s.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
              <s.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{s.name}</h3>
            <p className="text-gray-600 text-sm mb-4">{s.description}</p>
            <div className="flex items-center text-primary-600 text-sm font-medium">
              Obre <ArrowRight className="w-4 h-4 ml-1" />
            </div>
          </Link>
        ))}
      </div>

      {/* El mòdul */}
      <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm border border-gray-100">
        <p className="text-primary-700 font-medium text-sm mb-1">Optativa · Curs 2026-27</p>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Aprenentatge automàtic</h2>
        <div className="flex flex-wrap gap-3 mb-5 text-sm">
          <span className="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-1.5">
            <Target className="w-4 h-4" /> Un únic resultat d'aprenentatge
          </span>
          <span className="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-1.5">
            <Users className="w-4 h-4" /> DAM i DAW · 2n curs
          </span>
          <span className="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-1.5">
            <Clock className="w-4 h-4" /> {DADES_CURS.hores} h · {DADES_CURS.sessions} sessions de 2 h, dilluns i dimarts
          </span>
        </div>
        <blockquote className="border-l-4 border-primary-500 bg-primary-50 p-5 rounded-r-lg">
          <p className="text-primary-900 text-lg font-medium italic">
            Crea aplicacions fent ús de models d'aprenentatge automàtic.
          </p>
        </blockquote>
        <p className="text-gray-600 mt-4 leading-relaxed">
          Diu <strong>crea aplicacions</strong>. No diu memoritza algorismes ni demostra teoremes. Per
          això el 80 % de la nota són proves pràctiques amb ordinador, i el curs acaba amb un agent
          que has entrenat tu competint en una cursa.
        </p>
        <div className="mt-6">
          <MermaidDiagram chart={recorregut} />
        </div>
      </div>
    </div>
  );
}
