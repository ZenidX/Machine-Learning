import { Link } from "react-router-dom";
import { Table2, CircleSlash, BookOpen, Eye, Mountain, ClipboardCheck, Code2, Wrench, ListChecks, ChevronDown } from "lucide-react";
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
  Chivato,
} from "../components/Bloc";

const C = "emerald";

const funcionsFO00 = {
  titol: "Les funcions de Pandas que fas servir, per ordre d'importància",
  intro:
    "No són les que més surten als tutorials, són les que el seu resultat et fa prendre una decisió. La resta és decoració.",
  llista: [
    { nom: ".shape", text: "La més tonta i la que més errors caça. La primera sempre, i un altre cop després de cada filtre o partició: si el nombre de files no és el que esperaves, atura't aquí." },
    { nom: ".info()", text: "Millor primera mirada que .describe(): files, columnes, tipus i quants valors no són nuls, tot en una pantalla." },
    { nom: ".value_counts()", text: "Sobre l'etiqueta és la més important de totes en un problema de classificació. A Wine surt 59/71/48, que està equilibrat. Si sortís 95/5, l'exactitud deixaria de voler dir res." },
    { nom: ".groupby().mean()", text: "L'única que fa anàlisi de veritat. Les altres descriuen; aquesta compara, i és amb la que trobes quina columna separa les classes." },
    { nom: ".isna().sum()", text: "L'inventari del que falta. És barata i decideix tota la preparació de dades que ve després." },
    { nom: "df[df.columna > x]", text: "Les màscares booleanes no són una funció, són el mecanisme: el que et deixa preguntar qualsevol cosa, i no només les que algú va preveure." },
    { nom: ".sort_values() i .head()", text: "Els extrems. Allà hi ha els errors de dades i els casos interessants." },
  ],
  describe:
    "I .describe()? És la que més s'ensenya i la que menys es llegeix: a Wine et dona 8 estadístics per 13 columnes, 104 números. Té un ús real i només un: veure d'un cop d'ull que les columnes van en escales incompatibles (proline per centenars, hue per sota de 2). Això és el que decideix si cal escalar, i és l'entrebanc del k-NN del bloc següent.",
  tancament: ".describe() descriu. .groupby() compara. Analitzar és comparar.",
};

const cinquePreguntes = [
  { q: "Què és això?", eina: "type()" },
  { q: "Què porta dins?", eina: "dir(), TAB" },
  { q: "Quina mida té i de quins tipus és?", eina: ".shape, .dtypes, .info()" },
  { q: "Hi falta res? Hi ha repetits?", eina: ".isna().sum(), .duplicated().sum()" },
  { q: "Com es reparteix el que vull predir?", eina: ".value_counts()" },
];

function CinquePreguntes() {
  return (
    <div className="mt-3 rounded-lg border border-emerald-200 bg-white p-4">
      <p className="text-sm font-medium text-gray-900 mb-2">
        Les cinc preguntes que fa tot data scientist quan li arriba un dataset
      </p>
      <ol className="space-y-1.5">
        {cinquePreguntes.map((x, n) => (
          <li key={x.q} className="flex gap-3 text-sm">
            <span className="flex-shrink-0 font-semibold text-emerald-700 tabular-nums">{n + 1}.</span>
            <span className="text-gray-800">
              {x.q}{" "}
              <code className="bg-gray-50 border border-gray-200 px-1.5 py-0.5 rounded text-xs text-gray-700">{x.eina}</code>
            </span>
          </li>
        ))}
      </ol>
      <p className="text-xs text-gray-500 mt-2">
        Es fan a qualsevol objecte, també a un model. I són el primer que fas amb les dades d'un repte, abans de calcular res.
      </p>
    </div>
  );
}

const funcionsFO01 = {
  titol: "Les eines de NumPy que fas servir, per ordre d'importància",
  intro: "NumPy té centenars de funcions. Per fer machine learning, amb aquestes en tens prou per a gairebé tot.",
  llista: [
    { nom: ".shape", text: "Com a Pandas, la primera i la que més errors caça. Files = mostres, columnes = característiques. Si un model es queixa de dimensions, mira-la abans de res." },
    { nom: "X[:, j]", text: "«Totes les files, la columna j»: és com s'agafa una característica. [fila, columna] dins d'uns sols claudàtors, no [fila][columna]." },
    { nom: ".mean(axis=0)", text: "Les agregacions amb eix. axis=0 aixafa les files i et dona un valor per columna; axis=1, un per fila. És el concepte que més costa del bloc." },
    { nom: "X[X > 5]", text: "Les màscares booleanes: filtrar sense bucles. Combinades amb & i |, i cada condició entre parèntesis." },
    { nom: "a - b, a * 2", text: "Les operacions vectoritzades, element a element i sense bucle. Amb el broadcasting, una fila es resta de tota la taula d'un sol cop." },
    { nom: "np.sqrt(((a - b)**2).sum())", text: "La distància euclidiana, que és el mateix que np.linalg.norm(a - b). Una línia, i és el cor del k-NN." },
    { nom: "(pred == y).mean()", text: "La precisió d'un model: una màscara de True/False i la seva mitjana." },
    { nom: ".argmax() i .argsort()", text: "La posició, no el valor. Per trobar la mostra més gran o les k més properes." },
    { nom: ".copy()", text: "Una llesca no és una còpia: si la modifiques, modifiques l'original. Si l'has de tocar, copia-la abans." },
  ],
  tancament: "NumPy és càlcul: si escrius un bucle for sobre les files d'un array, gairebé segur que hi ha una manera vectoritzada.",
};

