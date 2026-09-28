# Gran Premi RL — el concurs final del bloc

Cloenda del bloc de Reinforcement Learning: els alumnes entrenen un agent
que competeix en directe, projectat a classe, contra la resta de la classe,
contra una línia base del professor i contra un agent aleatori.

## Entorn triat: Racing (`03_proyectos_dqn/racing`)

**Per què Racing i no LunarLander o Flappy Bird:**

- **És l'únic que és una batalla de veritat.** LunarLander i Flappy Bird són
  entorns d'un sol agent: "competir" hi vol dir comparar puntuacions
  mitjanes obtingudes per separat. Racing ja suporta N cotxes corrent
  simultàniament a la mateixa pista (`RacingGame(n_cars=N)`): és l'únic
  entorn del repositori on els agents dels alumnes comparteixen literalment
  la pantalla i es poden veure competint. Per un concurs que vol ser
  "el colmo del final", això pesa molt.
- **És vistós.** Pista amb sensors dibuixats, cotxes de colors, panell de
  distància i fitness en directe: es projecta bé i s'entén d'un cop d'ull
  qui va guanyant, fins i tot per algú que no ha tocat RL en sa vida.
- **Entrena ràpid en CPU.** L'agent (`CarAgent`, DQN amb 2 capes de 128) té
  un estat de només 6 valors; en uns minuts en un portàtil normal ja es
  veuen cotxes que saben seguir la pista. No cal GPU ni hores de Colab.
- **Ja funciona amb el que hi ha instal·lat.** Aquest és un motiu pràctic,
  no només pedagògic: a l'entorn de proves (`CEIABD-IA/.venv`) hi ha
  `torch`, `gymnasium` i `pygame`, però **no** `stable-baselines3`, **no**
  `box2d` (necessari per LunarLander) ni `flappy-bird-gymnasium`. Racing
  no en depèn de cap: és pur PyTorch + Pygame. Muntar el concurs sobre
  LunarLander o Flappy Bird voldria dir instal·lar dependències noves a
  tots els portàtils de classe abans de la sessió 1; amb Racing, no cal
  tocar res.

**Alternatives, si en algun moment interessen:**

- **CartPole** (`02_fundamentos/ejemplos/ejemplo_cartpole_dqn.py`): la més
  senzilla i fiable (`gymnasium` pur, sense Box2D), però és d'un sol
  agent — cap batalla real, només comparar mitjanes. Bona opció de reserva
  si Racing donés problemes en algun portàtil concret.
- **LunarLander / Flappy Bird**: més espectaculars a l'ull, però requereixen
  instal·lar `stable-baselines3` + `box2d-py` (LunarLander) o
  `flappy-bird-gymnasium` (Flappy Bird) — cap dels dos hi és ara mateix.
  Si es volen fer servir, cal instal·lar-los abans i adaptar
  `avalua_agent.py` (que ara assumeix `CarDQN`); no s'ha fet en aquesta
  entrega perquè l'encàrrec deia explícitament de no instal·lar res.

## Calendari (5 sessions, del 12 al 26 de gener de 2027)

| Sessió | Data | Tipus | Contingut |
|---|---|---|---|
| 1 | dt 12 gener | Teoria | Recapitulació DQN + presentació del concurs: reglament, entorn, com es puntua. Es reparteix `plantilla_agent.ipynb`. |
| 2 | dl 18 gener | Teoria | Arquitectura `CarDQN`, disseny de la recompensa, variants A-D de `racing_game.py`. Comença l'entrenament a la plantilla. |
| 3 | dt 19 gener | Entrenament lliure | Cadascú entrena i ajusta el seu agent (portàtil o Colab). Autoavaluació amb `avalua_agent.py --model`. |
| 4 | dl 25 gener | Entrenament lliure + tancament | Última finestra per pujar la versió final d'`agent.pth`. Al final de la sessió es tanca el lliurament i es genera el marcador de classificació. |
| 5 | dt 26 gener | **EL CONCURS** | Gran Cursa Final projectada a classe (`avalua_agent.py --cursa-final`) + lliurament del podi. |

