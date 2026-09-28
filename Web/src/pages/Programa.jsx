import {
  GraduationCap,
  CalendarDays,
  Layers,
  Route,
  Table2,
  Sigma,
  ClipboardCheck,
  Trophy,
  AlertTriangle,
  Clock,
  CheckCircle2,
  ArrowRight,
} from "lucide-react";
import { Link } from "react-router-dom";
import MermaidDiagram from "../components/MermaidDiagram";

const recorregutChart = `flowchart LR
    B0["Bloc 0<br/>Arrencada i Python"] --> B1["Bloc 1<br/>Fonaments de dades<br/>i algebra"]
    B1 --> B2["Bloc 2<br/>Supervisat i la<br/>matematica de sota"]
    B2 --> B3["Bloc 3<br/>Optimitzacio, dades<br/>reals i no supervisat"]
    B3 --> B4["Bloc 4<br/>Xarxes neuronals"]
    B4 --> B5["Bloc 5<br/>Reinforcement Learning<br/>i concurs"]
    MA(("Sis quaderns de<br/>matematiques")) -.-> B1
    MA -.-> B2
    MA -.-> B3
    style MA fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#4c1d95`;

const dadesFermes = [
  { etiqueta: "Hores", valor: "66 h" },
  { etiqueta: "Per setmana", valor: "4 h" },
  { etiqueta: "Sessions", valor: "33 de 2 h" },
  { etiqueta: "Dies", valor: "dilluns i dimarts" },
  { etiqueta: "Del", valor: "14 set 2026" },
  { etiqueta: "Al", valor: "26 gen 2027" },
];

const blocs = [
  {
    num: "0",
    titol: "Arrencada i Python",
    rang: "S01-S05",
    hores: "10 h",
    del: "14 set",
    al: "28 set",
  },
  {
    num: "1",
    titol: "Fonaments de dades i àlgebra",
    rang: "S06-S12",
    hores: "14 h",
    del: "29 set",
    al: "26 oct",
    actual: true,
  },
  {
    num: "2",
    titol: "Supervisat i la matemàtica que hi ha a sota",
    rang: "S13-S21",
    hores: "18 h",
    del: "27 oct",
    al: "24 nov",
  },
  {
    num: "3",
    titol: "Optimització, dades reals i no supervisat",
    rang: "S22-S25",
    hores: "8 h",
    del: "30 nov",
    al: "14 des",
  },
  {
    num: "4",
    titol: "Xarxes neuronals",
    rang: "S26-S28",
    hores: "6 h",
    del: "15 des",
    al: "11 gen",
  },
  {
    num: "5",
    titol: "Reinforcement Learning i concurs",
    rang: "S29-S33",
    hores: "10 h",
    del: "12 gen",
    al: "26 gen",
  },
];

