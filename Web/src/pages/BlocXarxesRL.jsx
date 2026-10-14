import {
  Gamepad2,
  Brain,
  Layers,
  BookOpen,
  Code2,
  Trophy,
  Terminal,
  ExternalLink,
  Bot,
  Gauge,
  Car,
  Grid3x3,
  Rocket,
  PersonStanding,
  Eye,
  Mountain,
  ClipboardCheck,
} from "lucide-react";
import MermaidDiagram from "../components/MermaidDiagram";
import {
  CapcaleraBloc,
  PassosBloc,
  Pas,
  Seccio,
  QuadernCard,
  Reptes,
  QuanCridar,
  ProvaBloc,
  ActivitatsBloc,
  SeguentBloc,
  Chivato,
} from "../components/Bloc";
import { chivatos } from "../data/chivatos";
import { githubUrl } from "../data/quaderns";

const C = "rose";

const flux = `flowchart LR
  A["Xarxes neuronals<br/>(PyTorch)"] --> B["La xarxa aproxima<br/>una funció"]
  B --> C["La xarxa fa de<br/>cervell d'un agent"]
  C --> D["L'agent aprèn<br/>jugant (RL)"]
  D --> E["El concurs:<br/>el teu cotxe a la pista"]`;

function ProjectCard({ icon: Icon, title, desc }) {
  return (
    <div className="border border-gray-100 rounded-lg p-4 bg-gray-50">
      <div className="flex items-center gap-2 mb-1">
        <Icon className="w-4 h-4 text-rose-600" />
        <h4 className="font-medium text-gray-900">{title}</h4>
      </div>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  );
}

