// El calendari del curs, una sola vegada. Tota la web en llegeix d'aquí:
// la portada (què toca aquesta setmana), el calendari i les pàgines de cada bloc.
// Font: docs/diagnostic-i-programacio-2627.md i docs/avaluacio-2627.md.

export const DADES_CURS = {
  hores: 68,
  sessions: 34,
  inici: "2026-09-21",
  final: "2027-02-02",
};

export const BLOCS = [
  { num: 1, titol: "Dades", llarg: "Python, NumPy i Pandas", ruta: "/dades", prova: "Pp1" },
  { num: 2, titol: "Supervisat", llarg: "Aprenentatge supervisat i la matemàtica de sota", ruta: "/supervisat", prova: "Pp2" },
  { num: 3, titol: "Dades brutes i no supervisat", llarg: "Pipelines, PCA i k-means", ruta: "/no-supervisat", prova: "Pp3" },
  { num: 4, titol: "Xarxes i RL", llarg: "Xarxes neuronals, Reinforcement Learning i el concurs", ruta: "/xarxes-i-rl", prova: "Pp4" },
];

// material i casa: codis de src/data/quaderns.js (o text lliure si no hi és).
export const SESSIONS = [
  // ---------- Bloc 1 · Dades ----------
  { s: "S01", data: "2026-09-21", bloc: 1, text: "Presentació del mòdul i bases de Python" },
  { s: "S02", data: "2026-09-22", bloc: 1, text: "Els models de ML, explorats les dues hores, amb el quadern d'Iris", material: ["ML_00"] },
  { s: "S03", data: "2026-09-28", bloc: 1, text: "Pràctica de Python i primer contacte amb els exercicis" },
  { s: "S04", data: "2026-09-29", bloc: 1, text: "Objectes de Python i primera anàlisi de dades: interrogar un objecte, atribut contra mètode, i una exploració guiada de principi a fi", material: ["FO_00"] },
  { s: "S05", data: "2026-10-05", bloc: 1, text: "NumPy 1: per què no llistes, l'array, indexació i llesques", material: ["FO_01"] },
  { s: "S06", data: "2026-10-06", bloc: 1, text: "NumPy 2: operacions, màscares booleanes, agregacions i eixos", material: ["FO_01"] },
  { s: "S07", data: "2026-10-13", bloc: 1, text: "Pandas 1: DataFrame i Series, carregar un CSV, loc i iloc", material: ["FO_02"], nota: "Recupera el dilluns 12, festiu: fa horari de dilluns." },
  { s: "S07b", data: "2026-10-14", bloc: 1, text: "Pandas 2: nuls, groupby, gràfics, i del DataFrame a X i y", material: ["FO_02"], nota: "Dimecres amb horari de dimarts." },
  { s: "S08", data: "2026-10-19", bloc: 1, text: "Prova escrita 1 i consolidació: exercicis 4 a 7 de Pandas i un assaig de la Pp1", material: ["FO_02"] },
  { s: "S09", data: "2026-10-20", bloc: 1, text: "Àlgebra lineal: norma, producte escalar, projecció, i que un model entrenat és un vector i una multiplicació", material: ["MA_01"], mates: true },
  { s: "S10", data: "2026-10-26", bloc: 1, text: "Diccionaris, funcions i comprensions de llista (quaderns al Moodle)" },
  { s: "S11", data: "2026-10-27", bloc: 1, text: "Prova pràctica 1 i tancament del bloc" },

  // ---------- Bloc 2 · Supervisat ----------
  { s: "S12", data: "2026-11-02", bloc: 2, text: "Entrenament i test, i per què se separen. Primer model complet", material: ["ML_00"] },
  { s: "S13", data: "2026-11-03", bloc: 2, text: "k veïns i la distància. El parany de les escales", material: ["ML_01"], casa: ["EX_01"] },
  { s: "S14", data: "2026-11-09", bloc: 2, text: "Arbres de decisió: la impuresa i la tria del tall", material: ["ML_02"] },
  { s: "S15", data: "2026-11-10", bloc: 2, text: "Entropia i informació: per què Gini, el guany d'informació, i que la log-loss i l'entropia creuada són el mateix número", material: ["MA_04"], mates: true },
  { s: "S16", data: "2026-11-16", bloc: 2, text: "Boscos aleatoris i mètriques: la precisió no serveix tota sola", material: ["ML_03"], casa: ["EX_02"] },
  { s: "S17", data: "2026-11-17", bloc: 2, text: "Regressió logística: la frontera, la sigmoide, i els pesos trobats per força bruta", material: ["ML_04"] },
  { s: "S18", data: "2026-11-23", bloc: 2, text: "Descens de gradient 1: què és una derivada, des de zero, i la derivada de la log-loss", material: ["MA_02"], mates: true },
  { s: "S19", data: "2026-11-24", bloc: 2, text: "Descens de gradient 2: la comprovació del gradient, l'entrenament amb bucle propi i la comparació amb scikit-learn", material: ["MA_02"], mates: true },
  { s: "S20", data: "2026-11-30", bloc: 2, text: "Probabilitat i versemblança: Bayes, d'on surt la log-loss, i Naive Bayes implementat de zero", material: ["MA_03"], mates: true },
  { s: "S21", data: "2026-12-01", bloc: 2, text: "SVM: el marge i el kernel. Prova pràctica 2", material: ["ML_05"], casa: ["EX_04"] },

  // ---------- Bloc 3 · Dades brutes i no supervisat ----------
  { s: "S22", data: "2026-12-07", bloc: 3, text: "Optimització amb restriccions: Lagrange, per què l'SVM depèn de pocs punts, i el kernel demostrat", material: ["MA_05"], mates: true, nota: "El dimarts 8 és festiu: aquesta setmana només hi ha dilluns." },
  { s: "S23", data: "2026-12-14", bloc: 3, text: "Dades brutes i pipelines: nuls, categòriques, i la fuita d'informació", material: ["EX_05", "EX_00"] },
  { s: "S24", data: "2026-12-15", bloc: 3, text: "PCA i vectors propis: la maledicció de la dimensionalitat, i reduir dimensions sense inventar-se res", material: ["MA_06"], mates: true },
  { s: "S25", data: "2026-12-21", bloc: 3, text: "k-means i les imatges com a taula. Prova pràctica 3", material: ["ML_06", "EX_03"], casa: ["EX_06"] },

  // ---------- Bloc 4 · Xarxes i RL ----------
  { s: "S26", data: "2027-01-11", bloc: 4, text: "Què és una xarxa neuronal, i que ja en saps el mecanisme: és el descens de gradient de les S18 i S19", material: ["DL_01", "DL_02"] },
  { s: "S27", data: "2027-01-12", bloc: 4, text: "PyTorch: tensors, autograd, arquitectures i entrenament", material: ["DL_02", "DL_03", "DL_04"] },
  { s: "S28", data: "2027-01-18", bloc: 4, text: "De la xarxa a l'agent: el pont cap a Reinforcement Learning", material: ["DL_05"] },
  { s: "S29", data: "2027-01-19", bloc: 4, text: "Fonaments de RL: l'agent, l'entorn, la recompensa", material: ["RL_01"] },
  { s: "S30", data: "2027-01-25", bloc: 4, text: "DQN i Gymnasium", material: ["RL_02"] },
  { s: "S31", data: "2027-01-26", bloc: 4, text: "Entrenament lliure: cadascú entrena el seu agent", material: ["CONCURS"] },
  { s: "S32", data: "2027-02-01", bloc: 4, text: "Entrenament lliure i ajust. Es tanca el lliurament dels agents", material: ["CONCURS"] },
  { s: "S33", data: "2027-02-02", bloc: 4, text: "El concurs i la defensa de l'agent", concurs: true },
];