const sessions = [
  {
    bloc: "Bloc 0 · Arrencada i Python",
    id: "bloc-0",
    nota: "Ja fet.",
    llista: [
      { s: "S01", dia: "dl 14 set", text: "Presentació del mòdul" },
      { s: "S02", dia: "dt 15 set", text: "Python: tipus, variables, cadenes" },
      { s: "S03", dia: "dl 21 set", text: "Python: condicionals" },
      {
        s: "S04",
        dia: "dt 22 set",
        text: "Els models de ML supervisat, conceptualment, amb Iris",
      },
      { s: "S05", dia: "dl 28 set", text: "Primer contacte amb conjunts de dades" },
    ],
  },
  {
    bloc: "Bloc 1 · Fonaments de dades i àlgebra",
    id: "bloc-1",
    nota: "És on som. Sense NumPy i Pandas no es pot manejar una taula de dades, i tot el que ve després es fa a cegues.",
    llista: [
      {
        s: "S06",
        dia: "dt 29 set",
        text: "NumPy 1: per què no llistes, l'array, indexació i llesques",
        material: "FO_01_numpy.ipynb",
      },
      {
        s: "S07",
        dia: "dl 5 oct",
        text: "NumPy 2: operacions, màscares booleanes, agregacions i eixos",
        material: "FO_01_numpy.ipynb",
      },
      {
        s: "S08",
        dia: "dt 6 oct",
        text: "Àlgebra lineal: norma, producte escalar, projecció, i que un model entrenat és un vector i una multiplicació",
        material: "MA_01_algebra_lineal.ipynb",
        mates: true,
      },
      {
        s: "S09",
        dia: "dt 13 oct",
        text: "Pandas 1: Series i DataFrame, carregar un CSV, seleccionar amb loc i iloc",
        material: "FO_02_pandas.ipynb",
      },
      {
        s: "S10",
        dia: "dl 19 oct",
        text: "Pandas 2: nuls, groupby, gràfics ràpids, i del DataFrame a X i y",
        material: "FO_02_pandas.ipynb",
      },
      {
        s: "S11",
        dia: "dt 20 oct",
        text: "Diccionaris, funcions i comprensions de llista",
      },
      {
        s: "S12",
        dia: "dl 26 oct",
        text: "Prova pràctica 1 i tancament del bloc",
        prova: true,
      },
    ],
  },
  {
    bloc: "Bloc 2 · Supervisat i la matemàtica que hi ha a sota",
    id: "bloc-2",
    nota: "Cada model s'explica, es fa córrer, i després es baixa fins a la fórmula que el fa funcionar.",
    llista: [
      {
        s: "S13",
        dia: "dt 27 oct",
        text: "Entrenament i test, i per què se separen. Primer model complet",
        material: "ML_00_demo_iris.ipynb",
      },
      {
        s: "S14",
        dia: "dl 2 nov",
        text: "k veïns i la distància. El parany de les escales",
        material: "ML_01_knn.ipynb",
        casa: "EX_01_wine.ipynb",
      },
      {
        s: "S15",
        dia: "dt 3 nov",
        text: "Arbres de decisió: la impuresa i la tria del tall",
        material: "ML_02_arbres.ipynb",
      },
      {
        s: "S16",
        dia: "dl 9 nov",
        text: "Entropia i informació: per què Gini, el guany d'informació, i que la log-loss i l'entropia creuada són el mateix número",
        material: "MA_04_entropia_informacio.ipynb",
        mates: true,
      },
      {
        s: "S17",
        dia: "dt 10 nov",
        text: "Boscos aleatoris i mètriques: la precisió no serveix tota sola",
        material: "ML_03_boscos.ipynb",
        casa: "EX_02_cancer.ipynb",
      },
      {
        s: "S18",
        dia: "dl 16 nov",
        text: "Regressió logística: la frontera, la sigmoide, i els pesos trobats per força bruta",
        material: "ML_04_regressio_logistica.ipynb",
      },
      {
        s: "S19",
        dia: "dt 17 nov",
        text: "Descens de gradient: què és una derivada, la derivada de la log-loss, i entrenar la logística amb un bucle propi",
        material: "MA_02_descens_gradient.ipynb",
        mates: true,
      },
      {
        s: "S20",
        dia: "dl 23 nov",
        text: "Probabilitat i versemblança: Bayes, d'on surt la log-loss, i Naive Bayes implementat de zero",
        material: "MA_03_probabilitat_versemblanca.ipynb",
        mates: true,
      },
      {
        s: "S21",
        dia: "dt 24 nov",
        text: "SVM: el marge i el kernel. Prova pràctica 2",
        material: "ML_05_svm.ipynb",
        casa: "EX_04_fronteres.ipynb",
        prova: true,
      },
    ],
  },
  {
    bloc: "Bloc 3 · Optimització, dades reals i no supervisat",
    id: "bloc-3",
    nota: null,
    llista: [
      {
        s: "S22",
        dia: "dl 30 nov",
        text: "Optimització amb restriccions: Lagrange, per què l'SVM depèn de pocs punts, i el kernel demostrat",
        material: "MA_05_marge_optimitzacio.ipynb",
        mates: true,
      },
      {
        s: "S23",
        dia: "dt 1 des",
        text: "Dades brutes i pipelines: nuls, categòriques, i la fuita d'informació",
        material: "EX_05_dades_brutes.ipynb",
      },
      {
        s: "S24",
        dia: "dl 7 des",
        text: "PCA i vectors propis: la maledicció de la dimensionalitat, i reduir dimensions sense inventar-se res",
        material: "MA_06_pca_vectors_propis.ipynb",
        mates: true,
      },
      {
        s: "S25",
        dia: "dl 14 des",
        text: "k-means i les imatges com a taula. Prova pràctica 3",
        material: "EX_03_digits.ipynb",
        prova: true,
      },
    ],
  },
  {
    bloc: "Bloc 4 · Xarxes neuronals",
    id: "bloc-4",
    nota: "Aquest bloc va comprimit a posta: qui hagi entès la S19 ja té feta la part difícil.",
    llista: [
      {
        s: "S26",
        dia: "dt 15 des",
        text: "Què és una xarxa neuronal, i que ja en sabeu el mecanisme: és el descens de gradient de la S19",
      },
      { s: "S27", dia: "dl 21 des", text: "PyTorch: tensors, arquitectures i entrenament" },
      { s: "S28", dia: "dl 11 gen", text: "De la xarxa a l'agent: el pont cap a Reinforcement Learning" },
    ],
  },
  {
    bloc: "Bloc 5 · Reinforcement Learning i concurs",
    id: "bloc-5",
    nota: null,
    llista: [
      { s: "S29", dia: "dt 12 gen", text: "Fonaments de RL: l'agent, l'entorn, la recompensa" },
      { s: "S30", dia: "dl 18 gen", text: "DQN i Gymnasium" },
      { s: "S31", dia: "dt 19 gen", text: "Entrenament lliure: cadascú entrena el seu agent" },
      { s: "S32", dia: "dl 25 gen", text: "Entrenament lliure i ajust. Lliurament dels agents" },
      { s: "S33", dia: "dt 26 gen", text: "El concurs", concurs: true },
    ],
  },
];

