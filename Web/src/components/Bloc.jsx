import { Link } from "react-router-dom";
import {
  ExternalLink,
  Download,
  Save,
  MousePointerClick,
  CheckCircle2,
  Mountain,
  Database,
  ClipboardCheck,
  PenLine,
  CalendarRange,
  MessageCircle,
} from "lucide-react";
import { quaderns, colabUrl, rutaQuadern } from "../data/quaderns";
import { reptes } from "../data/reptes";
import { SESSIONS, PROVES, BLOCS, ACTIVITATS, sessio, dataCurta, dataLlarga, diesFins, isoAvui } from "../data/curs";

// Classes completes per color: Tailwind només genera les que veu escrites senceres.
export const COLORS = {
  emerald: {
    text: "text-emerald-600",
    etiqueta: "text-emerald-700",
    boto: "bg-emerald-600 hover:bg-emerald-700",
    suau: "bg-emerald-50 border-emerald-200",
    xip: "bg-emerald-50 text-emerald-700 hover:bg-emerald-100",
  },
  sky: {
    text: "text-sky-600",
    etiqueta: "text-sky-700",
    boto: "bg-sky-600 hover:bg-sky-700",
    suau: "bg-sky-50 border-sky-200",
    xip: "bg-sky-50 text-sky-700 hover:bg-sky-100",
  },
  violet: {
    text: "text-violet-600",
    etiqueta: "text-violet-700",
    boto: "bg-violet-600 hover:bg-violet-700",
    suau: "bg-violet-50 border-violet-200",
    xip: "bg-violet-50 text-violet-700 hover:bg-violet-100",
  },
  indigo: {
    text: "text-indigo-600",
    etiqueta: "text-indigo-700",
    boto: "bg-indigo-600 hover:bg-indigo-700",
    suau: "bg-indigo-50 border-indigo-200",
    xip: "bg-indigo-50 text-indigo-700 hover:bg-indigo-100",
  },
  teal: {
    text: "text-teal-600",
    etiqueta: "text-teal-700",
    boto: "bg-teal-600 hover:bg-teal-700",
    suau: "bg-teal-50 border-teal-200",
    xip: "bg-teal-50 text-teal-700 hover:bg-teal-100",
  },
  rose: {
    text: "text-rose-600",
    etiqueta: "text-rose-700",
    boto: "bg-rose-600 hover:bg-rose-700",
    suau: "bg-rose-50 border-rose-200",
    xip: "bg-rose-50 text-rose-700 hover:bg-rose-100",
  },
};

export function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Navegació interna amb botons: amb HashRouter, un <a href="#..."> canviaria la ruta.
export function NavInterna({ items, color = "indigo" }) {
  const c = COLORS[color];
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((it) => (
        <button
          key={it.id}
          type="button"
          onClick={() => scrollToId(it.id)}
          className={`text-sm font-medium rounded-full px-4 py-1.5 transition-colors ${c.xip}`}
        >
          {it.label}
        </button>
      ))}
    </div>
  );
}

export function Seccio({ id, titol, icona: Icona, color = "indigo", children, className = "" }) {
  const c = COLORS[color];
  return (
    <section
      id={id}
      className={`bg-white rounded-xl p-6 shadow-sm border border-gray-100 scroll-mt-20 ${className}`}
    >
      {titol && (
        <div className="flex items-center gap-3 mb-4">
          {Icona && <Icona className={`w-6 h-6 flex-shrink-0 ${c.text}`} />}
          <h2 className="text-xl font-semibold text-gray-900">{titol}</h2>
        </div>
      )}
      {children}
    </section>
  );
}

// Títol gran d'un pas del bloc: Aprèn, Exemples, Reptes, Prova.
export function Pas({ id, num, titol, subtitol, color = "indigo" }) {
  const c = COLORS[color];
  return (
    <div id={id} className="scroll-mt-20 pt-2">
      <p className={`text-xs font-semibold uppercase tracking-wide ${c.etiqueta}`}>Pas {num}</p>
      <h2 className="text-2xl font-bold text-gray-900">{titol}</h2>
      {subtitol && <p className="text-gray-600 mt-1 max-w-3xl">{subtitol}</p>}
    </div>
  );
}

