# Didàctica de la matemàtica dels models

Notes per impartir el bloc de machine learning: quina matemàtica es dona, com s'aterra al
codi, i què passa a cada sessió.

Acompanya els quaderns de `Machine Learning/01_teoria/` i `Machine Learning/03_matematiques/`.

## El problema de partida, corregit

La primera versió d'aquest document partia d'una premissa: que l'alumnat de 2n de DAM i DAW
programa bé però que la matemàtica no és el seu terreny, i que per tant calia donar-ne la
mínima. **Aquesta premissa era equivocada per a aquest grup concret**, i val la pena deixar
escrit per què, perquè és el que ordena tot el material.

L'optativa es va plantejar difícil a posta i **es va anunciar com a difícil**. Tot i això s'hi
han apuntat 15 alumnes, i el que els té contents és precisament això. **Gaudeixen entenent la
matemàtica que hi ha darrere dels models**, i el «per què» els interessa tant com el «com».

Això canvia el problema. Ja no és *quanta matemàtica es pot donar sense perdre el grup*, sinó
una cosa força diferent, i és el risc real d'aquest curs:

> El professor explica teoria potent i no l'aterra al codi.

Una teoria que no baixa a una línia de NumPy es queda en espectacle. Impressiona el primer
dia i no es pot fer servir el segon. **El criteri de tot el material és aquest**: cada fórmula
que apareix en un text va seguida de la línia de codi que la calcula, i cada implementació
acaba amb una comprovació numèrica contra scikit-learn.

El resultat d'aprenentatge oficial diu «**crea aplicacions** fent ús de models d'aprenentatge
automàtic». No diu demostra ni dedueix. **La matemàtica, doncs, no és l'objectiu avaluable:
és el camí que aquest grup vol seguir per arribar-hi**, i es dona perquè la volen i perquè fa
millors programadors de models, no perquè la fitxa la demani. Això té una conseqüència directa
a l'avaluació, i és al final del document.

## El mètode: implementar-ho abans d'invocar-ho

Cada quadern segueix el mateix camí, i és el que sosté tot el bloc:

1. Es planteja un problema concret.
2. S'explica la fórmula que el resol, amb números petits fets a mà.
3. **S'implementa amb Python i NumPy, sense scikit-learn.**
4. **Es compara amb scikit-learn i ha de donar el mateix.**

El pas 4 és el que canvia la relació amb la llibreria. Quan un alumne escriu la seva funció
de distància, calcula els veïns, vota, i després veu que `KNeighborsClassifier` dona
exactament el mateix, `fit` deixa de ser màgia. I quan calcula la impuresa de Gini de tots
els talls possibles i li surt 2,45, que és el número que va aparèixer a la demostració del
primer dia, la cosa encaixa sola.

És més lent que explicar l'API. També és l'única manera que després sàpiguen per què un
model falla.

**Al bloc de matemàtiques el pas 4 puja de nivell**: ja no es comprova només que el resultat
coincideixi, sinó que **la derivada coincideix amb la derivada numèrica**, que la condició
teòrica es compleix a les dades reals, i que dues expressions que semblen diferents donen el
mateix número fins a l'últim decimal. Això és com es verifica matemàtica de veritat, i és
una habilitat transferible.

## Dues capes de material

El bloc de teoria i el de matemàtiques **no són el mateix contingut a dos nivells**: són dos
passos del mateix camí, i el segon comença on s'acaba el primer.

| | `01_teoria/` | `03_matematiques/` |
|---|---|---|
| Què respon | Què fa el model i com es fa servir | Per què el model és així i d'on surt la fórmula |
| Qui l'ha de fer | Tothom | Tothom en aquest grup, i és el que els enganxa |
| Nivell | Pitàgores, proporcions, l'equació de la recta, l'exponencial | Derivades, gradients, àlgebra lineal, versemblança, optimització amb restriccions |
| És avaluable | Sí | Com a eina de raonament, no com a deducció memoritzada |