const funcionsFO02 = {
  titol: "Les eines de Pandas d'aquest quadern, per ordre d'importància",
  intro: "Les de FO_00 continuen valent (.shape, .info(), .value_counts(), .groupby(), .isna()). Aquestes són les que afegeix aquest quadern.",
  llista: [
    { nom: "pd.read_csv()", text: "La porta d'entrada. Mira sempre el resultat amb .head() i .info() abans de tocar res: un separador o un decimal mal llegit fa que una columna de números surti com a text." },
    { nom: 'df["col"] i df[["a", "b"]]', text: "Uns claudàtors et donen una Series; dos, un DataFrame. La diferència decideix quins mètodes pots fer servir després." },
    { nom: ".loc[] contra .iloc[]", text: ".loc va per etiquetes (el nom de la fila i de la columna), .iloc per posició. Després d'un filtre, les etiquetes ja no són 0, 1, 2..." },
    { nom: "df[(cond1) & (cond2)]", text: "Filtrar amb diverses condicions. Els parèntesis són obligatoris, i and/or no funcionen." },
    { nom: ".groupby().agg([...])", text: "Comparar grups amb diverses funcions alhora: mitjana, mediana i quants n'hi ha. El count et diu si una mitjana es pot creure." },
    { nom: ".dropna() i .fillna()", text: "Eliminar o omplir. Abans de triar, mira quantes files et costa cada opció." },
    { nom: ".sort_values()", text: "Ordenar per veure els extrems: allà hi ha els errors de dades i els casos interessants." },
    { nom: ".plot()", text: "Un gràfic en una línia, directament des del DataFrame o d'un groupby. Per mirar, no per presentar." },
    { nom: ".apply() i .map()", text: "Una funció pròpia fila a fila, o recodificar valors coneguts amb un diccionari." },
    { nom: 'X = df[cols], y = df["objectiu"]', text: "Del DataFrame al model: les columnes amb què prediràs i la que vols predir, numèriques i sense nuls." },
  ],
  tancament: "Pandas és per mirar i preparar les dades. Quan estan netes, el model rep X i y.",
};

const repasPp1 = [
  {
    titol: "1. Carregar i fer inventari",
    codi: `df = pd.read_csv(URL)
df.shape                                  # files, columnes
df.info(); df.head()                      # números o dates llegits com a text?
df.isna().sum()[df.isna().sum() > 0]      # només les columnes amb nuls
df.duplicated().sum()`,
  },
  {
    titol: "2. Comptar i comparar grups",
    codi: `df["col"].value_counts()                         # quants de cada
df["col"].value_counts(normalize=True) * 100     # percentatge
df.groupby("grup")["valor"].agg(["count", "sum", "mean", "median"])`,
    nota: "Mitjana contra mediana: si la mitjana és molt més gran, hi ha uns pocs valors enormes que l'arrosseguen. Explica-ho amb els números.",
  },
  {
    titol: "3. Rànquings i filtres",
    codi: `df["col"].value_counts().head(10)
df.groupby("x")["v"].mean().nlargest(10)         # o sort_values(ascending=False).head(10)
df[df["any"] == 2022]                            # filtra abans d'agrupar
df[df["zona"].isin(["A", "B"])]`,
  },
  {
    titol: "4. Dates",
    codi: `df["data"] = pd.to_datetime(df["data"], errors="coerce")
df["any"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["decada"] = df["any"] // 10 * 10
df["any"].value_counts().sort_index()            # quants per any, ORDENATS per any`,
    nota: "És el que menys heu practicat. Surt als reptes RE_103 i RE_105.",
  },
  {
    titol: "5. Gràfics",
    codi: `s.plot(kind="bar")   /   s.plot()             # una sèrie: barres o línies
df.plot(kind="scatter", x="x", y="y", alpha=0.3)
t = df.pivot_table(index="any", columns="tipus", values="v", aggfunc="mean")
t.plot()                                         # una línia per grup
plt.title("..."); plt.xlabel("..."); plt.ylabel("...")`,
    nota: "Sempre amb títol i eixos amb nom.",
  },
  {
    titol: "6. NumPy: vectors i distàncies",
    codi: `# un vector per any (o per mes), amb els forats a 0
# perquè els dos vectors tinguin la mateixa llargada
a =(df[df["zona"] == "A"].groupby("any")["v"].sum()
       .reindex(range(any_inici, any_fi + 1), fill_value=0).to_numpy())
b = ...
np.linalg.norm(a - b)                            # norma de la diferència
a / a.sum()                                      # normalitzar pel total abans de comparar

# distància de cada fila a un punt (lat0, lon0)
d = np.sqrt((lat - lat0)**2 + (lon - lon0)**2)
np.argsort(d)[:5]                                # els 5 més propers (o df.assign(d=d).nsmallest(5, "d"))`,
    nota: "L'error típic: sense el reindex, si a un dels dos li falta un any els vectors no fan la mateixa llargada i la resta peta.",
  },
];

