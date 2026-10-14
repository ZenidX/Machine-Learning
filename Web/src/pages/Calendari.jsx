import { Link } from "react-router-dom";
import {
  CalendarRange,
  Percent,
  AlertTriangle,
  ClipboardCheck,
  PenLine,
  Trophy,
  Sigma,
  CheckCircle2,
  Clock,
  CalendarDays,
  ListChecks,
} from "lucide-react";
import { NavInterna } from "../components/Bloc";
import {
  SESSIONS,
  BLOCS,
  FESTIUS,
  DADES_CURS,
  provesDeSessio,
  activitatsDeSessio,
  estatSessio,
  dataCurta,
  isoAvui,
} from "../data/curs";

const dadesFermes = [
  { etiqueta: "Hores", valor: `${DADES_CURS.hores} h` },
  { etiqueta: "Sessions", valor: `${DADES_CURS.sessions} de 2 h` },
  { etiqueta: "Per setmana", valor: "4 h" },
  { etiqueta: "Dies", valor: "dilluns i dimarts" },
  { etiqueta: "Del", valor: "21 set 2026" },
  { etiqueta: "Al", valor: "2 feb 2027" },
];

const index = [
  { id: "nota", label: "La nota" },
  { id: "perill", label: "Què et pot costar el curs" },
  { id: "proves", label: "Les proves" },
  { id: "sessions", label: "Sessió a sessió" },
  { id: "festius", label: "Festius" },
];

function Xip({ children, className }) {
  return (
    <span className={`inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded border ${className}`}>
      {children}
    </span>
  );
}

