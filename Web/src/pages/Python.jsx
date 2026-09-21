import {
  Code2,
  ListChecks,
  Database,
  Cloud,
  Lightbulb,
  CheckCircle2,
  FileCode2,
  BarChart3,
  Sparkles,
  ExternalLink,
} from "lucide-react";
import { Link } from "react-router-dom";
import MermaidDiagram from "../components/MermaidDiagram";

const temesPython = [
  "Tipus bàsics de dades i variables",
  "Cadenes de text i llibreries bàsiques",
  "Condicionals",
  "Llistes i tuples",
  "Bucles for i while",
  "Diccionaris",
  "Funcions",
  "Comprensions de llista",
];

const exercicis = [
  {
    nom: "Intercanvi de variables",
    descripcio:
      "Bescanviar el valor de dues variables entre elles, sense perdre'n cap pel camí.",
  },
  {
    nom: "Inversió de cadena",
    descripcio:
      "Escriure una cadena de text al revés sense fer servir cap funció que ho faci automàticament.",
  },
  {
    nom: "Càlcul de la lletra del DNI",
    descripcio:
      "Calcular la lletra de control d'un DNI a partir del número, aplicant la regla del residu.",
  },
  {
    nom: "Positiu, negatiu o zero",
    descripcio:
      "Llegir un nombre i classificar-lo amb un condicional senzill.",
  },
  {
    nom: "Joc de pedra, paper o tisores (i una versió avançada)",
    descripcio:
      "Implementar el joc clàssic contra la màquina i, després, ampliar-lo amb més opcions o una lògica més fina.",
  },
  {
    nom: "Nombres únics ordenats",
    descripcio:
      "A partir d'una llista amb valors repetits, obtenir només els valors únics i ordenar-los.",
  },
  {
    nom: "Repàs de list comprehensions",
    descripcio:
      "Reescriure bucles habituals com a comprensions de llista, més curtes i més pròpies de Python.",
  },
  {
    nom: "Familiarització amb Jupyter Notebook i Colab",
    descripcio:
      "Primers passos amb notebooks: cel·les de codi i de text, execució per blocs, abans d'entrar a Pandas.",
  },
  {
    nom: "Cerques bàsiques amb Pandas",
    descripcio:
      "Primeres consultes sobre un DataFrame: seleccionar columnes i files, i filtrar per condició.",
  },
];

const temesDades = [
  "Jupyter i Colab",
  "Càrrega de dades",
  "Consultes i filtres amb Pandas",
  "Agrupacions",
  "Gràfics",
  "Com no fer un gràfic",
];

const diagrama = `flowchart LR
  A["Sintaxi bàsica"] --> B["Estructures de dades"]
  B --> C["Jupyter i Colab"]
  C --> D["Pandas"]
  D --> E["Gràfics"]
  E --> F["Projecte de dades"]`;

export default function Python() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Python i dades
        </h1>
        <p className="mt-2 text-gray-600 max-w-3xl">
          El curs comença amb un bloc de repàs de Python, perquè
          l'alumnat hi arriba amb nivells molt diferents i tot el que ve
          després —Pandas, scikit-learn, PyTorch— el dona per fet. A
          continuació, el bloc de dades hi construeix a sobre: carregar,
          consultar i representar informació real.
        </p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Code2 className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Bloc de Python (7 sessions)
          </h2>
        </div>
        <p className="text-gray-600 mb-4">
          Els temes es fan en aquest ordre, que és el que ha funcionat
          curs rere curs:
        </p>
        <ol className="grid sm:grid-cols-2 gap-3">
          {temesPython.map((tema, i) => (
            <li
              key={tema}
              className="flex items-start gap-3 rounded-lg bg-gray-50 p-3"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="text-gray-700">{tema}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ListChecks className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Els exercicis, el cor del bloc
          </h2>
        </div>
        <p className="text-gray-600 mb-4">
          Un lliurament curt per sessió. Són exercicis breus a posta: no
          per lluir-se, sinó perquè es facin.
        </p>
        <ul className="space-y-3">
          {exercicis.map((ex) => (
            <li
              key={ex.nom}
              className="flex items-start gap-3 border-b border-gray-100 pb-3 last:border-0 last:pb-0"
            >
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium text-gray-900">{ex.nom}</p>
                <p className="text-sm text-gray-600">{ex.descripcio}</p>
              </div>
            </li>
          ))}
        </ul>
        <div className="mt-6 grid sm:grid-cols-2 gap-4">
          <div className="flex items-start gap-3 rounded-lg bg-blue-50 p-4">
            <FileCode2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-blue-900">
              Hi ha una solució d'exemple del joc de pedra, paper i
              tisores feta per una alumna del curs passat.
            </p>
          </div>
          <div className="flex items-start gap-3 rounded-lg bg-blue-50 p-4">
            <FileCode2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-blue-900">
              I un exemple d'expressió regular explicat pas a pas, per
              a qui vulgui anar més enllà.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Database className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Bloc de dades (5 sessions)
          </h2>
        </div>
        <ol className="grid sm:grid-cols-2 gap-3 mb-4">
          {temesDades.map((tema, i) => (
            <li
              key={tema}
              className="flex items-start gap-3 rounded-lg bg-gray-50 p-3"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="text-gray-700">{tema}</span>
            </li>
          ))}
        </ol>
        <div className="flex items-start gap-3 rounded-lg bg-gray-50 p-4">
          <BarChart3 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-700">
            La feina grossa d'aquest bloc és el projecte d'anàlisi i
            representació de dades: agafar un conjunt de dades i
            explicar-lo amb Pandas i amb gràfics, de cap a peus.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Cloud className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Res d'instal·lacions
          </h2>
        </div>
        <p className="text-gray-600">
          Es treballa amb <strong>Google Colab</strong>: no cal
          instal·lar Python a cap ordinador. Per repassar la sintaxi pel
          teu compte hi ha{" "}
          <a
            href="https://www.pythonanywhere.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-700 font-medium"
          >
            pythonanywhere.com
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
          . És una decisió que es va prendre el curs passat per no
          cremar sessions en instal·lacions, i es manté.
        </p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          El recorregut del bloc
        </h2>
        <MermaidDiagram chart={diagrama} />
      </div>

      <div className="bg-amber-50 rounded-xl p-6 border border-amber-200">
        <div className="flex items-center gap-3 mb-3">
          <Lightbulb className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-semibold text-amber-900">
            Consells per a qui va just
          </h2>
        </div>
        <ul className="space-y-2 text-amber-900">
          <li className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 flex-shrink-0 mt-1" />
            <span>No cal saber-s'ho tot de memòria.</span>
          </li>
          <li className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 flex-shrink-0 mt-1" />
            <span>
              El que no s'entengui s'ha de preguntar el mateix dia, no
              deixar-ho córrer.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 flex-shrink-0 mt-1" />
            <span>
              Els exercicis són curts a posta perquè es facin, no per
              lluir-se.
            </span>
          </li>
        </ul>
      </div>

      <div className="flex flex-wrap gap-3 text-sm">
        <Link
          to="/programa"
          className="px-4 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50"
        >
          Veure el programa complet
        </Link>
        <Link
          to="/machine-learning"
          className="px-4 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50"
        >
          Continuar a Machine Learning
        </Link>
        <Link
          to="/recursos"
          className="px-4 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50"
        >
          Recursos
        </Link>
      </div>
    </div>
  );
}