const sospitesPp1 = [
  ["Text escrit de dues maneres", "majúscules, espais, accents. Mira-ho amb value_counts() i arregla-ho amb str.strip().str.upper()."],
  ["Nuls disfressats", "zeros, o coordenades (0, 0), que en realitat volen dir «no se sap»."],
  ["Valors impossibles", "anys del futur, o un període incomplet que per això sembla que baixa."],
  ["Números que arriben com a text", 'pd.to_numeric(df["col"], errors="coerce").'],
  ["Coses que haurien de ser-hi i no hi són", "una ciutat, un any."],
];

function RepasPp1() {
  return (
    <div className="space-y-4 text-sm text-gray-700">
      <p>
        Amb aquest repertori de Pandas i NumPy en tens prou. El que s'avalua és que el sàpigues
        encadenar i explicar cada resultat amb una frase.
      </p>
      {repasPp1.map((x) => (
        <div key={x.titol}>
          <p className="font-medium text-gray-900 mb-1">{x.titol}</p>
          <pre className="bg-gray-900 text-gray-100 rounded-lg p-3 overflow-x-auto text-xs">{x.codi}</pre>
          {x.nota && <p className="text-xs text-gray-600 mt-1">{x.nota}</p>}
        </div>
      ))}
      <div>
        <p className="font-medium text-gray-900 mb-1">7. Desconfia de les dades</p>
        <p className="mb-2">
          No resta si no ho veus, però suma si ho detectes i ho expliques.
        </p>
        <ul className="list-disc pl-5 space-y-1">
          {sospitesPp1.map(([t, d]) => (
            <li key={t}>
              <strong>{t}:</strong> {d}
            </li>
          ))}
        </ul>
      </div>
      <div className="bg-emerald-50 border-l-4 border-emerald-400 rounded-r-lg p-3 text-emerald-900">
        <p className="font-medium mb-1">8. Com es lliura</p>
        <ul className="list-disc pl-5 space-y-1">
          <li>A dalt del quadern, quina fitxa has triat.</li>
          <li>
            Cada resposta amb el seu codi i <strong>una frase que l'expliqui amb el número</strong>.
          </li>
          <li>Compta que el resultat surti del codi i que la frase el llegeixi bé.</li>
        </ul>
      </div>
    </div>
  );
}

function FuncionsFO00() {
  const f = funcionsFO00;
  return (
    <>
      <CinquePreguntes />
      <p className="mt-3 text-sm text-emerald-900 bg-emerald-50 border-l-4 border-emerald-400 rounded-r-lg p-3">
        Els atributs que acaben en guió baix, com .coef_ o .feature_importances_, volen dir «això ho
        he après de les dades». No existeixen abans de cridar .fit(), i buscar-los abans és el primer
        error que fa tothom.
      </p>
      <Chivato f={f} />
    </>
  );
}

