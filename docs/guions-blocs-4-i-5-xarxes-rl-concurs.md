# Guions dels blocs 4 i 5 — Xarxes neuronals, RL i el concurs

Vuit sessions, del 15 de desembre al 26 de gener. Un guió per sessió, per obrir i tirar.

Material a `Deep Learning/` i `Reinforcement Learning/`. **Avís sobre aquest material**: és
d'una edició anterior i **està escrit en castellà**, mentre que tot el bloc de Machine Learning
és en català. No s'ha traduït perquè és molt material i funciona; convé dir-ho a classe el
primer dia del bloc en lloc de deixar que ho descobreixin.

---

# Bloc 4 — Xarxes neuronals (S26–S28)

Tres sessions per a un bloc que normalment demanaria vuit. **Es pot fer, i el motiu és
concret**: la part difícil ja està feta a la S19. Qui va entendre el descens de gradient ja té
la retropropagació a mig camí, i aquest bloc és aplicar-ho amb una llibreria que ho automatitza.

El bloc no és un curs de deep learning: **és el pont cap a RL.** Tot el que no serveixi per
entendre un agent DQN es pot deixar per als enllaços.

## S26 · dimarts 15 de desembre · Què és una xarxa neuronal

**Quaderns:** `Deep Learning/01_teoria/DL_01_fundamentos.ipynb`, i el començament de `DL_02_pytorch_basico.ipynb`

| Temps | Què |
|---|---|
| 20 min | **Obre reconeixent el que ja saben.** Un perceptró és $\sigma(w\cdot x + b)$: la regressió logística de la S18, sencera. Escriu-la a la pissarra amb la notació de la S08 i que ho vegin ells. |
| 20 min | Què s'hi guanya apilant-ne: funcions d'activació, i per què sense una activació no lineal apilar capes no serveix de res (el producte de matrius lineals és una matriu lineal). **Demostra-ho**, no ho enunciïs. |
| 25 min | Forward propagation com una cadena de productes de matrius. `DL_01` ho té fet. |
| 30 min | **Retropropagació, i la frase que l'ha de desmuntar**: és la regla de la cadena aplicada al gradient de la S19. No és un algorisme nou, és el mateix descens amb la derivada calculada per trossos. Que vegin la correspondència terme a terme si es pot. |
| 15 min | Funcions de pèrdua: l'entropia creuada torna a sortir, i ja saben d'on ve (S16 i S20). |

**Si aquesta sessió va bé, el bloc va bé.** Tot l'estalvi de temps depèn que vegin que no estan
començant una cosa nova.

## S27 · dilluns 21 de desembre · PyTorch

**Quaderns:** `DL_02_pytorch_basico.ipynb`, `DL_03_arquitecturas.ipynb`, `DL_04_entrenamiento.ipynb`

**Objectiu:** saber escriure i entrenar una xarxa. Res més.

| Temps | Què |
|---|---|
| 20 min | Tensors: són arrays de NumPy que saben en quina GPU viuen i recorden com s'han calculat. |
| 25 min | **`autograd`, que és el moment de la sessió.** Ells van calcular el gradient de la log-loss a mà a la S19 i el van verificar per diferències finites. Ara ensenya que `loss.backward()` fa això mateix per a qualsevol funció. **Comprova-ho**: agafa una funció senzilla, calcula'n la derivada a mà, i compara-la amb la que dona `autograd`. |
| 30 min | El cicle d'entrenament: `zero_grad`, `forward`, `loss`, `backward`, `step`. Que reconeguin cada línia del bucle que van escriure a la S19. |
| 30 min | Una xarxa completa entrenada, amb la corba de pèrdua. Arquitectures, per damunt: MLP per a taules, CNN per a imatges, i prou. |
| 15 min | Guardar i carregar pesos, que **els caldrà obligatòriament per lliurar l'agent del concurs**. |

