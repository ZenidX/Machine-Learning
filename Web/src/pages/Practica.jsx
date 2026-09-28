import {
  FlaskConical,
  ListChecks,
  AlertTriangle,
  Download,
  Save,
  MousePointerClick,
  CheckCircle2,
  Key,
  Github,
  ExternalLink,
} from "lucide-react";

const COLAB_BASE =
  "https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/02_practica/";

const exercicis = [
  {
    fitxer: "EX_01_wine.ipynb",
    titol: "El dataset Wine",
    dades: "178 files × 13 columnes, 3 classes",
    descripcio:
      "El pas natural després d'Iris. Amb 13 columnes ja no es pot mirar tot en un gràfic, i com que una columna va per centenars i una altra no arriba a 1, el parany de les escales es mesura: k-NN passa del 72,2 % al 94,4 % només escalant.",
  },
  {
    fitxer: "EX_02_cancer.ipynb",
    titol: "Diagnòstic de càncer de mama",
    dades: "569 × 30, binari",
    descripcio:
      "La precisió tota sola no serveix. Un model encerta el 94,2 % i deixa passar 3 tumors malignes; un model que digui sempre \"benigne\" encerta el 63,2 % i els deixa passar tots.",
  },
  {
    fitxer: "EX_03_digits.ipynb",
    titol: "Xifres escrites a mà",
    dades: "1797 imatges de 8×8, 10 classes",
    descripcio:
      "Una imatge també és una taula: cada columna és un píxel. Els mateixos cinc models funcionen igual.",
  },
  {
    fitxer: "EX_04_fronteres.ipynb",
    titol: "La forma de cada model",
    dades: "Dades fabricades, 2 columnes",
    descripcio:
      "Amb dues columnes es pot dibuixar la frontera de cada model: la logística sempre traça una recta, l'arbre fa escales, l'SVM fa corbes.",
  },
  {
    fitxer: "EX_05_dades_brutes.ipynb",
    titol: "Quan les dades no vénen netes",
    dades: "Wine embrutat a posta",
    descripcio:
      "Valors que falten, columnes de text, duplicats. I per què l'ordre de les operacions importa.",
  },
];

export default function Practica() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Pràctica</h1>
        <p className="mt-2 text-lg text-gray-600">
          Cinc quaderns d'exercicis per fer després de la teoria dels cinc models.
        </p>
      </div>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <FlaskConical className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Els cinc exercicis</h2>
        </div>
        <p className="text-gray-700">
          Cada quadern fa servir un conjunt de dades diferent a posta: cadascun ensenya una
          cosa que el dataset Iris, amb el qual s'ha explicat la teoria, no pot ensenyar. Tot
          funciona a <strong>Google Colab</strong>, sense instal·lar res.
        </p>
      </section>

      <section className="bg-amber-50 border border-amber-200 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-semibold text-amber-900">Abans de començar</h2>
        </div>
        <ul className="space-y-3 text-amber-900 text-sm">
          <li className="flex items-start gap-2">
            <Save className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              Fes <strong>"Fitxer → Desa una còpia a Drive"</strong> nada més obrir el
              quadern, o perdràs la feina en tancar.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <MousePointerClick className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              <strong>No cliquis "Executa-ho tot"</strong>: les cel·les de codi són buides a
              posta i les has d'anar omplint una per una. Si ho executes tot de cop veuràs
              errors de variables que encara no existeixen, i és normal.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              Cada exercici acaba amb una línia <strong>"com saps que ho has fet bé"</strong>,
              amb el resultat aproximat que ha de sortir. Fes-la servir per comprovar-te.
            </span>
          </li>
        </ul>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ListChecks className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Els quaderns</h2>
        </div>
        <div className="space-y-4">
          {exercicis.map((ex, i) => (
            <div
              key={ex.fitxer}
              className="border border-gray-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
            >
              <div>
                <p className="text-xs font-medium text-indigo-600 mb-1">
                  Exercici {i + 1}
                </p>
                <h3 className="font-medium text-gray-900 mb-1">{ex.titol}</h3>
                <p className="text-sm text-gray-500 mb-2">{ex.dades}</p>
                <p className="text-sm text-gray-600">{ex.descripcio}</p>
              </div>
              <div className="flex-shrink-0 flex flex-col gap-2">
                <a
                  href={`${COLAB_BASE}${ex.fitxer}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 whitespace-nowrap"
                >
                  Obre a Colab
                  <ExternalLink className="w-4 h-4" />
                </a>
                <a
                  href={`${import.meta.env.BASE_URL}quaderns/${ex.fitxer}`}
                  download={ex.fitxer}
                  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50 whitespace-nowrap"
                >
                  Baixa el .ipynb
                  <Download className="w-4 h-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Download className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Dues maneres de treballar-hi</h2>
        </div>
        <div className="grid md:grid-cols-2 gap-5">
          <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
            <h3 className="font-semibold text-indigo-900 mb-1">Obre a Colab</h3>
            <p className="text-sm text-gray-700">
              El quadern s'obre directament al navegador. Recorda desar-ne una còpia al teu
              Drive de seguida, o perdràs la feina en tancar la pestanya.
            </p>
          </div>
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-1">Baixa el fitxer</h3>
            <p className="text-sm text-gray-700">
              Et descarregues el <code className="bg-white px-1.5 py-0.5 rounded text-xs">.ipynb</code> i
              te'l emportes on vulguis. Per obrir-lo al teu Colab: entra a{" "}
              <a
                href="https://colab.research.google.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-indigo-600 hover:text-indigo-800 underline"
              >
                colab.research.google.com
              </a>
              , tria <strong>Puja</strong> i selecciona el fitxer. També funciona amb Jupyter
              al teu ordinador.
            </p>
          </div>
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Key className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">Solucions</h2>
        </div>
        <p className="text-gray-700 text-sm">
          Existeixen, estan a la carpeta <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">solucions/</code> del
          repositori, i les reparteix el professor quan toca.
        </p>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Github className="w-6 h-6 text-gray-700" />
          <h2 className="text-xl font-semibold text-gray-900">Repositori</h2>
        </div>
        <a
          href="https://github.com/ZenidX/Machine-Learning"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-medium text-sm"
        >
          github.com/ZenidX/Machine-Learning
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </section>
    </div>
  );
}
