import { Link } from "react-router-dom";
import { Database, ExternalLink, AlertTriangle, HelpCircle, Mountain } from "lucide-react";
import { NavInterna, QuanCridar } from "../components/Bloc";
import { datasetsPractica } from "../data/datasetsPractica";

function FitxaDataset({ d }) {
  return (
    <section id={d.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 scroll-mt-20">
      <div className="flex flex-wrap items-start justify-between gap-3 mb-2">
        <div className="min-w-0">
          <h2 className="text-xl font-semibold text-gray-900">{d.nom}</h2>
          <p className="text-sm text-gray-500">
            {d.origen} · {d.llicencia}
          </p>
        </div>
        <span className="rounded px-2 py-1 bg-gray-100 text-gray-700 text-xs font-semibold">{d.mida}</span>
      </div>

      <p className="text-gray-700 mb-3">{d.context}</p>
      <p className="text-sm text-emerald-900 bg-emerald-50 border-l-4 border-emerald-400 rounded-r px-3 py-2 mb-4">
        <strong>On és la feina:</strong> {d.repte}
      </p>

      <pre className="bg-gray-900 text-gray-100 text-xs rounded-lg p-3 overflow-x-auto mb-4">
        <code>{`import pandas as pd\nimport numpy as np\n${d.carrega}`}</code>
      </pre>

      <div className="grid lg:grid-cols-2 gap-5">
        <div>
          <p className="text-sm font-semibold text-gray-900 mb-2">Les columnes que faràs servir</p>
          <table className="w-full text-sm">
            <tbody>
              {d.columnes.map(([col, que]) => (
                <tr key={col} className="border-t border-gray-100 align-top">
                  <td className="py-1.5 pr-3">
                    <code className="text-xs bg-gray-100 px-1 rounded">{col}</code>
                  </td>
                  <td className="py-1.5 text-gray-700">{que}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="space-y-4">
          <div>
            <p className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-emerald-600" /> Per començar
            </p>
            <ol className="list-decimal list-inside text-sm text-gray-700 space-y-1">
              {d.preguntes.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ol>
          </div>
          <div className="rounded-lg bg-amber-50 border border-amber-200 p-3">
            <p className="text-sm font-semibold text-amber-900 mb-1 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" /> Paranys
            </p>
            <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
              {d.paranys.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <a
        href={d.font}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-sm text-emerald-700 hover:underline mt-4"
      >
        La font de les dades <ExternalLink className="w-3.5 h-3.5" />
      </a>
    </section>
  );
}

export default function Datasets() {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3">
          <Database className="w-8 h-8 text-emerald-600" />
          <h1 className="text-3xl font-bold text-gray-900">Datasets per practicar</h1>
        </div>
        <p className="mt-2 text-lg text-gray-600 max-w-3xl">
          Onze conjunts de dades reals que no surten a cap repte ni a cap exemple del curs. Fes-hi el
          mateix que als reptes del bloc 1: carregar-los, mirar-ne la forma i els buits, fer-hi
          preguntes amb <code className="text-base bg-gray-100 px-1 rounded">.groupby()</code>, un
          gràfic i alguna operació amb NumPy.
        </p>
      </div>

      <div className="rounded-xl bg-emerald-50 border border-emerald-200 p-5 flex gap-3">
        <Mountain className="w-6 h-6 text-emerald-700 flex-shrink-0" />
        <p className="text-sm text-gray-800">
          <strong>La prova pràctica del bloc 1 és un repte com els que ja hi ha publicats</strong>, sobre
          un dataset que no has vist. No és cap d'aquests. La millor preparació és agafar-ne un que no
          coneguis i treure'n respostes sense ajuda. Si no saps per on començar, mira com estan fets els{" "}
          <Link to="/dades" className="text-emerald-700 font-medium hover:underline">
            reptes del bloc 1
          </Link>
          .
        </p>
      </div>

      <NavInterna color="emerald" items={datasetsPractica.map((d) => ({ id: d.id, label: d.nom }))} />

      {datasetsPractica.map((d) => (
        <FitxaDataset key={d.id} d={d} />
      ))}

      <QuanCridar color="emerald" />
    </div>
  );
}
