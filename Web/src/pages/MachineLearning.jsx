import { Link } from 'react-router-dom'
import {
  Brain,
  GitBranch,
  TreePine,
  Target,
  Layers,
  Wrench,
  Code2,
  RefreshCw,
  ShieldAlert,
  Sparkles,
} from 'lucide-react'
import MermaidDiagram from '../components/MermaidDiagram'

const tiposAprenentatgeChart = `
graph TD
    ML[Aprenentatge automàtic]
    ML --> SUP[Supervisat]
    ML --> NOSUP[No supervisat]
    ML --> RL[Per reforç]

    SUP --> REG["Regressió<br/>ex: preu d'un pis"]
    SUP --> CLASS["Classificació<br/>ex: correu spam o no"]

    NOSUP --> AGRUP["Agrupament k-means<br/>ex: segmentar clients"]
    NOSUP --> REDDIM["Reducció de dimensionalitat<br/>ex: visualitzar dades en 2D"]

    RL --> AGENT["Agent que aprèn per prova i error<br/>ex: jugar a un videojoc"]

    style ML fill:#4f46e5,color:#fff
    style SUP fill:#0ea5e9,color:#fff
    style NOSUP fill:#10b981,color:#fff
    style RL fill:#f59e0b,color:#fff
`

const fluxProjecteChart = `
flowchart LR
    A[Dades] --> B[Neteja]
    B --> C["Separació<br/>entrenament / test"]
    C --> D[Entrenament]
    D --> E["Avaluació<br/>amb mètriques"]
    E --> F[Ajust]
    F -.torna a entrenar.-> D
    E --> G[Model llest]

    style A fill:#e0e7ff,stroke:#4f46e5
    style D fill:#dbeafe,stroke:#0ea5e9
    style E fill:#d1fae5,stroke:#10b981
    style G fill:#4f46e5,color:#fff
`

