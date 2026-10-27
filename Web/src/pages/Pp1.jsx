import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import enunciat from "../data/pp1.md?raw";

// L'enunciat de la Pp1 (27-oct-2026), tal com es reparteix a classe.
const components = {
  h1: (p) => <h1 className="text-3xl font-bold text-gray-900 mb-4" {...p} />,
  h2: (p) => <h2 className="text-2xl font-bold text-gray-900 mt-10 mb-3 pt-6 border-t border-gray-200" {...p} />,
  p: (p) => <p className="text-gray-700 my-3 leading-relaxed" {...p} />,
  ul: (p) => <ul className="list-disc pl-6 my-3 space-y-1 text-gray-700" {...p} />,
  ol: (p) => <ol className="list-decimal pl-6 my-3 space-y-2 text-gray-800" {...p} />,
  a: (p) => <a className="text-indigo-700 hover:text-indigo-900 break-all" target="_blank" rel="noopener noreferrer" {...p} />,
  hr: () => null,
  table: (p) => (
    <div className="overflow-x-auto my-4">
      <table className="min-w-full text-sm border border-gray-200" {...p} />
    </div>
  ),
  th: (p) => <th className="bg-gray-50 text-left px-3 py-2 border-b border-gray-200 font-medium text-gray-900" {...p} />,
  td: (p) => <td className="px-3 py-2 border-b border-gray-100 text-gray-700 align-top" {...p} />,
  pre: (p) => <pre className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto text-xs sm:text-sm my-3" {...p} />,
  code: ({ className, ...p }) =>
    className ? (
      <code className={className} {...p} />
    ) : (
      <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm text-gray-800 break-words" {...p} />
    ),
};

export default function Pp1() {
  return (
    <div className="bg-white rounded-xl p-6 sm:p-8 shadow-sm border border-gray-100">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {enunciat}
      </ReactMarkdown>
    </div>
  );
}
