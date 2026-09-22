# Didàctica de la matemàtica dels models

Notes per impartir el bloc de machine learning: quina matemàtica cal, com introduir-la sense
perdre mig grup pel camí, i què passa a cada sessió.

Acompanya els quaderns de `Machine Learning/01_teoria/`.

## El problema de partida

L'alumnat és de 2n de DAM i DAW. Programen bé, però **la matemàtica no és el seu terreny**:
vénen d'un cicle formatiu, no d'una enginyeria. Recorden Pitàgoras i l'equació de la recta,
els logaritmes els tenen oblidats i el càlcul no l'han fet mai.

Alhora, el resultat d'aprenentatge del mòdul diu «**crea aplicacions** fent ús de models
d'aprenentatge automàtic». No diu demostra, ni dedueix.

Això deixa dues sortides dolentes i una de bona.

La primera sortida dolenta és **saltar-se la matemàtica**: ensenyar `fit` i `predict` i
prou. Funciona una setmana i es trenca a la primera pregunta de per què un model va
malament, perquè no tenen amb què pensar-hi.

La segona és **donar-la sencera**: gradients, multiplicadors de Lagrange, àlgebra lineal.
Es perd mig grup a la segona sessió i l'altre mig copia.

La bona és **donar la matemàtica que es pot calcular a mà i programar**, i ser explícit
sobre la que es deixa fora.

## L'estratègia: implementar-ho abans d'invocar-ho

Cada quadern segueix el mateix camí, i és el que sosté tot el bloc:

1. Es planteja un problema concret.
2. S'explica la fórmula que el resol, amb números petits fets a mà.
3. **S'implementa amb Python i numpy, sense scikit-learn.**
4. **Es compara amb scikit-learn i ha de donar el mateix.**

El pas 4 és el que canvia la relació amb la llibreria. Quan un alumne escriu la seva funció
de distància, calcula els veïns, vota, i després veu que `KNeighborsClassifier` dona
exactament el mateix, `fit` deixa de ser màgia. I quan calcula la impuresa de Gini de tots
els talls possibles i li surt 2,45, que és el número que va aparèixer a la demostració del
primer dia, la cosa encaixa sola.

És més lent que explicar l'API. També és l'única manera que després sàpiguen per què un
model falla.

## La matemàtica mínima, i on apareix

| Eina | On surt | Què cal recordar |
|---|---|---|
| Teorema de Pitàgoras | k-NN, SVM | La distància entre dos punts és l'arrel de la suma de quadrats |
| Proporcions i percentatges | Arbres (Gini) | Què vol dir que el 60 % d'un grup sigui d'una classe |
| Mitjanes | Boscos | La mitjana de moltes coses inexactes pot ser exacta |
| Equació de la recta | Logística, SVM | $y = mx + n$, i què vol dir estar a sobre o a sota |
| Exponencial | Logística | Que $e^{-z}$ es fa gran quan $z$ és molt negatiu i petit quan és molt positiu |
| Distància punt-recta | SVM | La fórmula amb el valor absolut a dalt i l'arrel a baix |

**Res més.** No hi ha derivades, ni matrius, ni optimització amb restriccions.

### Els dos punts on s'ha de fer trampa amb honestedat

**L'entrenament de la regressió logística.** De veritat es fa amb descens de gradient, que
demana derivades. Al quadern es fa una cerca per força bruta sobre una graella de pesos i
es dibuixa el paisatge de la funció de pèrdua amb corbes de nivell. Es veu la vall, es veu
el fons, i es marca on cau la solució de scikit-learn. Llavors ja es pot dir la frase: *el
que fa l'entrenament és baixar per aquest paisatge a passes petites*. És honest, és visual,
i qui vulgui estirar-ne el fil sap on continuar.

**La frontera de marge màxim de l'SVM.** Trobar-la és un problema d'optimització que no es
pot resoldre a mà. El que sí que es pot fer, i es fa, és **calcular el marge de diverses
rectes** i comprovar quina guanya. La idea queda; el mètode de resolució es delega a la
llibreria, dient-ho.

Val la pena dir en veu alta que s'està fent això. L'alumnat accepta bé un «això es resol amb
eines que veureu si feu una enginyeria, i mentrestant ho fem així»; el que no accepta bé és
descobrir que se li ha amagat alguna cosa.

## Seqüència i encaix amb les sessions

Els quaderns van de menys a més matemàtica, no per importància:

1. **k-NN** — la distància. És el més senzill i serveix per instaurar el mètode: implementar,
   comparar, entendre. Aquí surt per primera vegada **el parany de les escales**.
2. **Arbres** — la impuresa i la tria del tall. Connecta directament amb els condicionals que
   van fer al bloc de Python. Aquí surt **el sobreajust**, de la manera més visible de tot el
   curs.
3. **Boscos** — per què votar funciona, i per què només funciona si els errors són diferents.
4. **Regressió logística** — la frontera i la probabilitat. El quadern més exigent.
5. **SVM** — el marge i el kernel. Tanca la sèrie amb la taula comparativa dels cinc models.

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
la distància és la mateixa amb dos sumands que amb quatre o amb quatre-cents.

**Confondran precisió d'entrenament amb precisió d'examen.** És l'error conceptual més car
del bloc. Convé insistir-hi cada vegada que aparegui un número.

## Sobre l'avaluació

Segons la fitxa del mòdul, el gruix de la nota són **proves pràctiques amb ordinador,
semblants a les activitats fetes a classe**. Això encaixa amb aquest material: els exercicis
dels quaderns tenen les cel·les de codi buides amb comentaris guia, i una prova pràctica pot
ser exactament una d'aquestes cel·les sobre un dataset que no hagin vist.

El que **no** té sentit preguntar en aquest mòdul és la deducció d'una fórmula. Sí que en té
demanar que calculin una impuresa de Gini a mà sobre un grup petit, o que expliquin per què
cal escalar abans d'un k-NN.

Compte amb una cosa: els pesos de l'avaluació encara estan pendents de confirmar, perquè la
fitxa oficial i el que es va explicar al grup del curs passat no coincideixen. Hi ha el
detall a [`programacio-curs-2026-27.md`](programacio-curs-2026-27.md).
