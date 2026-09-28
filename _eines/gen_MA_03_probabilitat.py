# -*- coding: utf-8 -*-
"""Genera el quadern MA_03: probabilitat, versemblanca i d'on surt la log-loss.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_MA_03_probabilitat.py

Els numeros que apareixen escrits al text venen d'executar el quadern amb
_eines/executa_nb.py; si es canvia una cel.la de codi cal tornar-los a mirar.
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# Probabilitat i versemblança

**Optativa d'Aprenentatge automàtic · DAM/DAW 2n**

Al quadern de regressió logística vau fer servir aquesta funció de pèrdua:

$$\text{log-loss} = -\frac{1}{n}\sum_{i=1}^{n} \Big[ y_i \log p_i + (1-y_i)\log(1-p_i) \Big]$$

i us la vau creure. Té bon aspecte: baixa quan el model encerta i puja quan
falla. Però hi ha infinites fórmules amb aquesta propietat. Per exemple,
$\frac{1}{n}\sum_i (y_i - p_i)^2$ també baixa quan el model encerta, i és més
fàcil d'escriure.

**La pregunta d'avui: per què aquella, amb els logaritmes, i no una altra?**

La resposta no és «perquè funciona bé a la pràctica». És que la log-loss no és
una invenció: **és una conseqüència**. Surt d'una idea sola, la **màxima
versemblança**, que diu una cosa raonable: entre tots els models possibles,
tria el que fa que les dades que has observat siguin el més probables possible.

El camí és aquest, i no ens el saltarem enlloc:

1. Probabilitat condicionada, que és una divisió de dos recomptes.
2. El teorema de Bayes, i un resultat que sorprèn.
3. Versemblança, amb una moneda.
4. Per què hi apareix el logaritme.
5. La log-loss, derivada des de la versemblança.
6. Naive Bayes: un model sencer que surt de Bayes i de res més.

De probabilitat no cal que en sapigueu res més enllà de la secundària. Tot el
que faci falta el construïm aquí.
"""))

A(code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)   # tot el quadern ha de donar els mateixos numeros sempre

print("numpy", np.__version__)
"""))

# ---------------------------------------------------- 1. condicionada
A(md(r"""
## 1. Probabilitat condicionada: dos recomptes i una divisió

Comencem amb dades de veritat: `load_breast_cancer`, els 569 tumors de mama que
ja coneixeu del quadern `EX_02_cancer.ipynb`. Recordeu el parany de les
etiquetes: **`target = 0` és maligne i `target = 1` és benigne**, al contrari del
que sembla natural.

Una **probabilitat**, aquí, és una fracció de files. Si agafeu un tumor a
l'atzar del conjunt, la probabilitat que sigui maligne és el nombre de tumors
malignes dividit pel total. Res més.
"""))

A(code("""
from sklearn.datasets import load_breast_cancer

dades_c = load_breast_cancer(as_frame=True)
df_c = dades_c.frame

print("files, columnes:", df_c.shape)
print("noms de les classes:", dades_c.target_names)   # index 0 i index 1

# A = "el tumor es maligne". Es una mascara booleana: una fila, un True o un False
A_maligne = (df_c["target"].values == 0)
n_c = len(df_c)

print()
print("tumors malignes :", A_maligne.sum())
print("tumors benignes :", (~A_maligne).sum())
print("P(A) = %d / %d = %.4f" % (A_maligne.sum(), n_c, A_maligne.sum() / n_c))
"""))

A(md(r"""
Fixeu-vos que `A_maligne.sum()` compta els `True`, perquè `True` val 1 i `False`
val 0. Una màscara booleana **és** un recompte esperant a fer-se.

Ara el segon esdeveniment. La columna `mean radius` és el radi mitjà de les
cèl·lules del tumor, i va de 6,98 a 28,11 amb una mitjana de 14,13. Definim:

$$B = \text{«el radi mitjà del tumor és més gran que 15»}$$

I la pregunta que importa de veritat no és $P(A)$, sinó aquesta: **si ja sabeu
que el radi passa de 15, què canvia sobre la probabilitat que sigui maligne?**
Això és la probabilitat condicionada, i es defineix així:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

on $A \cap B$ vol dir «totes dues coses a la vegada». En codi, la intersecció és
l'operador `&` entre dues màscares.

La definició sembla abstracta, i no ho és gens. Si multipliqueu numerador i
denominador per $n$, els dos $n$ es cancel·len i us queda:

$$P(A \mid B) = \frac{\#(A \cap B) / n}{\#B / n} = \frac{\#(A \cap B)}{\#B}$$

**Una probabilitat condicionada és el recompte de files que compleixen totes
dues coses, dividit pel recompte de files que compleixen la condició.** El
condicionament no fa cap màgia: canvia el denominador. En comptes de dividir
entre les 569 files, divideix entre les files del subconjunt que us han dit que
mireu.
"""))

A(code("""
radi = df_c["mean radius"].values
print("radi mitja: min %.2f, max %.2f, mitjana %.2f" % (radi.min(), radi.max(), radi.mean()))

B_gran = radi > 15          # B = "el radi mitja passa de 15"

# els tres recomptes que fan falta
n_A_i_B = (A_maligne & B_gran).sum()    # malignes I de radi gran
n_B = B_gran.sum()                      # de radi gran, malignes o no

P_A = A_maligne.sum() / n_c
P_B = n_B / n_c
P_A_i_B = n_A_i_B / n_c

print()
print("P(B)       = %3d / %d = %.4f" % (n_B, n_c, P_B))
print("P(A i B)   = %3d / %d = %.4f" % (n_A_i_B, n_c, P_A_i_B))
print()
# les dues maneres de calcular-ho han de donar el mateix numero
print("P(A|B) per la definicio  = %.4f / %.4f = %.4f" % (P_A_i_B, P_B, P_A_i_B / P_B))
print("P(A|B) comptant files    = %3d / %3d      = %.4f" % (n_A_i_B, n_B, n_A_i_B / n_B))
"""))

A(md(r"""
Les dues línies donen **0,9306**. La divisió de probabilitats i la divisió de
recomptes són la mateixa operació escrita de dues maneres.

Comparem-ho amb la probabilitat de partida, i amb la condicionada a l'altre
costat del tall:

- $P(A) = 212/569 = 0{,}3726$: sense saber res, el 37,26 % dels tumors són malignes.
- $P(A \mid B) = 161/173 = 0{,}9306$: si el radi passa de 15, el 93,06 %.
- $P(A \mid \text{no } B) = 51/396 = 0{,}1288$: si no hi passa, el 12,88 %.

Una sola columna, un sol tall, i la probabilitat salta del 37 % al 93 %. **Això
és exactament el que fa un model de classificació**: usar el que sap de la fila
per moure la probabilitat lluny de la probabilitat de partida. L'arbre de
decisió que vau programar buscava el tall que movia més aquesta probabilitat;
ara ja en teniu el nom.
"""))

A(code("""
P_A_donat_B = n_A_i_B / n_B
P_A_donat_noB = (A_maligne & ~B_gran).sum() / (~B_gran).sum()

print("P(A | no B) = %d / %d = %.4f" % ((A_maligne & ~B_gran).sum(), (~B_gran).sum(), P_A_donat_noB))

etiquetes = ["P(A)\\nsense saber res", "P(A | radi > 15)", "P(A | radi <= 15)"]
valors = [P_A, P_A_donat_B, P_A_donat_noB]

plt.figure(figsize=(7, 4.5))
barres = plt.bar(etiquetes, valors, color=["tab:gray", "tab:red", "tab:blue"])
for barra, v in zip(barres, valors):
    plt.text(barra.get_x() + barra.get_width() / 2, v + 0.02, "%.1f %%" % (100 * v),
             ha="center")
plt.axhline(P_A, color="tab:gray", linestyle=":", linewidth=1)
plt.ylim(0, 1.05)
plt.ylabel("Probabilitat que el tumor sigui maligne")
plt.title("Condicionar mou la probabilitat")
plt.grid(axis="y", alpha=0.3)
plt.show()
"""))

# ---------------------------------------------------- 2. Bayes
A(md(r"""
## 2. El teorema de Bayes

La definició de la secció anterior es pot escriure per als dos costats:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} \qquad\text{i}\qquad P(B \mid A) = \frac{P(A \cap B)}{P(A)}$$