## Format de lliurament

Cada alumne entrega un fitxer anomenat exactament **`agent.pth`**: l'
`state_dict` de la xarxa `CarDQN(state_size=6, n_acciones=9)` tal com la
defineix `racing_game.py` (2 capes amagades de 128, tal com ve per
defecte). Es guarda així, mai l'agent sencer:

```python
torch.save(agent.q_network.state_dict(), "agent.pth")
```

**No es toca l'arquitectura de la xarxa.** Si algú canvia les mides de les
capes amagades, `avalua_agent.py` no podrà carregar el fitxer (dona un
error explicant exactament què no quadra). Els hiperparàmetres
d'entrenament (gamma, epsilon, episodis...) sí que es poden tocar lliurement.

Estructura de la carpeta de lliuraments que espera l'script jutge:

```
lliuraments/
  alba/agent.pth
  bernat/agent.pth
  carla/agent.pth
  ...
```

(Un fitxer `agent.pth` per subcarpeta; el nom de la subcarpeta és el que
sortirà al marcador.)

## Com es puntua

- **Mètrica**: la `fitness` del cotxe en acabar la partida — en la pràctica,
  la distància recorreguda abans de xocar o d'esgotar el límit de passos
  (`racing_game.py` no compta voltes ni checkpoints: el camp existeix però
  mai s'incrementa, així que la puntuació real és distància). És la mateixa
  mètrica que ja veuen als prints d'entrenament del bloc 3, no és res nou.
- **Reproduïble**: mateix nombre d'episodis per a tothom (5 per defecte),
  mateix límit de passos per episodi (2000, el mateix que fa servir
  l'entrenament original), i es sembren tots els generadors d'atzar
  (`random`, `numpy`, `torch`) abans de cada episodi. En la pràctica
  l'avaluació és determinista (política sense exploració, física sense
  atzar), de manera que els episodis repetits donen el mateix resultat —
  repetir-los és una xarxa de seguretat davant algú que faci servir mostreig
  estocàstic en lloc d'argmax, no un mecanisme per introduir variància.
- **Puntuació final**: mitjana de fitness dels episodis.
- **Empats**: es desempaten per (1) voltes completades — si mai n'hi
  arriba a haver —, (2) passos de mitjana que el cotxe es manté viu.
- **Agent encallat**: el límit de 2000 passos per episodi talla qualsevol
  cotxe que es quedi voltant sense avançar; no pot bloquejar l'avaluació.

## Contra qui competeixen

A més d'entre ells, el marcador sempre inclou dues referències fixes:

- **Agent aleatori**: tria accions a l'atzar. Qui no el supera clarament és
  que encara no ha après res útil.
- **Professor (línia base)**: un dels agents ja entrenats a
  `../modelos/car_agent_0.pth` (variant A, independent). És un llistó
  assolible però real. **Abans del concurs, val la pena substituir aquest
  fitxer per un agent millor entrenat expressament de línia base** (el codi
  no canvia; només cal sobreescriure `modelos/car_agent_0.pth` o el que
  apunti la constant `AGENT_PROFESSOR` a `avalua_agent.py`).

## Format de la competició

Dues fases, pensades per encaixar en la sessió 4 (classificació) i la
sessió 5 (concurs) de 2h:

1. **Classificació** (`avalua_agent.py --marcador`): cada `agent.pth`
   entregat es puntua en solitari contra la pista, com s'ha explicat més
   amunt. Dona un marcador complet i objectiu de tota la classe.
2. **Gran Cursa Final** (`avalua_agent.py --cursa-final`): els **6 millors**
   classificats + el professor + l'agent aleatori (**8 cotxes en total**,
   just el nombre de colors que ja defineix `racing_game.py`) corren tots
   alhora, en directe, a la mateixa pista. És el que es projecta a classe.
   La classificació final d'aquesta cursa (no la de la fase 1) decideix el
   podi — un agent pot anar més just en solitari i sortir-se'n millor (o
   pitjor) quan hi ha trànsit d'altres cotxes al mig.

