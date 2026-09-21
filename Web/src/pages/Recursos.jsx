import { useRef } from "react";
import { Link } from "react-router-dom";
import {
  Wrench,
  PlayCircle,
  BookOpen,
  GraduationCap,
  Lightbulb,
  ExternalLink,
  Cloud,
  Terminal,
  Sparkles,
  Database,
  Bot,
  TreePine,
  Flame,
  Gamepad2,
} from "lucide-react";

const EINES = [
  {
    nom: "Google Colab",
    url: "https://colab.research.google.com",
    icona: Cloud,
    desc: "Quaderns amb GPU gratuïta. És l'entorn principal del curs.",
  },
  {
    nom: "PythonAnywhere",
    url: "https://www.pythonanywhere.com",
    icona: Terminal,
    desc: "Per repassar sintaxi de Python des del navegador.",
  },
  {
    nom: "Teachable Machine",
    url: "https://teachablemachine.withgoogle.com",
    icona: Sparkles,
    desc: "Entrenar un classificador sense codi. Es fa servir el primer dia de curs.",
  },
  {
    nom: "Kaggle",
    url: "https://www.kaggle.com",
    icona: Database,
    desc: "Datasets i competicions de Machine Learning.",
  },
  {
    nom: "Hugging Face",
    url: "https://huggingface.co",
    icona: Bot,
    desc: "Models preentrenats i datasets llestos per fer servir.",
  },
  {
    nom: "scikit-learn",
    url: "https://scikit-learn.org",
    icona: TreePine,
    desc: "La llibreria de Machine Learning clàssic que fem servir al curs.",
  },
  {
    nom: "PyTorch",
    url: "https://pytorch.org",
    icona: Flame,
    desc: "La llibreria per a les xarxes neuronals.",
  },
  {
    nom: "Gymnasium",
    url: "https://gymnasium.farama.org",
    icona: Gamepad2,
    desc: "Entorns per practicar reinforcement learning.",
  },
];

const VIDEOS = [
  {
    nom: "3Blue1Brown — Xarxes neuronals",
    url: "https://www.3blue1brown.com/topics/neural-networks",
    desc: "La millor explicació visual que hi ha sobre com funcionen les xarxes neuronals.",
  },
  {
    nom: "Artem Kirsanov",
    url: "https://www.youtube.com/@ArtemKirsanov",
    desc: "Canal de divulgació sobre AI i Machine Learning.",
  },
  {
    nom: "Codemy.com — Deep Learning amb PyTorch",
    url: "https://codemy.com",
    desc: "Sèrie de vídeos per iniciar-se en Deep Learning fent servir PyTorch.",
  },
  {
    nom: "Graphics in 5 minutes — Reinforcement Learning from scratch",
    url: null,
    desc: "Es distribueix pel Moodle del centre.",
  },
  {
    nom: "Documental: «El algoritmo contra el crimen»",
    url: null,
    desc: "Es distribueix pel Moodle del centre.",
  },
  {
    nom: "Article: errades habituals en gràfics",
    url: null,
    desc: "Es distribueix pel Moodle del centre.",
  },
  {
    nom: "Article: llibreries gràfiques en Python",
    url: null,
    desc: "Es distribueix pel Moodle del centre.",
  },
];

const DOCS = [
  {
    nom: "Documentació de Gymnasium",
    url: "https://gymnasium.farama.org",
    desc: "Referència de l'API i dels tipus d'entorns.",
    extern: true,
  },
  {
    nom: "Llista de jocs de Gymnasium",
    url: "https://gymnasium.farama.org/environments/",
    desc: "Catàleg dels entorns disponibles, agrupats per família.",
    extern: true,
  },
  {
    nom: "Apunts de Reinforcement Learning",
    url: "/deep-rl",
    desc: "Apunts propis del professor sobre reinforcement learning.",
    extern: false,
  },
];

function scrollToRef(ref) {
  ref.current?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function CategoriaHeader({ icona: Icona, titol }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div className="bg-indigo-50 text-indigo-600 rounded-lg p-2">
        <Icona className="w-5 h-5" />
      </div>
      <h2 className="text-xl font-semibold text-gray-900">{titol}</h2>
    </div>
  );
}