export default function MachineLearning() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Machine learning</h1>
        <p className="mt-2 text-lg text-gray-600">
          El tros que hi ha entre saber Pandas i entrenar una xarxa neuronal: el nucli
          clàssic del mòdul.
        </p>
      </div>

      {/* 1. Conceptes bàsics */}
      <section id="conceptes-basics" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">1. Conceptes bàsics, per situar</h2>
        </div>

        <div className="space-y-4 text-gray-700">
          <p>
            El terme <strong>intel·ligència artificial</strong> neix el 1956, a la Conferència
            de Dartmouth, on John McCarthy el va fer servir per primera vegada per descriure
            màquines capaces de fer tasques que semblen requerir intel·ligència. Sis anys abans,
            el 1950, Alan Turing ja havia proposat el seu famós test: si una persona no pot
            distingir si parla amb una màquina o amb un humà, la màquina "passa" la prova.
          </p>

          <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4">
            <p className="font-medium text-indigo-900 mb-1">IA no és el mateix que ML</p>
            <p className="text-indigo-800 text-sm">
              La intel·ligència artificial és el camp general: qualsevol tècnica que faci que
              una màquina es comporti de manera "intel·ligent". El <strong>machine learning</strong> és
              una branca concreta de la IA que permet a les màquines aprendre patrons a partir de
              dades, en comptes de seguir regles programades explícitament punt per punt.
            </p>
          </div>

          <div className="bg-emerald-50 border border-emerald-100 rounded-lg p-4">
            <p className="font-medium text-emerald-900 mb-1">Data science tampoc és ML</p>
            <p className="text-emerald-800 text-sm">
              La data science estudia i analitza dades per extreure'n informació i entendre què
              ha passat. El machine learning va un pas més enllà: agafa aquestes dades per
              construir models que fan prediccions sobre casos nous.
            </p>
          </div>

          <div>
            <h3 className="font-medium text-gray-900 mb-2">Llenguatges de l'ecosistema</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li><strong>Python</strong>: el que fem servir al curs, pel seu ecosistema (scikit-learn, Pandas, PyTorch...).</li>
              <li><strong>R</strong>: nascut per a l'estadística, encara molt viu en aquest camp.</li>
              <li><strong>Julia</strong> i <strong>Mojo</strong>: llenguatges emergents pensats per a rendiment en càlcul numèric.</li>
            </ul>
          </div>

          <div>
            <h3 className="font-medium text-gray-900 mb-2">Perfils professionals</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
              <div className="bg-gray-50 rounded-lg p-3"><strong>Machine learning engineer</strong>: porta models a producció.</div>
              <div className="bg-gray-50 rounded-lg p-3"><strong>AI engineer</strong>: integra IA (sovint generativa) en aplicacions.</div>
              <div className="bg-gray-50 rounded-lg p-3"><strong>Data scientist</strong>: analitza dades i en treu models i conclusions.</div>
              <div className="bg-gray-50 rounded-lg p-3"><strong>Data analyst</strong>: explora dades i en fa informes.</div>
              <div className="bg-gray-50 rounded-lg p-3"><strong>Data engineer</strong>: construeix els pipelines que porten les dades on calen.</div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Aprenentatge supervisat */}
      <section id="supervisat" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Target className="w-6 h-6 text-sky-600" />
          <h2 className="text-xl font-semibold text-gray-900">2. Aprenentatge supervisat</h2>
          <span className="text-xs font-medium bg-sky-100 text-sky-700 px-2 py-1 rounded-full">8 sessions · el cor del curs</span>
        </div>

        <div className="space-y-4 text-gray-700">
          <p>
            És el bloc que cal construir de nou: el curs passat es va cobrir amb exercicis de
            DataCamp i aquest curs es fa amb material propi, tot amb <strong>scikit-learn</strong>.
          </p>

          <div>
            <h3 className="font-medium text-gray-900 mb-2">Entrenament i test</h3>
            <p className="text-sm">
              Un model no es pot avaluar amb les mateixes dades amb què s'ha entrenat: si ho fem,
              només mesurem si ha memoritzat, no si ha après. Per això les dades es divideixen en
              un conjunt d'<strong>entrenament</strong> (amb el qual el model ajusta els seus
              paràmetres) i un conjunt de <strong>test</strong> (que el model no veu fins a
              l'avaluació final).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-1">Regressió lineal</h4>
              <p className="text-sm text-gray-600">
                Prediu un valor numèric continu (un preu, una temperatura) ajustant una recta
                (o un pla, en més dimensions) a les dades.
              </p>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-1">Classificació</h4>
              <p className="text-sm text-gray-600">
                Prediu una categoria (spam o no, aprovat o suspès) en comptes d'un número.
              </p>
            </div>
          </div>

          <div className="bg-sky-50 border border-sky-100 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <TreePine className="w-5 h-5 text-sky-700" />
              <h4 className="font-medium text-sky-900">Per què els arbres de decisió entren primer</h4>
            </div>
            <p className="text-sky-800 text-sm">
              Un arbre de decisió es pot dibuixar a la pissarra: una sèrie de preguntes de
              sí/no ("l'edat és més gran que 30?", "el sou supera els 2000€?") que acaben en una
              predicció. S'entén sense cap matemàtica, i és la porta d'entrada natural al ML
              supervisat. A partir d'aquí surt sol el pas següent: un <strong>bosc aleatori</strong> és
              simplement molts arbres diferents votant, que juntes prediuen millor que un de sol.
            </p>
          </div>

          <div>
            <h3 className="font-medium text-gray-900 mb-2">Mètriques</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left px-3 py-2 font-medium text-gray-700">Mètrica</th>
                    <th className="text-left px-3 py-2 font-medium text-gray-700">Què mesura</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  <tr>
                    <td className="px-3 py-2 font-medium">Exactitud (accuracy)</td>
                    <td className="px-3 py-2 text-gray-600">Percentatge total d'encerts.</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2 font-medium">Precisió</td>
                    <td className="px-3 py-2 text-gray-600">De tot el que el model diu que és positiu, quant n'encerta.</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2 font-medium">Record (recall)</td>
                    <td className="px-3 py-2 text-gray-600">De tots els casos positius reals, quants en detecta.</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2 font-medium">Matriu de confusió</td>
                    <td className="px-3 py-2 text-gray-600">Taula amb encerts i errors desglossats per classe.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-gray-900 mb-2">Sobreajust</h3>
            <p className="text-sm">
              Un model que s'ajusta massa a les dades d'entrenament acaba memoritzant-les en
              comptes d'aprendre'n el patró general: funciona molt bé amb les dades que ja ha
              vist i malament amb dades noves. Separar entrenament i test és precisament el que
              permet detectar-ho.
            </p>
          </div>
        </div>
      </section>

      {/* 3. No supervisat i dades reals */}
      <section id="no-supervisat" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Layers className="w-6 h-6 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900">3. Aprenentatge no supervisat i dades reals</h2>
          <span className="text-xs font-medium bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">5 sessions</span>
        </div>

        <div className="space-y-4 text-gray-700">
          <p>
            Aquest és el bloc que separa un dataset de joguina (net, endreçat, llest per
            entrenar) d'un de real, amb totes les misèries que arrosseguen les dades del món
            real.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="bg-gray-50 rounded-lg p-3 text-sm"><strong>Dades nul·les:</strong> valors que falten i què fer-ne (eliminar-los, imputar-los).</div>
            <div className="bg-gray-50 rounded-lg p-3 text-sm"><strong>Variables categòriques:</strong> convertir text ("Barcelona", "Girona"...) en números que el model pugui fer servir.</div>
            <div className="bg-gray-50 rounded-lg p-3 text-sm"><strong>Escalat:</strong> posar totes les variables numèriques a una escala comparable.</div>
            <div className="bg-gray-50 rounded-lg p-3 text-sm">
              <div className="flex items-center gap-1 mb-1"><Wrench className="w-4 h-4" /><strong>Pipelines:</strong></div>
              encadenar tots aquests passos amb un objecte de scikit-learn perquè no calgui
              repetir-los a mà cada vegada.
            </div>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-1">Agrupament amb k-means</h4>
            <p className="text-sm text-gray-600">
              Sense etiquetes prèvies, l'algorisme busca grups de dades semblants entre si
              (per exemple, segmentar clients per hàbits de compra).
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-1">Reducció de dimensionalitat (idea)</h4>
            <p className="text-sm text-gray-600">
              Quan hi ha moltes variables, es poden resumir en unes poques que conserven la
              informació més rellevant; útil, per exemple, per poder visualitzar dades
              d'alta dimensió en un gràfic de 2D.
            </p>
          </div>
        </div>
      </section>

      {/* 4. R al costat de Python */}
      <section id="r-python" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Code2 className="w-6 h-6 text-orange-600" />
          <h2 className="text-xl font-semibold text-gray-900">4. R al costat de Python</h2>
          <span className="text-xs font-medium bg-orange-100 text-orange-700 px-2 py-1 rounded-full">1-2 sessions</span>
        </div>

        <div className="space-y-4 text-gray-700">
          <p>
            <strong>R</strong> és un llenguatge nascut als anys 90 pensat des de l'inici per a
            l'estadística, i per això continua molt viu en aquest àmbit: molts mètodes
            estadístics hi tenen la implementació de referència.
          </p>

          <div className="bg-orange-50 border border-orange-100 rounded-lg p-4 text-sm text-orange-900">
            Aquest bloc <strong>no és sis setmanes</strong> com al curs anterior. És una
            comparació breu: la mateixa regressió lineal del bloc de supervisat, feta en R i en
            Python, línia a línia, per entendre per què R existeix i on encaixa. El curs es fa
            en Python.
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="border border-gray-200 rounded-lg p-4">
              <p className="font-medium text-gray-900 mb-2">Python</p>
              <pre className="bg-gray-900 text-gray-100 rounded p-3 overflow-x-auto text-xs">{`from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)`}</pre>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <p className="font-medium text-gray-900 mb-2">R</p>
              <pre className="bg-gray-900 text-gray-100 rounded p-3 overflow-x-auto text-xs">{`model <- lm(y ~ ., data = train)
pred <- predict(model, test)`}</pre>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Diagrames */}
      <section id="mapa-aprenentatge" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <GitBranch className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Mapa dels tipus d'aprenentatge</h2>
        </div>
        <MermaidDiagram chart={tiposAprenentatgeChart} />
      </section>

      <section id="flux-projecte" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <RefreshCw className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Flux d'un projecte de ML</h2>
        </div>
        <p className="text-gray-700 text-sm mb-4">
          No és un procés lineal: l'avaluació amb mètriques sovint obliga a tornar enrere,
          ajustar el model (o les dades) i tornar a entrenar.
        </p>
        <MermaidDiagram chart={fluxProjecteChart} />
      </section>

      {/* 6. Ètica */}
      <section id="etica" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <ShieldAlert className="w-6 h-6 text-rose-600" />
          <h2 className="text-xl font-semibold text-gray-900">Ètica, repartida per tot el curs</h2>
        </div>
        <div className="space-y-3 text-gray-700 text-sm">
          <p>
            El biaix no és un tema per reservar per al maig: apareix en tres moments concrets,
            i cadascun té el seu bloc en aquest curs.
          </p>
          <ul className="list-disc list-inside space-y-1">
            <li>Quan es <strong>tria el dataset</strong>: si les dades ja arrosseguen un biaix, el model l'aprèn i el reprodueix.</li>
            <li>Quan es <strong>neteja</strong>: decidir què fer amb els valors que falten o com es codifiquen les variables categòriques no és neutre.</li>
            <li>Quan s'<strong>interpreten les mètriques</strong>: una exactitud alta pot amagar que el model falla sistemàticament amb un grup concret.</li>
          </ul>
          <div className="flex items-start gap-2 bg-rose-50 border border-rose-100 rounded-lg p-4">
            <Sparkles className="w-5 h-5 text-rose-700 shrink-0 mt-0.5" />
            <p className="text-rose-900">
              Ja a la primera sessió del curs, amb Teachable Machine, es veu en directe: un
              classificador d'imatges entrenat amb exemples esbiaixats a propòsit, per notar
              de seguida com de fràgil pot ser un model si les dades d'entrada no estan ben
              triades.
            </p>
          </div>
        </div>
      </section>

      {/* Navegació */}
      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Continua per aquí</h2>
        <div className="flex flex-wrap gap-3">
          <Link to="/python" className="text-sm font-medium text-indigo-600 hover:text-indigo-800">Python per a dades →</Link>
          <Link to="/deep-rl" className="text-sm font-medium text-indigo-600 hover:text-indigo-800">Xarxes neuronals i Reinforcement Learning →</Link>
          <Link to="/programa" className="text-sm font-medium text-indigo-600 hover:text-indigo-800">Programa del curs →</Link>
          <Link to="/recursos" className="text-sm font-medium text-indigo-600 hover:text-indigo-800">Recursos →</Link>
        </div>
      </section>
    </div>
  )
}
