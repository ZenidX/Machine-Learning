import {
  ClipboardCheck,
  CalendarRange,
  AlertTriangle,
  Trophy,
  ListChecks,
  Percent,
} from "lucide-react";
import { Link } from "react-router-dom";

const ACTIVITAT = "activitat";
const ESCRITA = "escrita";
const PRACTICA = "practica";

const estils = {
  [ACTIVITAT]: {
    etiqueta: "Activitat",
    punt: "bg-gray-300",
    xip: "bg-gray-100 text-gray-700 border-gray-200",
    fila: "border-gray-200",
  },
  [ESCRITA]: {
    etiqueta: "Prova escrita",
    punt: "bg-amber-400",
    xip: "bg-amber-50 text-amber-800 border-amber-200",
    fila: "border-amber-200 bg-amber-50/40",
  },
  [PRACTICA]: {
    etiqueta: "Prova pràctica",
    punt: "bg-rose-500",
    xip: "bg-rose-50 text-rose-800 border-rose-200",
    fila: "border-rose-200 bg-rose-50/40",
  },
};

const blocs = [
  {
    titol: "Bloc 1 · Fonaments de dades",
    periode: "29 de setembre – 27 d'octubre",
    files: [
      { tipus: ACTIVITAT, codi: "A01", nom: "FO_00 · objectes de Python", surt: "S04 · 29 set", venc: "dg 4 d'octubre" },
      { tipus: ACTIVITAT, codi: "A02", nom: "FO_01 · NumPy, exercicis 1 a 3", surt: "S05 · 5 oct", venc: "dg 11 d'octubre" },
      { tipus: ACTIVITAT, codi: "A03", nom: "FO_01 · NumPy, exercicis 4 a 7", surt: "S06 · 6 oct", venc: "dg 11 d'octubre" },
      { tipus: ACTIVITAT, codi: "A04", nom: "FO_02 · Pandas, exercicis 1 a 3", surt: "S07 · 13 oct", venc: "dg 18 d'octubre" },
      { tipus: ESCRITA, codi: "Pe1", nom: "Atribut contra mètode, què retorna cada cosa, què vol dir axis", surt: "S08 · dl 19 oct", venc: "a classe" },
      { tipus: ACTIVITAT, codi: "A05", nom: "FO_02 · Pandas, exercicis 4 a 7", surt: "S08 · 19 oct", venc: "dg 25 d'octubre" },
      { tipus: ACTIVITAT, codi: "A06", nom: "MA_01 · àlgebra lineal", surt: "S09 · 20 oct", venc: "dg 25 d'octubre" },
      { tipus: ACTIVITAT, codi: "A07", nom: "Diccionaris, funcions i comprensions", surt: "S10 · 26 oct", venc: "dg 1 de novembre" },
      { tipus: PRACTICA, codi: "Pp1", nom: "Pots manejar dades? Un CSV que no has vist: carregar, nuls, groupby i un gràfic", surt: "S11 · dt 27 oct", venc: "a classe" },
    ],
  },
  {
    titol: "Bloc 2 · Supervisat i la matemàtica que hi ha a sota",
    periode: "2 de novembre – 1 de desembre",
    files: [
      { tipus: ACTIVITAT, codi: "A08", nom: "ML_01 · k veïns més propers", surt: "S13 · 3 nov", venc: "dg 8 de novembre" },
      { tipus: ACTIVITAT, codi: "A09", nom: "EX_01 · Wine", surt: "S13 · a casa", venc: "dg 8 de novembre" },
      { tipus: ESCRITA, codi: "Pe2", nom: "Per què es parteix el conjunt, què és el sobreajust", surt: "S14 · dl 9 nov", venc: "a classe" },
      { tipus: ACTIVITAT, codi: "A10", nom: "ML_02 · arbres de decisió", surt: "S14 · 9 nov", venc: "dg 15 de novembre" },
      { tipus: ACTIVITAT, codi: "A11", nom: "MA_04 · entropia i informació", surt: "S15 · 10 nov", venc: "dg 15 de novembre" },
      { tipus: ACTIVITAT, codi: "A12", nom: "ML_03 · boscos aleatoris", surt: "S16 · 16 nov", venc: "dg 22 de novembre" },
      { tipus: ACTIVITAT, codi: "A13", nom: "EX_02 · càncer de mama", surt: "S16 · a casa", venc: "dg 22 de novembre" },
      { tipus: ACTIVITAT, codi: "A14", nom: "ML_04 · regressió logística", surt: "S17 · 17 nov", venc: "dg 22 de novembre" },
      { tipus: ACTIVITAT, codi: "A15", nom: "MA_02 · gradient, la part conceptual", surt: "S18 · 23 nov", venc: "dg 29 de novembre" },
      { tipus: ACTIVITAT, codi: "A16", nom: "MA_02 · gradient, la part de fer-ho", surt: "S19 · 24 nov", venc: "dg 29 de novembre" },
      { tipus: ESCRITA, codi: "Pe3", nom: "Què és una derivada aquí, què fa el descens de gradient, per què la log-loss", surt: "S20 · dl 30 nov", venc: "a classe" },
      { tipus: ACTIVITAT, codi: "A17", nom: "MA_03 · probabilitat i versemblança", surt: "S20 · 30 nov", venc: "dg 6 de desembre" },
      { tipus: ACTIVITAT, codi: "A18", nom: "ML_05 · màquines de vectors de suport", surt: "S21 · 1 des", venc: "dg 6 de desembre" },
      { tipus: ACTIVITAT, codi: "A19", nom: "EX_04 · la forma de cada model", surt: "S21 · a casa", venc: "dg 6 de desembre" },
      { tipus: PRACTICA, codi: "Pp2", nom: "Pots entrenar, mesurar i verificar? Dos models amb la mètrica adequada, i una funció de pèrdua implementada i comprovada", surt: "S21 · dt 1 des", venc: "a classe" },
    ],
  },
  {
    titol: "Bloc 3 · Optimització, dades reals i no supervisat",
    periode: "7 – 21 de desembre",
    files: [
      { tipus: ACTIVITAT, codi: "A20", nom: "MA_05 · marge i optimització", surt: "S22 · 7 des", venc: "dg 13 de desembre" },
      { tipus: ACTIVITAT, codi: "A21", nom: "EX_05 · quan les dades no vénen netes", surt: "S23 · 14 des", venc: "dg 20 de desembre" },
      { tipus: ACTIVITAT, codi: "A22", nom: "MA_06 · PCA i vectors propis", surt: "S24 · 15 des", venc: "dg 20 de desembre" },
      { tipus: ACTIVITAT, codi: "A23", nom: "EX_03 · xifres escrites a mà", surt: "S25 · 21 des", venc: "dg 11 de gener", nota: "Salta les vacances de Nadal" },
      { tipus: PRACTICA, codi: "Pp3", nom: "Pots treballar sense enganyar-te? Un CSV brut i un Pipeline que no filtri informació", surt: "S25 · dl 21 des", venc: "a classe" },
    ],
  },
  {
    titol: "Blocs 4 i 5 · Xarxes neuronals, RL i el concurs",
    periode: "11 de gener – 2 de febrer",
    files: [
      { tipus: ACTIVITAT, codi: "A24", nom: "De PyTorch a DQN", surt: "S27 · 12 gen", venc: "dg 17 de gener" },
      { tipus: ESCRITA, codi: "Pe4", nom: "Què és una xarxa, per què la retropropagació és el gradient, què és una Q-xarxa", surt: "S28 · dl 18 gen", venc: "a classe", nota: "La més important de les cinc" },
      { tipus: ACTIVITAT, codi: "A25", nom: "Q-learning amb el Taxi", surt: "S29 · 19 gen", venc: "dg 24 de gener" },
      { tipus: ESCRITA, codi: "Pe5", nom: "Agent, entorn, recompensa, exploració contra explotació", surt: "S31 · dt 26 gen", venc: "a classe" },
      { tipus: ACTIVITAT, codi: "—", nom: "Lliurament de l'agent del concurs", surt: "S32 · dl 1 feb", venc: "al final de la sessió", nota: "Es tanca el lliurament: l'endemà es competeix amb el que hi hagi" },
      { tipus: PRACTICA, codi: "Pp4", nom: "L'agent i la seva defensa davant del grup", surt: "S33 · dt 2 feb", venc: "a classe" },
    ],
  },
];