### El bloc de teoria: els cinc models

Van de menys a més matemàtica, no per importància:

1. **k-NN** — la distància. És el més senzill i serveix per instaurar el mètode: implementar,
   comparar, entendre. Aquí surt per primera vegada **el parany de les escales**.
2. **Arbres** — la impuresa i la tria del tall. Connecta directament amb els condicionals que
   van fer al bloc de Python. Aquí surt **el sobreajust**, de la manera més visible del curs.
3. **Boscos** — per què votar funciona, i per què només funciona si els errors són diferents.
4. **Regressió logística** — la frontera i la probabilitat.
5. **SVM** — el marge i el kernel. Tanca la sèrie amb la taula comparativa dels cinc models.

### El bloc de matemàtiques: sis quaderns

Cadascun agafa una idea que als quaderns de teoria va quedar a mitges i la porta fins al fons.

| Quadern | La pregunta que respon | El moment que ha de funcionar |
|---|---|---|
| `MA_01_algebra_lineal` | Què són de veritat les dades i els pesos | Treure el `coef_` d'un model entrenat, calcular `X @ w + b` a mà i veure que el signe encerta les 150 files |
| `MA_02_descens_gradient` | Com aprenen els models | Comprovar que el gradient analític coincideix amb el numèric, i entrenar la logística amb un bucle propi |
| `MA_03_probabilitat_versemblanca` | D'on surt la funció de pèrdua | Veure que la log-loss és la versemblança amb un logaritme i un signe menys |
| `MA_04_entropia_informacio` | Què és el desordre que mesuren els arbres | Veure que la log-loss i l'entropia creuada són el mateix número |
| `MA_05_marge_optimitzacio` | Per què l'SVM depèn de pocs punts | Comprovar que tots els vectors de suport compleixen la condició de folgança, i reconstruir `w` a partir dels multiplicadors |
| `MA_06_pca_vectors_propis` | Com es redueixen dimensions | Trobar la direcció de màxima variància per força bruta i veure que és un vector propi |

**L'ordre importa**: `MA_01` abans que tot, i `MA_02` abans de `MA_05`. Els altres són
independents entre si i es poden intercalar amb el model corresponent del bloc de teoria.

## La trampa que s'ha desfet, i la que queda

La versió anterior d'aquest material feia **dues trampes conscients**. Amb aquest grup, una
ja no cal, i l'altra es manté però s'explicita.

**Desfeta: l'entrenament de la regressió logística.** Al quadern `ML_04` els pesos es troben
per força bruta, provant una graella i quedant-se el millor. Servia per no haver d'explicar
càlcul. **`MA_02` desfà aquesta trampa sencera**: hi ha la derivada de la log-loss, la
comprovació del gradient contra el gradient numèric, i l'entrenament amb un bucle de descens
de gradient. El quadern de força bruta es manté, perquè el càlcul de quantes combinacions
caldrien amb 30 pesos és exactament el que justifica el gradient.

**Es manté: el problema dual de l'SVM.** Derivar-lo sencer és massa, i no per nivell de
dificultat sinó perquè no hi cap en el temps del curs. El que es fa a `MA_05` és presentar el
resultat del dual, **dir en veu alta que no es deriva i per què**, i verificar-lo
numèricament amb un model ja entrenat: comprovar la folgança complementària a les dades i
reconstruir `w` a partir dels multiplicadors. La diferència entre fer trampa i ser honest és
dir què t'estàs saltant.

Val la pena dir en veu alta que s'està fent això. Aquest grup accepta bé un «això es resol amb
eines que veureu si feu una enginyeria, i mentrestant ho verifiquem numèricament»; el que no
accepta bé és descobrir que se li ha amagat alguna cosa.

## Què passarà a classe

**Preguntaran per què hi ha cinc models si tots fan el mateix.** No fan el mateix: decideixen
diferent, es trenquen diferent i demanen preparacions diferents de les dades. La taula final
del quadern de l'SVM existeix per a aquesta pregunta.