// Les proves, amb la sessió on cauen.
export const PROVES = [
  { codi: "Pe1", tipus: "escrita", s: "S08", data: "2026-10-19", bloc: 1, titol: "Atribut contra mètode, què retorna cada cosa, què vol dir axis" },
  { codi: "Pp1", tipus: "practica", s: "S11", data: "2026-10-27", bloc: 1, titol: "Pots manejar dades?", detall: "Un CSV que no has vist: carregar-lo, files i columnes, inventari de nuls, dues preguntes amb groupby, un gràfic, i una norma o una distància amb NumPy." },
  { codi: "Pe2", tipus: "escrita", s: "S14", data: "2026-11-09", bloc: 2, titol: "Per què es parteix el conjunt, què és el sobreajust, què vol dir que un model «encerti»" },
  { codi: "Pe3", tipus: "escrita", s: "S20", data: "2026-11-30", bloc: 2, titol: "Què és una derivada aquí, què fa el descens de gradient, per què la log-loss" },
  { codi: "Pp2", tipus: "practica", s: "S21", data: "2026-12-01", bloc: 2, titol: "Pots entrenar, mesurar i verificar?", detall: "Sobre un conjunt que no has vist: dos models comparats amb la mètrica adequada, una funció de pèrdua implementada i comprovada contra scikit-learn, i explicar per què un model prediu el que prediu mirant-ne els pesos o les importàncies." },
  { codi: "Pp3", tipus: "practica", s: "S25", data: "2026-12-21", bloc: 3, titol: "Pots treballar sense enganyar-te?", detall: "Un CSV brut, amb nuls, columnes de text i duplicats. Un Pipeline que no filtri informació del test a l'entrenament, entrenar, i justificar les decisions de neteja. Es mesura si el número és honest, no si és alt." },
  { codi: "Pe4", tipus: "escrita", s: "S28", data: "2027-01-18", bloc: 4, titol: "Què és una xarxa, per què la retropropagació és el gradient, què és una Q-xarxa", nota: "La més important de les cinc" },
  { codi: "Pe5", tipus: "escrita", s: "S31", data: "2027-01-26", bloc: 4, titol: "Agent, entorn, recompensa, exploració contra explotació" },
  { codi: "Pp4", tipus: "practica", s: "S33", data: "2027-02-02", bloc: 4, titol: "L'agent i la seva defensa davant del grup", detall: "L'agent lliurat, que funcioni, i que puguis explicar quina recompensa vas dissenyar i per què, què vas provar i què vas descartar. No es puntua la posició al marcador." },
];