function Fila({ f }) {
  const e = estils[f.tipus];
  return (
    <div className={`border rounded-lg p-4 ${e.fila}`}>
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2">
        <div className="flex gap-3">
          <span className={`mt-1.5 w-2 h-2 rounded-full flex-shrink-0 ${e.punt}`} />
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className={`text-xs font-medium px-2 py-0.5 rounded border ${e.xip}`}>
                {e.etiqueta}
              </span>
              {f.codi !== "—" && (
                <code className="text-xs font-medium text-gray-500">{f.codi}</code>
              )}
            </div>
            <p className="text-sm text-gray-900">{f.nom}</p>
            {f.nota && <p className="text-xs text-gray-500 mt-1">{f.nota}</p>}
          </div>
        </div>
        <div className="sm:text-right flex-shrink-0 pl-5 sm:pl-0">
          <p className="text-xs text-gray-500">{f.surt}</p>
          <p className="text-sm font-medium text-gray-900 whitespace-nowrap">{f.venc}</p>
        </div>
      </div>
    </div>
  );
}

export default function Avaluacio() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Avaluació i calendari</h1>
        <p className="mt-2 text-lg text-gray-600">
          Què es lliura, quan, i quant compta cada cosa.
        </p>
      </div>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Percent className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Com es calcula la nota</h2>
        </div>
        <div className="grid sm:grid-cols-3 gap-4">
          <div className="border border-rose-200 bg-rose-50/40 rounded-lg p-4">
            <p className="text-3xl font-bold text-rose-700">80 %</p>
            <p className="font-medium text-gray-900 mt-1">4 proves pràctiques</p>
            <p className="text-sm text-gray-600 mt-1">
              Amb ordinador, i <strong>semblants als exercicis de classe</strong> o variacions
              seves. Cal un mínim de 5 a cadascuna.
            </p>
          </div>
          <div className="border border-amber-200 bg-amber-50/40 rounded-lg p-4">
            <p className="text-3xl font-bold text-amber-700">10 %</p>
            <p className="font-medium text-gray-900 mt-1">5 proves escrites</p>
            <p className="text-sm text-gray-600 mt-1">
              Curtes, a l'inici de sessió, sense ordinador. Han de superar el 3 per poder
              ponderar.
            </p>
          </div>
          <div className="border border-gray-200 bg-gray-50 rounded-lg p-4">
            <p className="text-3xl font-bold text-gray-700">10 %</p>
            <p className="font-medium text-gray-900 mt-1">25 activitats</p>
            <p className="text-sm text-gray-600 mt-1">
              Els quaderns amb les cel·les buides. Es qualifiquen <strong>0 o 10</strong>: només
              cal lliurar-les.
            </p>
          </div>
        </div>
      </section>

      <section className="bg-rose-50 border border-rose-200 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-rose-600" />
          <h2 className="text-xl font-semibold text-rose-900">
            Tres coses que et poden costar el curs
          </h2>
        </div>
        <ul className="space-y-3 text-sm text-rose-900">
          <li>
            <strong>Lliurar una activitat fora de termini compta com a negativa</strong>, no com
            a no lliurada. No és el mateix, i amb 25 activitats es nota.
          </li>
          <li>
            <strong>Les proves pràctiques demanen un mínim de 5.</strong> La primera és el 27
            d'octubre i ja compta: no és un assaig.
          </li>
          <li>
            <strong>No presentar-se a una prova sense justificar-ho</strong> suposa perdre el
            dret a fer-la.
          </li>
        </ul>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-3">
          <ClipboardCheck className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Per què les proves cauen on cauen
          </h2>
        </div>
        <p className="text-gray-700 text-sm mb-3">
          Cap prova pregunta què has après la setmana passada. Pregunta{" "}
          <strong>si tens el que et cal per al que ve ara</strong>. El curs acaba amb un agent
          competint, i per arribar-hi fan falta unes quantes peces que no es poden saltar.
        </p>
        <div className="grid sm:grid-cols-2 gap-3">
          {[
            ["Pp1 · 27 d'octubre", "Pots manejar dades? Sense això, tot el bloc següent es fa a cegues."],
            ["Pp2 · 1 de desembre", "Pots entrenar, mesurar i verificar? Qui no hi arribi, al gener no entendrà què fa una xarxa."],
            ["Pp3 · 21 de desembre", "Pots treballar sense enganyar-te? Aquí no es mesura la precisió, es mesura si el número és honest."],
            ["Pp4 · 2 de febrer", "L'agent que has entrenat, i saber explicar per què l'has fet així."],
          ].map(([t, d]) => (
            <div key={t} className="border border-gray-200 rounded-lg p-3">
              <p className="font-medium text-gray-900 text-sm">{t}</p>
              <p className="text-sm text-gray-600 mt-0.5">{d}</p>
            </div>
          ))}
        </div>
        <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4">
          <p className="text-sm text-amber-900">
            <strong>I les escrites van just abans de cada salt.</strong> Valen un 2 % cadascuna,
            o sigui que la seva feina no és posar-te nota: és que tu i el professor sapigueu si
            t'estàs despenjant mentre encara es pot fer alguna cosa.
          </p>
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-5">
          <CalendarRange className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">El calendari sencer</h2>
        </div>
        <p className="text-sm text-gray-600 mb-5">
          Les activitats <strong>vencen sempre el diumenge de la setmana en què es donen</strong>.
          És l'única regla, i no té excepcions més enllà de les vacances de Nadal.
        </p>
        <div className="space-y-7">
          {blocs.map((b) => (
            <div key={b.titol}>
              <div className="flex flex-wrap items-baseline gap-x-3 mb-3 pb-2 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">{b.titol}</h3>
                <span className="text-sm text-gray-500">{b.periode}</span>
              </div>
              <div className="space-y-2">
                {b.files.map((f) => (
                  <Fila key={b.titol + f.codi + f.nom} f={f} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <Trophy className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-semibold text-gray-900">La quarta prova pràctica és el concurs</h2>
        </div>
        <div className="space-y-3 text-gray-700 text-sm">
          <p>
            El 2 de febrer els agents que heu entrenat competeixen projectats a classe. Però{" "}
            <strong>el que es qualifica no és la posició al marcador</strong>: és l'agent lliurat,
            que funcioni, i que puguis explicar davant del grup quina recompensa vas dissenyar i
            per què.
          </p>
          <p>
            Guanyar el concurs és el premi, no la nota. Si fos la nota, guanyaria qui tingui
            millor portàtil.
          </p>
        </div>
      </section>

      <section className="bg-gray-50 border border-gray-200 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-3">
          <ListChecks className="w-6 h-6 text-gray-600" />
          <h2 className="text-lg font-semibold text-gray-900">On trobes cada cosa</h2>
        </div>
        <div className="flex flex-wrap gap-3 text-sm">
          <Link to="/fonaments" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Fonaments de dades
          </Link>
          <span className="text-gray-300">·</span>
          <Link to="/matematiques" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Matemàtiques
          </Link>
          <span className="text-gray-300">·</span>
          <Link to="/practica" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Pràctica i caixa d'eines
          </Link>
          <span className="text-gray-300">·</span>
          <Link to="/programa" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Programa sessió a sessió
          </Link>
        </div>
      </section>
    </div>
  );
}