const SESSIONS_FETES = ["S01", "S02", "S03", "S04", "S05"];
const SESSIO_PROPERA = "S06";

const indexInterno = [
  { id: "recorregut", label: "El recorregut" },
  { id: "blocs", label: "Els sis blocs" },
  { id: "sessions", label: "Sessió a sessió" },
  { id: "festius", label: "Festius i vacances" },
  { id: "avaluacio", label: "Avaluació" },
  { id: "concurs", label: "El concurs final" },
];

function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function estatSessio(s) {
  if (SESSIONS_FETES.includes(s)) return "feta";
  if (s === SESSIO_PROPERA) return "propera";
  return "pendent";
}

export default function Programa() {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <GraduationCap className="w-8 h-8 text-primary-600" />
          <h1 className="text-3xl font-bold text-gray-900">Programa del curs</h1>
        </div>
        <p className="text-gray-600 max-w-3xl">
          Mòdul MPOML — Aprenentatge automàtic, optativa de 2n curs dels cicles de grau superior
          DAM i DAW. Resultat d'aprenentatge únic:{" "}
          <strong>Crea aplicacions fent ús de models d'aprenentatge automàtic.</strong>
        </p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <CalendarDays className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">El calendari, en sis dades</h2>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {dadesFermes.map((d) => (
            <div key={d.etiqueta} className="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p className="text-xs uppercase tracking-wide text-gray-500">{d.etiqueta}</p>
              <p className="font-semibold text-gray-900">{d.valor}</p>
            </div>
          ))}
        </div>
        <p className="text-sm text-gray-600 mt-4">
          Dues sessions de 2 h per setmana, dilluns i dimarts. Les 33 sessions ja tenen descomptats
          els festius que cauen en dia de classe i les vacances de Nadal.
        </p>
        <div className="flex flex-wrap gap-2 mt-4">
          {indexInterno.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => scrollToId(item.id)}
              className="text-sm px-3 py-1.5 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-50"
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      <div id="recorregut" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Route className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">El recorregut</h2>
        </div>
        <p className="text-gray-600 mb-4">
          De Python a un agent que aprèn a jugar sol, passant per NumPy i Pandas, els models
          supervisats i les xarxes neuronals. Els sis quaderns de matemàtiques no són un bloc
          apart: ocupen sessions dins dels blocs 1, 2 i 3, on toca la teoria de cada model.
        </p>
        <MermaidDiagram chart={recorregutChart} />
      </div>

      <div id="blocs" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Layers className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Els sis blocs</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="p-3 border border-gray-200 font-semibold text-gray-900">Bloc</th>
                <th className="p-3 border border-gray-200 font-semibold text-gray-900">Sessions</th>
                <th className="p-3 border border-gray-200 font-semibold text-gray-900">Hores</th>
                <th className="p-3 border border-gray-200 font-semibold text-gray-900">Del</th>
                <th className="p-3 border border-gray-200 font-semibold text-gray-900">Al</th>
              </tr>
            </thead>
            <tbody>
              {blocs.map((b) => (
                <tr key={b.num} className={b.actual ? "bg-primary-50" : undefined}>
                  <td className="p-3 border border-gray-200 text-gray-900">
                    <span className="font-semibold">{b.num}</span> · {b.titol}
                    {b.actual && (
                      <span className="ml-2 text-xs font-semibold text-primary-700">
                        bloc en curs
                      </span>
                    )}
                  </td>
                  <td className="p-3 border border-gray-200 text-gray-700 whitespace-nowrap">
                    {b.rang}
                  </td>
                  <td className="p-3 border border-gray-200 text-gray-700 whitespace-nowrap">
                    {b.hores}
                  </td>
                  <td className="p-3 border border-gray-200 text-gray-700 whitespace-nowrap">
                    {b.del}
                  </td>
                  <td className="p-3 border border-gray-200 text-gray-700 whitespace-nowrap">
                    {b.al}
                  </td>
                </tr>
              ))}
              <tr className="bg-gray-50 font-semibold">
                <td className="p-3 border border-gray-200 text-gray-900">Total</td>
                <td className="p-3 border border-gray-200 text-gray-900">33 sessions</td>
                <td className="p-3 border border-gray-200 text-gray-900">66 h</td>
                <td className="p-3 border border-gray-200 text-gray-900">14 set</td>
                <td className="p-3 border border-gray-200 text-gray-900">26 gen</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className="mt-4 bg-emerald-50 border border-emerald-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <Table2 className="w-5 h-5 text-emerald-700" />
            <p className="font-semibold text-emerald-900">Els quaderns del bloc en curs</p>
          </div>
          <p className="text-sm text-emerald-900">
            NumPy i Pandas, a les sessions S06, S07, S09 i S10. Es poden obrir a Colab o baixar des
            de la pàgina de fonaments.
          </p>
          <Link
            to="/fonaments"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-emerald-800 hover:text-emerald-900 mt-3"
          >
            Veure els quaderns de fonaments
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="mt-4 bg-violet-50 border border-violet-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <Sigma className="w-5 h-5 text-violet-700" />
            <p className="font-semibold text-violet-900">Les sessions de matemàtiques</p>
          </div>
          <p className="text-sm text-violet-900">
            S08, S16, S19, S20, S22 i S24. Són la teoria del model corresponent portada fins al
            fons: cada fórmula seguida de la línia de NumPy que la calcula, i cada implementació
            comparada amb scikit-learn.
          </p>
          <Link
            to="/matematiques"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-violet-800 hover:text-violet-900 mt-3"
          >
            Veure el bloc de matemàtiques
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <div id="sessions" className="space-y-4">
        <div className="flex items-center gap-3">
          <CalendarDays className="w-6 h-6 text-primary-600" />
          <h2 className="text-2xl font-bold text-gray-900">Sessió a sessió</h2>
        </div>

        <div className="flex flex-wrap gap-3 text-xs">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-emerald-200 bg-emerald-50 text-emerald-700 font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" /> Feta
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-primary-300 bg-primary-50 text-primary-700 font-medium">
            <Clock className="w-3.5 h-3.5" /> Propera sessió
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-violet-200 bg-violet-50 text-violet-700 font-medium">
            <Sigma className="w-3.5 h-3.5" /> Sessió de matemàtiques
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-gray-200 bg-white text-gray-600 font-medium">
            <ClipboardCheck className="w-3.5 h-3.5" /> Prova pràctica
          </span>
        </div>

        {sessions.map((grup) => (
          <div
            key={grup.id}
            id={grup.id}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
          >
            <h3 className="text-lg font-bold text-gray-900">{grup.bloc}</h3>
            {grup.nota && <p className="text-sm text-gray-600 mt-1">{grup.nota}</p>}

            <div className="mt-4 space-y-2">
              {grup.llista.map((ses) => {
                const estat = estatSessio(ses.s);
                const base = ses.mates
                  ? "border-violet-200 bg-violet-50"
                  : estat === "propera"
                    ? "border-primary-300 bg-primary-50"
                    : estat === "feta"
                      ? "border-emerald-100 bg-emerald-50/60"
                      : "border-gray-200 bg-white";
                return (
                  <div
                    key={ses.s}
                    className={`border rounded-lg p-4 flex flex-col sm:flex-row sm:items-start gap-3 ${base}`}
                  >
                    <div className="flex items-center gap-3 sm:w-40 flex-shrink-0">
                      <span
                        className={`inline-flex items-center justify-center w-11 h-8 rounded-md text-sm font-bold ${
                          ses.mates
                            ? "bg-violet-600 text-white"
                            : estat === "feta"
                              ? "bg-emerald-600 text-white"
                              : estat === "propera"
                                ? "bg-primary-600 text-white"
                                : "bg-gray-200 text-gray-700"
                        }`}
                      >
                        {ses.s}
                      </span>
                      <span className="text-sm text-gray-600 whitespace-nowrap">{ses.dia}</span>
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="text-gray-800 text-sm">{ses.text}</p>
                      <div className="flex flex-wrap items-center gap-2 mt-2">
                        {estat === "feta" && (
                          <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700">
                            <CheckCircle2 className="w-3.5 h-3.5" /> feta
                          </span>
                        )}
                        {estat === "propera" && (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary-700">
                            <Clock className="w-3.5 h-3.5" /> propera sessió
                          </span>
                        )}
                        {ses.mates && (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-violet-700">
                            <Sigma className="w-3.5 h-3.5" /> matemàtiques
                          </span>
                        )}
                        {ses.prova && (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-gray-700">
                            <ClipboardCheck className="w-3.5 h-3.5" /> prova pràctica
                          </span>
                        )}
                        {ses.concurs && (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-amber-700">
                            <Trophy className="w-3.5 h-3.5" /> concurs
                          </span>
                        )}
                        {ses.material && (
                          <code className="text-xs bg-white/80 border border-gray-200 text-gray-600 px-1.5 py-0.5 rounded">
                            {ses.material}
                          </code>
                        )}
                        {ses.casa && (
                          <span className="text-xs text-gray-600">
                            a casa:{" "}
                            <code className="bg-white/80 border border-gray-200 px-1.5 py-0.5 rounded">
                              {ses.casa}
                            </code>
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div id="festius" className="bg-white rounded-xl p-6 shadow-sm border-2 border-amber-300">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-bold text-gray-900">Festius i vacances</h2>
        </div>
        <ul className="space-y-3 text-sm text-gray-800">
          <li className="flex gap-2">
            <span className="font-semibold text-amber-700 whitespace-nowrap">12 d'octubre</span>
            <span>
              cau en dilluns de classe. Aquella setmana només hi ha la sessió del dimarts, la S09.
            </span>
          </li>
          <li className="flex gap-2">
            <span className="font-semibold text-amber-700 whitespace-nowrap">8 de desembre</span>
            <span>
              cau en dimarts de classe. Aquella setmana només hi ha la sessió del dilluns, la S24.
            </span>
          </li>
          <li className="flex gap-2">
            <span className="font-semibold text-amber-700 whitespace-nowrap">Nadal</span>
            <span>
              del 22 de desembre al 7 de gener no hi ha classe. El curs es reprèn amb la S28, l'11
              de gener.
            </span>
          </li>
        </ul>
      </div>

      <div id="avaluacio" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ClipboardCheck className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Com s'avalua</h2>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-5">
          <p className="text-sm text-amber-900">
            <strong>Els pesos percentuals encara no estan confirmats.</strong> Els instruments sí:
            són els que hi ha aquí sota. Els percentatges es confirmaran i s'anunciaran quan
            estiguin decidits; fins llavors aquesta pàgina no en dona cap.
          </p>
        </div>

        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-1">Proves pràctiques</h3>
            <p className="text-sm text-gray-700">
              Amb ordinador, i semblants als exercicis de classe. Una per bloc:{" "}
              <strong>S12</strong> (26 d'octubre), <strong>S21</strong> (24 de novembre) i{" "}
              <strong>S25</strong> (14 de desembre).
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-1">Activitats dels quaderns</h3>
            <p className="text-sm text-gray-700">
              Les cel·les buides dels quaderns de pràctica. Amb aquesta programació{" "}
              <strong>són feina de casa i no són opcionals</strong>, perquè el temps de classe
              se'l menja la matemàtica. Es lliuren i es qualifiquen fet o no fet.
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-1">Projecte final de Reinforcement Learning</h3>
            <p className="text-sm text-gray-700">
              L'agent del concurs de la S33: l'agent entrenat, que funcioni, i la justificació de
              les decisions que s'hi han pres.
            </p>
          </div>
        </div>

        <div className="mt-5 bg-violet-50 border border-violet-200 rounded-lg p-4">
          <p className="text-sm text-violet-900">
            <strong>El bloc de matemàtiques no s'avalua com a deducció.</strong> No es demana
            derivar el gradient de la log-loss en un examen. Sí que es demana implementar una
            funció de pèrdua i comprovar-la, verificar un gradient per diferències finites, o
            explicar per què un model dona el que dona mirant-ne els pesos.
          </p>
        </div>
      </div>

      <div id="concurs" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Trophy className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-bold text-gray-900">El concurs de la sessió 33</h2>
        </div>
        <div className="space-y-4 text-gray-700">
          <p>
            L'últim dia del curs, el <strong>26 de gener</strong>, els agents que heu entrenat
            competeixen en entorns virtuals. Les sessions S31 i S32 són d'entrenament lliure: cadascú
            ajusta el seu agent i el lliura abans del concurs.
          </p>
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-sm text-amber-900">
              <strong>No es puntua per posició al marcador.</strong> Es puntua l'agent lliurat, que
              funcioni, i la justificació de les decisions. Si es puntués la posició, qui tingui
              l'ordinador més potent tindria avantatge. Guanyar el concurs és el premi, no la nota.
            </p>
          </div>
          <Link
            to="/deep-rl"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 hover:text-primary-800"
          >
            Veure el bloc de xarxes i Reinforcement Learning
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