Si la classe és petita (≤8 alumnes) es pot saltar la fase 1 i fer-los
competir tots directament a la Gran Cursa Final amb `--top` igual al
nombre d'alumnes.

**Què es projecta**: la finestra de pygame de la Gran Cursa Final, amb el
panell de distància/fitness en directe (ja el dibuixa `racing_game.py`) més
una llegenda a la dreta amb el nom de cada alumne al costat del seu color de
cotxe (l'afegeix `avalua_agent.py`). En acabar, es projecta la classificació
final per terminal.

## Ús de `avalua_agent.py`

```bash
# Un alumne prova el seu propi agent abans d'entregar
python avalua_agent.py --model lliuraments/alba/agent.pth

# El professor genera el marcador de tota la classe (sessió 4)
python avalua_agent.py --marcador lliuraments/ --sortida marcador.csv

# La Gran Cursa Final, projectada (sessió 5)
python avalua_agent.py --cursa-final lliuraments/ --top 6 --render
```

Opcions més rellevants: `--episodis` (per defecte 5), `--max-passos` (per
defecte 2000), `--top` (alumnes que passen a la final, per defecte 6).
`--render` obre la finestra de pygame; sense ell, l'script corre en text
pla (útil per calcular el marcador ràpid sense esperar cap finestra).

## Plantilla dels alumnes: `plantilla_agent.ipynb`

Reparteix aquest notebook a la sessió 1. Inclou:

- Importació de `racing_game.py` i explicació ràpida de l'entorn (estat,
  accions, recompensa).
- Un bucle d'entrenament propi (`entrena(...)`), separat del de
  `racing_game.py` perquè aquell sempre obre finestra; aquest funciona amb
  `render=False` a qualsevol portàtil **i a Google Colab** (que no té
  pantalla).
- Desat del model amb el nom i el format exactes que espera el jutge.
- Una cel·la d'autoavaluació que crida `avalua_agent.avaluar_agent(...)`
  directament, perquè cada alumne vegi la seva puntuació abans d'entregar.

Verificat sencer amb `_eines/executa_nb.py`, 0 errors (vegeu més avall).

## Estat de l'entorn de proves — què queda per verificar

Interpret fet servir per a tota la verificació:
`E:\WORK\Xavi\ProjectsITIC\CEIABD-IA\.venv\Scripts\python.exe` (Python 3.12).

Comprovat a aquest entorn:

| Paquet | Estat |
|---|---|
| `torch` 2.6.0+cu124 | ✅ instal·lat |
| `gymnasium` 1.2.3 | ✅ instal·lat |
| `pygame` 2.6.1 | ✅ instal·lat |
| `stable_baselines3` | ❌ **no instal·lat** |
| `box2d` | ❌ **no instal·lat** (calen per LunarLander) |
| `flappy_bird_gymnasium` | ❌ **no instal·lat** |

Com que el concurs es basa en Racing (pur `torch` + `pygame`), cap
d'aquestes tres mancances afecta `avalua_agent.py` ni la plantilla: tots
dos s'han executat de veritat en aquest entorn, sense instal·lar res nou.

**El que sí queda pendent de comprovar a un portàtil real de classe** (aquí
no hi ha pantalla física, només s'ha simulat amb el driver `dummy` de SDL):
que la finestra de `--render` es vegi bé projectada i que el ritme
(`clock.tick(60)`) sigui còmode de seguir amb 8 cotxes alhora. Val la pena
fer un assaig de la Gran Cursa Final abans de la sessió 5, no el dia mateix.