**El que es deixa fora a posta:** RNN, LSTM, autoencoders, transfer learning, i tot
`DL_04` més enllà de l'optimitzador i l'*early stopping*. Són als quaderns per a qui vulgui, i
es diu que hi són.

## S28 · dilluns 11 de gener · De la xarxa a l'agent

**Quadern:** `DL_05_redes_para_RL.ipynb`

**Objectiu:** el pont. En sortir d'aquí han d'entendre què és una xarxa que decideix accions.

| Temps | Què |
|---|---|
| 20 min | Repàs curt del bloc, després de dues setmanes de vacances. No en donis per sabut res. |
| 30 min | **El canvi de problema.** Fins ara la xarxa rebia dades i deia una classe, i algú li deia la resposta correcta. Ara rep un estat i diu una acció, i **ningú no li diu què havia de fer**: només rep una recompensa, potser molt més tard. Aquesta és la diferència entre supervisat i RL, i s'ha d'entendre abans de veure una sola línia de codi. |
| 35 min | La xarxa Q: entrada l'estat, sortida un valor per acció. Amb `CarDQN` del concurs com a exemple concret: 6 valors d'entrada, 9 accions de sortida, dues capes de 128. **És literalment la xarxa que entrenaran.** |
| 25 min | Per què calen dues xarxes (principal i objectiu) i per què es guarda l'experiència en memòria. A nivell de per què, no de com. |
| 10 min | **Presentació del concurs.** Ensenya el `README.md` de `06_concurs/` i la pista de Racing corrent amb els agents ja entrenats de `modelos/`. |

---

# Bloc 5 — Reinforcement Learning i el concurs (S29–S33)

El tancament del curs. **El material del concurs ja existeix** a
`Reinforcement Learning/06_concurs/`: el reglament, la plantilla d'agent i l'script jutge.

L'entorn és **Racing**, i la raó és que és l'únic del repositori on els agents comparteixen
literalment la pantalla (`RacingGame(n_cars=N)`): els altres només permeten comparar
puntuacions obtingudes per separat. A més entrena en CPU en minuts i no necessita instal·lar
res que no hi hagi ja. El detall i les alternatives són al README del concurs.

## S29 · dimarts 12 de gener · Fonaments de RL

**Quadern:** `Reinforcement Learning/01_teoria/RL_01_fundamentos.ipynb`

| Temps | Què |
|---|---|
| 30 min | Agent, entorn, estat, acció, recompensa. Amb un exemple que es pugui dibuixar a la pissarra. |
| 25 min | **El problema del crèdit diferit**: com saps quina de les 200 accions t'ha fet perdre. És el que fa RL difícil i mereix el temps. |
| 25 min | Exploració contra explotació, i `epsilon`. Que juguin amb el valor i vegin l'efecte. |
| 25 min | Q-learning amb una taula, sobre Taxi (`02_fundamentos/ejemplos/ejemplo_qlearning_taxi.py`). **La taula primer, la xarxa després**: així la xarxa s'entén com el que substitueix una taula que no cabria. |
| 10 min | **Reglament del concurs, repartit i llegit en veu alta.** Format del lliurament: un fitxer `agent.pth`, amb el nom exacte. Es reparteix `plantilla_agent.ipynb`. |

## S30 · dilluns 18 de gener · DQN

**Quadern:** `RL_02_dqn.ipynb`

| Temps | Què |
|---|---|
| 25 min | De la taula a la xarxa: per què amb estats continus la taula no serveix. |
| 30 min | DQN sencer: memòria d'experiència, xarxa objectiu, i el bucle d'entrenament. Amb CartPole, que és ràpid i fiable. |
| 35 min | **`racing_game.py` i `CarAgent`**: l'arquitectura que faran servir, els 6 sensors i les 9 accions, i **el disseny de la recompensa**, que és on de veritat es guanya el concurs. Ensenya dues recompenses diferents entrenades i el comportament tan diferent que en surt. |
| 30 min | **Comencen a entrenar**, amb la plantilla oberta. Que tothom acabi la sessió amb un agent que ja corre, encara que ho faci malament. |

