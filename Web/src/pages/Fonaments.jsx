import {
  Table2,
  ListChecks,
  AlertTriangle,
  Download,
  Save,
  MousePointerClick,
  CheckCircle2,
  Github,
  ExternalLink,
  CircleSlash,
  DownloadCloud,
  ChevronRight,
} from "lucide-react";
import { Link } from "react-router-dom";

const COLAB_BASE =
  "https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/01_fonaments/";

const quaderns = [
  {
    fitxer: "FO_00_objectes_i_autocompletar.ipynb",
    titol: "Objectes de Python i autocompletat",
    sessions: "S04 · 29 de setembre",
    mida: "exploració de dades guiada de punta a punta",
    descripcio:
      "Com es pregunta a un objecte de Python què té a dins: type(), dir(), objecte.metode? i l'autocompletat amb la tecla TAB. La diferència entre un atribut i un mètode, que és per què df.shape va sense parèntesis i df.head() amb. I els objectes que et trobaràs a tot el curs: el Bunch que tornen els load_*, l'ndarray, el DataFrame, la Series, i un model de scikit-learn abans i després d'entrenar-lo. Acaba amb una exploració de dades guiada de principi a fi.",
    destacat:
      "Els atributs que acaben en guió baix, com .coef_ o .feature_importances_, volen dir «això ho he après de les dades». No existeixen abans de cridar .fit(), i buscar-los abans és el primer error que fa tothom.",
    funcions: {
      titol: "Les funcions que fas servir avui, per ordre d'importància",
      intro:
        "No són les que més surten als tutorials, són les que el seu resultat et fa prendre una decisió. La resta és decoració.",
      llista: [
        {
          nom: ".shape",
          text: "La més tonta i la que més errors caça. La primera sempre, i un altre cop després de cada filtre o partició: si el nombre de files no és el que esperaves, atura't aquí.",
        },
        {
          nom: ".info()",
          text: "Millor primera mirada que .describe(): files, columnes, tipus i quants valors no són nuls, tot en una pantalla.",
        },
        {
          nom: ".value_counts()",
          text: "Sobre l'etiqueta és la més important de totes en un problema de classificació. A Wine surt 59/71/48, que està equilibrat. Si sortís 95/5, l'exactitud deixaria de voler dir res.",
        },
        {
          nom: ".groupby().mean()",
          text: "L'única que fa anàlisi de veritat. Les altres descriuen; aquesta compara, i és amb la que trobes quina columna separa les classes.",
        },
        {
          nom: ".isna().sum()",
          text: "L'inventari del que falta. És barata i decideix tota la preparació de dades que ve després.",
        },
        {
          nom: "df[df.columna > x]",
          text: "Les màscares booleanes no són una funció, són el mecanisme: el que et deixa preguntar qualsevol cosa, i no només les que algú va preveure.",
        },
        {
          nom: ".sort_values() i .head()",
          text: "Els extrems. Allà hi ha els errors de dades i els casos interessants.",
        },
      ],
      describe:
        "I .describe()? És la que més s'ensenya i la que menys es llegeix: a Wine et dona 8 estadístics per 13 columnes, 104 números. Té un ús real i només un: veure d'un cop d'ull que les columnes van en escales incompatibles (proline per centenars, hue per sota de 2). Això és el que decideix si cal escalar, i és l'entrebanc del k-NN del bloc següent.",
      tancament: ".describe() descriu. .groupby() compara. Analitzar és comparar.",
    },
  },
  {
    fitxer: "FO_01_numpy.ipynb",
    titol: "NumPy",
    sessions: "S05 i S06 · 5 i 6 d'octubre",
    mida: "30 cel·les de codi",
    descripcio:
      "Per què no n'hi ha prou amb les llistes de Python, amb la comparació de temps executada. L'array, shape i dtype, indexació i llesques, i el parany de la llesca contra la còpia. Operacions vectoritzades, màscares booleanes, i les agregacions amb el concepte d'eix. Acaba ensenyant que la distància euclidiana i la precisió d'un model són una línia de NumPy cadascuna.",
  },
  {
    fitxer: "FO_02_pandas.ipynb",
    titol: "Pandas",
    sessions: "S07 i S08 · 13 i 19 d'octubre",
    mida: "41 cel·les de codi",
    descripcio:
      "Què afegeix Pandas sobre NumPy: noms de columna i tipus barrejats. Series i DataFrame, i carregar melb_data.csv, que són 13.580 habitatges venuts a Melbourne, amb nuls i columnes de text de veritat. Seleccionar amb loc i iloc, filtrar, l'inventari de valors que falten, groupby i agg, i finalment com es passa d'un DataFrame a les X i y de scikit-learn.",
  },
];

