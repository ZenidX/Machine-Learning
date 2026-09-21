import {
  AlertTriangle,
  Route,
  Layers,
  CheckCircle2,
  CalendarDays,
  GraduationCap,
  PackageCheck,
  Hammer,
  ArrowRight,
  ChevronRight,
} from "lucide-react";
import { Link } from "react-router-dom";
import MermaidDiagram from "../components/MermaidDiagram";

const recorregutChart = `flowchart LR
    subgraph curs["Recorregut del curs"]
        direction LR
        P["Repas de Python"] --> AD["Analisi de dades"]
        AD --> ML["Machine Learning classic<br/>(supervisat + no supervisat)"]
        ML --> XN["Xarxes neuronals"]
        XN --> RL["Reinforcement Learning"]
    end
    ET(("Etica i<br/>responsabilitat")) -.-> P
    ET -.-> AD
    ET -.-> ML
    ET -.-> XN
    ET -.-> RL
    style ET fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#78350f
    style curs fill:#f8fafc,stroke:#cbd5e1`;

const blocs = [
  {
    id: "bloc-0",
    num: "0",
    titol: "Punt de partida",
    sessions: "1 sessió",
    periode: "setembre",
    contingut: [
      "Que és i que no és l'aprenentatge automàtic, per a què s'usa i on falla.",
      "Recorregut pel curs i per com s'avalua.",
      "Teachable Machine en directe: entrenar un classificador d'imatges amb la webcam sense escriure una línia de codi, i parlar de biaix ensenyant-lo en calent.",
    ],
    estat: "preparar",
    estatText: "Guió de sessió per preparar; el material de Teachable Machine no cal construir-lo, es fa en directe.",
    link: null,
  },
  {
    id: "bloc-1",
    num: "1",
    titol: "Python per treballar amb dades",
    sessions: "7 sessions",
    periode: "setembre a novembre",
    contingut: [
      "Tipus i variables, cadenes, condicionals, llistes i tuples, bucles, diccionaris, funcions, comprensions de llista.",
      "Lliuraments curts i freqüents (intercanvi de variables, inversió de cadena, lletra del DNI, pedra-paper-tisores, nombres únics ordenats).",
    ],
    proves: ["Prova escrita 1: conceptes bàsics de Python.", "Prova pràctica 1: dos o tres exercicis de la mateixa família que els de classe."],
    estat: "fet",
    estatText: "Ja fet: materials i lliuraments del Moodle del curs passat, i funcionaven.",
    link: { to: "/python", label: "Veure el bloc de Python" },
  },
  {
    id: "bloc-2",
    num: "2",
    titol: "Dades: Pandas i visualització",
    sessions: "5 sessions",
    periode: "novembre a desembre",
    contingut: [
      "Jupyter i Colab, càrrega de dades, consultes i filtres amb Pandas, agrupacions, gràfics.",
      "Com no fer un gràfic: es conserva l'article sobre errades en gràfics del curs passat, bon material de discussió.",
    ],
    proves: ["Prova escrita 2: exploració i visualització de dades.", "Prova pràctica 2: projecte d'anàlisi i representació de dades sobre un dataset donat."],
    estat: "fet",
    estatText: "La prova pràctica del projecte de dades ja existeix i es manté.",
    link: null,
  },
  {
    id: "bloc-3",
    num: "3",
    titol: "Aprenentatge supervisat",
    sessions: "8 sessions",
    periode: "gener a febrer",
    contingut: [
      "Entrenament i test (i per què se separen), regressió lineal, classificació.",
      "Arbres de decisió i boscos aleatoris: els arbres entren primer perquè es poden dibuixar i explicar sense matemàtiques, i d'aquí surt sol el concepte de bosc.",
      "Mètriques (exactitud, precisió, record, matriu de confusió) i sobreajust.",
      "Tot amb scikit-learn.",
    ],
    proves: ["Prova escrita 3: supervisat, mètriques i sobreajust.", "Prova pràctica 3: entrenar i avaluar un model sobre un dataset nou, amb justificació de les decisions."],
    estat: "construir",
    estatText: "Per construir sencer. És la feina grossa: el curs passat es va cobrir amb DataCamp i convé tenir material propi.",
    link: { to: "/machine-learning", label: "Veure el bloc de Machine Learning" },
  },
  {
    id: "bloc-4",
    num: "4",
    titol: "Dades reals i no supervisat",
    sessions: "5 sessions",
    periode: "febrer a març",
    contingut: [
      "Dades nul·les, variables categòriques, escalat, pipelines.",
      "Agrupament amb k-means i reducció de dimensionalitat, a nivell d'idea.",
    ],
    proves: ["Prova escrita 4: preparació de dades i no supervisat."],
    estat: "construir",
    estatText: "Per construir; es pot partir del material de tècniques d'optimització de la programació anterior si encara és accessible.",
    link: null,
  },
  {
    id: "bloc-5",
    num: "5",
    titol: "R al costat de Python",
    sessions: "1-2 sessions",
    periode: "març",
    contingut: [
      "Què és R, d'on ve i per què continua viu en estadística.",
      "La mateixa regressió del bloc 3, feta en R, comparada línia a línia amb la de Python.",
    ],
    proves: ["Sense prova pròpia: entra a la prova escrita 5."],
    estat: "construir",
    estatText: "Per construir: la sessió de comparació amb R.",
    link: null,
  },
  {
    id: "bloc-6",
    num: "6",
    titol: "Xarxes neuronals i Reinforcement Learning",
    sessions: "5-6 sessions",
    periode: "abril a maig",
    contingut: [
      "Idea de xarxa neuronal i per què cal, de la xarxa a l'agent.",
      "Q-learning, DQN, Gymnasium.",
    ],
    proves: ["Prova escrita 5: xarxes, RL i R.", "Prova pràctica 4: agent DQN a un videojoc (pràctica final que ja existeix i funciona)."],
    estat: "fet",
    estatText: "Ja fet i reaprofitable: els quaderns de Deep Learning/01_teoria i tot Reinforcement Learning, amb models entrenats a modelos/.",
    link: { to: "/deep-rl", label: "Veure el bloc de Deep Learning i RL" },
  },
];