**El que has de deixar clar avui:** el que distingeix un bon agent no és la mida de la xarxa,
és la funció de recompensa. Si no es diu, tots pujaran les capes a 512 i no milloraran res.

## S31 · dimarts 19 de gener · Entrenament lliure

| Temps | Què |
|---|---|
| 10 min | Recordatori del format de lliurament i de la data de tancament. |
| 100 min | **Entrenament i ajust, cadascú al seu ritme.** El professor circula. |
| 10 min | Autoavaluació amb `avalua_agent.py --model` i comparació amb la línia base. |

**El teu paper avui no és explicar, és desencallar.** Les tres coses que fallaran, per ordre:
la recompensa no incentiva el que creuen, l'`epsilon` baixa massa de pressa, i no guarden els
pesos. La tercera és la que fa perdre una tarda de feina, així que insisteix-hi al principi.

## S32 · dilluns 25 de gener · Entrenament lliure i lliurament

| Temps | Què |
|---|---|
| 90 min | Última finestra d'entrenament i ajust. |
| 20 min | **Tancament del lliurament.** Es recullen els `agent.pth`. Sense excepcions: demà es competeix amb el que hi hagi. |
| 10 min | Es genera el marcador de classificació amb `avalua_agent.py --marcador`, **i no s'ensenya**. Que quedi per a demà. |

**Prepara't per a la nit abans:** executa el marcador tu, amb temps, i comprova que tots els
lliuraments carreguen. Un `state_dict` amb una arquitectura diferent de la de la plantilla no
carrega, i val més descobrir-ho avui que davant de la classe.

## S33 · dimarts 26 de gener · EL CONCURS

**El tancament del curs.** `avalua_agent.py --cursa-final`, projectat.

| Temps | Què |
|---|---|
| 15 min | Presentació del marcador de classificació i dels que passen a la cursa final. |
| 15 min | **Els agents de referència primer**: l'aleatori i la línia base del professor. Serveix per calibrar la mirada del públic abans de començar. |
| 45 min | **La Gran Cursa Final**, projectada. Els millors agents a la mateixa pista. |
| 25 min | **Cada finalista explica el seu agent**: quina recompensa va dissenyar i per què. **Això és el que es puntua**, i s'ha de veure que es puntua. |
| 20 min | Podi, i tancament del curs. |

**La regla que ha d'estar dita des de la S29 i repetida avui:** el concurs **no es puntua per
posició al marcador**. Es puntua l'agent lliurat, que funcioni, i la justificació de les
decisions. Si es puntués la posició, guanyaria qui té el portàtil més potent, i això no és el
que s'avalua.

**I la frase del tancament**, si es vol lligar el curs sencer: l'agent que acaba de guanyar
aprèn amb el mateix descens de gradient que van implementar a mà el 17 de novembre, sobre una
funció de pèrdua que van deduir el 23 de novembre. No hi ha hagut màgia en cap moment del curs.

---

## Els punts on aquests dos blocs es trenquen

**Si l'1 de desembre encara s'està al bloc 2**, s'ha de saltar directament aquí i deixar `MA_05`
i `MA_06` com a material de consulta. **El concurs no es toca**: és el que sosté la motivació
del grup i és l'única cosa del curs que no es pot recuperar més endavant.

**Si la S26 va mal**, el problema no és la xarxa: és que la S19 no va quallar. Amb tres sessions
no hi ha marge per reparar-ho aquí, així que val més detectar-ho al desembre i decidir
conscientment què es deixa de banda.

**El risc tècnic del concurs és el parc de portàtils.** Racing s'ha triat perquè no demana
instal·lar res de nou, però convé provar-ho en una màquina de classe abans de la S30, no el dia.