Aïlleu $P(A \cap B)$ de la segona: $P(A \cap B) = P(B \mid A)\,P(A)$. Substituïu-ho
a la primera i ja ho teniu:

$$\boxed{\;P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}\;}$$

Dues línies, cap idea nova. El teorema de Bayes no afegeix res a la definició de
probabilitat condicionada: **la gira**. Serveix per passar de la pregunta que
sabeu respondre a la pregunta que voleu respondre.

Cada peça té nom, i els noms es fan servir molt:

- $P(A)$ és la **probabilitat a priori** (*prior*): què sabíeu abans de mirar res.
- $P(B \mid A)$ és la **versemblança** (*likelihood*): com de compatible és l'evidència amb la hipòtesi.
- $P(A \mid B)$ és la **probabilitat a posteriori** (*posterior*): què sabeu després de mirar.

Comprovem-ho amb les dades de la secció 1, on tenim els dos costats a mà.
"""))

A(code("""
# el costat que Bayes "gira": entre els malignes, quants tenen radi gran
P_B_donat_A = (A_maligne & B_gran).sum() / A_maligne.sum()
print("P(B|A) = %d / %d = %.4f" % ((A_maligne & B_gran).sum(), A_maligne.sum(), P_B_donat_A))

per_bayes = P_B_donat_A * P_A / P_B
print()
print("P(A|B) per Bayes      = %.4f * %.4f / %.4f = %.6f" % (P_B_donat_A, P_A, P_B, per_bayes))
print("P(A|B) comptant files = %.6f" % P_A_donat_B)
print("difereixen en %.2e" % abs(per_bayes - P_A_donat_B))
"""))

A(md(r"""
Coincideixen fins a l'últim decimal que el `float` pot representar. Com havia de
ser: hem fet àlgebra, no aproximacions.

### 2.1 El resultat que sorprèn

Ara el cas que val la pena tenir present tota la vida. Una prova mèdica amb
molt bona pinta:

- **Sensibilitat 99 %**: si estàs malalt, la prova surt positiva el 99 % dels cops. Això és $P(+ \mid \text{malalt}) = 0{,}99$.
- **Especificitat 99 %**: si estàs sa, la prova surt negativa el 99 % dels cops. Això és $P(- \mid \text{sa}) = 0{,}99$, i per tant $P(+ \mid \text{sa}) = 0{,}01$.
- **Prevalença 1 de cada 1.000**: la malaltia la té una persona de cada mil. Això és el *prior*, $P(\text{malalt}) = 0{,}001$.

Us fan la prova i surt **positiva**. Quina probabilitat teniu d'estar malalts?

La resposta intuïtiva és «99 %», i és equivocada. La intuïció confon
$P(+ \mid \text{malalt})$, que és el 99 %, amb $P(\text{malalt} \mid +)$, que és el
que us pregunten. **Són dues coses diferents, i Bayes és el que les relaciona.**

$$P(\text{malalt} \mid +) = \frac{P(+ \mid \text{malalt})\,P(\text{malalt})}{P(+)}$$

El denominador $P(+)$ no us l'han donat, però es construeix: una prova pot sortir
positiva per dos camins incompatibles, que estiguis malalt i encerti, o que
estiguis sa i s'equivoqui. Sumant-los:

$$P(+) = P(+ \mid \text{malalt})\,P(\text{malalt}) + P(+ \mid \text{sa})\,P(\text{sa})$$
"""))

A(code("""
prevalenca = 0.001     # P(malalt), el prior
sensibilitat = 0.99    # P(+ | malalt)
especificitat = 0.99   # P(- | sa),  aixi que P(+ | sa) = 1 - especificitat

p_positiu_si_malalt = sensibilitat
p_positiu_si_sa = 1 - especificitat

# denominador: els dos camins cap a un positiu
p_positiu = (p_positiu_si_malalt * prevalenca
             + p_positiu_si_sa * (1 - prevalenca))

p_malalt_si_positiu = p_positiu_si_malalt * prevalenca / p_positiu

print("P(+)                = %.6f" % p_positiu)
print("P(malalt | +)       = %.6f" % p_malalt_si_positiu)
print("es a dir, el %.2f %%" % (100 * p_malalt_si_positiu))
"""))

A(md(r"""
**9,02 %.** Una prova que encerta el 99 % dels cops, davant d'un positiu, deixa
el pacient amb un 9 % de probabilitat d'estar malalt i un 91 % d'estar sa.