const estatStyles = {
  fet: {
    icon: PackageCheck,
    label: "Material ja fet",
    className: "bg-emerald-50 text-emerald-700 border-emerald-200",
  },
  construir: {
    icon: Hammer,
    label: "Per construir",
    className: "bg-amber-50 text-amber-700 border-amber-200",
  },
  preparar: {
    icon: Hammer,
    label: "Per preparar",
    className: "bg-amber-50 text-amber-700 border-amber-200",
  },
};

function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  }
}

export default function Programa() {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <GraduationCap className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Programa del curs</h1>
        </div>
        <p className="text-gray-600 max-w-3xl">
          Mòdul MPOML — Aprenentatge automàtic (Machine Learning), optativa de 2n curs dels cicles
          de grau superior DAM (ICB0) i DAW (ICC0). Resultat d'aprenentatge únic:{" "}
          <strong>Crea aplicacions fent ús de models d'aprenentatge automàtic.</strong>
        </p>
      </div>

      <div id="avis" className="bg-white rounded-xl p-6 shadow-sm border-2 border-amber-300">
        <div className="flex items-start gap-3 mb-4">
          <AlertTriangle className="w-7 h-7 text-amber-600 flex-shrink-0 mt-1" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">
              Dues coses pendents de confirmar
            </h2>
            <p className="text-gray-700 mt-1">
              La fitxa oficial del mòdul i la presentació que es va fer a l'alumnat el curs 25-26
              no coincideixen en les hores ni en l'avaluació. Tot el que hi ha en aquesta pàgina
              és una proposta de treball, no un fet confirmat, fins que això es resolgui.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-amber-50 text-left">
                <th className="p-3 border border-amber-200 font-semibold text-gray-900">
                  &nbsp;
                </th>
                <th className="p-3 border border-amber-200 font-semibold text-gray-900">
                  Fitxa oficial del mòdul
                </th>
                <th className="p-3 border border-amber-200 font-semibold text-gray-900">
                  Presentació al grup 25-26
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="p-3 border border-amber-200 font-medium text-gray-700">Hores</td>
                <td className="p-3 border border-amber-200">66 h, 2 h setmanals</td>
                <td className="p-3 border border-amber-200">99 h, 4 h setmanals (dilluns i divendres)</td>
              </tr>
              <tr>
                <td className="p-3 border border-amber-200 font-medium text-gray-700">
                  Proves escrites
                </td>
                <td className="p-3 border border-amber-200">10 %</td>
                <td className="p-3 border border-amber-200">60 %, en paper, mínim 3</td>
              </tr>
              <tr>
                <td className="p-3 border border-amber-200 font-medium text-gray-700">
                  Activitats i projectes
                </td>
                <td className="p-3 border border-amber-200">10 %</td>
                <td className="p-3 border border-amber-200">40 %, mínim 2 miniprojectes</td>
              </tr>
              <tr>
                <td className="p-3 border border-amber-200 font-medium text-gray-700">
                  Proves pràctiques
                </td>
                <td className="p-3 border border-amber-200">80 %</td>
                <td className="p-3 border border-amber-200">no hi apareixen</td>
              </tr>
              <tr>
                <td className="p-3 border border-amber-200 font-medium text-gray-700">
                  Mínim per fer mitjana
                </td>
                <td className="p-3 border border-amber-200">3 a escrites, 5 a pràctiques</td>
                <td className="p-3 border border-amber-200">4 a cada instrument</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p className="text-sm text-gray-500 mt-4">
          Per això aquesta pàgina no dona percentatges d'avaluació com a definitius, i el
          calendari de blocs es presenta com una proposta a dos escenaris (secció{" "}
          <button
            type="button"
            onClick={() => scrollToId("calendari")}
            className="text-blue-600 underline hover:text-blue-800"
          >
            Dos escenaris de calendari
          </button>
          ) fins que se sàpiga quina versió val.
        </p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Route className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">El recorregut del curs</h2>
        </div>
        <p className="text-gray-600 mb-4">
          De repassar Python a entrenar un agent que juga sol, passant per l'anàlisi de dades, el
          machine learning clàssic i les xarxes neuronals. L'ètica no és un bloc final que ningú
          escolta al maig: hi és present a cada etapa, com un fil que travessa tot el curs.
        </p>
        <MermaidDiagram chart={recorregutChart} />
      </div>

      <div id="blocs" className="space-y-4">
        <div className="flex items-center gap-3">
          <Layers className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">Els blocs (proposta)</h2>
        </div>
        <p className="text-gray-600">
          Trenta-tres sessions de 2 h si el mòdul acaba sent de 66 h. Els períodes són orientatius,
          a ajustar amb el calendari real del grup i amb l'escenari d'hores que finalment valgui.
        </p>

        {blocs.map((bloc) => {
          const estat = estatStyles[bloc.estat];
          const EstatIcon = estat.icon;
          return (
            <div
              key={bloc.id}
              id={bloc.id}
              className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
            >
              <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-3">
                  <span className="flex items-center justify-center w-9 h-9 rounded-full bg-blue-50 text-blue-700 font-bold flex-shrink-0">
                    {bloc.num}
                  </span>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{bloc.titol}</h3>
                    <p className="text-sm text-gray-500">
                      {bloc.sessions} · {bloc.periode}
                    </p>
                  </div>
                </div>
                <span
                  className={`inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full border ${estat.className}`}
                >
                  <EstatIcon className="w-3.5 h-3.5" />
                  {estat.label}
                </span>
              </div>

              <ul className="space-y-1.5 mb-3">
                {bloc.contingut.map((linia, i) => (
                  <li key={i} className="flex gap-2 text-gray-700 text-sm">
                    <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
                    <span>{linia}</span>
                  </li>
                ))}
              </ul>

              {bloc.proves && (
                <div className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3 mb-3">
                  {bloc.proves.map((p, i) => (
                    <div key={i}>{p}</div>
                  ))}
                </div>
              )}

              <p className="text-sm text-gray-500 italic">{bloc.estatText}</p>

              {bloc.link && (
                <Link
                  to={bloc.link.to}
                  className="inline-flex items-center gap-1.5 text-sm text-blue-600 hover:text-blue-800 font-medium mt-3"
                >
                  {bloc.link.label}
                  <ArrowRight className="w-4 h-4" />
                </Link>
              )}
            </div>
          );
        })}
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <CheckCircle2 className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">Decisions ja preses</h2>
        </div>
        <ul className="space-y-4">
          <li className="flex gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
            <p className="text-gray-700">
              <strong>R queda reduït a una o dues sessions.</strong> És a la llista d'eines de la
              fitxa, així que no desapareix, però no es menja sis setmanes com preveia la
              programació anterior: es veu com a comparació, fent la mateixa regressió en R i en
              Python per entendre per què R continua viu en estadística.
            </p>
          </li>
          <li className="flex gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
            <p className="text-gray-700">
              <strong>Reinforcement Learning manté la mida del curs passat</strong>, quatre o cinc
              sessions al final amb la pràctica de l'agent DQN. La resta del curs és machine
              learning clàssic.
            </p>
          </li>
          <li className="flex gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
            <p className="text-gray-700">
              <strong>Els arbres de decisió entren com a porta d'entrada al supervisat.</strong>{" "}
              Eren un bloc sencer de la programació anterior i el curs passat van quedar diluïts;
              encaixen de manera natural al principi perquè es poden dibuixar i s'entenen sense
              matemàtiques, i d'aquí surt sol el concepte de bosc aleatori.
            </p>
          </li>
        </ul>
      </div>

      <div id="calendari" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-2">
          <CalendarDays className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">Dos escenaris de calendari</h2>
        </div>
        <p className="text-gray-600 mb-6">
          Mentre no se sàpiga si el mòdul és de 66 h o de 99 h, el calendari es presenta com a dos
          escenaris possibles, no com un fet.
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="border border-gray-200 rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-gray-900">Escenari A · 66 h</h3>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                Fitxa oficial
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-3">
              2 h setmanals, una sola sessió. Hi caben unes <strong>33 sessions</strong>, els set
              blocs tal com es descriuen a dalt, sense marge per a res més.
            </p>
            <table className="w-full text-sm">
              <tbody>
                {[
                  ["Bloc 0 · Punt de partida", "1"],
                  ["Bloc 1 · Python per a dades", "7"],
                  ["Bloc 2 · Pandas i visualització", "5"],
                  ["Bloc 3 · Aprenentatge supervisat", "8"],
                  ["Bloc 4 · Dades reals i no supervisat", "5"],
                  ["Bloc 5 · R al costat de Python", "2"],
                  ["Bloc 6 · Xarxes i Reinforcement Learning", "5"],
                ].map(([nom, sessions]) => (
                  <tr key={nom} className="border-t border-gray-100">
                    <td className="py-1.5 text-gray-700">{nom}</td>
                    <td className="py-1.5 text-right text-gray-500">{sessions} sess.</td>
                  </tr>
                ))}
                <tr className="border-t-2 border-gray-300 font-semibold">
                  <td className="py-1.5 text-gray-900">Total</td>
                  <td className="py-1.5 text-right text-gray-900">33 sess. · 66 h</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="border border-gray-200 rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-gray-900">Escenari B · 99 h</h3>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-200">
                Presentació 25-26
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-3">
              4 h setmanals en dues sessions (dilluns i divendres). Hi caben unes{" "}
              <strong>50 sessions</strong>: els mateixos set blocs amb més marge, i espai real per
              a dos blocs que ara no hi entren:
            </p>
            <ul className="space-y-2 text-sm">
              <li className="flex gap-2">
                <ChevronRight className="w-4 h-4 text-purple-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700">
                  <strong>Deep Learning en condicions</strong>, més enllà de la introducció que ja
                  hi ha al bloc 6.
                </span>
              </li>
              <li className="flex gap-2">
                <ChevronRight className="w-4 h-4 text-purple-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700">
                  <strong>IA generativa</strong>, que la presentació antiga anunciava i que ara no
                  hi és.
                </span>
              </li>
            </ul>
            <p className="text-xs text-gray-500 mt-4 italic">
              El detall sessió a sessió d'aquest escenari encara està per fer: només es pot afirmar
              que hi caben aquests dos blocs extra, no com queden repartits.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