// Les activitats: es qualifiquen 0 o 10 i vencen el diumenge de la setmana en què es donen.
export const ACTIVITATS = [
  { codi: "A01", nom: "FO_00 · objectes de Python", s: "S04", venc: "2026-10-04" },
  { codi: "A02", nom: "FO_01 · NumPy, exercicis 1 a 3", s: "S05", venc: "2026-10-11" },
  { codi: "A03", nom: "FO_01 · NumPy, exercicis 4 a 7", s: "S06", venc: "2026-10-11" },
  { codi: "A04", nom: "FO_02 · Pandas, exercicis 1 a 3", s: "S07", venc: "2026-10-18" },
  { codi: "A05", nom: "FO_02 · Pandas, exercicis 4 a 7", s: "S07b", venc: "2026-10-25" },
  { codi: "A06", nom: "MA_01 · àlgebra lineal", s: "S09", venc: "2026-10-25" },
  { codi: "A07", nom: "Diccionaris, funcions i comprensions", s: "S10", venc: "2026-11-01" },
  { codi: "A08", nom: "ML_01 · k veïns més propers", s: "S13", venc: "2026-11-08" },
  { codi: "A09", nom: "EX_01 · Wine", s: "S13", venc: "2026-11-08" },
  { codi: "A10", nom: "ML_02 · arbres de decisió", s: "S14", venc: "2026-11-15" },
  { codi: "A11", nom: "MA_04 · entropia i informació", s: "S15", venc: "2026-11-15" },
  { codi: "A12", nom: "ML_03 · boscos aleatoris", s: "S16", venc: "2026-11-22" },
  { codi: "A13", nom: "EX_02 · càncer de mama", s: "S16", venc: "2026-11-22" },
  { codi: "A14", nom: "ML_04 · regressió logística", s: "S17", venc: "2026-11-22" },
  { codi: "A15", nom: "MA_02 · gradient, la part conceptual", s: "S18", venc: "2026-11-29" },
  { codi: "A16", nom: "MA_02 · gradient, la part de fer-ho", s: "S19", venc: "2026-11-29" },
  { codi: "A17", nom: "MA_03 · probabilitat i versemblança", s: "S20", venc: "2026-12-06" },
  { codi: "A18", nom: "ML_05 · màquines de vectors de suport", s: "S21", venc: "2026-12-06" },
  { codi: "A19", nom: "EX_04 · la forma de cada model", s: "S21", venc: "2026-12-06" },
  { codi: "A20", nom: "MA_05 · marge i optimització", s: "S22", venc: "2026-12-13" },
  { codi: "A21", nom: "EX_05 · quan les dades no vénen netes", s: "S23", venc: "2026-12-20" },
  { codi: "A22", nom: "MA_06 · PCA i vectors propis", s: "S24", venc: "2026-12-20" },
  { codi: "A23", nom: "EX_03 · xifres escrites a mà", s: "S25", venc: "2027-01-10", nota: "Salta les vacances de Nadal" },
  { codi: "A24", nom: "De PyTorch a DQN", s: "S27", venc: "2027-01-17" },
  { codi: "A25", nom: "Q-learning amb el Taxi", s: "S29", venc: "2027-01-24" },
];

