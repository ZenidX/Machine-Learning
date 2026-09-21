import { Link } from 'react-router-dom'
import {
  CalendarRange, Code2, Brain, Gamepad2, Wrench,
  ArrowRight, Target, Users, AlertTriangle, Sparkles,
} from 'lucide-react'
import MermaidDiagram from '../components/MermaidDiagram'

const seccions = [
  {
    name: 'Programa',
    description: "Com s'organitza el curs, els blocs i què queda per decidir",
    href: '/programa',
    icon: CalendarRange,
    color: 'bg-blue-600',
  },
  {
    name: 'Python i dades',
    description: 'Repàs de Python, Jupyter i Colab, Pandas i visualització',
    href: '/python',
    icon: Code2,
    color: 'bg-emerald-600',
  },
  {
    name: 'Machine Learning',
    description: 'Supervisat, arbres de decisió, no supervisat i preparació de dades',
    href: '/machine-learning',
    icon: Brain,
    color: 'bg-violet-600',
  },
  {
    name: 'Xarxes i RL',
    description: 'Xarxes neuronals amb PyTorch i agents que aprenen jugant',
    href: '/deep-rl',
    icon: Gamepad2,
    color: 'bg-rose-600',
  },
  {
    name: 'Recursos',
    description: 'Eines, vídeos i documentació per treballar',
    href: '/recursos',
    icon: Wrench,
    color: 'bg-amber-600',
  },
]

const recorregut = `
flowchart LR
    P["Python<br/>la sintaxi mínima"] --> D["Dades<br/>Pandas i gràfics"]
    D --> ML["Machine Learning<br/>models que prediuen"]
    ML --> XN["Xarxes neuronals<br/>PyTorch"]
    XN --> RL["Reinforcement Learning<br/>agents que juguen"]

    E["Ètica i biaix"] -.travessa tot el curs.-> ML

    style P fill:#d1fae5
    style D fill:#dbeafe
    style ML fill:#ede9fe
    style XN fill:#fce7f3
    style RL fill:#ffe4e6
    style E fill:#fef3c7
`

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 lg:p-12 text-white">
        <p className="text-primary-200 font-medium mb-2">Optativa · Curs 2026-27</p>
        <h1 className="text-3xl lg:text-4xl font-bold mb-4">
          Aprenentatge automàtic
        </h1>
        <p className="text-lg text-primary-100 mb-6 max-w-3xl">
          De no haver programat mai en Python a entrenar un agent que aprèn a jugar sol.
          Aquest és el recorregut del curs.
        </p>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center space-x-2 bg-white/10 rounded-lg px-4 py-2">
            <Target className="w-5 h-5" />
            <span>Un únic resultat d'aprenentatge</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 rounded-lg px-4 py-2">
            <Users className="w-5 h-5" />
            <span>DAM i DAW · 2n curs</span>
          </div>
        </div>
      </div>

      {/* El RA */}
      <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm border border-gray-100">
        <h2 className="text-2xl font-bold text-gray-900 mb-3">Què s'espera de tu en acabar</h2>
        <p className="text-gray-700 text-lg leading-relaxed mb-4">
          El mòdul té un sol resultat d'aprenentatge, i és aquest:
        </p>
        <blockquote className="border-l-4 border-primary-500 bg-primary-50 p-5 rounded-r-lg">
          <p className="text-primary-900 text-lg font-medium italic">
            Crea aplicacions fent ús de models d'aprenentatge automàtic.
          </p>
        </blockquote>
        <p className="text-gray-600 mt-4 leading-relaxed">
          Fixa-t'hi bé: diu <strong>crea aplicacions</strong>. No diu memoritza algorismes ni
          demostra teoremes. El curs va d'entrenar models i fer-los servir per resoldre alguna
          cosa, i per això la major part de les sessions són davant de l'ordinador.
        </p>
      </div>

      {/* Recorregut */}
      <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm border border-gray-100">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">El recorregut</h2>
        <p className="text-gray-600 mb-6">
          Cada bloc necessita l'anterior. No es pot entrenar un model sense saber carregar dades,
          i no es pot entendre un agent sense haver vist abans una xarxa neuronal.
        </p>
        <MermaidDiagram chart={recorregut} />
      </div>

      {/* Seccions */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {seccions.map((s) => (
          <Link
            key={s.name}
            to={s.href}
            className="bg-white rounded-xl p-6 shadow-sm card-hover border border-gray-100"
          >
            <div className={`${s.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
              <s.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{s.name}</h3>
            <p className="text-gray-600 text-sm mb-4">{s.description}</p>
            <div className="flex items-center text-primary-600 text-sm font-medium">
              Veure més <ArrowRight className="w-4 h-4 ml-1" />
            </div>
          </Link>
        ))}
      </div>

      {/* Com es treballa */}
      <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Sparkles className="w-6 h-6 text-primary-600" />
          <h2 className="text-2xl font-bold text-gray-900">Com es treballa</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-5">
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
            <h3 className="font-semibold text-emerald-900 mb-1">Sense instal·lar res</h3>
            <p className="text-sm text-gray-700">
              Es treballa amb Google Colab des del navegador. No perdrem sessions instal·lant
              Python a cada portàtil.
            </p>
          </div>
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-1">Exercicis curts i sovint</h3>
            <p className="text-sm text-gray-700">
              Un lliurament petit per sessió. Són curts a posta: el que compta és fer-los tots,
              no que cap sigui espectacular.
            </p>
          </div>
          <div className="p-4 bg-violet-50 border border-violet-200 rounded-lg">
            <h3 className="font-semibold text-violet-900 mb-1">Codi en viu</h3>
            <p className="text-sm text-gray-700">
              La teoria és curta i de seguida es programa a classe, amb els errors inclosos.
            </p>
          </div>
        </div>
      </div>

      {/* Avís */}
      <div className="flex items-start space-x-4 p-6 bg-amber-50 border-2 border-amber-300 rounded-xl">
        <AlertTriangle className="w-7 h-7 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <h2 className="font-bold text-amber-900 text-lg mb-2">
            L'avaluació encara no és definitiva
          </h2>
          <p className="text-amber-900 text-sm leading-relaxed">
            Hi ha dues versions que no coincideixen entre la fitxa oficial del mòdul i el que es va
            explicar al grup del curs passat, tant en hores com en pesos de les notes. Fins que no
            estigui confirmada, la pàgina del programa mostra totes dues i cap com a bona.
          </p>
          <Link
            to="/programa"
            className="inline-flex items-center text-amber-900 font-medium text-sm mt-3 underline"
          >
            Veure les dues versions
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-gray-900 rounded-xl p-8 text-center">
        <h2 className="text-2xl font-bold text-white mb-4">Per on comencem</h2>
        <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
          Pel principi: repassar Python fins que la sintaxi deixi de fer nosa. Tot el que ve
          després es recolza en això.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link
            to="/python"
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Python i dades
          </Link>
          <Link
            to="/programa"
            className="bg-white hover:bg-gray-100 text-gray-900 px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Veure el programa
          </Link>
        </div>
      </div>
    </div>
  )
}
