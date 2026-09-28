import {
  FlaskConical,
  ListChecks,
  AlertTriangle,
  Download,
  Save,
  MousePointerClick,
  CheckCircle2,
  Wrench,
  Key,
  Github,
  ExternalLink,
} from "lucide-react";

const COLAB_BASE =
  "https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/02_practica/";

const CAIXA_EINES = "EX_00_caixa_eines.ipynb";

const eines = [
  "train_test_split",
  "StandardScaler",
  "SimpleImputer",
  "OneHotEncoder",
  "drop_duplicates",
  "Pipeline",
  "ColumnTransformer",
  "confusion_matrix",
  "classification_report",
  "precision_score",
  "recall_score",
  "DummyClassifier",
  "SelectKBest",
  "cross_val_score",
  "GridSearchCV",
  "meshgrid + contourf",
];

const exercicis = [
  {
    fitxer: "EX_01_wine.ipynb",
    titol: "El dataset Wine",
    dades: "178 files × 13 columnes, 3 classes",
    descripcio:
      "El pas natural després d'Iris. Amb 13 columnes ja no es pot mirar tot en un gràfic, i les columnes van en escales molt diferents: una va per centenars i una altra no arriba a 1. Hi posaràs a prova què li fa això a un model que mesura distàncies, i què canvia quan les escales s'igualen.",
  },
  {
    fitxer: "EX_02_cancer.ipynb",
    titol: "Diagnòstic de càncer de mama",
    dades: "569 × 30, binari",
    descripcio:
      "Un problema binari amb les dues classes desiguals, i on els dos errors possibles no costen el mateix. Hi posaràs a prova si l'exactitud és una mesura suficient, què hi afegeix la matriu de confusió, i com queda el teu model comparat amb un que respongui sempre la classe majoritària.",
  },
  {
    fitxer: "EX_03_digits.ipynb",
    titol: "Xifres escrites a mà",
    dades: "1797 imatges de 8×8, 10 classes",
    descripcio:
      "Una imatge també és una taula: cada píxel és una columna. Hi posaràs a prova si els models que ja coneixes serveixen igual quan les columnes són píxels i les classes són deu.",
  },
  {
    fitxer: "EX_04_fronteres.ipynb",
    titol: "La forma de cada model",
    dades: "Dades fabricades, 2 columnes",
    descripcio:
      "Amb només dues columnes, la frontera de decisió es pot dibuixar. Hi posaràs a prova quina forma li surt a cadascun dels cinc models sobre les mateixes dades, i què d'aquella forma ve del model i no de les dades.",
  },
  {
    fitxer: "EX_05_dades_brutes.ipynb",
    titol: "Quan les dades no vénen netes",
    dades: "Wine embrutat a posta",
    descripcio:
      "Valors que falten, columnes de text i files duplicades. Hi posaràs a prova l'ordre de les operacions: què passa segons en quin moment del procés es netegen i s'escalen les dades.",
  },
];

export default function Practica() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Pràctica</h1>
        <p className="mt-2 text-lg text-gray-600">
          Cinc quaderns d'exercicis per fer després de la teoria dels cinc models, i una caixa
          d'eines per tenir oberta al costat mentre els fas.
        </p>
      </div>

      <section
        id="caixa-eines"
        className="bg-white rounded-xl p-6 shadow-sm border-2 border-indigo-300"
      >
        <div className="flex items-center gap-3 mb-4">
          <Wrench className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            La caixa d'eines: tingues-la oberta al costat
          </h2>
        </div>
        <div className="flex flex-col lg:flex-row lg:items-start gap-5">
          <div className="min-w-0 flex-1 space-y-3">
            <p className="text-gray-700">
              Els exercicis demanen eines que a classe no s'expliquen una per una. Aquest quadern les
              té totes: <strong>què fa cada eina, què li dones, què et torna</strong>, un exemple
              mínim sobre una taula de joguina de sis files, i el parany de cadascuna.
            </p>
            <p className="text-gray-700">
              No has d'endevinar quina funció toca: <strong>l'enunciat et diu quina eina fer
              servir</strong>. El que no et diu és quin resultat surt. La feina és executar-les, i
              veure com s'hi arriba.
            </p>
            <p className="text-gray-700">
              És una referència per consultar, no un exercici.{" "}
              <strong>Aquí no hi ha cel·les buides i totes funcionen</strong>, o sigui que aquest sí
              que el pots executar sencer: l'avís de no clicar «Executa-ho tot» val per als altres
              cinc, no per aquest.
            </p>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {eines.map((e) => (
                <code
                  key={e}
                  className="text-xs bg-indigo-50 border border-indigo-200 text-indigo-800 px-1.5 py-0.5 rounded"
                >
                  {e}
                </code>
              ))}
            </div>
          </div>
          <div className="flex-shrink-0 flex flex-col gap-2 lg:w-52">
            <a
              href={`${COLAB_BASE}${CAIXA_EINES}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 whitespace-nowrap"
            >
              Obre a Colab
              <ExternalLink className="w-4 h-4" />
            </a>
            <a
              href={`${import.meta.env.BASE_URL}quaderns/${CAIXA_EINES}`}
              download={CAIXA_EINES}
              className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50 whitespace-nowrap"
            >
              Baixa el .ipynb
              <Download className="w-4 h-4" />
            </a>
          </div>
        </div>
      </section>

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
        <div className="mt-4 bg-gray-50 border-l-4 border-indigo-400 rounded-r-lg p-4">
          <p className="text-gray-800">
            La comprovació de cada exercici et diu si <strong>el procediment</strong> és correcte, no
            quin número t'ha de sortir. El número és la teva feina.
          </p>
        </div>
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
              Cada exercici acaba amb una <strong>comprovació del procediment</strong>: et diu si
              has fet els passos com toca. El resultat no te'l dona ningú, és el que has de trobar
              tu.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <Wrench className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              Si una eina que demana l'exercici no la coneixes, no t'encallis: és a{" "}
              <strong>la caixa d'eines</strong>, aquí a dalt.
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
        <div className="space-y-3 text-gray-700 text-sm">
          <p>Existeixen, i les reparteix el professor quan toca.</p>
          <p>
            Per comprovar-te <strong>no et fa falta la solució</strong>. L'enunciat et diu quines
            eines fer servir, la caixa d'eines t'explica cadascuna, i la comprovació et diu si el
            procediment és correcte. Amb això pots saber si vas bé sense que ningú t'ensenyi el
            resultat abans d'hora, que és el que et deixaria sense l'exercici.
          </p>
          <button
            type="button"
            onClick={() => {
              const el = document.getElementById("caixa-eines");
              if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
            }}
            className="inline-flex items-center gap-1.5 font-medium text-indigo-600 hover:text-indigo-800"
          >
            <Wrench className="w-4 h-4" />
            Anar a la caixa d'eines
          </button>
        </div>
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