Si no us ho creieu (fa bé de no creure-s'ho), compteu persones en comptes de
manipular probabilitats. Agafem un milió de persones i seguim els números.
"""))

A(code("""
N = 1_000_000

malalts = N * prevalenca                      # 1.000 persones
sans = N - malalts                            # 999.000 persones

positius_malalts = malalts * sensibilitat            # la prova els enxampa
positius_sans = sans * (1 - especificitat)           # falsos positius
positius_total = positius_malalts + positius_sans

print("de %d persones:" % N)
print("  malalts                       : %10.0f" % malalts)
print("  sans                          : %10.0f" % sans)
print()
print("  positius que estan malalts    : %10.0f" % positius_malalts)
print("  positius que estan sans       : %10.0f" % positius_sans)
print("  positius en total             : %10.0f" % positius_total)
print()
print("  fraccio de positius malalts   : %.0f / %.0f = %.4f" % (
    positius_malalts, positius_total, positius_malalts / positius_total))
"""))

A(md(r"""
Aquí es veu d'on surt el 9 %: **hi ha 999.000 persones sanes i només 1.000
malaltes**. Un error de l'1 % sobre 999.000 persones són 9.990 falsos positius,
deu vegades més que els 990 positius de veritat. La prova no és dolenta; el que
passa és que la malaltia és rara, i el *prior* pesa.

Regla per recordar-ho: **davant d'una malaltia rara, un positiu aïllat és
informació feble**. El 9,02 % no deixa de ser un salt de 90 vegades sobre el
0,1 % de partida, i per això es demana una segona prova: el 9,02 % passa a ser
el *prior* de la següent.
"""))

A(code("""
plt.figure(figsize=(7, 4.5))
plt.bar(["positius\\nque estan malalts", "positius\\nque estan sans"],
        [positius_malalts, positius_sans],
        color=["tab:red", "tab:orange"])
plt.text(0, positius_malalts + 250, "%.0f" % positius_malalts, ha="center")
plt.text(1, positius_sans + 250, "%.0f" % positius_sans, ha="center")
plt.ylabel("Nombre de persones (d'un milio)")
plt.title("Qui son els positius d'una prova del 99 %")
plt.grid(axis="y", alpha=0.3)
plt.show()
"""))

A(md(r"""
### 2.2 Per què la precisió global enganya

Això connecta directament amb el que vau veure a `EX_02_cancer.ipynb`, on un
`DummyClassifier` que responia sempre la classe majoritària treia una precisió
que semblava decent. Ara en teniu la versió extrema.

Calculem dues coses sobre el milió de persones: l'**exactitud global** de la
prova del 99 %, i l'exactitud d'un «model» que no mira res i sempre diu
«negatiu».
"""))

A(code("""
encerts_prova = positius_malalts + sans * especificitat   # positius correctes + negatius correctes
exactitud_prova = encerts_prova / N

exactitud_sempre_negatiu = sans / N    # encerta tots els sans i cap malalt

print("exactitud de la prova del 99 %%     : %.4f" % exactitud_prova)
print("exactitud de dir sempre 'negatiu'  : %.4f" % exactitud_sempre_negatiu)
print()
print("malalts detectats per la prova     : %.0f de %.0f" % (positius_malalts, malalts))
print("malalts detectats dient 'negatiu'  : 0 de %.0f" % malalts)
"""))

A(md(r"""
El model que no fa res treu **99,9 %** i guanya la prova mèdica, que treu
**99,0 %**. I no detecta ni un malalt.

La precisió global és una mitjana ponderada pel nombre de casos de cada classe.
Quan una classe és el 99,9 % de les dades, la mitjana només parla d'aquella
classe i la minoritària no hi deixa rastre. Per això a `EX_02_cancer.ipynb` vau
haver de mirar la matriu de confusió i els falsos negatius, i no el percentatge
d'encerts.

Guardeu la idea, perquè a la secció 5 tornarà amb una altra cara: **una mètrica
que només mira si l'etiqueta predita és correcta no distingeix un model segur
d'un model que dubta**. La log-loss sí.
"""))

# ---------------------------------------------------- 3. versemblança
A(md(r"""
## 3. Versemblança: la moneda

Canviem de pregunta. Fins ara teníem el model i preguntàvem per les dades. Ara
tenim les dades i preguntem pel model.

Tireu una moneda 10 vegades i surten **7 cares i 3 creus**. La moneda té una
probabilitat $p$ de treure cara, i no sabeu quant val. **Quin valor de $p$ fa
que el que heu observat sigui el més probable possible?**

Si la moneda té probabilitat $p$ de cara, i les tirades són independents, la
probabilitat de treure aquesta seqüència concreta de 7 cares i 3 creus és el
producte de les 10 probabilitats:

$$\mathcal{L}(p) = \underbrace{p \cdot p \cdots p}_{7} \cdot \underbrace{(1-p)\cdots(1-p)}_{3} = p^7 (1-p)^3$$

Aquesta funció es diu **versemblança** (*likelihood*). Compte amb una cosa, que
és la font de la meitat de la confusió amb aquest tema: $\mathcal{L}(p)$ **no és
una probabilitat sobre $p$**. Les dades estan fixades (7 i 3, ja han passat) i el
que varia és $p$. És la probabilitat de les dades, llegida com a funció del
paràmetre.

**Simplificació que estem fent**, dita en veu alta: hem tret del càlcul el
nombre de maneres d'ordenar 7 cares i 3 creus, que és $\binom{10}{7} = 120$. La
versemblança completa de «7 cares en 10 tirades, en qualsevol ordre» seria
$120\, p^7 (1-p)^3$. El 120 no depèn de $p$, per tant multiplica tota la corba
per una constant i **no mou el màxim**, que és el que busquem. Per a tot el que
farem avui es pot ignorar.

La calculem sobre una graella de valors de $p$ i mirem on és més gran.
"""))

A(code("""
cares, creus = 7, 3

graella_p = np.linspace(0, 1, 1001)          # 0, 0.001, 0.002, ..., 1
L = graella_p ** cares * (1 - graella_p) ** creus

i_max = np.argmax(L)
print("valor de p que maximitza la versemblanca: %.4f" % graella_p[i_max])
print("versemblanca en aquest punt             : %.10f" % L[i_max])
print()
for p_provat in [0.3, 0.5, 0.6, 0.7, 0.8, 0.9]:
    print("  L(%.1f) = %.10f" % (p_provat, p_provat ** cares * (1 - p_provat) ** creus))
"""))

A(md(r"""
El màxim cau a **0,7**, que és la fracció de cares observada. La versemblança hi
val **0,0022235661**, i a $p = 0{,}5$ val **0,0009765625**: les dades observades
són unes 2,28 vegades més probables amb una moneda del 0,7 que amb una moneda
justa.

Noteu també que tots els valors són petitíssims. Qualsevol $p$ concret dona una
probabilitat baixa d'aquesta seqüència exacta, i això és normal: hi ha moltes
seqüències possibles. El que importa no és el valor absolut, és **on és el
màxim**.
"""))

A(code("""
plt.figure(figsize=(8, 4.5))
plt.plot(graella_p, L, color="tab:blue", linewidth=2)
plt.axvline(0.7, color="tab:red", linestyle="--", linewidth=1, label="$p = 0{,}7$")
plt.scatter([0.7], [0.7 ** cares * 0.3 ** creus], color="tab:red", zorder=5)
plt.xlabel("$p$ (probabilitat de cara de la moneda)")
plt.ylabel(r"$\\mathcal{L}(p) = p^7 (1-p)^3$")
plt.title("Versemblanca de 7 cares en 10 tirades")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
### 3.1 La demostració, sense graella

La graella dona el màxim amb tants decimals com punts hi posem. Es pot trobar
exacte, i aquí apareix per primera vegada el logaritme.

Derivar $p^7(1-p)^3$ demana la regla del producte. En canvi, prenent logaritmes
el producte es converteix en suma, perquè $\log(ab) = \log a + \log b$ i
$\log(a^k) = k \log a$:

$$\ell(p) = \log \mathcal{L}(p) = 7 \log p + 3 \log(1-p)$$

Derivem, recordant que la derivada de $\log x$ és $1/x$, i que la de
$\log(1-p)$ porta un $-1$ de la regla de la cadena:

$$\frac{d\ell}{dp} = \frac{7}{p} - \frac{3}{1-p}$$

Al màxim la derivada val zero:

$$\frac{7}{p} = \frac{3}{1-p} \;\Longrightarrow\; 7(1-p) = 3p \;\Longrightarrow\; 7 = 10p \;\Longrightarrow\; p = \frac{7}{10}$$

Els números 7 i 3 no tenen res d'especial. Amb $c$ cares i $k$ creus el mateix
càlcul dona:

$$\hat{p} = \frac{c}{c+k}$$

**La fracció observada és l'estimador de màxima versemblança.** El resultat és
el que qualsevol hauria dit sense fer cap càlcul, i això és bon senyal: el
mètode, aplicat al cas fàcil, no diu cap bestiesa. Ara ja el podrem aplicar a
casos on la intuïció no arriba.
"""))

A(code("""
p_formula = cares / (cares + creus)
p_max_graella = graella_p[np.argmax(L)]

print("formula analitica : %.10f" % p_formula)
print("maxim de la graella: %.10f" % p_max_graella)
print("difereixen en %.2e (nomes pel gra de la graella, 0,001)" % abs(p_formula - p_max_graella))

# la derivada ha de valer zero a p = 7/10
derivada = cares / p_formula - creus / (1 - p_formula)
print()
print("derivada de la log-versemblanca a p = %.1f: %.2e" % (p_formula, derivada))
"""))

# ---------------------------------------------------- 4. logaritme
A(md(r"""
## 4. Per què el logaritme

A la secció anterior el logaritme ha aparegut per comoditat de càlcul. No és
l'única raó, i la primera és més greu: **sense logaritme, el càlcul no es pot
fer amb un ordinador.**

### 4.1 El producte es va a zero

Amb 10 tirades la versemblança valia 0,0022. Amb 2.000 files, que és un dataset
petit, es multipliquen 2.000 números menors que 1. Provem-ho.
"""))

A(code("""
probabilitats = np.full(2000, 0.5)      # 2.000 factors, tots 0,5

producte = np.prod(probabilitats)
suma_logs = np.sum(np.log(probabilitats))

print("producte de 2.000 factors de 0,5 :", producte)
print("suma de 2.000 logaritmes de 0,5  : %.4f" % suma_logs)
print("comprovacio: 2000 * log(0,5)     = %.4f" % (2000 * np.log(0.5)))
"""))

A(md(r"""
El producte dona **`0.0` exactament**. No un número petit: zero. I amb un zero
no s'hi pot fer res, perquè tots els models del món donen zero i cap no és
millor que un altre. La suma de logaritmes dona **-1386,2944**, un número
perfectament utilitzable.

Això es diu **desbordament per sota** (*underflow*). Un `float` de 64 bits no pot
representar números positius arbitràriament petits: per sota d'aproximadament
$5 \times 10^{-324}$ l'única cosa que li queda és el zero. Busquem on es trenca.
"""))

A(code("""
for k in [500, 1000, 1023, 1074, 1075, 1200]:
    print("producte de %5d factors de 0,5 : %s" % (k, np.prod(np.full(k, 0.5))))

print()
print("el primer k amb producte exactament 0.0 es k = 1075")
print("i 0,5^1074 = %s, l'ultim numero positiu que hi cap" % np.prod(np.full(1074, 0.5)))
"""))

A(md(r"""
Amb 1.075 factors de 0,5 ja s'ha perdut tot. Amb probabilitats més petites, que
és el cas normal, es trenca abans. La suma de logaritmes, en canvi, creix de
manera lineal: 100.000 files donarien un número de l'ordre de -70.000, que cap
en un `float` sense cap problema.

### 4.2 El logaritme no mou el màxim

Queda una objecció òbvia: canviar la funció que maximitzem és canviar el
problema. Aquí no, i la raó és que **el logaritme és estrictament creixent**: si
$a > b$ llavors $\log a > \log b$, sempre, per a $a, b > 0$.

Per tant, si $p^{\star}$ és el valor on $\mathcal{L}$ és més gran que a qualsevol
altre lloc, també és el valor on $\log \mathcal{L}$ és més gran que a qualsevol
altre lloc. **El punt del màxim no es mou; el valor del màxim sí.** I el punt és
el que volem, perquè el que busquem és el model, no el número.

Comprovem-ho amb la mateixa graella de la moneda.
"""))

A(code("""
# log(0) es -inf, i a la graella hi ha p = 0 i p = 1. numpy avisa; li diem
# que calli en aquest bloc perque sabem que aquests dos punts no son el maxim.
with np.errstate(divide="ignore"):
    log_L = cares * np.log(graella_p) + creus * np.log(1 - graella_p)

print("maxim de L      a p = %.3f (valor %.10f)" % (graella_p[np.argmax(L)], L.max()))
print("maxim de log(L) a p = %.3f (valor %.4f)" % (graella_p[np.nanargmax(log_L)],
                                                   np.nanmax(log_L)))
print()
print("log de la versemblanca maxima: log(%.10f) = %.4f" % (L.max(), np.log(L.max())))
"""))

A(code("""
plt.figure(figsize=(8, 4.5))
plt.plot(graella_p, log_L, color="tab:green", linewidth=2)
plt.axvline(0.7, color="tab:red", linestyle="--", linewidth=1, label="$p = 0{,}7$")
plt.ylim(-30, 0)
plt.xlabel("$p$ (probabilitat de cara de la moneda)")
plt.ylabel(r"$\\ell(p) = 7\\log p + 3\\log(1-p)$")
plt.title("La log-versemblanca te el maxim al mateix lloc")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Compareu aquest gràfic amb el de la secció 3: la forma és molt diferent (aquest
cau a $-\infty$ als extrems) i el cim és al mateix lloc. Tres avantatges, i cap
cost:

1. No hi ha desbordament.
2. Els productes es tornen sumes, i les sumes es deriven terme a terme.
3. El màxim no es mou.

A partir d'aquí, **sempre treballarem amb log-versemblança**.
"""))

# ---------------------------------------------------- 5. log-loss
A(md(r"""
## 5. De la versemblança a la log-loss

Ara el pas que respon la pregunta del principi.

Tenim $n$ files. Cada fila té una etiqueta observada $y_i$, que val 0 o 1, i el
model li assigna una probabilitat $p_i$ de ser de la classe 1. Igual que amb la
moneda, volem els paràmetres que facin **les etiquetes observades** el més
probables possible.

Per a una sola fila, la probabilitat que el model assigna a l'etiqueta que s'ha
observat de veritat és:

$$P(y_i \mid p_i) = p_i^{\,y_i}\,(1-p_i)^{\,1-y_i}$$

Aquesta expressió sembla gratuïtament complicada, i és un truc de notació.
Mireu-la posant-hi els dos únics valors que $y_i$ pot prendre:

- Si $y_i = 1$: queda $p_i^1 (1-p_i)^0 = p_i \cdot 1 = p_i$.
- Si $y_i = 0$: queda $p_i^0 (1-p_i)^1 = 1 \cdot (1-p_i) = 1-p_i$.

**És un `if` escrit amb exponents.** Diu «si l'etiqueta és 1 agafa $p_i$, si és 0
agafa $1-p_i$», i es fa així perquè un `if` no es pot derivar i un producte
d'exponents sí.
"""))

A(code("""
def prob_etiqueta(y, p):
    \"\"\"Probabilitat que el model assigna a l'etiqueta observada y.\"\"\"
    return p ** y * (1 - p) ** (1 - y)

p_exemple = 0.8

print("model diu p = %.1f" % p_exemple)
print("  si l'etiqueta real es 1 -> %.1f   (ha d'agafar p)" % prob_etiqueta(1, p_exemple))
print("  si l'etiqueta real es 0 -> %.1f   (ha d'agafar 1-p)" % prob_etiqueta(0, p_exemple))

# el mateix amb vectors, que es com ho farem de veritat
y_v = np.array([1, 0, 1, 0])
p_v = np.array([0.9, 0.2, 0.3, 0.8])
print()
print("y                     :", y_v)
print("p                     :", p_v)
print("prob de l'etiqueta    :", prob_etiqueta(y_v, p_v))
print("comprovacio amb where :", np.where(y_v == 1, p_v, 1 - p_v))
"""))

A(md(r"""
Les dues últimes línies donen el mateix vector. L'expressió amb exponents i el
`np.where` són la mateixa cosa; la primera es pot derivar.

Ara el muntatge sencer, en quatre passos. Cada pas és una de les idees que ja
hem establert.

**Pas 1. Multiplicar per totes les files.** Si les files són independents, la
probabilitat d'observar totes les etiquetes és el producte:

$$\mathcal{L} = \prod_{i=1}^{n} p_i^{\,y_i}(1-p_i)^{\,1-y_i}$$

**Pas 2. Prendre logaritmes** (secció 4: el producte es desborda i el màxim no
es mou). El logaritme d'un producte és la suma de logaritmes, i el logaritme
d'una potència baixa l'exponent a multiplicar:

$$\ell = \log \mathcal{L} = \sum_{i=1}^{n} \Big[ y_i \log p_i + (1-y_i)\log(1-p_i) \Big]$$

**Pas 3. Canviar el signe.** $\ell$ és un número negatiu (logaritmes de coses
menors que 1) i el volem **màxim**. Els algorismes d'optimització, per conveni,
minimitzen. Canviar el signe converteix el problema de maximitzar en un de
minimitzar, i el punt òptim és el mateix.

**Pas 4. Dividir per $n$.** Per tenir un número comparable entre conjunts de
mida diferent. Dividir per una constant positiva tampoc no mou l'òptim.

$$-\frac{1}{n}\sum_{i=1}^{n} \Big[ y_i \log p_i + (1-y_i)\log(1-p_i) \Big]$$

I aquesta és la log-loss del quadern de regressió logística, lletra per lletra.

**Dit clar: la log-loss no és una fórmula caiguda del cel. És la versemblança,
amb un logaritme perquè el producte es desborda, un signe menys perquè els
optimitzadors minimitzen, i una divisió per $n$ per comoditat.** Minimitzar la
log-loss i maximitzar la probabilitat de les dades observades són **el mateix
problema**. Per això la regressió logística minimitza aquesta i no
$\frac{1}{n}\sum (y_i - p_i)^2$: l'altra també baixa quan el model encerta, però
no respon cap pregunta. Aquesta respon «quins pesos fan les meves dades el més
probables possible».

Comprovem-ho contra scikit-learn.
"""))

A(code("""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

X_c = dades_c.data.values
y_c = dades_c.target.values

X_tr, X_te, y_tr, y_te = train_test_split(X_c, y_c, test_size=0.3,
                                          random_state=42, stratify=y_c)

# les 30 columnes tenen escales molt diferents; sense escalar, l'optimitzador
# de la regressio logistica no acaba de convergir i avisa
escalador = StandardScaler().fit(X_tr)
model_lr = LogisticRegression(max_iter=5000, random_state=42)
model_lr.fit(escalador.transform(X_tr), y_tr)

# predict_proba dona dues columnes, [P(classe 0), P(classe 1)]. Volem la segona
p_te = model_lr.predict_proba(escalador.transform(X_te))[:, 1]

print("files a l'examen      :", len(y_te))
print("precisio del model    : %.4f" % model_lr.score(escalador.transform(X_te), y_te))
print("p mes petita / gran   : %.3e / %.10f" % (p_te.min(), p_te.max()))
"""))

A(md(r"""
Abans de calcular, un detall que no es pot passar per alt: la probabilitat més
petita que dona el model és de l'ordre de $10^{-22}$, i res no impedeix que
alguna vegada surti un `0.0` rodó. Llavors $\log(0) = -\infty$, la mitjana surt
`-inf` i s'ha acabat el càlcul.

La solució és **retallar** les probabilitats a un interval
$[\varepsilon, 1-\varepsilon]$ amb $\varepsilon$ molt petit, típicament $10^{-15}$.
Això té un preu que cal dir: **la pèrdua d'una fila mal predita queda limitada a
$-\log(10^{-15}) \approx 34{,}5$** en comptes de ser infinita. És una mentida
controlada i deliberada, i és exactament el que fa scikit-learn a dins.
"""))

A(code("""
eps = 1e-15
p_retallat = np.clip(p_te, eps, 1 - eps)

# la formula, tal com l'hem derivat
la_meva_log_loss = -np.mean(y_te * np.log(p_retallat)
                            + (1 - y_te) * np.log(1 - p_retallat))

la_de_sklearn = log_loss(y_te, p_te)

print("la meva log-loss : %.12f" % la_meva_log_loss)
print("sklearn log_loss : %.12f" % la_de_sklearn)
print("diferencia       : %.3e" % abs(la_meva_log_loss - la_de_sklearn))
print()
print("que passa sense retallar, si alguna p fos 0:")
with np.errstate(divide="ignore"):
    print("  log(0) =", np.log(0.0))
print("  -log(1e-15) = %.4f  <- el maxim castig que permet el retall" % -np.log(eps))
"""))

A(md(r"""
Diferència de l'ordre de $10^{-17}$, que és el soroll de l'aritmètica de coma
flotant. La nostra fórmula i la de scikit-learn són la mateixa fórmula.

Val la pena mirar el càstig que rep una fila individual, que és
$-\log(\text{probabilitat de l'etiqueta certa})$. La corba explica per què la
log-loss no és la precisió.
"""))

A(code("""
eix_p = np.linspace(0.001, 0.999, 500)

plt.figure(figsize=(8, 4.5))
plt.plot(eix_p, -np.log(eix_p), color="tab:red", linewidth=2,
         label="etiqueta real $y=1$")
plt.plot(eix_p, -np.log(1 - eix_p), color="tab:blue", linewidth=2,
         label="etiqueta real $y=0$")
plt.axvline(0.5, color="gray", linestyle=":", linewidth=1)
plt.ylim(0, 7)
plt.xlabel("$p$ que ha donat el model (probabilitat de la classe 1)")
plt.ylabel(r"castig de la fila: $-\\log$(prob. de l'etiqueta certa)")
plt.title("El castig creix sense limit quan el model s'equivoca amb seguretat")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
La corba és asimètrica d'una manera que importa. Encertar amb $p = 0{,}99$
costa 0,01; encertar amb $p = 0{,}51$ costa 0,67, seixanta vegades més, tot i
que **la predicció és la mateixa i la precisió no ho nota**. I equivocar-se amb
seguretat costa el que sigui: a $p = 0{,}001$ amb $y = 1$, el càstig és 6,9, i
sense el retall seria infinit.

És la mateixa lliçó de la secció 2.2, portada a la funció de pèrdua. La precisió
mira si l'etiqueta predita és correcta. La log-loss mira **si la probabilitat era
honesta**. Un model que digui 0,99 quan no ho sap el paga car, i això és el que
el fa calibrar-se.
"""))

# ---------------------------------------------------- 6. Naive Bayes
A(md(r"""
## 6. Naive Bayes: un model sencer que surt de Bayes

Fins aquí Bayes ens ha servit per pensar. Ara en sortirà un classificador
complet, i no hi caldrà cap idea nova.

Volem, per a una flor amb mesures $x = (x_1, x_2, x_3, x_4)$, la probabilitat de
cada espècie. Això és $P(C \mid x)$, i Bayes el gira:

$$P(C \mid x) = \frac{P(x \mid C)\,P(C)}{P(x)}$$

El denominador $P(x)$ és el mateix per a totes les classes, i el que volem és
saber **quina classe guanya**, no el valor exacte. Per comparar classes es pot
ignorar:

$$P(C \mid x) \;\propto\; P(x \mid C)\,P(C)$$

- $P(C)$ és el *prior*: la fracció de flors de cada espècie al conjunt.
- $P(x \mid C)$ és la versemblança: com de típiques són aquestes quatre mesures dins d'aquella espècie.

Queda una cosa per resoldre, i és la gran: **com es calcula $P(x \mid C)$ amb
quatre columnes contínues?** Comptar files no serveix, perquè cap altra flor no
té exactament les mateixes quatre mesures. Fan falta dues decisions.

**Decisió 1: assumir que cada columna, dins de cada classe, segueix una
distribució normal.** Llavors $P(x_j \mid C)$ es calcula amb la densitat normal,
que depèn de dos números per columna i classe, la mitjana i la desviació:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

I aquests dos números surten... de màxima versemblança. La mitjana i la variància
de la mostra són els estimadors de màxima versemblança dels paràmetres d'una
normal (n'heu de demostrar la mitjana a l'exercici 2).

**Decisió 2, la que dona nom al model: assumir que les quatre columnes són
independents dins de cada classe.** Això permet multiplicar:

$$P(x \mid C) = P(x_1 \mid C)\cdot P(x_2 \mid C)\cdot P(x_3 \mid C)\cdot P(x_4 \mid C)$$

**Aquí és on el model és «naive».** La suposició és falsa a Iris, i ho
comprovarem amb números al final de la secció: la llargada i l'amplada del pètal
van juntes, també dins d'una mateixa espècie. El model se'n desentén i
multiplica igual.
Funciona prou bé tot i això, i és una de les coses més estranyes d'aquest model:
la suposició és dolenta i les prediccions són bones, perquè per decidir qui
guanya no cal que les probabilitats siguin correctes, n'hi ha prou que estiguin
ordenades bé.
"""))

A(code("""
from sklearn.datasets import load_iris

iris = load_iris()
X_i, y_i = iris.data, iris.target
classes = np.unique(y_i)

print("files, columnes:", X_i.shape)
print("classes:", classes, iris.target_names)
print("columnes:", iris.feature_names)

# per cada classe i cada columna: mitjana i variancia (els parametres de la normal)
mitjanes = np.array([X_i[y_i == c].mean(axis=0) for c in classes])
variancies = np.array([X_i[y_i == c].var(axis=0) for c in classes])
priors = np.array([(y_i == c).mean() for c in classes])

print()
print("mitjanes (3 classes x 4 columnes):")
print(np.round(mitjanes, 4))
print()
print("variancies:")
print(np.round(variancies, 6))
print()
print("priors:", np.round(priors, 4))
"""))

A(md(r"""
Els *priors* valen 1/3 cadascun perquè Iris té 50 flors de cada espècie. En un
conjunt desequilibrat no seria així, i el *prior* pesaria en la decisió tal com
pesava a la prova mèdica de la secció 2.

Implementem la densitat normal i comprovem-la contra `scipy.stats.norm.pdf`,
que és la manera de saber que no ens hem equivocat amb el $2\pi$ ni amb el 2 del
denominador.
"""))

A(code("""
from scipy.stats import norm

def densitat_normal(x, mu, var):
    \"\"\"f(x) = 1/(sigma*sqrt(2pi)) * exp(-(x-mu)^2 / (2*sigma^2)), amb var = sigma^2.\"\"\"
    return 1 / np.sqrt(2 * np.pi * var) * np.exp(-(x - mu) ** 2 / (2 * var))

# la primera flor (setosa), columna 2 (llargada del petal), dins de la classe setosa
x_prova = X_i[0, 2]
mu_prova, var_prova = mitjanes[0, 2], variancies[0, 2]

print("x = %.2f, mu = %.3f, sigma = %.4f" % (x_prova, mu_prova, np.sqrt(var_prova)))
print("la meva densitat : %.8f" % densitat_normal(x_prova, mu_prova, var_prova))
print("scipy norm.pdf   : %.8f" % norm.pdf(x_prova, loc=mu_prova, scale=np.sqrt(var_prova)))
print("diferencia       : %.2e" % abs(densitat_normal(x_prova, mu_prova, var_prova)
                                      - norm.pdf(x_prova, loc=mu_prova, scale=np.sqrt(var_prova))))
"""))

A(md(r"""
Ara el model. Podríem multiplicar les quatre densitats pel *prior* i comparar,
però ja sabem què passa si multipliquem probabilitats: amb quatre columnes
aguantaria, amb les 30 del dataset de tumors o les 64 dels dígits, no.

Fem-ho amb logaritmes des del principi. El logaritme del producte és la suma
dels logaritmes, i el logaritme de la densitat normal es simplifica bé:

$$\log f(x) = -\frac{1}{2}\log(2\pi\sigma^2) - \frac{(x-\mu)^2}{2\sigma^2}$$

Noteu que l'exponencial desapareix, que és precisament el que la fa numèricament
perillosa. La puntuació de cada classe queda com una suma:

$$\text{puntuació}(C) = \log P(C) + \sum_{j=1}^{4} \log f_{C,j}(x_j)$$

i la predicció és la classe amb la puntuació més alta. Aquestes puntuacions no
són probabilitats (són logaritmes de números sense normalitzar, i surten
negatives), però estan **ordenades igual** que les probabilitats, i per decidir
n'hi ha prou.
"""))

A(code("""
def log_densitat_normal(x, mu, var):
    return -0.5 * np.log(2 * np.pi * var) - (x - mu) ** 2 / (2 * var)

def puntuacions(X, mitjanes, variancies, priors):
    \"\"\"Una fila per mostra, una columna per classe: log P(C) + suma dels log f.\"\"\"
    resultat = np.zeros((len(X), len(priors)))
    for k in range(len(priors)):
        # (n, 4): el log de la densitat de cada columna sota la classe k
        log_f = log_densitat_normal(X, mitjanes[k], variancies[k])
        resultat[:, k] = np.log(priors[k]) + log_f.sum(axis=1)   # sumem les 4 columnes
    return resultat

punt_iris = puntuacions(X_i, mitjanes, variancies, priors)
prediccio_meva = classes[np.argmax(punt_iris, axis=1)]

print("puntuacions de les 3 primeres flors (files) per classe (columnes):")
print(np.round(punt_iris[:3], 3))
print()
print("classe guanyadora de cada una:", prediccio_meva[:3])
print()
print("precisio del meu Naive Bayes: %.4f (%d de %d)" % (
    (prediccio_meva == y_i).mean(), (prediccio_meva == y_i).sum(), len(y_i)))
"""))

A(code("""
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB().fit(X_i, y_i)
prediccio_sklearn = gnb.predict(X_i)

coincidencia = (prediccio_meva == prediccio_sklearn).mean()

print("precisio de GaussianNB      : %.4f" % (prediccio_sklearn == y_i).mean())
print("coincidencia amb la meva    : %.4f (%d de %d flors)" % (
    coincidencia, (prediccio_meva == prediccio_sklearn).sum(), len(y_i)))
print()
print("mitjanes iguals? diferencia maxima: %.2e" % np.abs(gnb.theta_ - mitjanes).max())
print("variancies iguals? diferencia max : %.2e" % np.abs(gnb.var_ - variancies).max())
print()
print("flors que falla la meva implementacio:", np.where(prediccio_meva != y_i)[0])
print("flors que falla GaussianNB           :", np.where(prediccio_sklearn != y_i)[0])
"""))

A(md(r"""
**Coincidència del 100 %**: les 150 flors reben la mateixa predicció. Les
mitjanes surten idèntiques i les variàncies difereixen en $3{,}1 \times 10^{-9}$,
cosa que té explicació i la veurem a la secció 7.

La precisió és del **96 %**, 144 de 150, i les dues implementacions fallen
exactament les mateixes 6 flors. No està mal per a un model que ha après quatre
mitjanes i quatre variàncies per classe, i que no ha fet cap iteració
d'optimització: **Naive Bayes no s'entrena, es calcula**. Amb una sola passada
per les dades ja té tots els paràmetres.

Vegem les densitats que ha ajustat, per a la columna que separa millor.
"""))

A(code("""
col = 2   # llargada del petal
x_eix = np.linspace(0, 8, 400)
colors_i = ["tab:blue", "tab:orange", "tab:green"]

plt.figure(figsize=(8, 5))
for k, c in enumerate(classes):
    plt.hist(X_i[y_i == c, col], bins=15, density=True, alpha=0.3, color=colors_i[k])
    plt.plot(x_eix, densitat_normal(x_eix, mitjanes[k, col], variancies[k, col]),
             color=colors_i[k], linewidth=2, label=iris.target_names[c])

plt.xlabel("Llargada del petal (cm)")
plt.ylabel("Densitat")
plt.title("Les normals que Naive Bayes ajusta a cada classe")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
### 6.1 Comprovem que la suposició és falsa

Hem dit que les columnes no són independents. No ho deixem com a afirmació:
mirem-ho. Si dues columnes fossin independents, la seva correlació hauria de ser
propera a zero.

Compte amb quina correlació cal mirar, perquè aquí és fàcil fer trampa sense
voler. El model suposa independència **dins de cada classe**, no sobre el
conjunt sencer. Calculem les dues coses i comparem-les.
"""))

A(code("""
noms_curts = ["sepal_llarg", "sepal_ample", "petal_llarg", "petal_ample"]

# sobre el conjunt sencer: barreja les tres especies
r_total = np.corrcoef(X_i.T)
print("sobre les 150 flors totes juntes:")
print("  corr(petal_llarg, petal_ample) = %+.3f" % r_total[2, 3])
print("  corr(sepal_llarg, petal_llarg) = %+.3f" % r_total[0, 2])

# el que el model suposa de veritat: independencia DINS de cada classe
print()
print("dins de cada classe, que es el que el model suposa independent:")
for c in classes:
    r = np.corrcoef(X_i[y_i == c].T)
    print("  %-11s corr(%s, %s) = %+.3f" % (iris.target_names[c], noms_curts[2],
                                            noms_curts[3], r[2, 3]))

# la parella mes correlacionada de totes, dins de versicolor
r_v = np.corrcoef(X_i[y_i == 1].T)
i, j = np.unravel_index(np.argmax(np.abs(r_v - np.eye(4))), r_v.shape)
print()
print("la parella mes correlacionada dins de versicolor: %s i %s, %+.3f" % (
    noms_curts[i], noms_curts[j], r_v[i, j]))
"""))

A(md(r"""
Sobre el conjunt sencer la correlació entre llargada i amplada del pètal és
**+0,963**, gairebé perfecta. Aquest número és el que se cita sempre, i és
enganyós per al nostre propòsit: bona part d'aquesta correlació ve de les
diferències **entre** espècies, no de cap relació dins d'una espècie. Les setoses
tenen pètals petits en totes dues mesures i les virgíniques grans en totes dues,
i això sol ja fabrica una correlació alta.

Els números que ens acusen són els de dins de cada classe: **+0,332** a setosa,
**+0,787** a versicolor i **+0,322** a virginica. El de versicolor és una relació
forta i les altres dues no són zero. **La suposició és falsa, encara que no tant
com el +0,963 faria pensar.**

La conseqüència és que multiplicar les densitats com si fossin informació
independent és **comptar part de la mateixa evidència dues vegades**, i el model
surt més segur de si mateix del que li toca.

Conseqüència pràctica que val la pena saber: les probabilitats de
`predict_proba` d'un Naive Bayes solen ser massa extremes, molt a prop de 0 o
d'1. **Serveixen per ordenar les classes, no per llegir-les com a probabilitats
de veritat.** Si el que us cal és una probabilitat honesta, la regressió
logística la dona millor, perquè és l'únic que optimitza.
"""))

# ---------------------------------------------------- 7. var_smoothing
A(md(r"""
## 7. Per què no coincideix exactament: `var_smoothing`

Les variàncies diferien en $3{,}1 \times 10^{-9}$. No és un error d'arrodoniment
nostre: és una decisió de disseny de scikit-learn que està documentada, i val la
pena veure-la perquè el patró es repeteix per tota la llibreria.

`GaussianNB` té un paràmetre `var_smoothing`, que per defecte val $10^{-9}$, i
la documentació diu que és «la porció de la variància més gran de totes les
característiques que s'afegeix a totes les variàncies per estabilitat de
càlcul». És a dir, scikit-learn no fa servir la variància que ha calculat, sinó:

$$\sigma^2_{\text{usada}} = \sigma^2_{\text{mostra}} + 10^{-9}\cdot \max_j \operatorname{Var}(x_j)$$

El motiu és de supervivència. Si una columna dins d'una classe té tots els
valors iguals, la variància surt 0, i la densitat normal divideix per
$2\sigma^2$: divisió per zero, i el model peta. Afegir un número minúscul a
totes les variàncies garanteix que això no pugui passar mai.
"""))

A(code("""
max_variancia = X_i.var(axis=0).max()
correccio = gnb.var_smoothing * max_variancia

print("var_smoothing              : %.1e" % gnb.var_smoothing)
print("variancia mes gran de totes: %.6f" % max_variancia)
print("correccio que suma sklearn : %.4e" % correccio)
print("diferencia que havia sortit: %.4e" % np.abs(gnb.var_ - variancies).max())
"""))

A(code("""
# ara reproduim sklearn exactament, afegint la mateixa correccio
variancies_suavitzades = variancies + correccio
print("ara les variancies difereixen en %.2e" % np.abs(gnb.var_ - variancies_suavitzades).max())

def log_probabilitats(P):
    \"\"\"Normalitza les puntuacions a log-probabilitats restant el logaritme de la suma.\"\"\"
    # es resta el maxim abans d'exponenciar per no desbordar: exp(-800) seria 0
    m = P.max(axis=1, keepdims=True)
    return P - (m + np.log(np.exp(P - m).sum(axis=1, keepdims=True)))

P_sense = puntuacions(X_i, mitjanes, variancies, priors)
P_amb = puntuacions(X_i, mitjanes, variancies_suavitzades, priors)

dif_sense = np.abs(log_probabilitats(P_sense) - gnb.predict_log_proba(X_i)).max()
dif_amb = np.abs(log_probabilitats(P_amb) - gnb.predict_log_proba(X_i)).max()

print()
print("diferencia amb predict_log_proba, SENSE suavitzat: %.3e" % dif_sense)
print("diferencia amb predict_log_proba, AMB suavitzat  : %.3e" % dif_amb)
"""))

A(md(r"""
Sense la correcció la diferència és $1{,}1 \times 10^{-4}$; amb la correcció baixa
a $1{,}1 \times 10^{-13}$, que és soroll de coma flotant. Hem reproduït
`GaussianNB` exactament.

La lliçó no és sobre `var_smoothing`. És aquesta: **quan la vostra
implementació i la de la llibreria no coincideixen, la diferència té una causa
concreta i normalment està escrita a la documentació.** Un $10^{-4}$ no és «un
error d'arrodoniment»; un $10^{-13}$ sí. Saber distingir-los és el que us
permetrà, quan la diferència sigui gran de veritat, saber que teniu un
*bug* i no un detall d'implementació.
"""))

# ---------------------------------------------------- exercicis
A(md(r"""
## Exercicis

Quatre exercicis. Cadascun porta una línia de «com saps que ho has fet bé» amb
el resultat que ha de sortir.
"""))

A(md(r"""
### Exercici 1 — La mateixa prova, una malaltia menys rara

El 9,02 % de la secció 2 depèn tant de la prevalença com de la qualitat de la
prova. Escriu una funció `prob_malalt(prevalenca, sensibilitat, especificitat)`
que apliqui Bayes i retorni $P(\text{malalt} \mid +)$, i fes-la servir per
calcular-ho amb la mateixa prova del 99 % i 99 % per a quatre prevalences:
1 de cada 1.000, 1 de cada 100, 1 de cada 20 i 1 de cada 10.

Després respon amb una frase: si la prova no ha canviat, per què canvia tant la
resposta?
"""))

A(code("""
# Exercici 1
# Escriu prob_malalt(prevalenca, sensibilitat, especificitat) i aplica-la a
# les prevalences 0.001, 0.01, 0.05 i 0.1 amb sensibilitat = especificitat = 0.99.
# Imprimeix cada resultat en percentatge.

"""))

A(md(r"""
**Com saps que ho has fet bé:** surt **9,02 %** per a 1/1.000, **50,00 %** exacte
per a 1/100, **83,90 %** per a 1/20 i **91,67 %** per a 1/10. El 50 % rodó de la
prevalença 1/100 no és casualitat: amb 10.000 persones hi ha 100 malalts i 99
donen positiu, i dels 9.900 sans l'1 % en són 99 també. Els dos grups de
positius tenen la mateixa mida.
"""))

A(md(r"""
### Exercici 2 — Màxima versemblança per a la mitjana d'una normal

A la secció 6 hem donat per bo que la mitjana de la mostra és l'estimador de
màxima versemblança de $\mu$. Comprova-ho numèricament.

Genera una mostra de 200 valors d'una normal amb `np.random.seed(7)` i
`np.random.normal(170, 10, 200)` (alçades, en cm). **Fes com si no sabessis que
$\mu = 170$**, però dona per conegut que $\sigma = 10$.

La log-versemblança d'una mostra sota una normal de mitjana $\mu$ és la suma dels
logaritmes de les densitats de cada valor:

$$\ell(\mu) = \sum_{i=1}^{200} \left[ -\frac{1}{2}\log(2\pi\sigma^2) - \frac{(x_i-\mu)^2}{2\sigma^2} \right]$$

Calcula-la per a una graella de $\mu$ entre 160 i 180 amb 20.001 punts, dibuixa
la corba, troba el $\mu$ que la maximitza i compara'l amb `mostra.mean()`.

Extra, sense codi: mirant la fórmula, el primer terme no depèn de $\mu$ i el
segon és $-\frac{1}{2\sigma^2}\sum (x_i-\mu)^2$. Maximitzar això és el mateix que
minimitzar $\sum (x_i-\mu)^2$. Digues per què això explica que la resposta
hagi de ser la mitjana.
"""))

A(code("""
# Exercici 2
# 1. genera la mostra amb np.random.seed(7) i np.random.normal(170, 10, 200)
# 2. defineix una graella de mu: np.linspace(160, 180, 20001)
# 3. per cada mu de la graella, calcula la log-versemblanca de tota la mostra
#    (pista: es pot fer amb un bucle sobre la graella, o amb broadcasting)
# 4. dibuixa la corba i marca el maxim
# 5. compara el mu del maxim amb mostra.mean()

"""))

A(md(r"""
**Com saps que ho has fet bé:** la mostra té mitjana **169,7204**, i el màxim de
la graella cau a **169,7200**: els dos coincideixen fins allà on arriba el gra
de la graella, que és 0,001. Fixa't que el màxim **no** cau a 170: la màxima
versemblança dona el paràmetre que millor explica **la mostra que tens**, no el
que va generar les dades. Amb 200 valors encara hi ha aquesta distància.
"""))

A(md(r"""
### Exercici 3 — El teu Naive Bayes sobre Wine

Aplica la implementació de la secció 6 al dataset `load_wine`: 178 vins, 13
columnes de mesures químiques, 3 classes. No cal reescriure res, les funcions
`log_densitat_normal` i `puntuacions` ja estan fetes i no depenen del nombre de
columnes ni de classes.

Calcula les mitjanes, les variàncies i els *priors* per classe, prediu, i compara
amb `GaussianNB`. Mira també si els *priors* són iguals entre ells, com passava a
Iris.
"""))

A(code("""
# Exercici 3
# from sklearn.datasets import load_wine
# 1. carrega les dades a X_w, y_w
# 2. calcula mitjanes, variancies i priors per classe (les tres classes de y_w)
# 3. fes servir puntuacions() i argmax per predir
# 4. entrena GaussianNB i compara les prediccions: quin percentatge coincideix?
# 5. imprimeix els priors: son iguals entre ells?

"""))

A(md(r"""
**Com saps que ho has fet bé:** coincidència del **100 %** amb `GaussianNB` i una
precisió del **98,88 %** (176 de 178 vins). Els *priors* **no** són iguals: surten
0,3315, 0,3989 i 0,2697, perquè Wine té 59, 71 i 48 vins de cada classe. Amb 13
columnes multiplicades, si ho haguessis fet sense logaritmes els números serien
prou petits per haver de començar a preocupar-se.
"""))

A(md(r"""
### Exercici 4 — Un model que encerta tot i té una log-loss pèssima

Aquest exercici tanca la idea de la secció 5 i la de la secció 2.2.

Agafa `y_te` i `p_te` de la secció 5. Construeix dos vectors de probabilitats
falsos, que no venen de cap model:

- `p_dubitatiu = np.where(y_te == 1, 0.51, 0.49)`: encerta **totes** les
  etiquetes amb el tall a 0,5, però sempre per un pèl.
- `p_segur = np.where(y_te == 1, 0.99, 0.01)`: encerta totes i molt segur.

Per a tots dos, i per a les `p_te` del model de veritat, calcula la precisió
(fracció d'etiquetes encertades, amb el tall a 0,5) i la log-loss. Després
respon: quin dels tres triaries, i per què la precisió no t'ho diu?
"""))

A(code("""
# Exercici 4
# 1. construeix p_dubitatiu i p_segur amb np.where
# 2. per cada un dels tres vectors de probabilitats (p_dubitatiu, p_segur, p_te):
#    - precisio: (np.round(p) == y_te).mean()  o be (p > 0.5).astype(int) == y_te
#    - log-loss: log_loss(y_te, p)
# 3. imprimeix-ho en una taula de tres files

"""))

A(md(r"""
**Com saps que ho has fet bé:** `p_dubitatiu` té precisió **1,0000** i log-loss
**0,6733**. `p_segur` té la mateixa precisió **1,0000** i log-loss **0,0101**. El
model de veritat té precisió **0,9883** (falla 2 de 171) i log-loss **0,0655**.

Les tres columnes diuen coses diferents, i això és el resultat de l'exercici. La
precisió no distingeix `p_dubitatiu` de `p_segur`, tot i que un dubta de tot i
l'altre no. La log-loss els separa per un factor de 67. I el model de veritat,
que **falla dues files**, treu una log-loss deu vegades millor que el que encerta
totes: perquè quan encerta, encerta amb convicció.
"""))

# ---------------------------------------------------- resum
A(md(r"""
## Resum

Què s'ha demostrat en aquest quadern, amb números:

- Una probabilitat condicionada és **una divisió de dos recomptes**. La definició
  $P(A|B) = P(A\cap B)/P(B)$ i el recompte $161/173$ donen el mateix 0,9306.
- El teorema de Bayes **surt en dues línies** de la definició, i s'ha comprovat
  que reprodueix el recompte directe fins a $10^{-16}$.
- Una prova del 99 % sobre una malaltia d'1 per mil dona, davant d'un positiu,
  un **9,02 %** de probabilitat de malaltia. I aquella prova té pitjor exactitud
  global (99,0 %) que un model que sempre diu «negatiu» (99,9 %) i no detecta ni
  un malalt.
- La **fracció observada és l'estimador de màxima versemblança** d'una
  proporció: la graella dona 0,700 i la derivada de la log-versemblança dona
  7/10 exacte.
- Multiplicar 2.000 probabilitats de 0,5 dona **`0.0` exactament**; la suma de
  logaritmes dona -1386,2944. El producte es trenca a partir de 1.075 factors.
  El logaritme, per ser creixent, **no mou el punt del màxim**.
- La **log-loss és la log-versemblança amb el signe canviat i dividida per $n$**.
  No hi ha cap altra justificació, i no fa falta: la nostra implementació i
  `sklearn.metrics.log_loss` coincideixen amb una diferència de $1{,}4\times10^{-17}$.
- Un **Naive Bayes gaussià sencer** cap en mitja pàgina de NumPy, no té cap
  iteració d'entrenament, i dona el **100 %** de coincidència amb `GaussianNB`
  sobre les 150 flors d'Iris (96 % de precisió, 144 de 150). La seva suposició
  d'independència és falsa: dins de versicolor, la correlació entre llargada i
  amplada del pètal és +0,787 (i +0,963 sobre el conjunt sencer, número que
  exagera perquè hi barreja les diferències entre espècies).
- La diferència que quedava amb scikit-learn ($1{,}1\times10^{-4}$) **tenia nom i
  estava documentada**: `var_smoothing`. Afegint-la, baixa a $1{,}1\times10^{-13}$.

Resposta a la pregunta del principi: la regressió logística minimitza aquella
fórmula amb logaritmes perquè **minimitzar-la és maximitzar la probabilitat
d'haver observat les dades que teniu**. Qualsevol altra funció que baixi quan el
model encerta seria una tria arbitrària; aquesta és una conseqüència.

Simplificacions que hem fet, dites en veu alta:

- Hem tret el coeficient binomial $\binom{10}{7}$ de la versemblança de la
  moneda. És una constant, no mou el màxim.
- Hem ignorat el denominador $P(x)$ a Naive Bayes. És el mateix per a totes les
  classes, no canvia quina guanya.
- Hem retallat les probabilitats a $[10^{-15}, 1-10^{-15}]$ a la log-loss. Això
  limita el càstig d'una fila a 34,5 en comptes d'infinit.
- A l'exercici 2 hem donat $\sigma$ per conegut per estimar només $\mu$. Estimar
  els dos alhora es fa igual, amb una derivada parcial per a cada paràmetre.
- Hem dit que maximitzar la versemblança és el que fa la regressió logística,
  i no hem dit **com** troba el màxim. Amb la moneda es podia aïllar $p$ de la
  derivada; amb 30 pesos no es pot, i cal baixar el pendent a poc a poc.

## I ara què

Queda un fil per estirar. A la secció 5 la log-loss ha sortit de comptar
probabilitats; als arbres de decisió, la impuresa de Gini va sortir de comptar
classes en un node, i semblaven dues coses sense cap relació.

No ho són. Totes dues mesuren **quanta informació falta**, i hi ha una tercera
fórmula, l'**entropia**, que les connecta i que explica per què la log-loss
també es diu «entropia creuada». Això és el quadern següent d'aquest bloc,
`MA_04_entropia_informacio.ipynb`.
"""))

# ---------------------------------------------------------------- escriu
if __name__ == "__main__":
    info = escriu(cells,
                  "Machine Learning/03_matematiques/MA_03_probabilitat_versemblanca.ipynb",
                  titol_colab="MA_03 - Probabilitat i versemblanca")
    print(info)
