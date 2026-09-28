import {
  Sigma,
  ListChecks,
  AlertTriangle,
  Download,
  Save,
  MousePointerClick,
  CheckCircle2,
  Github,
  ExternalLink,
  Info,
} from "lucide-react";
import { Link } from "react-router-dom";

const COLAB_BASE =
  "https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/03_matematiques/";

const quaderns = [
  {
    fitxer: "MA_01_algebra_lineal.ipynb",
    titol: "Àlgebra lineal",
    sessio: "S09 · 20 d'octubre",
    descripcio:
      "Norma, producte escalar, projecció, i la matriu entesa com una transformació. Acaba traient el coef_ d'un model ja entrenat i fent la predicció a mà amb X @ w + b per a les 150 flors d'Iris: el mateix número que dona scikit-learn.",
  },
  {
    fitxer: "MA_02_descens_gradient.ipynb",
    titol: "Descens de gradient",
    sessio: "S18 i S19 · 23 i 24 de novembre",
    descripcio:
      "Què és una derivada, des de zero. La derivada de la log-loss, verificada contra el gradient numèric per diferències finites. I la regressió logística entrenada amb un bucle propi, sense scikit-learn.",
  },
  {
    fitxer: "MA_03_probabilitat_versemblanca.ipynb",
    titol: "Probabilitat i versemblança",
    sessio: "S20 · 30 de novembre",
    descripcio:
      "Bayes, i per què una prova amb un 99 % d'encert pot dir ben poca cosa. D'on surt la log-loss: és la versemblança amb un logaritme i un signe menys. Naive Bayes implementat de zero.",
  },
  {
    fitxer: "MA_04_entropia_informacio.ipynb",
    titol: "Entropia i informació",
    sessio: "S15 · 10 de novembre",
    descripcio:
      "L'entropia mesurada en bits, i per què Gini i entropia donen arbres iguals. El guany d'informació, i la trampa de la columna d'identificadors. Que la log-loss i l'entropia creuada són el mateix número.",
  },
  {
    fitxer: "MA_05_marge_optimitzacio.ipynb",
    titol: "Marge i optimització",
    sessio: "S22 · 7 de desembre",
    descripcio:
      "Multiplicadors de Lagrange amb un exemple que es pot tocar. Per què l'SVM només depèn d'uns pocs punts, que és una conseqüència matemàtica i no una optimització del programa. El truc del kernel, demostrat.",
  },
  {
    fitxer: "MA_06_pca_vectors_propis.ipynb",
    titol: "PCA i vectors propis",
    sessio: "S24 · 15 de desembre",
    descripcio:
      "La maledicció de la dimensionalitat, mesurada. La direcció de màxima variància trobada per força bruta, i el descobriment que allò que surt és un vector propi. PCA implementat en cinc passos.",
  },
];

