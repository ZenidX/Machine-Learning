import { Link } from "react-router-dom";
import { Table2, ChevronRight, CircleSlash, BookOpen, Eye, Mountain, ClipboardCheck, Code2, Wrench } from "lucide-react";
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

function Chivato({ f }) {
  return (
    <details className="mt-3 group rounded-lg border border-gray-200 bg-gray-50">
      <summary className="flex cursor-pointer list-none items-center gap-2 p-3 text-sm font-medium text-gray-800 hover:bg-gray-100 rounded-lg">
        <ChevronRight className="w-4 h-4 flex-shrink-0 transition-transform group-open:rotate-90" />
        {f.titol}
      </summary>
      <div className="border-t border-gray-200 p-4 space-y-3">
        <p className="text-sm text-gray-600">{f.intro}</p>
        <ol className="space-y-2">
          {f.llista.map((x, n) => (
            <li key={x.nom} className="flex gap-3 text-sm">
              <span className="flex-shrink-0 font-medium text-gray-400 tabular-nums">{n + 1}.</span>
              <span>
                <code className="bg-white border border-gray-200 px-1.5 py-0.5 rounded text-xs text-gray-900">{x.nom}</code>
                <span className="ml-2 text-gray-700">{x.text}</span>
              </span>
            </li>
          ))}
        </ol>
        {f.describe && <p className="text-sm text-gray-600 border-t border-gray-200 pt-3">{f.describe}</p>}
        <p className="text-sm font-medium text-gray-900">{f.tancament}</p>
      </div>
    </details>
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
      <Pas id="prova" num={4} titol="Prova" color={C} subtitol="La Pp1 és la porta del bloc 2 i ja compta amb mínim de 5: no és un assaig." />
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

      <SeguentBloc actual={1} />
    </div>
  );
}