export default function Fonaments() {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3">
          <Table2 className="w-8 h-8 text-emerald-600" />
          <h1 className="text-3xl font-bold text-gray-900">Fonaments de dades</h1>
        </div>
        <p className="mt-2 text-lg text-gray-600">
          Tres quaderns: objectes de Python, NumPy i Pandas.
        </p>
      </div>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Table2 className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">Per què ara</h2>
        </div>
        <p className="text-gray-700">
          Aquests tres quaderns són <strong>l'eina que falta</strong> per poder fer els models que ja
          s'han vist explicats a classe. Sense saber manejar una taula de dades, la resta del curs
          es queda en teoria: es pot entendre què fa un arbre de decisió i no poder-lo entrenar
          contra res.
        </p>
        <p className="text-gray-700 mt-3">
          Ocupen les sessions S04 a S08 del{" "}
          <Link to="/programa" className="text-emerald-700 font-medium hover:text-emerald-900">
            bloc 1
          </Link>
          . L'ordre no és casual: primer saber interrogar un objecte per no anar a cegues, després
          NumPy, i Pandas al final perquè està construït a sobre de NumPy. Amb NumPy fet, la primera
          sessió de{" "}
          <Link to="/matematiques" className="text-emerald-700 font-medium hover:text-emerald-900">
            matemàtiques
          </Link>{" "}
          ja no necessita res més.
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
              Els tres quaderns funcionen a <strong>Google Colab</strong> sense instal·lar res.
            </span>
          </li>
        </ul>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ListChecks className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">Els tres quaderns</h2>
        </div>
        <div className="space-y-4">
          {quaderns.map((q, i) => (
            <div
              key={q.fitxer}
              className="border border-gray-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
            >
              <div>
                <p className="text-xs font-medium text-emerald-600 mb-1">
                  Quadern {i + 1} · {q.sessions}
                </p>
                <h3 className="font-medium text-gray-900 mb-1">{q.titol}</h3>
                <p className="text-sm text-gray-500 mb-2">{q.mida}</p>
                <p className="text-sm text-gray-600">{q.descripcio}</p>
                {q.destacat && (
                  <p className="mt-3 text-sm text-emerald-900 bg-emerald-50 border-l-4 border-emerald-400 rounded-r-lg p-3">
                    {q.destacat}
                  </p>
                )}
                {q.funcions && (
                  <details className="mt-3 group rounded-lg border border-gray-200 bg-gray-50">
                    <summary className="flex cursor-pointer list-none items-center gap-2 p-3 text-sm font-medium text-gray-800 hover:bg-gray-100 rounded-lg">
                      <ChevronRight className="w-4 h-4 flex-shrink-0 transition-transform group-open:rotate-90" />
                      {q.funcions.titol}
                    </summary>
                    <div className="border-t border-gray-200 p-4 space-y-3">
                      <p className="text-sm text-gray-600">{q.funcions.intro}</p>
                      <ol className="space-y-2">
                        {q.funcions.llista.map((f, n) => (
                          <li key={f.nom} className="flex gap-3 text-sm">
                            <span className="flex-shrink-0 font-medium text-gray-400 tabular-nums">
                              {n + 1}.
                            </span>
                            <span>
                              <code className="bg-white border border-gray-200 px-1.5 py-0.5 rounded text-xs text-gray-900">
                                {f.nom}
                              </code>
                              <span className="ml-2 text-gray-700">{f.text}</span>
                            </span>
                          </li>
                        ))}
                      </ol>
                      <p className="text-sm text-gray-600 border-t border-gray-200 pt-3">
                        {q.funcions.describe}
                      </p>
                      <p className="text-sm font-medium text-gray-900">
                        {q.funcions.tancament}
                      </p>
                    </div>
                  </details>
                )}
              </div>
              <div className="flex-shrink-0 flex flex-col gap-2">
                <a
                  href={`${COLAB_BASE}${q.fitxer}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700 whitespace-nowrap"
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
          <CircleSlash className="w-6 h-6 text-rose-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            A NumPy, and i or no funcionen amb màscares
          </h2>
        </div>
        <div className="space-y-3 text-gray-700 text-sm">
          <p>
            Una màscara booleana no és un sol valor de cert o fals, és un array de milers, i{" "}
            <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">and</code> i{" "}
            <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">or</code> de Python no saben
            què fer-ne: donen un error de valor ambigu. Van amb{" "}
            <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">&amp;</code> i{" "}
            <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">|</code>, i cada condició
            necessita els seus parèntesis, perquè aquests operadors lliguen més fort que la
            comparació.
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="border border-rose-200 bg-rose-50 rounded-lg p-4">
              <p className="font-medium text-rose-900 mb-2">Peta</p>
              <pre className="bg-gray-900 text-gray-100 rounded p-3 overflow-x-auto text-xs">{`x[x > 2 and x < 8]
x[x > 2 & x < 8]`}</pre>
            </div>
            <div className="border border-emerald-200 bg-emerald-50 rounded-lg p-4">
              <p className="font-medium text-emerald-900 mb-2">Funciona</p>
              <pre className="bg-gray-900 text-gray-100 rounded p-3 overflow-x-auto text-xs">{`x[(x > 2) & (x < 8)]
x[(x < 2) | (x > 8)]`}</pre>
            </div>
          </div>
          <p>Ho provaràs i petarà. Quan passi, ja saps què és.</p>
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <DownloadCloud className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">El CSV de Pandas es baixa sol</h2>
        </div>
        <p className="text-gray-700 text-sm">
          El quadern de Pandas treballa amb{" "}
          <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">melb_data.csv</code>, i se'l
          descarrega ell mateix quan s'executa a Colab.{" "}
          <strong>No has de pujar cap fitxer a mà</strong> ni muntar el teu Drive.
        </p>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Download className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">Dues maneres de treballar-hi</h2>
        </div>
        <div className="grid md:grid-cols-2 gap-5">
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
            <h3 className="font-semibold text-emerald-900 mb-1">Obre a Colab</h3>
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
                className="text-emerald-700 hover:text-emerald-900 underline"
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
          className="inline-flex items-center gap-1 text-emerald-700 hover:text-emerald-900 font-medium text-sm"
        >
          github.com/ZenidX/Machine-Learning
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
        <p className="text-sm text-gray-600 mt-2">
          Els quaderns viuen a{" "}
          <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">
            Machine Learning/01_fonaments/
          </code>
          .
        </p>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Continua per aquí</h2>
        <div className="flex flex-wrap gap-3">
          <Link to="/python" className="text-sm font-medium text-emerald-700 hover:text-emerald-900">
            Python per a dades →
          </Link>
          <Link to="/matematiques" className="text-sm font-medium text-emerald-700 hover:text-emerald-900">
            Matemàtiques →
          </Link>
          <Link to="/machine-learning" className="text-sm font-medium text-emerald-700 hover:text-emerald-900">
            Machine Learning →
          </Link>
          <Link to="/programa" className="text-sm font-medium text-emerald-700 hover:text-emerald-900">
            Programa del curs →
          </Link>
        </div>
      </section>
    </div>
  );
}