export default function Matematiques() {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3">
          <Sigma className="w-8 h-8 text-violet-600" />
          <h1 className="text-3xl font-bold text-gray-900">Matemàtiques</h1>
        </div>
        <p className="mt-2 text-lg text-gray-600">
          Sis quaderns amb la matemàtica que hi ha sota els models del curs.
        </p>
      </div>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Sigma className="w-6 h-6 text-violet-600" />
          <h2 className="text-xl font-semibold text-gray-900">Com funcionen aquests quaderns</h2>
        </div>
        <p className="text-gray-700">
          <strong>Cada fórmula va seguida de la línia de NumPy que la calcula</strong>, i{" "}
          <strong>cada implementació acaba comparant-se amb scikit-learn</strong>. No és matemàtica
          per decorar la teoria: és matemàtica que s'executa i que es verifica contra un resultat
          conegut. Si el número que et surt no coincideix amb el de la llibreria, alguna cosa del
          que has escrit no és el que creus.
        </p>
        <p className="text-gray-700 mt-3">
          Els sis quaderns no són un bloc a part del curs. Ocupen sessions dins dels blocs 1, 2 i 3,
          just quan toca la teoria del model corresponent:{" "}
          <Link to="/programa" className="text-violet-700 font-medium hover:text-violet-900">
            S09, S15, S18, S19, S20 i S22
          </Link>
          .
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
              Fes <strong>Fitxer → Desa una còpia a Drive</strong> just en obrir el quadern, o
              perdràs la feina en tancar la pestanya.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <MousePointerClick className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              <strong>No cliquis «Executa-ho tot»</strong>: les cel·les d'exercici són buides a
              posta i les has d'anar omplint una per una. Si ho executes tot de cop veuràs errors
              de variables que encara no existeixen, i és normal.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>
              La comprovació final de cada apartat és la comparació amb scikit-learn. Fes-la servir
              per saber si el que has implementat és correcte.
            </span>
          </li>
        </ul>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ListChecks className="w-6 h-6 text-violet-600" />
          <h2 className="text-xl font-semibold text-gray-900">Els sis quaderns</h2>
        </div>
        <div className="space-y-4">
          {quaderns.map((q, i) => (
            <div
              key={q.fitxer}
              className="border border-gray-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
            >
              <div>
                <p className="text-xs font-medium text-violet-600 mb-1">
                  Quadern {i + 1} · {q.sessio}
                </p>
                <h3 className="font-medium text-gray-900 mb-1">{q.titol}</h3>
                <p className="text-sm text-gray-600">{q.descripcio}</p>
              </div>
              <div className="flex-shrink-0 flex flex-col gap-2">
                <a
                  href={`${COLAB_BASE}${q.fitxer}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-violet-600 text-white text-sm font-medium hover:bg-violet-700 whitespace-nowrap"
                >
                  Obre a Colab
                  <ExternalLink className="w-4 h-4" />
                </a>
                <a
                  href={`${import.meta.env.BASE_URL}quaderns/${q.fitxer}`}
                  download={q.fitxer}
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
          <Download className="w-6 h-6 text-violet-600" />
          <h2 className="text-xl font-semibold text-gray-900">Dues maneres de treballar-hi</h2>
        </div>
        <div className="grid md:grid-cols-2 gap-5">
          <div className="p-4 bg-violet-50 border border-violet-200 rounded-lg">
            <h3 className="font-semibold text-violet-900 mb-1">Obre a Colab</h3>
            <p className="text-sm text-gray-700">
              El quadern s'obre al navegador, sense instal·lar res. Desa-ne una còpia al teu Drive
              de seguida, o perdràs la feina en tancar la pestanya.
            </p>
          </div>
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-1">Baixa el fitxer</h3>
            <p className="text-sm text-gray-700">
              Et descarregues el{" "}
              <code className="bg-white px-1.5 py-0.5 rounded text-xs">.ipynb</code> i te'l
              emportes on vulguis. Per obrir-lo al teu Colab: entra a{" "}
              <a
                href="https://colab.research.google.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-violet-700 hover:text-violet-900 underline"
              >
                colab.research.google.com
              </a>
              , tria <strong>Puja</strong> i selecciona el fitxer. També funciona amb Jupyter al teu
              ordinador.
            </p>
          </div>
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
          className="inline-flex items-center gap-1 text-violet-700 hover:text-violet-900 font-medium text-sm"
        >
          github.com/ZenidX/Machine-Learning
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
        <p className="text-sm text-gray-600 mt-2">
          Els quaderns viuen a{" "}
          <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">
            Machine Learning/03_matematiques/
          </code>
          .
        </p>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border-2 border-gray-300">
        <div className="flex items-center gap-3 mb-4">
          <Info className="w-6 h-6 text-gray-700" />
          <h2 className="text-xl font-semibold text-gray-900">Una cosa que no es deriva</h2>
        </div>
        <div className="space-y-3 text-gray-700 text-sm">
          <p>
            Hi ha un punt del curs on la matemàtica no arriba fins al final:{" "}
            <strong>el problema dual de l'SVM</strong>. La derivació completa, de la formulació amb
            restriccions al problema dual i les condicions que en surten, no hi cap en el temps que
            tenim.
          </p>
          <p>
            El que es fa al quadern <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">MA_05</code> és{" "}
            <strong>presentar-ne el resultat, dir clarament que no s'ha derivat, i verificar-lo
            numèricament</strong> amb un model ja entrenat: es comprova que els coeficients del dual
            són els que diu la teoria i que els punts amb coeficient diferent de zero són
            exactament els vectors de suport.
          </p>
          <p>
            Queda dit perquè la diferència importa: tot el que hi ha als altres cinc quaderns el
            pots comprovar tu mateix des de zero. Això no, i és honest saber-ho.
          </p>
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Continua per aquí</h2>
        <div className="flex flex-wrap gap-3">
          <Link to="/machine-learning" className="text-sm font-medium text-violet-700 hover:text-violet-900">
            Machine Learning →
          </Link>
          <Link to="/practica" className="text-sm font-medium text-violet-700 hover:text-violet-900">
            Pràctica →
          </Link>
          <Link to="/programa" className="text-sm font-medium text-violet-700 hover:text-violet-900">
            Programa del curs →
          </Link>
        </div>
      </section>
    </div>
  );
}