function EinaCard({ eina }) {
  const Icona = eina.icona;
  return (
    <a
      href={eina.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-3 p-4 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50/40 transition-colors"
    >
      <Icona className="w-5 h-5 text-indigo-500 shrink-0 mt-0.5" />
      <div className="min-w-0">
        <div className="flex items-center gap-1.5 font-medium text-gray-900">
          {eina.nom}
          <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
        </div>
        <p className="text-sm text-gray-600 mt-0.5">{eina.desc}</p>
      </div>
    </a>
  );
}

function RecursItem({ item }) {
  if (item.url) {
    return (
      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block p-4 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50/40 transition-colors"
      >
        <div className="flex items-center gap-1.5 font-medium text-gray-900">
          {item.nom}
          <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
        </div>
        <p className="text-sm text-gray-600 mt-0.5">{item.desc}</p>
      </a>
    );
  }
  return (
    <div className="p-4 rounded-lg border border-gray-100">
      <div className="font-medium text-gray-900">{item.nom}</div>
      <p className="text-sm text-gray-600 mt-0.5">{item.desc}</p>
    </div>
  );
}

export default function Recursos() {
  const einesRef = useRef(null);
  const videosRef = useRef(null);
  const docsRef = useRef(null);
  const moodleRef = useRef(null);
  const consellsRef = useRef(null);

  const seccions = [
    { nom: "Eines de treball", ref: einesRef },
    { nom: "Vídeos i divulgació", ref: videosRef },
    { nom: "Documentació", ref: docsRef },
    { nom: "Al Moodle", ref: moodleRef },
    { nom: "Consells", ref: consellsRef },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Recursos</h1>
        <p className="text-gray-600 mt-2">
          Eines, materials i documentació per seguir el mòdul. Cap eina de la
          llista demana instal·lar res al portàtil: tot funciona des del
          navegador.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {seccions.map((s) => (
          <button
            key={s.nom}
            type="button"
            onClick={() => scrollToRef(s.ref)}
            className="text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-full px-4 py-1.5 transition-colors"
          >
            {s.nom}
          </button>
        ))}
      </div>

      <div ref={einesRef} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <CategoriaHeader icona={Wrench} titol="Eines de treball" />
        <div className="grid sm:grid-cols-2 gap-3">
          {EINES.map((eina) => (
            <EinaCard key={eina.nom} eina={eina} />
          ))}
        </div>
      </div>

      <div ref={videosRef} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <CategoriaHeader icona={PlayCircle} titol="Vídeos i divulgació" />
        <div className="grid sm:grid-cols-2 gap-3">
          {VIDEOS.map((item) => (
            <RecursItem key={item.nom} item={item} />
          ))}
        </div>
      </div>

      <div ref={docsRef} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <CategoriaHeader icona={BookOpen} titol="Documentació de referència" />
        <div className="grid sm:grid-cols-2 gap-3">
          {DOCS.map((item) =>
            item.extern ? (
              <RecursItem key={item.nom} item={item} />
            ) : (
              <Link
                key={item.nom}
                to={item.url}
                className="block p-4 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50/40 transition-colors"
              >
                <div className="font-medium text-gray-900">{item.nom}</div>
                <p className="text-sm text-gray-600 mt-0.5">{item.desc}</p>
              </Link>
            )
          )}
        </div>
      </div>

      <div ref={moodleRef} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <CategoriaHeader icona={GraduationCap} titol="Material del mòdul al Moodle" />
        <p className="text-gray-700">
          Les presentacions de teoria (Python, arbres de decisió, boscos
          aleatoris, pipelines) i els enunciats dels exercicis es distribueixen
          pel Moodle del centre. No hi ha enllaços de descàrrega en aquesta
          pàgina: aquest material el va preparar una altra docent i no es
          publica aquí.
        </p>
      </div>

      <div
        ref={consellsRef}
        className="bg-amber-50 rounded-xl p-6 shadow-sm border border-amber-200"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-amber-100 text-amber-600 rounded-lg p-2">
            <Lightbulb className="w-5 h-5" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900">
            Consells per treballar
          </h2>
        </div>
        <ul className="space-y-2 text-gray-800 list-disc list-inside">
          <li>
            Els exercicis són curts a posta: el que compta és fer-los tots,
            no que cadascun sigui perfecte.
          </li>
          <li>
            El que no s'entengui, es pregunta el mateix dia. Deixar-ho
            passar només fa que s'acumuli.
          </li>
          <li>
            Us podeu ajudar entre vosaltres, però l'aprenentatge és
            individual: cadascú ha de sortir sabent fer l'exercici.
          </li>
          <li>
            La IA es pot fer servir per entendre coses, però si us resol els
            exercicis no aprendreu a programar, i es nota a les proves.
          </li>
        </ul>
      </div>
    </div>
  );
}