**Algú notarà que el bosc aleatori surt pitjor que l'arbre sol a Iris.** És cert i està
documentat. Iris és minúscul i fàcil. Al quadern de boscos hi ha un segon exemple, fabricat
amb `make_classification`, on el bosc sí que guanya clarament. Ensenyar els dos casos junts
val més que qualsevol explicació.

**Es quedaran encallats amb les 4 dimensions.** Iris té quatre columnes i no es pot dibuixar.
La frase que ho desencalla: *no cal poder imaginar-ho per poder calcular-ho*. La fórmula de
la distància és la mateixa amb dos sumands que amb quatre o amb quatre-cents. I al final del
curs, `MA_06` els dona l'eina per dibuixar-ho tot i així.

**Confondran precisió d'entrenament amb precisió d'examen.** És l'error conceptual més car
del bloc. Convé insistir-hi cada vegada que aparegui un número.

**Amb el bloc de matemàtiques, preguntaran si això entra a l'examen.** La resposta honesta és
que el que entra és fer-ho servir, no reproduir-ho. Vegeu l'apartat següent.

**I n'hi haurà que vulguin més.** És el grup que és. Convé tenir a mà on continuar: el
descens de gradient porta a les xarxes neuronals, que ja són al bloc 4 del curs; els vectors
propis porten al PCA i a tot el no supervisat; i la versemblança porta als models
probabilístics. Els enllaços de divulgació són a `_moodle-25-26/ENLLACOS.md`.

## Com es dissenya un exercici, i l'error que s'hi va cometre

Aquesta secció existeix per una correcció del 29 de setembre. El material de pràctica tenia
**dos defectes que es tapaven l'un amb l'altre**, i val la pena deixar-los escrits perquè és
fàcil tornar-hi a caure.

### Primer defecte: els enunciats regalaven la troballa

Cada exercici acaba amb una línia de «com saps que ho has fet bé». La intenció era bona: que
l'alumne es pugui comprovar sol, sense esperar el professor. El problema és **què s'hi posava**:

> Com saps que ho has fet bé: sense escalar la precisió ronda el 72 %; escalant puja al 94,4 %.

> Com saps que ho has fet bé: la matriu surt `[[60, 3], [7, 101]]`: 3 malignes sense detectar.

La segona és la pitjor de totes. **Tot el sentit d'aquell exercici és el cop de descobrir que
darrere d'un 94 % de precisió hi ha tres tumors que passen**, i estava dit a l'enunciat, abans
de començar. Amb això, l'exercici es fa en cinc minuts, sembla trivial i no ensenya res. Les
paraules d'en Xavi: *«si añades la solución los alumnos lo ven estúpidamente simple»*.

### Segon defecte: se'ls demanaven eines que no s'expliquen enlloc

Comparant el codi que els exercicis demanen amb tot el que apareix als quaderns previs:

| Exercici | Eines que demanava i que no sortien a cap quadern |
|---|---|
| `EX_02_cancer` | `confusion_matrix`, `classification_report`, `precision_score`, `recall_score` |
| `EX_03_digits` | `confusion_matrix` |
| `EX_05_dades_brutes` | `ColumnTransformer`, `OneHotEncoder`, `SimpleImputer`, `drop_duplicates` |

A `EX_02` la troballa **no es podia descobrir sense la matriu de confusió**, i la matriu no
s'havia explicat mai. O sigui que l'enunciat regalava el resultat perquè, sense regalar-lo,
l'exercici era impossible. **Els dos defectes se sostenien mútuament**, i per això calia
arreglar-los junts.

### La regla, en dues categories

No tot número és una filtració. La distinció que decideix cada cas:

| | Què és | Què s'hi fa |
|---|---|---|
| **A · càlcul amb una sola resposta** | Una forma d'array, un recompte de files, una distància, una entropia, que la teva implementació coincideixi amb la de scikit-learn | **Dona el número.** No hi ha res a descobrir, només a calcular bé, i tenir la diana és el que els deixa trobar el seu propi error. És una prova unitària |
| **B · una troballa que és el sentit de l'exercici** | Quin model guanya, quant puja una cosa en fer-ne una altra, quina conclusió surt de l'experiment | **No el donis mai.** Es substitueix per una comprovació de propietat |

Una **comprovació de propietat** verifica el *mecanisme* sense dir el *resultat*:

> Com saps que ho has fet bé: comprova que el teu conjunt escalat té mitjana ≈ 0 i desviació ≈ 1
> a cada columna. Si això no es compleix, l'escalat no s'ha aplicat com et penses i la comparació
> que facis després no val res. Un cop comprovat, compara les dues precisions i respon tu quina
> guanya i per quant.

Altres formes que funcionen: comparar contra un `DummyClassifier` («el que no guanyi el model
tonto, no compta»), comprovar que les caselles d'una matriu de confusió sumen les mostres del
test, comprovar que després d'imputar no queda cap nul, o comprovar la coherència entre la
precisió d'entrenament i la d'examen.

**La frase que resumeix el criteri, i que va a la web:** la comprovació et diu si el procediment
és correcte, no quin número t'ha de sortir. El número és la teva feina.

### La caixa d'eines

El segon defecte es tapa amb `02_practica/EX_00_caixa_eines.ipynb`: una referència consultable
amb, per a cada eina, què fa, què li dones i què et torna, un exemple mínim i el parany. Dues
decisions de disseny que la fan útil i no una drecera:

- **Els exemples van sobre taules de joguina de sis files inventades**, mai sobre els conjunts
  de dades dels exercicis. Així es veu què fa cada peça amb dades que es compten amb el dit, i no
  es regala cap resultat.
- **Ensenya les peces, no com s'encadenen.** Compondre-les és la feina. Per això cada exercici
  porta una llista de les eines que necessita i **no** l'ordre en què van.

### Els solucionaris no van al repositori

Hi eren, i el repositori és públic i està enllaçat des de la web. Pitjor: la pàgina de pràctica
deia el nom exacte de la carpeta. Ara són al `.gitignore` i es queden en local.

**Avís per si algun dia importa:** treure'ls del control de versions no els treu de l'historial
de git. Qui sàpiga mirar els commits anteriors els pot recuperar. Per a un grup de 2n de cicle
és una barrera suficient; si mai deixa de ser-ho, l'única solució de veritat és reescriure
l'historial o refer els exercicis.

## Sobre l'avaluació

Segons la fitxa del mòdul, el gruix de la nota són **proves pràctiques amb ordinador,
semblants a les activitats fetes a classe**. Això encaixa amb aquest material: els exercicis
dels quaderns tenen les cel·les de codi buides amb comentaris guia, i una prova pràctica pot
ser exactament una d'aquestes cel·les sobre un dataset que no hagin vist.

**El bloc de matemàtiques no canvia què s'avalua, canvia amb què poden respondre.** No té
sentit demanar en un examen la deducció del gradient de la log-loss. Sí que en té:

- calcular una impuresa de Gini a mà sobre un grup petit;
- explicar per què cal escalar abans d'un k-NN, o abans d'un PCA;
- **implementar una funció de pèrdua i comprovar-la** contra la de scikit-learn;
- **verificar un gradient** per diferències finites, que és una tècnica, no una demostració;
- dir per què un model dona el resultat que dona, mirant-ne els pesos.

Les tres últimes només són possibles gràcies al bloc de matemàtiques, i són bones preguntes
d'examen pràctic.

Compte amb una cosa: els pesos de l'avaluació encara estan pendents de confirmar, perquè la
fitxa oficial i el que es va explicar al grup del curs passat no coincideixen. Hi ha el
detall a [`diagnostic-i-programacio-2627.md`](diagnostic-i-programacio-2627.md).
