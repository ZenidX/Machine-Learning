import { Link } from "react-router-dom";
import {
  Brain,
  BookOpen,
  Mountain,
  ClipboardCheck,
  GitBranch,
  RefreshCw,
  ShieldAlert,
  Sigma,
  Eye,
  ChevronRight,
  Lightbulb,
} from "lucide-react";
import MermaidDiagram from "../components/MermaidDiagram";
import {
  CapcaleraBloc,
  PassosBloc,
  Pas,
  Seccio,
  QuadernCard,
  AbansDeComencar,
  Reptes,
  QuanCridar,
  ProvaBloc,
  ActivitatsBloc,
  SeguentBloc,
} from "../components/Bloc";

const C = "sky";

const tipusAprenentatge = `
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
`;

const fluxProjecte = `
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
`;

const eines = [
  "train_test_split", "StandardScaler", "SimpleImputer", "OneHotEncoder", "drop_duplicates",
  "Pipeline", "ColumnTransformer", "confusion_matrix", "classification_report", "precision_score",
  "recall_score", "DummyClassifier", "SelectKBest", "cross_val_score", "GridSearchCV", "meshgrid + contourf",
];

export default function BlocSupervisat() {
  return (
    <div className="space-y-8">
      <CapcaleraBloc num={2} icona={Brain} color={C}>
        Cinc models supervisats amb scikit-learn, i cadascun baixat fins a la fórmula que el fa
        funcionar. És el cor del curs. Acaba amb la prova pràctica 2, l'1 de desembre.
      </CapcaleraBloc>

      <PassosBloc color={C} />

      <Seccio titol="Les idees que travessen tot el bloc" icona={Lightbulb} color={C}>
        <div className="space-y-5 text-gray-700">
          <div>
            <h3 className="font-medium text-gray-900 mb-1">Entrenament i test</h3>
            <p className="text-sm">
              Un model no es pot avaluar amb les mateixes dades amb què s'ha entrenat: si ho fas,
              només mesures si ha memoritzat, no si ha après. Per això les dades es divideixen en un
              conjunt d'<strong>entrenament</strong> (amb el qual el model ajusta els seus paràmetres)
              i un de <strong>test</strong> (que el model no veu fins a l'avaluació final).
            </p>
          </div>
          <div>
            <h3 className="font-medium text-gray-900 mb-1">Sobreajust</h3>
            <p className="text-sm">
              Un model que s'ajusta massa a les dades d'entrenament les acaba memoritzant en comptes
              d'aprendre'n el patró general: funciona molt bé amb el que ja ha vist i malament amb dades
              noves. Separar entrenament i test és precisament el que permet detectar-ho.
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
                  <tr><td className="px-3 py-2 font-medium">Exactitud (accuracy)</td><td className="px-3 py-2 text-gray-600">Percentatge total d'encerts.</td></tr>
                  <tr><td className="px-3 py-2 font-medium">Precisió</td><td className="px-3 py-2 text-gray-600">De tot el que el model diu que és positiu, quant n'encerta.</td></tr>
                  <tr><td className="px-3 py-2 font-medium">Record (recall)</td><td className="px-3 py-2 text-gray-600">De tots els casos positius reals, quants en detecta.</td></tr>
                  <tr><td className="px-3 py-2 font-medium">Matriu de confusió</td><td className="px-3 py-2 text-gray-600">Taula amb encerts i errors desglossats per classe.</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <div className="bg-violet-50 border border-violet-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Sigma className="w-5 h-5 text-violet-700" />
              <p className="font-medium text-violet-900">Cada model es baixa fins a la fórmula</p>
            </div>
            <p className="text-violet-900 text-sm">
              Els arbres continuen a l'entropia, la regressió logística al descens de gradient, i la
              log-loss a la versemblança. Els quaderns de matemàtiques (MA) van intercalats a la llista
              d'aquí sota, just on toquen: cada fórmula seguida de la línia de NumPy que la calcula, i cada
              implementació comparada amb scikit-learn. Si el número que et surt no coincideix amb el de la
              llibreria, alguna cosa del que has escrit no és el que creus.
            </p>
          </div>
          <details className="group rounded-lg border border-gray-200 bg-gray-50">
            <summary className="flex cursor-pointer list-none items-center gap-2 p-3 text-sm font-medium text-gray-800 hover:bg-gray-100 rounded-lg">
              <ChevronRight className="w-4 h-4 flex-shrink-0 transition-transform group-open:rotate-90" />
              Per situar: IA, ML i data science no són el mateix
            </summary>
            <div className="border-t border-gray-200 p-4 space-y-3 text-sm text-gray-700">
              <p>
                El terme <strong>intel·ligència artificial</strong> neix el 1956, a la Conferència de
                Dartmouth. Sis anys abans, el 1950, Alan Turing ja havia proposat el seu test: si una
                persona no pot distingir si parla amb una màquina o amb un humà, la màquina el passa.
              </p>
              <p>
                La IA és el camp general. El <strong>machine learning</strong> n'és una branca concreta:
                màquines que aprenen patrons a partir de dades, en comptes de seguir regles escrites
                punt per punt. La <strong>data science</strong> analitza dades per entendre què ha passat;
                el ML fa un pas més i construeix models que prediuen casos nous.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div className="bg-white rounded-lg p-3"><strong>Machine learning engineer</strong>: porta models a producció.</div>
                <div className="bg-white rounded-lg p-3"><strong>AI engineer</strong>: integra IA (sovint generativa) en aplicacions.</div>
                <div className="bg-white rounded-lg p-3"><strong>Data scientist</strong>: analitza dades i en treu models i conclusions.</div>
                <div className="bg-white rounded-lg p-3"><strong>Data analyst</strong>: explora dades i en fa informes.</div>
                <div className="bg-white rounded-lg p-3"><strong>Data engineer</strong>: construeix els pipelines que porten les dades on calen.</div>
              </div>
            </div>
          </details>
        </div>
      </Seccio>

      <div className="grid lg:grid-cols-2 gap-6">
        <Seccio titol="Els tipus d'aprenentatge" icona={GitBranch} color={C}>
          <MermaidDiagram chart={tipusAprenentatge} />
        </Seccio>
        <Seccio titol="El flux d'un projecte" icona={RefreshCw} color={C}>
          <p className="text-gray-700 text-sm mb-4">
            No és lineal: l'avaluació sovint obliga a tornar enrere, ajustar el model o les dades i
            tornar a entrenar.
          </p>
          <MermaidDiagram chart={fluxProjecte} />
        </Seccio>
      </div>

      <AbansDeComencar />

      {/* ---------- 1 · Aprèn ---------- */}
      <Pas id="apren" num={1} titol="Aprèn" color={C} subtitol="Els quaderns de teoria en l'ordre del calendari, amb els de matemàtiques on fan falta." />
      <Seccio icona={BookOpen} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="ML_00" color={C} />
          <QuadernCard codi="ML_01" color={C} />
          <QuadernCard codi="ML_02" color={C} />
          <QuadernCard codi="MA_04" color="violet" etiqueta="matemàtiques dels arbres" />
          <QuadernCard codi="ML_03" color={C} />
          <QuadernCard codi="ML_04" color={C} />
          <QuadernCard codi="MA_02" color="violet" etiqueta="matemàtiques de la logística" />
          <QuadernCard codi="MA_03" color="violet" etiqueta="d'on surt la log-loss" />
          <QuadernCard codi="ML_05" color={C} />
        </div>
        <p className="text-sm text-gray-600 mt-4">
          El marge de l'SVM es tanca al bloc 3, amb el quadern MA_05. El descens de gradient té dues
          sessions a posta: és el quadern més dur del curs i el que sosté tot el bloc de xarxes.
        </p>
      </Seccio>

      {/* ---------- 2 · Exemples ---------- */}
      <Pas id="exemples" num={2} titol="Exemples" color={C} subtitol="Exemples resolts: per veure com es fa. Cadascun fa servir un conjunt de dades que ensenya una cosa que Iris no pot ensenyar." />
      <Seccio icona={Eye} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="EX_01" color={C} etiqueta="exemple resolt" />
          <QuadernCard codi="EX_02" color={C} etiqueta="exemple resolt" />
          <QuadernCard codi="EX_04" color={C} etiqueta="exemple resolt" />
          <QuadernCard codi="EX_00" color="indigo" etiqueta="referència">
            <div className="flex flex-wrap gap-1.5 pt-2">
              {eines.map((e) => (
                <code key={e} className="text-xs bg-indigo-50 border border-indigo-200 text-indigo-800 px-1.5 py-0.5 rounded">
                  {e}
                </code>
              ))}
            </div>
          </QuadernCard>
        </div>
      </Seccio>

      <div>
        <Seccio titol="Ètica: on entra el biaix" icona={ShieldAlert} color="rose">
          <div className="space-y-3 text-gray-700 text-sm">
            <ul className="list-disc list-inside space-y-1">
              <li>Quan es <strong>tria el dataset</strong>: si les dades ja arrosseguen un biaix, el model l'aprèn i el reprodueix.</li>
              <li>Quan es <strong>neteja</strong>: què fer amb els valors que falten o com es codifiquen les categories no és neutre.</li>
              <li>Quan s'<strong>interpreten les mètriques</strong>: una exactitud alta pot amagar que el model falla sempre amb un grup concret.</li>
            </ul>
            <p>
              El cas més clar és l'EX_02: hi ha dos errors possibles i no costen el mateix, i una
              exactitud alta pot amagar exactament l'error que importa. L'exemple ensenya com es
              mesura.
            </p>
          </div>
        </Seccio>
      </div>

      {/* ---------- 3 · Reptes ---------- */}
      <Pas id="reptes" num={3} titol="Reptes" color={C} subtitol="Un problema real, un model que has de triar tu, i una mètrica que has de saber defensar." />
      <Seccio icona={Mountain} color={C}>
        <div className="space-y-4">
          <Reptes bloc={2} color={C} />
          <QuanCridar color={C} />
        </div>
      </Seccio>

      {/* ---------- 4 · Prova ---------- */}
      <Pas id="prova" num={4} titol="Prova" color={C} subtitol="La Pp2 és la porta cap a les xarxes: qui no hi arribi, al gener no entendrà què fa loss.backward()." />
      <Seccio icona={ClipboardCheck} color={C}>
        <ProvaBloc bloc={2} color={C} />
        <div className="mt-4">
          <ActivitatsBloc bloc={2} />
        </div>
        <p className="text-sm text-gray-700 mt-4">
          <strong>Les matemàtiques no s'avaluen com a deducció.</strong> No es demana derivar el
          gradient de la log-loss. Sí que es demana implementar una funció de pèrdua i comprovar-la,
          verificar un gradient per diferències finites, o explicar per què un model dona el que dona
          mirant-ne els pesos.
        </p>
      </Seccio>

      <SeguentBloc actual={2} />
    </div>
  );
}