export default function BlocDades() {
  return (
    <div className="space-y-8">
      <CapcaleraBloc num={1} icona={Table2} color={C}>
        Del Python bàsic a manejar una taula de dades amb NumPy i Pandas. Sense això, cap model del
        curs es pot entrenar contra res. Acaba amb la prova pràctica 1, el 27 d'octubre.
      </CapcaleraBloc>

      <PassosBloc color={C} />

      <Seccio titol="Per què aquest bloc va primer" icona={Table2} color={C}>
        <p className="text-gray-700">
          Ja has vist què fa un arbre de decisió o un k-NN. El que falta és l'eina per fer-los servir
          tu: carregar dades, mirar-les, filtrar-les i passar-les a un model. L'ordre no és casual:
          primer saber interrogar un objecte de Python per no anar a cegues, després NumPy, i Pandas
          al final perquè està construït a sobre de NumPy. Amb NumPy fet, el quadern d'àlgebra
          lineal ja no necessita res més.
        </p>
      </Seccio>

      <AbansDeComencar />

      {/* ---------- 1 · Aprèn ---------- */}
      <Pas id="apren" num={1} titol="Aprèn" color={C} subtitol="Quatre quaderns, en aquest ordre. Cada un té cel·les buides que són la teva feina." />

      <Seccio icona={BookOpen} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="FO_00" color={C}>
            <FuncionsFO00 />
          </QuadernCard>
          <QuadernCard codi="FO_01" color={C}>
            <Chivato f={funcionsFO01} />
          </QuadernCard>
          <QuadernCard codi="FO_02" color={C}>
            <Chivato f={funcionsFO02} />
          </QuadernCard>
          <QuadernCard codi="MA_01" color="violet" etiqueta="matemàtiques" />
        </div>
      </Seccio>

      <Seccio titol="A NumPy, and i or no funcionen amb màscares" icona={CircleSlash} color="rose">
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
      </Seccio>

      <Seccio titol="Repàs de Python: diccionaris, funcions i comprensions" icona={Code2} color={C}>
        <p className="text-gray-700 text-sm">
          La S10 tanca les peces de Python que encara falten i que els quaderns següents donen per
          fetes. Els quaderns d'aquesta sessió són al Moodle del centre. Per provar sintaxi solta, sense
          obrir cap quadern, tens{" "}
          <a href="https://www.pythonanywhere.com" target="_blank" rel="noopener noreferrer" className="text-emerald-700 font-medium hover:text-emerald-900">
            pythonanywhere.com
          </a>
          .
        </p>
      </Seccio>

      {/* ---------- 2 · Exemples ---------- */}
      <Pas id="exemples" num={2} titol="Exemples" color={C} subtitol="Exemples resolts: per veure com es fa abans de fer-ho tu." />

      <Seccio icona={Eye} color={C}>
        <p className="text-sm text-gray-700">
          L'exemple resolt d'aquest bloc és dins del primer quadern: l'FO_00 acaba amb una exploració
          de dades guiada de principi a fi, de carregar la taula a treure'n una conclusió. Mira-la
          sencera abans de començar els reptes. Si una eina no la coneixes, és a la{" "}
          <Link to="/recursos" className="text-emerald-700 font-medium hover:text-emerald-900 inline-flex items-center gap-1">
            <Wrench className="w-3.5 h-3.5" /> caixa d'eines
          </Link>
          .
        </p>
      </Seccio>

      {/* ---------- 3 · Reptes ---------- */}
      <Pas id="reptes" num={3} titol="Reptes" color={C} subtitol="Dades reals, una pregunta, i tu sol. Aquí és on es comprova si saps manejar dades." />
      <Seccio icona={Mountain} color={C}>
        <div className="space-y-4">
          <Reptes bloc={1} color={C} />
          <QuanCridar color={C} />
        </div>
      </Seccio>

      {/* ---------- 4 · Prova ---------- */}
      <Pas id="prova" num={4} titol="Prova" color={C} subtitol="La Pp1 (dimarts 27 d'octubre) és l'únic que s'avalua d'aquest bloc. Els quaderns i els reptes no es lliuren: són la pràctica per arribar-hi." />
      <Seccio icona={ClipboardCheck} color={C}>
        <ProvaBloc bloc={1} color={C} />
        <div className="mt-4">
          <ActivitatsBloc bloc={1} />
        </div>
        <p className="text-sm text-gray-700 mt-4">
          <strong>L'enunciat diu quines eines fer servir.</strong> El que s'avalua és que les sàpigues
          encadenar i llegir-ne el resultat, no que endevinis el nom d'un mètode. Si has fet els
          exercicis de Pandas i algun repte, ja has fet la prova abans.
        </p>
      </Seccio>

      <details className="group bg-white rounded-xl shadow-sm border border-gray-100">
        <summary className="flex items-center gap-3 p-6 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
          <ListChecks className="w-6 h-6 flex-shrink-0 text-emerald-600" />
          <h2 className="text-xl font-semibold text-gray-900 flex-1">Què has de saber per a la Pp1</h2>
          <ChevronDown className="w-5 h-5 text-gray-400 transition-transform group-open:rotate-180" />
        </summary>
        <div className="px-6 pb-6">
          <RepasPp1 />
        </div>
      </details>

      <SeguentBloc actual={1} />
    </div>
  );
}