export default function BlocXarxesRL() {
  return (
    <div className="space-y-8">
      <CapcaleraBloc num={4} icona={Gamepad2} color={C}>
        De PyTorch a un agent que aprèn jugant, i el concurs final. Ja en saps el mecanisme: una xarxa
        s'entrena amb el descens de gradient de MA_02. Acaba amb la prova pràctica 4, el 2 de febrer:
        el teu agent i la seva defensa.
      </CapcaleraBloc>

      <PassosBloc color={C} />

      <Seccio titol="De la xarxa a l'agent" icona={Brain} color={C}>
        <p className="text-gray-700 mb-4">
          Primer les xarxes neuronals amb PyTorch com a eina general, i després aquestes mateixes
          xarxes passen a ser el cervell d'un agent que aprèn per prova i error. El Reinforcement
          Learning clàssic guarda en una taula el valor de cada parell (estat, acció), però això no
          escala: quan els estats són píxels o valors continus, cal una xarxa que generalitzi. Aquest
          pas, d'una taula a una xarxa, és el que connecta les dues meitats del bloc.
        </p>
        <MermaidDiagram chart={flux} />
      </Seccio>

      {/* ---------- 1 · Aprèn ---------- */}
      <Pas id="apren" num={1} titol="Aprèn" color={C} subtitol="Sis quaderns de xarxes i tres de RL. S'obren a Colab; per als projectes amb finestra (Pygame) cal treballar en local." />

      <Seccio titol="Xarxes neuronals" icona={Layers} color={C}>
        <div className="space-y-4">
          {["DL_00", "DL_01", "DL_02", "DL_03", "DL_04", "DL_05"].map((c) => (
            <QuadernCard key={c} codi={c} color={C}>
              <Chivato f={chivatos[c]} />
            </QuadernCard>
          ))}
        </div>
        <p className="text-gray-700 text-sm mt-4 mb-3">
          A <code className="bg-gray-100 px-1 rounded">Deep Learning/02_fundamentos/</code> hi ha el
          codi base (models, entrenament i utilitats) i tres exemples executables. Els datasets (MNIST,
          CIFAR-10) es baixen sols la primera vegada.
        </p>
        <div className="grid sm:grid-cols-3 gap-3">
          <ProjectCard icon={Code2} title="MLP amb MNIST" desc="Classificació de dígits escrits a mà amb un perceptró multicapa." />
          <ProjectCard icon={Code2} title="CNN amb CIFAR-10" desc="Classificació d'imatges amb una xarxa convolucional." />
          <ProjectCard icon={Code2} title="LSTM de sentiments" desc="Anàlisi de sentiment en text amb una xarxa recurrent." />
        </div>
      </Seccio>

      <Seccio titol="Reinforcement Learning" icona={Gamepad2} color={C}>
        <div className="space-y-4">
          {["RL_01", "RL_02", "RL_03"].map((c) => (
            <QuadernCard key={c} codi={c} color={C}>
              <Chivato f={chivatos[c]} />
            </QuadernCard>
          ))}
        </div>
        <p className="text-gray-700 text-sm mt-4 mb-3">
          A <code className="bg-gray-100 px-1 rounded">Reinforcement Learning/02_fundamentos/</code> hi
          ha el codi base dels agents i dos exemples de referència:
        </p>
        <div className="grid sm:grid-cols-2 gap-3 mb-6">
          <ProjectCard icon={Bot} title="Q-learning amb Taxi" desc="L'agent clàssic de taula Q a l'entorn Taxi de Gymnasium." />
          <ProjectCard icon={Bot} title="DQN amb CartPole" desc="La mateixa idea però amb una xarxa neuronal com a aproximador." />
        </div>
        <h3 className="font-medium text-gray-900 mb-2">Projectes amb DQN</h3>
        <div className="grid sm:grid-cols-3 gap-3 mb-6">
          <ProjectCard icon={Gauge} title="Flappy Bird" desc="Agent DQN que aprèn a travessar els tubs del joc." />
          <ProjectCard icon={Gamepad2} title="Nibbler" desc="Variant tipus Snake: l'agent aprèn a créixer sense xocar." />
          <ProjectCard icon={Car} title="Racing" desc="Cotxe que aprèn a conduir en pista. És l'entorn del concurs." />
        </div>
        <h3 className="font-medium text-gray-900 mb-2">Projectes avançats, per a qui vulgui més</h3>
        <div className="grid sm:grid-cols-2 gap-3">
          <ProjectCard icon={Car} title="Highway" desc="Conducció autònoma 2D: autopista, pàrquing i interseccions, amb DQN/PPO i curriculum learning." />
          <ProjectCard icon={Rocket} title="LunarLander" desc="Aterratge amb Stable-Baselines3, comparant PPO, DQN, A2C i variants contínues (SAC/TD3)." />
          <ProjectCard icon={Grid3x3} title="MiniGrid" desc="Navegació per laberints: obrir portes i recollir objectes, amb MLP o CNN segons la variant." />
          <ProjectCard icon={PersonStanding} title="PyBullet" desc="Robòtica i física 3D: robots que aprenen a caminar, nedar o saltar amb PPO, SAC o TD3." />
        </div>
        <p className="text-gray-700 text-sm mt-4">
          A <code className="bg-gray-100 px-1 rounded">Reinforcement Learning/modelos/</code> hi ha pesos
          ja entrenats (CartPole, Nibbler, Racing, Flappy Bird, LunarLander...). Et deixen veure un
          agent que ja juga bé sense esperar l'entrenament, i comparar-lo amb el teu.
        </p>
      </Seccio>

      <Seccio titol="Com posar-ho en marxa en local" icona={Terminal} color={C}>
        <p className="text-gray-700 text-sm mb-3">
          Cada carpeta (Deep Learning i Reinforcement Learning) té el seu{" "}
          <code className="bg-gray-100 px-1 rounded">requirements.txt</code>, així que convé un entorn
          virtual per carpeta:
        </p>
        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{`cd "Deep Learning"          # o "Reinforcement Learning"
python -m venv .venv
.venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
jupyter lab`}
        </pre>
      </Seccio>

      {/* ---------- 2 · Exemples ---------- */}
      <Pas id="exemples" num={2} titol="Exemples" color={C} subtitol="El pas de PyTorch a DQN fet de principi a fi, i la plantilla on entrenes el teu agent." />
      <Seccio icona={Eye} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="DL_PR" color={C} etiqueta="de PyTorch a DQN">
            <Chivato f={chivatos.DL_PR} />
          </QuadernCard>
          <QuadernCard codi="CONCURS" color={C} etiqueta="el teu agent">
            <Chivato f={chivatos.CONCURS} />
          </QuadernCard>
        </div>
      </Seccio>

      {/* ---------- 3 · Reptes ---------- */}
      <Pas id="reptes" num={3} titol="Reptes" color={C} />
      <Seccio icona={Mountain} color={C}>
        <div className="space-y-4">
          <Reptes bloc={4} color={C} />
          <QuanCridar color={C} />
        </div>
      </Seccio>

      {/* ---------- 4 · Prova ---------- */}
      <Pas id="prova" num={4} titol="Prova i concurs" color={C} subtitol="La Pe4 és el punt de control del material més dur del curs. La Pp4 és la defensa del teu agent." />
      <Seccio icona={ClipboardCheck} color={C}>
        <ProvaBloc bloc={4} color={C} />
        <div className="mt-4">
          <ActivitatsBloc bloc={4} />
        </div>
      </Seccio>

      <Seccio titol="El concurs: Gran Premi RL" icona={Trophy} color="indigo">
        <div className="space-y-3 text-gray-700 text-sm">
          <p>
            Entorn: <strong>Racing</strong>, el de{" "}
            <code className="bg-gray-100 px-1 rounded">03_proyectos_dqn/racing</code>. Diversos cotxes
            corren alhora a la mateixa pista, així que és una cursa de veritat. Entrena ràpid en CPU:
            no cal GPU.
          </p>
          <ul className="list-disc list-inside space-y-1">
            <li>
              Lliures un fitxer <code className="bg-gray-100 px-1 rounded">agent.pth</code>: els pesos
              d'una <code className="bg-gray-100 px-1 rounded">CarDQN</code> amb 6 entrades i 9 sortides.
              No en canviïs la forma: el jutge la dona per fixada.
            </li>
            <li>Les sessions S31 i S32 són d'entrenament lliure. El lliurament es tanca al final de la S32.</li>
            <li>Et pots autoavaluar abans amb <code className="bg-gray-100 px-1 rounded">avalua_agent.py --model</code>.</li>
            <li>El 2 de febrer es corre la cursa final i defenses el teu agent davant del grup.</li>
          </ul>
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-amber-900">
              <strong>No es puntua la posició al marcador.</strong> Es puntua l'agent lliurat, que
              funcioni, i que puguis explicar quina recompensa vas dissenyar i per què. Qui no pugui
              justificar el seu agent, no el té. Guanyar és el premi, no la nota: si fos la nota,
              guanyaria qui tingués el millor portàtil.
            </p>
          </div>
          <a
            href={githubUrl("Reinforcement Learning/06_concurs/README.md")}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 font-medium text-indigo-600 hover:text-indigo-800"
          >
            <BookOpen className="w-4 h-4" />
            Reglament complet del concurs
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </Seccio>

      <SeguentBloc actual={4} />
    </div>
  );
}