function FilaSessio({ ses, avui }) {
  const estat = estatSessio(ses, avui);
  const proves = provesDeSessio(ses.s);
  const activitats = activitatsDeSessio(ses.s);
  const fons =
    estat === "avui"
      ? "border-primary-300 bg-primary-50"
      : estat === "feta"
        ? "border-gray-100 bg-gray-50/60"
        : "border-gray-200 bg-white";
  return (
    <div className={`border rounded-lg p-4 flex flex-col sm:flex-row sm:items-start gap-3 ${fons}`}>
      <div className="flex items-center gap-3 sm:w-40 flex-shrink-0">
        <span
          className={`inline-flex items-center justify-center w-12 h-8 rounded-md text-sm font-bold ${
            estat === "avui"
              ? "bg-primary-600 text-white"
              : estat === "feta"
                ? "bg-gray-300 text-gray-700"
                : "bg-gray-800 text-white"
          }`}
        >
          {ses.s}
        </span>
        <span className="text-sm text-gray-600 whitespace-nowrap">{dataCurta(ses.data)}</span>
      </div>
      <div className="min-w-0 flex-1">
        <p className={`text-sm ${estat === "feta" ? "text-gray-500" : "text-gray-800"}`}>{ses.text}</p>
        {ses.nota && <p className="text-xs text-gray-500 mt-1">{ses.nota}</p>}
        <div className="flex flex-wrap items-center gap-1.5 mt-2">
          {estat === "feta" && (
            <span className="inline-flex items-center gap-1 text-xs text-gray-500">
              <CheckCircle2 className="w-3.5 h-3.5" /> feta
            </span>
          )}
          {estat === "avui" && (
            <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary-700">
              <Clock className="w-3.5 h-3.5" /> avui
            </span>
          )}
          {ses.mates && (
            <Xip className="bg-violet-50 text-violet-700 border-violet-200">
              <Sigma className="w-3 h-3" /> matemàtiques
            </Xip>
          )}
          {proves.map((p) => (
            <Xip
              key={p.codi}
              className={p.tipus === "practica" ? "bg-rose-50 text-rose-800 border-rose-200" : "bg-amber-50 text-amber-800 border-amber-200"}
            >
              {p.tipus === "practica" ? <ClipboardCheck className="w-3 h-3" /> : <PenLine className="w-3 h-3" />}
              {p.codi}
            </Xip>
          ))}
          {ses.concurs && (
            <Xip className="bg-amber-50 text-amber-800 border-amber-200">
              <Trophy className="w-3 h-3" /> concurs
            </Xip>
          )}
          {(ses.material || []).map((m) => (
            <code key={m} className="text-xs bg-white border border-gray-200 text-gray-600 px-1.5 py-0.5 rounded">
              {m}
            </code>
          ))}
          {(ses.casa || []).map((m) => (
            <span key={m} className="text-xs text-gray-600">
              exemple: <code className="bg-white border border-gray-200 px-1.5 py-0.5 rounded">{m}</code>
            </span>
          ))}
          {activitats.map((a) => (
            <Xip key={a.codi} className="bg-gray-100 text-gray-700 border-gray-200">
              {a.codi} · venç {dataCurta(a.venc)}
            </Xip>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function Calendari() {
  const avui = isoAvui();
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <CalendarRange className="w-8 h-8 text-primary-600" />
          <h1 className="text-3xl font-bold text-gray-900">Calendari i avaluació</h1>
        </div>
        <p className="text-gray-600 max-w-3xl">
          Què es fa cada dia, què es lliura, quan són les proves i quant compta cada cosa. És l'únic
          calendari del curs: la portada i les pàgines dels blocs en llegeixen d'aquí.
        </p>
      </div>

      <section className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 space-y-4">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {dadesFermes.map((d) => (
            <div key={d.etiqueta} className="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p className="text-xs uppercase tracking-wide text-gray-500">{d.etiqueta}</p>
              <p className="font-semibold text-gray-900">{d.valor}</p>
            </div>
          ))}
        </div>
        <NavInterna items={index} />
      </section>

      <section id="nota" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 scroll-mt-20">
        <div className="flex items-center gap-3 mb-4">
          <Percent className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Com es calcula la nota</h2>
        </div>
        <div className="grid sm:grid-cols-3 gap-4">
          <div className="border border-rose-200 bg-rose-50/40 rounded-lg p-4">
            <p className="text-3xl font-bold text-rose-700">80 %</p>
            <p className="font-medium text-gray-900 mt-1">4 proves pràctiques</p>
            <p className="text-sm text-gray-600 mt-1">
              Amb ordinador, i <strong>semblants a les activitats i els reptes</strong> o variacions
              seves. Cal un mínim de 5 a cadascuna.
            </p>
          </div>
          <div className="border border-amber-200 bg-amber-50/40 rounded-lg p-4">
            <p className="text-3xl font-bold text-amber-700">10 %</p>
            <p className="font-medium text-gray-900 mt-1">5 proves escrites</p>
            <p className="text-sm text-gray-600 mt-1">
              Curtes, a l'inici de sessió, sense ordinador. Han de superar el 3 per poder ponderar.
            </p>
          </div>
          <div className="border border-gray-200 bg-gray-50 rounded-lg p-4">
            <p className="text-3xl font-bold text-gray-700">10 %</p>
            <p className="font-medium text-gray-900 mt-1">25 activitats</p>
            <p className="text-sm text-gray-600 mt-1">
              Quaderns lliurats. Es qualifiquen <strong>0 o 10</strong>: només cal lliurar-los a temps.
            </p>
          </div>
        </div>
        <pre className="mt-4 bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto text-xs sm:text-sm">{`Nota = 10 % · mitjana(Pe1…Pe5)
     + 10 % · mitjana(A01…A25)
     + 80 % · mitjana(Pp1…Pp4)`}</pre>
      </section>

      <section id="perill" className="bg-rose-50 border border-rose-200 rounded-xl p-6 scroll-mt-20">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-rose-600" />
          <h2 className="text-xl font-semibold text-rose-900">Tres coses que et poden costar el curs</h2>
        </div>
        <ul className="space-y-3 text-sm text-rose-900">
          <li>
            <strong>Lliurar una activitat fora de termini compta com a negativa</strong>, no com a no
            lliurada. No és el mateix, i amb 25 activitats es nota.
          </li>
          <li>
            <strong>Les proves pràctiques demanen un mínim de 5.</strong> La primera és el 27
            d'octubre i ja compta: no és un assaig.
          </li>
          <li>
            <strong>No presentar-se a una prova sense justificar-ho</strong> suposa perdre el dret a
            fer-la.
          </li>
        </ul>
      </section>

      <section id="proves" className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 scroll-mt-20">
        <div className="flex items-center gap-3 mb-3">
          <ClipboardCheck className="w-6 h-6 text-indigo-600" />
          <h2 className="text-xl font-semibold text-gray-900">Per què les proves cauen on cauen</h2>
        </div>
        <p className="text-gray-700 text-sm mb-3">
          Cap prova pregunta què has après la setmana passada. Pregunta{" "}
          <strong>si tens el que et cal per al que ve ara</strong>. El curs acaba amb un agent
          competint, i per arribar-hi fan falta unes quantes peces que no es poden saltar.
        </p>
        <div className="grid sm:grid-cols-2 gap-3">
          {BLOCS.map((b) => {
            const textos = {
              Pp1: "Pots manejar dades? Sense això, tot el bloc següent es fa a cegues.",
              Pp2: "Pots entrenar, mesurar i verificar? Qui no hi arribi, al gener no entendrà què fa una xarxa.",
              Pp3: "Pots treballar sense enganyar-te? Aquí no es mesura la precisió, es mesura si el número és honest.",
              Pp4: "L'agent que has entrenat, i saber explicar per què l'has fet així.",
            };
            const dates = { Pp1: "27 d'octubre", Pp2: "1 de desembre", Pp3: "21 de desembre", Pp4: "2 de febrer" };
            return (
              <Link key={b.prova} to={b.ruta} className="border border-gray-200 rounded-lg p-3 hover:border-indigo-200 hover:bg-indigo-50/40">
                <p className="font-medium text-gray-900 text-sm">
                  {b.prova} · {dates[b.prova]} <span className="text-gray-500 font-normal">· bloc {b.num}</span>
                </p>
                <p className="text-sm text-gray-600 mt-0.5">{textos[b.prova]}</p>
              </Link>
            );
          })}
        </div>
        <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4">
          <p className="text-sm text-amber-900">
            <strong>Les escrites van just abans de cada salt</strong> (S08, S14, S20, S28 i S31). Valen
            un 2 % cadascuna: la seva feina no és posar-te nota, és que sàpigues si t'estàs despenjant
            mentre encara es pot fer alguna cosa. La Pe4, el 18 de gener, és la més important.
          </p>
        </div>
        <div className="mt-3 bg-violet-50 border border-violet-200 rounded-lg p-4">
          <p className="text-sm text-violet-900">
            <strong>Les matemàtiques no s'avaluen com a deducció.</strong> No es demana derivar el
            gradient de la log-loss. Sí que es demana implementar una funció de pèrdua i comprovar-la,
            verificar un gradient per diferències finites, o explicar per què un model dona el que dona
            mirant-ne els pesos.
          </p>
        </div>
      </section>

      <section id="sessions" className="space-y-4 scroll-mt-20">
        <div className="flex items-center gap-3">
          <CalendarDays className="w-6 h-6 text-primary-600" />
          <h2 className="text-2xl font-bold text-gray-900">Sessió a sessió</h2>
        </div>
        <p className="text-sm text-gray-600">
          Les activitats <strong>vencen sempre el diumenge de la setmana en què es donen</strong>.
          L'única excepció són les vacances de Nadal.
        </p>
        <div className="flex flex-wrap gap-2 text-xs">
          <Xip className="bg-primary-50 text-primary-700 border-primary-300"><Clock className="w-3 h-3" /> avui</Xip>
          <Xip className="bg-violet-50 text-violet-700 border-violet-200"><Sigma className="w-3 h-3" /> matemàtiques</Xip>
          <Xip className="bg-amber-50 text-amber-800 border-amber-200"><PenLine className="w-3 h-3" /> prova escrita</Xip>
          <Xip className="bg-rose-50 text-rose-800 border-rose-200"><ClipboardCheck className="w-3 h-3" /> prova pràctica</Xip>
          <Xip className="bg-gray-100 text-gray-700 border-gray-200"><ListChecks className="w-3 h-3" /> activitat i venciment</Xip>
        </div>

        {BLOCS.map((b) => {
          const llista = SESSIONS.filter((s) => s.bloc === b.num);
          const del = llista[0];
          const al = llista[llista.length - 1];
          return (
            <div key={b.num} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="text-lg font-bold text-gray-900">
                  <Link to={b.ruta} className="hover:text-primary-700">
                    Bloc {b.num} · {b.titol}
                  </Link>
                </h3>
                <span className="text-sm text-gray-500">
                  {del.s}–{al.s} · {llista.length * 2} h · {dataCurta(del.data)} – {dataCurta(al.data)}
                </span>
              </div>
              <div className="mt-4 space-y-2">
                {llista.map((ses) => (
                  <FilaSessio key={ses.s} ses={ses} avui={avui} />
                ))}
              </div>
              {b.num === 4 && (
                <p className="text-xs text-gray-500 mt-3">
                  Lliurament de l'agent del concurs: es tanca al final de la S32. L'endemà es competeix
                  amb el que hi hagi.
                </p>
              )}
            </div>
          );
        })}
      </section>

      <section id="festius" className="bg-white rounded-xl p-6 shadow-sm border-2 border-amber-300 scroll-mt-20">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-amber-600" />
          <h2 className="text-xl font-bold text-gray-900">Festius i vacances</h2>
        </div>
        <ul className="space-y-3 text-sm text-gray-800">
          {FESTIUS.map((f) => (
            <li key={f.quan} className="flex gap-2">
              <span className="font-semibold text-amber-700 whitespace-nowrap">{f.quan}</span>
              <span>{f.text}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
