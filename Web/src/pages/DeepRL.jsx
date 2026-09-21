import { useRef } from 'react'
import { Link } from 'react-router-dom'
import {
  Brain,
  Gamepad2,
  Layers,
  BookOpen,
  Code2,
  FolderGit2,
  Trophy,
  Terminal,
  ExternalLink,
  Bot,
  Gauge,
  Car,
  Grid3x3,
  Rocket,
  PersonStanding,
} from 'lucide-react'
import MermaidDiagram from '../components/MermaidDiagram'

const flujoChart = `flowchart LR
  A["Xarxes neuronals<br/>(PyTorch)"] --> B["La xarxa aproxima<br/>una funció"]
  B --> C["La xarxa fa de<br/>cervell d'un agent"]
  C --> D["L'agent aprèn<br/>jugant (RL)"]
  D --> E["Pràctica final:<br/>agent DQN a un videojoc"]`

function Section({ id, title, icon: Icon, children }) {
  return (
    <section id={id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 scroll-mt-24">
      <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2 mb-4">
        {Icon && <Icon className="w-5 h-5 text-blue-600" />}
        {title}
      </h2>
      {children}
    </section>
  )
}

function ProjectCard({ icon: Icon, title, desc }) {
  return (
    <div className="border border-gray-100 rounded-lg p-4 bg-gray-50">
      <div className="flex items-center gap-2 mb-1">
        <Icon className="w-4 h-4 text-blue-600" />
        <h4 className="font-medium text-gray-900">{title}</h4>
      </div>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  )
}

export default function DeepRL() {
  const topRef = useRef(null)

  const scrollTo = (id) => {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const nav = [
    { id: 'de-la-xarxa-a-lagent', label: 'De la xarxa a l’agent' },
    { id: 'deep-learning', label: 'Deep Learning' },
    { id: 'reinforcement-learning', label: 'Reinforcement Learning' },
    { id: 'models-entrenats', label: 'Models ja entrenats' },
    { id: 'practica-final', label: 'Pràctica final' },
    { id: 'posar-en-marxa', label: 'Posar-ho en marxa' },
  ]

  return (
    <div ref={topRef} className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Xarxes neuronals i Reinforcement Learning</h1>
        <p className="mt-2 text-gray-600 max-w-3xl">
          El tram final del curs: de PyTorch a un agent que aprèn jugant. Bloc 6 de la programació,
          amb tot el material ja fet i provat al repositori.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {nav.map((n) => (
            <button
              key={n.id}
              onClick={() => scrollTo(n.id)}
              className="text-sm px-3 py-1.5 rounded-full bg-gray-100 text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors"
            >
              {n.label}
            </button>
          ))}
        </div>
      </div>

      <Section id="de-la-xarxa-a-lagent" title="De la xarxa a l’agent" icon={Brain}>
        <p className="text-gray-700 mb-4">
          El fil conductor d’aquest bloc és senzill: primer es treballen les xarxes neuronals amb
          PyTorch com a eina general, i després aquestes mateixes xarxes passen a ser el cervell d’un
          agent que aprèn per prova i error jugant. El Reinforcement Learning "tradicional" fa servir
          taules per emmagatzemar el valor de cada parell (estat, acció), però això no escala: quan els
          estats són píxels o valors continus, cal una xarxa neuronal que generalitzi. Aquest pas
          d’una taula a una xarxa és el que connecta els dos blocs.
        </p>
        <MermaidDiagram chart={flujoChart} />
      </Section>

      <Section id="deep-learning" title="Deep Learning" icon={Layers}>
        <p className="text-gray-700 mb-4">
          A <code className="text-sm bg-gray-100 px-1 rounded">Deep Learning/01_teoria/</code> hi ha cinc
          quaderns que van dels fonaments fins a les xarxes pensades per a RL:
        </p>
        <ul className="space-y-2 text-gray-700 mb-4">
          <li>
            <span className="font-medium text-gray-900">DL_00_indice</span> — índex del bloc, amb el
            mapa de tot el contingut i requisits.
          </li>
          <li>
            <span className="font-medium text-gray-900">DL_01_fundamentos</span> — perceptró, funcions
            d’activació i backpropagation.
          </li>
          <li>
            <span className="font-medium text-gray-900">DL_02_pytorch_basico</span> — tensors, autograd
            i mòduls <code className="text-sm bg-gray-100 px-1 rounded">nn</code>.
          </li>
          <li>
            <span className="font-medium text-gray-900">DL_03_arquitecturas</span> — MLP, CNN, RNN/LSTM
            i autoencoders.
          </li>
          <li>
            <span className="font-medium text-gray-900">DL_04_entrenamiento</span> — optimització,
            regularització i callbacks.
          </li>
          <li>
            <span className="font-medium text-gray-900">DL_05_redes_para_RL</span> — per què Q-learning
            amb taules no escala i com una xarxa neuronal fa d’aproximador de funció; és el pont cap
            al bloc de RL.
          </li>
        </ul>

        <p className="text-gray-700 mb-3">
          A <code className="text-sm bg-gray-100 px-1 rounded">02_fundamentos/</code> hi ha el codi base
          (carpeta <code className="text-sm bg-gray-100 px-1 rounded">core/</code>: models, entrenament i
          utils) i tres exemples executables:
        </p>
        <div className="grid sm:grid-cols-3 gap-3 mb-4">
          <ProjectCard icon={Code2} title="MLP amb MNIST" desc="Classificació de dígits escrits a mà amb un perceptró multicapa." />
          <ProjectCard icon={Code2} title="CNN amb CIFAR-10" desc="Classificació d’imatges amb una xarxa convolucional." />
          <ProjectCard icon={Code2} title="LSTM de sentiments" desc="Anàlisi de sentiment en text amb una xarxa recurrent." />
        </div>

        <p className="text-gray-700">
          El pas cap a RL es tanca amb la pràctica de{' '}
          <code className="text-sm bg-gray-100 px-1 rounded">04_practica/DL_practica_pytorch_a_DQN.ipynb</code>,
          amb les solucions resoltes a{' '}
          <code className="text-sm bg-gray-100 px-1 rounded">02_fundamentos/DL_practica_pytorch_a_DQN_soluciones.ipynb</code>.
          Els datasets (MNIST, CIFAR-10) es descarreguen sols la primera vegada que s’executa el
          quadern: no hi són al repositori.
        </p>
      </Section>

      <Section id="reinforcement-learning" title="Reinforcement Learning" icon={Gamepad2}>
        <p className="text-gray-700 mb-4">
          A <code className="text-sm bg-gray-100 px-1 rounded">Reinforcement Learning/01_teoria/</code> hi
          ha la teoria en tres quaderns encadenats:
        </p>
        <ul className="space-y-2 text-gray-700 mb-4">
          <li>
            <span className="font-medium text-gray-900">RL_01_fundamentos</span> — el marc
            agent-entorn, el procés de decisió de Markov, polítiques i funcions de valor, SARSA i
            Q-learning.
          </li>
          <li>
            <span className="font-medium text-gray-900">RL_02_dqn</span> — Deep Q-Networks i Gymnasium,
            amb pràctica inclosa.
          </li>
          <li>
            <span className="font-medium text-gray-900">RL_03_sb3</span> — Stable-Baselines3, PPO i SAC.
          </li>
        </ul>

        <p className="text-gray-700 mb-3">
          A <code className="text-sm bg-gray-100 px-1 rounded">02_fundamentos/</code> hi ha el codi base
          d’agents (<code className="text-sm bg-gray-100 px-1 rounded">core/agentes.py</code>) i dos
          exemples de referència:
        </p>
        <div className="grid sm:grid-cols-2 gap-3 mb-6">
          <ProjectCard icon={Bot} title="Q-learning amb Taxi" desc="L’agent clàssic de taula Q a l’entorn Taxi de Gymnasium." />
          <ProjectCard icon={Bot} title="DQN amb CartPole" desc="La mateixa idea però amb una xarxa neuronal com a aproximador." />
        </div>

        <h3 className="font-medium text-gray-900 mb-2">Projectes amb DQN</h3>
        <div className="grid sm:grid-cols-3 gap-3 mb-6">
          <ProjectCard icon={Gauge} title="Flappy Bird" desc="Agent DQN que aprèn a travessar els tubs del joc." />
          <ProjectCard icon={Gamepad2} title="Nibbler" desc="Variant tipus Snake: l’agent aprèn a créixer sense xocar." />
          <ProjectCard icon={Car} title="Racing" desc="Cotxe que aprèn a conduir en pista, amb diversos agents entrenats." />
        </div>

        <h3 className="font-medium text-gray-900 mb-2">Projectes avançats</h3>
        <div className="grid sm:grid-cols-2 gap-3">
          <ProjectCard icon={Car} title="Highway" desc="Conducció autònoma 2D: autopista, pàrquing i interseccions, amb DQN/PPO i fins i tot curriculum learning." />
          <ProjectCard icon={Rocket} title="LunarLander" desc="Aterratge amb Stable-Baselines3, comparant PPO, DQN, A2C i variants contínues (SAC/TD3)." />
          <ProjectCard icon={Grid3x3} title="MiniGrid" desc="Navegació per laberints: obrir portes i recollir objectes, amb MLP o CNN segons la variant." />
          <ProjectCard icon={PersonStanding} title="PyBullet" desc="Robòtica i física 3D: robots que aprenen a caminar, nedar o saltar amb PPO, SAC o TD3." />
        </div>
      </Section>

      <Section id="models-entrenats" title="Els models ja entrenats" icon={Trophy}>
        <p className="text-gray-700">
          A <code className="text-sm bg-gray-100 px-1 rounded">Reinforcement Learning/modelos/</code> hi
          ha pesos ja entrenats (CartPole, Nibbler, Racing, Flappy Bird, LunarLander...). És l’única
          carpeta de model entrenat que sí que es guarda al repositori: permet ensenyar en directe un
          agent que ja juga bé, sense haver d’esperar l’entrenament a classe.
        </p>
      </Section>

      <Section id="practica-final" title="La pràctica final: agent DQN a un videojoc" icon={FolderGit2}>
        <p className="text-gray-700">
          A <code className="text-sm bg-gray-100 px-1 rounded">Reinforcement Learning/05_Practica/</code>{' '}
          hi ha la pràctica final del bloc, que ja existia el curs passat i funciona: l’alumnat tria
          un entorn (un dels projectes DQN o un altre de Gymnasium) i hi entrena un agent des de zero,
          documentant el procés i els resultats. És la prova pràctica 4 del curs, la de més pes de tot el
          bloc.
        </p>
      </Section>

      <Section id="posar-en-marxa" title="Com posar-ho en marxa" icon={Terminal}>
        <p className="text-gray-700 mb-3">
          Cada bloc (Deep Learning i Reinforcement Learning) té el seu propi{' '}
          <code className="text-sm bg-gray-100 px-1 rounded">requirements.txt</code>, així que convé un
          entorn virtual per bloc:
        </p>
        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{`cd "Deep Learning"          # o "Reinforcement Learning"
python -m venv .venv
.venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
jupyter lab`}
        </pre>
        <p className="text-gray-700 mt-3">
          Els datasets i els entorns de Gymnasium es descarreguen sols la primera vegada que
          s’executa el quadern.
        </p>
      </Section>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2 mb-3">
          <BookOpen className="w-5 h-5 text-blue-600" />
          Repositori
        </h2>
        <p className="text-gray-700 mb-4">
          Tots els quaderns, el codi i els models entrenats d’aquest bloc són al repositori públic
          del mòdul.
        </p>
        <a
          href="https://github.com/ZenidX/Machine-Learning"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          github.com/ZenidX/Machine-Learning
          <ExternalLink className="w-4 h-4" />
        </a>

        <div className="mt-6 flex flex-wrap gap-3 text-sm">
          <Link to="/machine-learning" className="text-blue-600 hover:text-blue-700 underline">
            Visió general del mòdul
          </Link>
          <Link to="/programa" className="text-blue-600 hover:text-blue-700 underline">
            Programa del curs
          </Link>
          <Link to="/recursos" className="text-blue-600 hover:text-blue-700 underline">
            Recursos
          </Link>
        </div>
      </div>
    </div>
  )
}
