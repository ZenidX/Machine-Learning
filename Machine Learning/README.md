# Bloc de Machine Learning — la matemàtica i l'aplicació

Material del bloc central del curs: els models clàssics, la matemàtica que hi ha a sota i
la pràctica corresponent. És el tram que va entre saber Pandas i entrenar xarxes neuronals.

## De què va aquest bloc

Dels cinc models que apareixen a la demostració d'arrencada, cadascun té aquí el seu
quadern. No són cinc receptes: són **cinc maneres diferents de decidir**, i la gràcia està
a entendre en què es diferencien.

| | Com decideix | Matemàtica que fa servir |
|---|---|---|
| k veïns més propers | Mira a qui t'assembles i els fa votar | Distància euclidiana, o sigui Pitàgoras |
| Arbre de decisió | Encadena condicions sobre les columnes | Impuresa de Gini i proporcions |
| Bosc aleatori | Fa votar molts arbres diferents | Mitjanes, mostreig a l'atzar |
| Regressió logística | Traça una frontera i mesura de quin costat caus | Equació de la recta i funció sigmoide |
| Màquines de vectors de suport | Busca la frontera que passa més lluny de tothom | Distància d'un punt a una recta |

## Com estan fets els quaderns

Tots segueixen la mateixa estructura, i és deliberada:

1. **El problema primer, la fórmula després.** Cada quadern arrenca amb una pregunta
   concreta, no amb una definició.
2. **La matemàtica, explicada des d'on són.** L'alumnat ve d'un cicle formatiu, no d'una
   enginyeria: es treballa amb àlgebra bàsica, gràfics i proporcions. On la teoria demanaria
   derivades, s'ensenya el paisatge de la funció de pèrdua dibuixat i es descriu en paraules
   què fa l'entrenament.
3. **Implementar-ho a mà.** Cada model s'escriu primer amb Python i numpy, sense
   scikit-learn. Això és el que converteix la fórmula en una cosa que han vist funcionar.
4. **Comprovar que coincideix amb la llibreria.** Es compara la implementació pròpia amb la
   de scikit-learn i han de donar el mateix. **Aquest és el moment clau de cada quadern:**
   el que fa la llibreria és exactament el que acaben d'escriure.
5. **Pràctica amb les cel·les buides.** Cada quadern acaba amb exercicis on el codi està
   per omplir, amb comentaris que guien.

## Ordre

Els quaderns estan ordenats **de menys a més matemàtica**, no per importància:

```
00_demo/     ML_00_demo_iris          Demostració d'arrencada, sense entrar en res
01_teoria/   ML_01_knn                Distàncies
             ML_02_arbres             Impuresa i tria del tall
             ML_03_boscos             Per què votar funciona
             ML_04_regressio_logistica  De la recta a la probabilitat
             ML_05_svm                El marge, i què fer quan cap recta serveix
```

El fil que els lliga: k-NN i els arbres decideixen mirant les dades tal com són; la
regressió logística i l'SVM tracen fronteres; els boscos són la resposta al problema que
deixa obert l'arbre sol.

## Dues idees que travessen tot el bloc

**L'escalat.** Els models basats en distàncies (k-NN i SVM) són sensibles a les unitats de
cada columna: si una va en centímetres i una altra en mil·límetres, la segona domina. Surt
al quadern de k-NN i es repeteix al de l'SVM, i es demostra cada vegada canviant les
unitats i mirant com cau la precisió.

**El sobreajust.** Un model que encerta el 100 % a l'entrenament i falla a l'examen no ha
après: ha memoritzat. Es veu de la manera més nítida al quadern dels arbres, amb la corba
de precisió segons la profunditat.

## Verificar els quaderns

Les cel·les de codi s'han d'executar totes abans de portar-les a classe, i **els números
que apareixen al text han de ser els reals**. Hi ha una eina per comprovar-ho:

```bash
# des de E:\WORK\Xavi\ProjectsITIC
CEIABD-IA\.venv\Scripts\python.exe "OPT-ML\_eines\executa_nb.py" "OPT-ML\Machine Learning\01_teoria\ML_01_knn.ipynb"
```

Executa totes les cel·les en ordre, ensenya el que s'imprimeix i acaba amb el recompte
d'errors. Per generar quaderns nous hi ha `_eines/nbgen.py`, que evita el parany del format
`.ipynb` (cada línia ha d'acabar en salt de línia o el codi es pega).

## D'on ve

L'origen són dos quaderns del CE d'IA i Big Data, a
`ProjectsITIC\CEIABD-IA\VowelsClassificationMachineLearning\`, que cobreixen els mateixos
models sobre Iris i Wine però en anglès, amb nivell de cicle d'especialització i sense
entrar en la matemàtica. Aquests quaderns en són l'adaptació: en català, al nivell d'una
optativa de 2n, i amb la part matemàtica que allà no hi era.