export const FESTIUS = [
  { quan: "12 d'octubre", text: "Cau en dilluns de classe, però es recupera: el dimarts 13 fa horari de dilluns (S07) i el dimecres 14, de dimarts (S07b)." },
  { quan: "8 de desembre", text: "Cau en dimarts de classe. Aquella setmana només hi ha la sessió del dilluns, la S22." },
  { quan: "Nadal", text: "Del 22 de desembre al 7 de gener no hi ha classe. El curs es reprèn amb la S26, l'11 de gener." },
];

// ---------- Dates ----------

const DIES_CURT = ["dg", "dl", "dt", "dc", "dj", "dv", "ds"];
const DIES_LLARG = ["diumenge", "dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte"];
const MESOS_CURT = ["gen", "feb", "març", "abr", "maig", "juny", "jul", "ag", "set", "oct", "nov", "des"];
const MESOS_DE = ["de gener", "de febrer", "de març", "d'abril", "de maig", "de juny", "de juliol", "d'agost", "de setembre", "d'octubre", "de novembre", "de desembre"];

export function aData(iso) {
  const [a, m, d] = iso.split("-").map(Number);
  return new Date(a, m - 1, d);
}

export function isoAvui(ara = new Date()) {
  const p = (n) => String(n).padStart(2, "0");
  return `${ara.getFullYear()}-${p(ara.getMonth() + 1)}-${p(ara.getDate())}`;
}

export const dataCurta = (iso) => {
  const d = aData(iso);
  return `${DIES_CURT[d.getDay()]} ${d.getDate()} ${MESOS_CURT[d.getMonth()]}`;
};

export const dataLlarga = (iso) => {
  const d = aData(iso);
  return `${DIES_LLARG[d.getDay()]} ${d.getDate()} ${MESOS_DE[d.getMonth()]}`;
};

export function diesFins(iso, avui = isoAvui()) {
  return Math.round((aData(iso) - aData(avui)) / 86400000);
}

export function estatSessio(ses, avui = isoAvui()) {
  if (ses.data < avui) return "feta";
  if (ses.data === avui) return "avui";
  return "pendent";
}

// Dilluns i diumenge de la setmana d'una data (ISO).
export function setmanaDe(iso) {
  const d = aData(iso);
  const desdeDilluns = (d.getDay() + 6) % 7;
  const dl = new Date(d.getFullYear(), d.getMonth(), d.getDate() - desdeDilluns);
  const dg = new Date(dl.getFullYear(), dl.getMonth(), dl.getDate() + 6);
  return { dilluns: isoAvui(dl), diumenge: isoAvui(dg) };
}

export const sessio = (codi) => SESSIONS.find((x) => x.s === codi);
export const provesDeSessio = (codi) => PROVES.filter((p) => p.s === codi);
export const activitatsDeSessio = (codi) => ACTIVITATS.filter((a) => a.s === codi);
export const sessionsDelBloc = (num) => SESSIONS.filter((x) => x.bloc === num);
export const provesDelBloc = (num) => PROVES.filter((p) => p.bloc === num);