export function CapcaleraBloc({ num, icona: Icona, color, children }) {
  const bloc = BLOCS.find((b) => b.num === num);
  const c = COLORS[color];
  return (
    <div>
      <p className={`text-sm font-semibold ${c.etiqueta}`}>Bloc {num}</p>
      <div className="flex items-center gap-3">
        {Icona && <Icona className={`w-8 h-8 ${c.text}`} />}
        <h1 className="text-3xl font-bold text-gray-900">{bloc.titol}</h1>
      </div>
      <p className="mt-2 text-lg text-gray-600 max-w-3xl">{children}</p>
    </div>
  );
}

// Sessions on surt un quadern, tretes del calendari (no hi ha una segona taula de dates).
function sessionsDe(codi) {
  return SESSIONS.filter((s) => (s.material || []).includes(codi) || (s.casa || []).includes(codi));
}

export function QuadernCard({ codi, color = "indigo", etiqueta, children }) {
  const q = quaderns[codi];
  if (!q) return null;
  const c = COLORS[color];
  const ses = sessionsDe(codi);
  const quan = ses.length ? ses.map((s) => `${s.s} · ${dataCurta(s.data)}`).join(", ") : null;
  return (
    <div className="border border-gray-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
      <div className="min-w-0">
        <p className={`text-xs font-medium mb-1 ${c.etiqueta}`}>
          <code>{codi}</code>
          {etiqueta && <> · {etiqueta}</>}
          {quan && <span className="text-gray-500 font-normal"> · {quan}</span>}
        </p>
        <h3 className="font-medium text-gray-900 mb-1">{q.titol}</h3>
        {q.dades && <p className="text-sm text-gray-500 mb-2">{q.dades}</p>}
        <p className="text-sm text-gray-600">{q.descripcio}</p>
        {children}
      </div>
      <div className="flex-shrink-0 flex flex-col gap-2">
        <a
          href={colabUrl(rutaQuadern(q))}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-white text-sm font-medium whitespace-nowrap ${c.boto}`}
        >
          Obre a Colab
          <ExternalLink className="w-4 h-4" />
        </a>
        {q.descarrega && (
          <a
            href={`${import.meta.env.BASE_URL}quaderns/${q.fitxer}`}
            download={q.fitxer}
            className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50 whitespace-nowrap"
          >
            Baixa el .ipynb
            <Download className="w-4 h-4" />
          </a>
        )}
      </div>
    </div>
  );
}

export function AbansDeComencar() {
  return (
    <section className="bg-amber-50 border border-amber-200 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-amber-900 mb-3">Abans d'obrir cap quadern</h2>
      <ul className="space-y-3 text-amber-900 text-sm">
        <li className="flex items-start gap-2">
          <Save className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>
            Fes <strong>Fitxer → Desa una còpia a Drive</strong> just en obrir-lo, o perdràs la
            feina en tancar la pestanya.
          </span>
        </li>
        <li className="flex items-start gap-2">
          <MousePointerClick className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>
            <strong>No cliquis «Executa-ho tot»</strong>: les cel·les d'exercici són buides a posta
            i les has d'anar omplint una per una. Si ho executes tot de cop veuràs errors de
            variables que encara no existeixen, i és normal.
          </span>
        </li>
        <li className="flex items-start gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>
            Les comprovacions et diuen si <strong>el procediment</strong> és correcte, no quin
            número t'ha de sortir. El número és la teva feina.
          </span>
        </li>
      </ul>
    </section>
  );
}

const NIVELLS = ["", "Dificultat 1", "Dificultat 2", "Dificultat 3"];

export function Reptes({ bloc, color = "indigo" }) {
  const c = COLORS[color];
  const llista = reptes.filter((r) => r.bloc === bloc);
  return (
    <div className="space-y-4">
      <div className={`border rounded-lg p-4 text-sm text-gray-800 ${c.suau}`}>
        <p>
          Un repte és un cas amb <strong>dades reals que no has vist mai</strong> i una pregunta per
          respondre. El fas sol: el quadern et dona les dades i l'encàrrec, i la resta és teva. Que
          alguna cosa et surti malament forma part de la feina.
        </p>
      </div>
      {llista.length === 0 ? (
        <div className="border-2 border-dashed border-gray-200 rounded-lg p-6 text-center">
          <Mountain className="w-8 h-8 text-gray-300 mx-auto mb-2" />
          <p className="font-medium text-gray-700">Els reptes d'aquest bloc arriben aviat</p>
          <p className="text-sm text-gray-500 mt-1">
            Mentrestant, mira els exemples resolts d'aquí dalt.
          </p>
        </div>
      ) : (
        llista.map((r) => (
          <div
            key={r.codi}
            className="border border-gray-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4"
          >
            <div className="min-w-0">
              <p className={`text-xs font-medium mb-1 ${c.etiqueta}`}>
                <code>{r.codi}</code>
                {r.dificultat ? <span className="text-gray-500 font-normal"> · {NIVELLS[r.dificultat]}</span> : null}
              </p>
              <h3 className="font-medium text-gray-900 mb-1">{r.titol}</h3>
              {r.enunciat && <p className="text-sm text-gray-700 mb-2">{r.enunciat}</p>}
              <p className="text-sm text-gray-600 flex items-start gap-1.5">
                <Database className="w-4 h-4 flex-shrink-0 mt-0.5 text-gray-400" />
                <span>
                  {r.font ? (
                    <a href={r.font} target="_blank" rel="noopener noreferrer" className="underline hover:text-gray-900">
                      {r.dataset}
                    </a>
                  ) : (
                    r.dataset
                  )}
                  {r.llicencia && <span className="text-gray-500"> · {r.llicencia}</span>}
                </span>
              </p>
            </div>
            <div className="flex-shrink-0 flex flex-col gap-2">
              <a
                href={colabUrl(`Machine Learning/04_reptes/${r.fitxer}`)}
                target="_blank"
                rel="noopener noreferrer"
                className={`inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-white text-sm font-medium whitespace-nowrap ${c.boto}`}
              >
                Obre a Colab
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

// Les preguntes per les quals val la pena cridar en Xavi.
export function QuanCridar({ color = "indigo", compacte = false }) {
  const c = COLORS[color];
  return (
    <div className={`border rounded-lg p-4 ${c.suau}`}>
      <div className="flex items-center gap-2 mb-2">
        <MessageCircle className={`w-5 h-5 ${c.text}`} />
        <p className="font-semibold text-gray-900">Quan cridar en Xavi</p>
      </div>
      <p className="text-sm text-gray-700 mb-2">
        Per dubtes de <strong>criteri</strong>, no de sintaxi. Per exemple:
      </p>
      <ul className="text-sm text-gray-800 space-y-1 list-disc list-inside">
        <li>Esborro aquestes files o les imputo?</li>
        <li>Aquest resultat té sentit?</li>
        <li>Quin model triaria algú amb experiència, i per què?</li>
        <li>Les dades m'estan enganyant?</li>
      </ul>
      {!compacte && (
        <p className="text-sm text-gray-600 mt-2">
          Per a la sintaxi hi ha els exemples resolts, la caixa d'eines i la documentació.
        </p>
      )}
    </div>
  );
}

export function ProvaBloc({ bloc, color = "indigo" }) {
  const c = COLORS[color];
  const avui = isoAvui();
  const proves = PROVES.filter((p) => p.bloc === bloc);
  return (
    <div className="space-y-3">
      {proves.map((p) => {
        const dies = diesFins(p.data, avui);
        const practica = p.tipus === "practica";
        return (
          <div
            key={p.codi}
            className={`rounded-lg p-4 border ${practica ? "border-rose-200 bg-rose-50/50" : "border-amber-200 bg-amber-50/50"}`}
          >
            <div className="flex flex-wrap items-center gap-2 mb-1">
              {practica ? (
                <ClipboardCheck className="w-4 h-4 text-rose-600" />
              ) : (
                <PenLine className="w-4 h-4 text-amber-600" />
              )}
              <code className="text-sm font-semibold text-gray-900">{p.codi}</code>
              <span className="text-sm text-gray-600">
                {practica ? "Prova pràctica" : "Prova escrita"} · {p.s} · {dataLlarga(p.data)}
              </span>
              {dies >= 0 && (
                <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-white border border-gray-200 text-gray-700">
                  {dies === 0 ? "avui" : dies === 1 ? "demà" : `d'aquí ${dies} dies`}
                </span>
              )}
            </div>
            <p className="text-sm font-medium text-gray-900">{p.titol}</p>
            {p.detall && <p className="text-sm text-gray-700 mt-1">{p.detall}</p>}
            {p.nota && <p className="text-xs text-gray-500 mt-1">{p.nota}</p>}
          </div>
        );
      })}
      <Link
        to="/calendari"
        className={`inline-flex items-center gap-1.5 text-sm font-medium ${c.etiqueta}`}
      >
        <CalendarRange className="w-4 h-4" />
        Com compta cada prova a la nota
      </Link>
    </div>
  );
}

export function PassosBloc({ color }) {
  return (
    <NavInterna
      color={color}
      items={[
        { id: "apren", label: "1 · Aprèn" },
        { id: "exemples", label: "2 · Exemples" },
        { id: "reptes", label: "3 · Reptes" },
        { id: "prova", label: "4 · Prova" },
      ]}
    />
  );
}

export function SeguentBloc({ actual }) {
  const seg = BLOCS.find((b) => b.num === actual + 1);
  const ant = BLOCS.find((b) => b.num === actual - 1);
  return (
    <div className="flex flex-wrap justify-between gap-3 text-sm">
      {ant ? (
        <Link to={ant.ruta} className="px-4 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50">
          ← Bloc {ant.num} · {ant.titol}
        </Link>
      ) : (
        <span />
      )}
      {seg && (
        <Link to={seg.ruta} className="px-4 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50">
          Bloc {seg.num} · {seg.titol} →
        </Link>
      )}
    </div>
  );
}


// Les activitats del bloc (0 o 10, fora de termini compten com a negatives).
export function ActivitatsBloc({ bloc }) {
  const avui = isoAvui();
  const llista = ACTIVITATS.filter((a) => sessio(a.s)?.bloc === bloc);
  if (!llista.length) return null;
  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700">
        Les activitats d'aquest bloc · es qualifiquen 0 o 10 · fora de termini compten com a negatives
      </div>
      <ul className="divide-y divide-gray-100">
        {llista.map((a) => {
          const vencuda = a.venc < avui;
          return (
            <li key={a.codi} className="px-4 py-2 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 text-sm">
              <span className="text-gray-900">
                <code className="text-xs text-gray-500 mr-2">{a.codi}</code>
                {a.nom}
                {a.nota && <span className="text-xs text-gray-500"> · {a.nota}</span>}
              </span>
              <span className={`whitespace-nowrap ${vencuda ? "text-gray-400" : "text-gray-700 font-medium"}`}>
                surt a la {a.s} · venç {dataCurta(a.venc)}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

// Els reptes que ja tenen el quadern resolt publicat (camp "resolt" de src/data/reptes.js).
export function ReptesResolts() {
  const llista = reptes.filter((r) => r.resolt);
  if (!llista.length) {
    return (
      <p className="text-sm text-gray-500">
        Encara no n'hi ha cap. Les solucions dels reptes es publiquen aquí quan toca.
      </p>
    );
  }
  return (
    <div className="space-y-3">
      {llista.map((r) => (
        <div key={r.codi} className="border border-gray-200 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="min-w-0">
            <p className="text-xs font-medium text-indigo-700 mb-0.5">
              <code>{r.codi}</code>
              <span className="text-gray-500 font-normal"> · bloc {r.bloc}</span>
            </p>
            <p className="font-medium text-gray-900">{r.titol}</p>
            <p className="text-sm text-gray-600">{r.dataset}</p>
          </div>
          <a
            href={colabUrl(r.resolt)}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 whitespace-nowrap"
          >
            Veure la solució a Colab
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      ))}
    </div>
  );
}
