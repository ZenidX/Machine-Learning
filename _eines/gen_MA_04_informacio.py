# -*- coding: utf-8 -*-
"""Genera el quadern MA_04: entropia, informacio i la tesi log-loss = entropia creuada.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_MA_04_informacio.py
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# Entropia i informació: el que mesuren de debò un arbre i una log-loss

**Optativa d'Aprenentatge automàtic · bloc de matemàtiques**

Al quadern `ML_02_arbres` vau implementar la impuresa de Gini, vau calcular el guany
d'un tall i vau trobar a mà el `petal_llarg <= 2.45` que tria `DecisionTreeClassifier`.
Allà l'entropia va aparèixer de passada, com una alternativa a Gini que «es calcula
diferent però mesura el mateix».

Aquest quadern va a buscar d'on surt aquesta fórmula i fins on arriba. La tesi que es
demostra amb codi al final és aquesta:

> **La impuresa que minimitza un arbre de decisió i la pèrdua que minimitza una
> regressió logística són la mateixa magnitud, mesurada de dues maneres.**

Això no és una analogia docent. A la secció 7 implementarem la log-loss i l'entropia
creuada per separat, amb noms diferents, i comprovarem que donen el mateix número fins
als últims decimals, i que coincideix amb `sklearn.metrics.log_loss`.

El camí és: sorpresa → entropia → guany d'informació → divergència de Kullback-Leibler
→ entropia creuada → log-loss. És dens i hi ha logaritmes a cada pas. No hi ha manera
d'escurçar-lo.
"""))

A(code(r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
np.set_printoptions(precision=4, suppress=True)

print("numpy", np.__version__)
'''))

# ---------------------------------------------------------------- 1 sorpresa
A(md(r"""
## 1. La informació com a sorpresa

Comencem per una pregunta que sembla trivial: **quanta informació hi ha en saber el
resultat d'una cosa que ja saps?** Cap. Si algú us diu «demà el Sol sortirà per
l'est», no us ha dit res: ja ho sabíeu, la probabilitat era 1. En canvi, si us diu
«demà el Sol sortirà per l'oest», us ha dit moltíssim.

La informació, doncs, no està en el missatge: està en **com d'improbable era**. Volem
una funció $s(p)$ que digui quanta informació aporta observar un esdeveniment de
probabilitat $p$. Li exigim dues coses, i les dues són raonables:

**Propietat 1: $s(1) = 0$.** Un esdeveniment segur no informa de res.

**Propietat 2: additivitat.** Si observo dos esdeveniments **independents**, un de
probabilitat $p$ i un altre de probabilitat $q$, la informació total ha de ser la suma
de les dues:

$$s(p \cdot q) = s(p) + s(q)$$

Aquesta és la propietat clau, i és una exigència sobre com volem que es comporti la
mesura: si llenço dues monedes, la segona m'ha d'informar tant com la primera, i el
total ha de ser el doble. Fixeu-vos en la forma de l'equació: a l'esquerra hi ha un
**producte** de probabilitats (perquè així es combinen les probabilitats
d'esdeveniments independents) i a la dreta una **suma**. Hi ha una única família de
funcions contínues que converteix productes en sumes, i és el logaritme.

Si volem, a més, que la informació sigui positiva (i $\log p \le 0$ perquè
$p \le 1$), hem de posar-hi un signe menys:

$$\boxed{\;s(p) = -\log_2 p\;}$$

La base del logaritme decideix la unitat. Amb base 2 la unitat es diu **bit**, i a la
secció següent veurem que aquest nom és literal, no metafòric.

Comprovem les dues propietats amb NumPy.
"""))

A(code(r'''
def sorpresa(p):
    """Informacio, en bits, d'observar un esdeveniment de probabilitat p."""
    return -np.log2(p) + 0.0    # el + 0.0 evita que surti -0.0 quan p val 1


# Propietat 1: un esdeveniment segur no informa de res
print("s(1)   =", sorpresa(1.0), "bits")

# Propietat 2: additivitat sobre esdeveniments independents
p, q = 0.5, 0.25
print(f"s({p} * {q}) = {sorpresa(p * q):.4f} bits")
print(f"s({p}) + s({q}) = {sorpresa(p) + sorpresa(q):.4f} bits")
print("additiva:", np.isclose(sorpresa(p * q), sorpresa(p) + sorpresa(q)))
'''))

A(md(r"""
Ara uns quants casos concrets, per agafar escala.
"""))

A(code(r'''
casos = {
    "cara d'una moneda justa": 1 / 2,
    "un 6 amb un dau de 6 cares": 1 / 6,
    "un valor concret d'un dau de 8 cares": 1 / 8,
    "dues cares seguides amb moneda justa": 1 / 4,
    "un esdeveniment d'1 entre 1.000": 1 / 1000,
    "un esdeveniment d'1 entre 1.000.000": 1 / 1000000,
}

probabilitats = np.array(list(casos.values()))
bits = sorpresa(probabilitats)

for nom, p_cas, b in zip(casos, probabilitats, bits):
    print(f"{nom:45s} p={p_cas:<10.6g} sorpresa = {b:6.3f} bits")
'''))

A(md(r"""
El dau de 6 cares dona 2,585 bits i el de 8 cares exactament 3. Dues cares seguides
donen 2 bits, que és el doble d'una sola cara: la additivitat funciona. I un
esdeveniment d'1 entre un milió dona 19,93 bits, que és el doble dels 9,97 d'un
esdeveniment d'1 entre mil, perquè $10^6 = 10^3 \cdot 10^3$. La sorpresa creix com el
logaritme de la raresa, no com la raresa: passar d'1 entre mil a 1 entre un milió
multiplica la improbabilitat per mil i la informació només per dos.
"""))

A(md(r"""
Dibuixem la funció sencera. A l'esquerra, $s(p)$ amb l'eix de $p$ normal: val 0 a $p=1$ i
s'enfila sense límit quan $p \to 0$. A la dreta, la mateixa funció amb l'eix de $p$ en
escala logarítmica: es torna una **recta**, i cada vegada que un esdeveniment és mil
vegades més rar la sorpresa puja uns 10 bits ($\log_2 1000 \approx 9{,}97$).
"""))

A(code(r'''
sorpresa_corba = np.linspace(0.001, 1, 1000)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))

ax1.plot(sorpresa_corba, sorpresa(sorpresa_corba), color="tab:blue", linewidth=2)
for nom_curt, p_cas in [("moneda: cara", 1 / 2), ("dues cares", 1 / 4),
                        ("dau de 6: un 6", 1 / 6), ("dau de 8: un valor", 1 / 8)]:
    ax1.scatter([p_cas], [sorpresa(p_cas)], color="tab:red", zorder=3)
    ax1.annotate(f"{nom_curt}: {sorpresa(p_cas):.2f} bits", (p_cas, sorpresa(p_cas)),
                 xytext=(10, 0), textcoords="offset points", fontsize=9, va="center")
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 8)
ax1.set_xlabel("p (probabilitat de l'esdeveniment)")
ax1.set_ylabel("sorpresa $s(p) = -\\log_2 p$ (bits)")
ax1.set_title("Com més improbable, més sorpresa")
ax1.grid(alpha=0.3)

p_log = np.logspace(-6, 0, 400)
ax2.semilogx(p_log, sorpresa(p_log), color="tab:blue", linewidth=2)
for p_cas, nom_curt in [(1e-3, "1 entre mil"), (1e-6, "1 entre un milió")]:
    ax2.scatter([p_cas], [sorpresa(p_cas)], color="tab:red", zorder=3)
    ax2.annotate(f"{nom_curt}: {sorpresa(p_cas):.2f} bits", (p_cas, sorpresa(p_cas)),
                 xytext=(12, 0), textcoords="offset points", fontsize=9, va="center")
ax2.set_xlabel("p (escala logarítmica)")
ax2.set_ylabel("sorpresa (bits)")
ax2.set_title("En escala logarítmica, una recta")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
'''))

# ---------------------------------------------------------------- 2 entropia
A(md(r"""
## 2. L'entropia és la sorpresa mitjana

La sorpresa parla d'**un** resultat concret. L'entropia parla de **tota la
distribució**: és la sorpresa que esperem de mitjana abans de saber el resultat. Com
qualsevol mitjana ponderada, es calcula multiplicant cada valor per la seva
probabilitat i sumant:

$$H(p) \;=\; \mathbb{E}[s] \;=\; \sum_i p_i \, s(p_i) \;=\; -\sum_i p_i \log_2 p_i$$

Aquesta és exactament la fórmula que vau veure de passada al quadern d'arbres. Ara ja
sabeu què hi fa el logaritme: hi és perquè és l'única manera de mesurar informació que
sigui additiva sobre esdeveniments independents.

### El conveni $0 \log 0 = 0$, i per què no és un pegat

Si alguna classe té probabilitat 0, la fórmula demana calcular $0 \cdot \log_2 0$, que
és $0 \cdot (-\infty)$: indeterminat. El conveni universal és prendre'l com a 0, i no
és una decisió arbitrària per esquivar un `-inf`. És el valor del límit:

$$\lim_{p \to 0^+} p \log_2 p = 0$$

El factor lineal $p$ va a zero més de pressa que el logaritme va a $-\infty$, i el
producte guanya el lineal. Amb això, la funció $p \mapsto -p\log_2 p$ és contínua a
tot $[0, 1]$ si la definim com a 0 a l'origen: el conveni és l'**única** extensió
contínua possible. La lectura intuïtiva també quadra: un esdeveniment que no passa
mai no contribueix gens a la sorpresa mitjana, encara que la seva sorpresa individual
sigui infinita.

Comprovem el límit numèricament abans d'implementar res.
"""))

A(code(r'''
p_petits = np.array([1e-1, 1e-2, 1e-3, 1e-6, 1e-12, 1e-30])
contribucio = -p_petits * np.log2(p_petits)

for p_i, c in zip(p_petits, contribucio):
    print(f"p = {p_i:<8.0e}  ->  -p*log2(p) = {c:.3e}")
'''))

A(md(r"""
Va a zero, i de pressa. A la implementació, doncs, filtrem les probabilitats nul·les
amb una màscara abans de cridar `np.log2`: així no calculem mai `log2(0)` i no hi ha
cap avís numèric ni cap `-inf` que s'arrossegui.
"""))

A(code(r'''
def entropia(p):
    """Entropia en bits d'una distribucio discreta p (vector de probabilitats).

    Les probabilitats nul.les es descarten: pel conveni 0*log(0) = 0 no aporten res,
    i aixi evitem calcular log2(0).
    """
    p = np.asarray(p, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)) + 0.0)


def entropia_etiquetes(y):
    """Entropia en bits de la distribucio de classes d'un vector d'etiquetes."""
    _, comptes = np.unique(np.asarray(y), return_counts=True)
    return entropia(comptes / comptes.sum())


print("moneda justa            H =", entropia([0.5, 0.5]), "bits")
print("moneda trucada 0.9/0.1  H =", round(entropia([0.9, 0.1]), 4), "bits")
print("moneda de dues cares    H =", entropia([1.0, 0.0]), "bits")
print("dau de 8 cares          H =", entropia(np.full(8, 1 / 8)), "bits")
print("dau de 6 cares          H =", round(entropia(np.full(6, 1 / 6)), 4), "bits")
'''))

A(md(r"""
### El bit té un significat literal

Els dos números exactes de dalt no són casualitat:

- Moneda justa: $H = 1$ bit, **exactament**.
- Dau de 8 cares: $H = 3$ bits, **exactament**.

L'entropia és el nombre mitjà de **preguntes de sí o no** que necessiteu per endevinar
el resultat, si feu les preguntes de la millor manera possible. Amb la moneda, una
pregunta («ha sortit cara?») i ja ho sabeu: 1 bit. Amb el dau de 8 cares, tres
preguntes que parteixin el conjunt per la meitat cada vegada («és del 1 al 4?», «és
del 1 al 2?», «és l'1?»): $8 = 2^3$, i cada pregunta us elimina la meitat dels
candidats, així que en calen 3. Amb la moneda de dues cares, zero preguntes: ja sabeu
la resposta.

Amb el dau de 6 cares surten 2,585 bits, que no és un enter. La interpretació segueix
valent, però com a **mitjana**: no podeu fer 2,585 preguntes per a un sol llançament,
però si heu d'endevinar el resultat de mil llançaments seguits podeu dissenyar un
esquema de preguntes que se'n surti amb 2.585 preguntes de mitjana. Aquest és el
teorema de la codificació de Shannon, i aquí ens el saltem: ens quedem amb el fet que
l'entropia és una **longitud mitjana òptima** mesurada en bits.

### La corba d'una moneda esbiaixada

Per al cas binari, amb $p$ la probabilitat de cara, l'entropia val

$$H(p) = -p\log_2 p - (1-p)\log_2(1-p)$$

i té una única variable. Dibuixem-la.
"""))

A(code(r'''
ps = np.linspace(0, 1, 501)
H_binaria = np.array([entropia([p_i, 1 - p_i]) for p_i in ps])

plt.figure(figsize=(8, 5))
plt.plot(ps, H_binaria, color="tab:blue")
plt.axvline(0.5, color="tab:red", linestyle="--", label="màxim a p = 0,5 (H = 1 bit)")
plt.scatter([0, 1], [0, 0], color="tab:green", zorder=5,
            label="H = 0 als extrems (cap incertesa)")
plt.xlabel("p (probabilitat de cara)")
plt.ylabel("Entropia H(p) en bits")
plt.title("Entropia d'una moneda esbiaixada")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print("H(0)    =", H_binaria[0])
print("H(0.5)  =", H_binaria[250])
print("H(1)    =", H_binaria[-1])
'''))

A(md(r"""
La corba és una campana asimètrica només en aparença: de fet és perfectament simètrica
respecte a $p = 0{,}5$, perquè la fórmula tracta igual les dues classes. Val 0 als dos
extrems (si sabeu del cert què sortirà, no hi ha incertesa) i té el màxim al mig, on
val 1 bit. Cap distribució binària pot superar 1 bit d'entropia: el màxim d'incertesa
amb dues opcions és no tenir-ne cap preferència.

Fixeu-vos que els zeros dels extrems els calcula bé gràcies al conveni de la secció
anterior: a $p = 0$ el primer terme és $0 \log_2 0$ i el segon $1 \log_2 1 = 0$.
"""))

A(md(r"""
### L'entropia com a àrea

La fórmula $H = \sum_i p_i\, s(p_i)$ té una lectura geomètrica directa: per a cada resultat,
un rectangle d'**amplada** $p_i$ (quant passa) i **alçada** $s(p_i)$ (quanta sorpresa fa
quan passa). L'entropia és l'**àrea total**. Comparem la moneda justa amb una de trucada
al 90/10.
"""))

A(code(r'''
fig, eixos = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
for ax, (nom, dist) in zip(eixos, [("Moneda justa", [0.5, 0.5]),
                                   ("Moneda trucada 90/10", [0.9, 0.1])]):
    dist = np.array(dist)
    esquerra = np.concatenate([[0], np.cumsum(dist)[:-1]])
    ax.bar(esquerra, sorpresa(dist), width=dist, align="edge",
           color=["tab:blue", "tab:orange"], edgecolor="white")
    for x0, p_i, s_i, eti in zip(esquerra, dist, sorpresa(dist), ["cara", "creu"]):
        ax.text(min(x0 + p_i / 2, 0.88), s_i + 0.1, f"{eti}\np = {p_i:g}\ns = {s_i:.2f}",
                ha="center", fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.6)
    ax.set_xlabel("amplada de cada rectangle = $p_i$")
    ax.set_title(f"{nom}: àrea = H = {entropia(dist):.3f} bits")
    ax.grid(alpha=0.3, axis="y")
eixos[0].set_ylabel("alçada = sorpresa $s(p_i)$ (bits)")
plt.tight_layout()
plt.show()
'''))

A(md(r"""
La creu de la moneda trucada fa molta sorpresa (3,32 bits), però el seu rectangle és molt
estret perquè passa poc. La cara gairebé no sorprèn. L'àrea total, 0,469 bits, és menys de
la meitat que la de la moneda justa: és el punt $p = 0{,}9$ de la corba de dalt.
"""))

# ---------------------------------------------------------------- 3 entropia vs gini
A(md(r"""
## 3. Entropia contra Gini

Aquestes són les dues mesures d'impuresa que fa servir un arbre de decisió, l'una al
costat de l'altra:

$$H = -\sum_i p_i \log_2 p_i \qquad\qquad G = 1 - \sum_i p_i^2$$

Són fórmules diferents: l'una té un logaritme i l'altra un quadrat. Fan servir escales
diferents: per al cas binari $H$ arriba a 1 i $G$ a 0,5. I tot i això, entrenar un
arbre amb l'una o amb l'altra dona arbres gairebé idèntics. La raó és geomètrica i es
veu d'un cop en un gràfic.
"""))

A(code(r'''
def gini(p):
    """Impuresa de Gini d'una distribucio discreta p."""
    p = np.asarray(p, dtype=float)
    return float(1 - np.sum(p ** 2))


def gini_etiquetes(y):
    """Impuresa de Gini de la distribucio de classes d'un vector d'etiquetes."""
    _, comptes = np.unique(np.asarray(y), return_counts=True)
    return gini(comptes / comptes.sum())


G_binaria = np.array([gini([p_i, 1 - p_i]) for p_i in ps])

plt.figure(figsize=(8, 5))
plt.plot(ps, H_binaria, color="tab:blue", label="Entropia  H = -Σ p·log₂(p)")
plt.plot(ps, G_binaria, color="tab:orange", label="Gini  G = 1 - Σ p²")
plt.plot(ps, H_binaria / 2, color="tab:blue", linestyle=":",
         label="Entropia / 2 (mateixa escala que Gini)")
plt.axvline(0.5, color="gray", linestyle="--", alpha=0.6)
plt.xlabel("p (proporció de la primera classe)")
plt.ylabel("Impuresa")
plt.title("Entropia i Gini per al cas binari")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
**Per què donen arbres gairebé iguals.** Les dues corbes comparteixen les tres
propietats que fan que un arbre triï bé:

1. **Els mateixos zeros**: totes dues valen 0 a $p=0$ i a $p=1$, és a dir, en un node
   pur.
2. **El mateix màxim**: totes dues tenen el màxim exactament a $p=0{,}5$, la barreja
   més equilibrada.
3. **La mateixa concavitat**: totes dues són còncaves, i per això el guany d'un tall
   (la impuresa del pare menys la mitjana ponderada dels fills) és sempre $\ge 0$.
   Aquesta és la propietat que fa que partir mai no empitjori la mesura.

Un arbre no fa servir el **valor** de la impuresa per a res: fa servir només l'**ordre**
entre candidats, perquè es queda amb el tall de guany màxim. I dues funcions amb els
mateixos zeros, el mateix màxim i la mateixa forma ordenen els talls de manera molt
semblant.

El «molt semblant» no és «igual», i això és important. Les corbes **no són
proporcionals**: la línia de punts és $H/2$ i no se superposa amb Gini. L'entropia
castiga més els nodes molt barrejats, perquè el logaritme baixa amb pendent més fort a
prop de 0. Així que hi ha talls on les dues mesures discrepen, i quan discrepen a
l'arrel, tot l'arbre de sota surt diferent.

Anem a mesurar exactament quant discrepen, sobre Iris i Wine. Primer el tall de
l'arrel, que és la comparació més neta: un sol tall, cap efecte acumulat.
"""))

A(code(r'''
from sklearn.datasets import load_iris, load_wine
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

iris = load_iris(as_frame=True)
dades = iris.frame.copy()
dades["especie"] = iris.target_names[iris.target]
dades = dades.rename(columns={
    "sepal length (cm)": "sepal_llarg",
    "sepal width (cm)": "sepal_ample",
    "petal length (cm)": "petal_llarg",
    "petal width (cm)": "petal_ample",
})
X = dades[["sepal_llarg", "sepal_ample", "petal_llarg", "petal_ample"]]
y = dades["especie"]

vi = load_wine(as_frame=True)
X_vi = vi.frame[vi.feature_names]
y_vi = vi.frame["target"]


def arrel(Xd, yd, criteri):
    """Columna i llindar de l'arrel d'un arbre d'un sol tall."""
    a = DecisionTreeClassifier(max_depth=1, criterion=criteri, random_state=42)
    a.fit(Xd, yd)
    return (Xd.columns[a.tree_.feature[0]], round(float(a.tree_.threshold[0]), 4))


for nom, Xd, yd in (("Iris", X, y), ("Wine", X_vi, y_vi)):
    g = arrel(Xd, yd, "gini")
    e = arrel(Xd, yd, "entropy")
    print(f"{nom:5s} gini   : {g[0]} <= {g[1]}")
    print(f"{nom:5s} entropy: {e[0]} <= {e[1]}")
    print(f"{nom:5s} el mateix tall: {g == e}")
    print()
'''))

A(md(r"""
A Iris les dues mesures trien el mateix tall a l'arrel, i és el `petal_llarg <= 2.45`
que ja coneixeu. A Wine **no**: Gini tria `proline <= 755.0` i l'entropia tria
`flavanoids <= 1.575`. Les dues columnes són bones (a la secció 8 les retrobareu com a
primera i segona en informació mútua), però la discrepància és real i està aquí mateix,
al primer tall del segon dataset que hem provat. Qui digui que els dos criteris «donen
el mateix» ja ha fallat aquí.

Ara els arbres sencers. Comparem els **talls node a node**, no només l'exactitud (*accuracy*), per
veure si la divergència de l'arrel es propaga.
"""))

A(code(r'''
def talls(Xd, yd, criteri, **kwargs):
    """Llista de (columna, llindar) dels nodes interns, en ordre de recorregut."""
    a = DecisionTreeClassifier(criterion=criteri, random_state=42, **kwargs)
    a.fit(Xd, yd)
    t = a.tree_
    cols = list(Xd.columns)
    return [(cols[t.feature[i]], round(float(t.threshold[i]), 4))
            for i in range(t.node_count) if t.feature[i] >= 0]


for nom, Xd, yd in (("Iris", X, y), ("Wine", X_vi, y_vi)):
    tg = talls(Xd, yd, "gini")
    te = talls(Xd, yd, "entropy")
    print(f"--- {nom} (arbre sencer) ---")
    print("  gini   :", tg)
    print("  entropy:", te)
    print("  talls idèntics:", tg == te)
    print()
'''))

A(md(r"""
El resultat és desigual, i val la pena llegir-lo amb calma. A **Iris**, els dos arbres
sencers són **exactament idèntics**: els vuit talls, en el mateix ordre i amb els
mateixos llindars. A **Wine**, en canvi, no comparteixen ni el nombre de nodes interns
(11 amb Gini, 7 amb entropia) ni cap dels talls. La diferència ve d'on ja divergien: si
l'arrel canvia, tot l'arbre de sota es construeix sobre dades partides d'una altra
manera, i no hi ha cap raó perquè torni a coincidir.

Iris és un dataset on les dues classes difícils se separen amb un marge net i qualsevol
mesura raonable hi troba el mateix; Wine té 13 columnes correlacionades i molts talls
gairebé empatats, així que qualsevol diferència d'escala entre les dues mesures decideix
el desempat.

Llavors, en quin sentit són «gairebé iguals»? En el que compta: **en l'exactitud**. Un
sol `train_test_split` no serveix per contestar-ho, perquè amb 45 flors d'examen la
diferència entre un criteri i l'altre queda enterrada sota el soroll de quines flors han
caigut a l'examen. Cal repetir-ho amb moltes particions i mirar la mitjana.
"""))

A(code(r'''
def exactitud_mitjana(Xd, yd, criteri, n_repeticions=40, **kwargs):
    """Exactitud d'examen mitjana sobre n particions diferents."""
    puntuacions = []
    for llavor in range(n_repeticions):
        Xtr, Xte, ytr, yte = train_test_split(
            Xd, yd, test_size=0.3, random_state=llavor, stratify=yd)
        a = DecisionTreeClassifier(criterion=criteri, random_state=42, **kwargs)
        a.fit(Xtr, ytr)
        puntuacions.append(a.score(Xte, yte))
    return np.mean(puntuacions), np.std(puntuacions)


files = []
for nom, Xd, yd in (("Iris", X, y), ("Wine", X_vi, y_vi)):
    for limit in ({"max_depth": 3}, {}):
        etiqueta = "max_depth=3" if limit else "sense límit"
        mg, sg = exactitud_mitjana(Xd, yd, "gini", **limit)
        me, se = exactitud_mitjana(Xd, yd, "entropy", **limit)
        files.append({
            "dataset": nom, "profunditat": etiqueta,
            "gini": f"{mg:.4f} ± {sg:.4f}",
            "entropy": f"{me:.4f} ± {se:.4f}",
            "diferència": f"{abs(mg - me):.4f}",
        })

pd.DataFrame(files)
'''))

A(md(r"""
Aquí es veu en quin sentit són «gairebé iguals», i el sentit és aquest: **en exactitud**,
malgrat que els arbres de Wine no s'assemblin gens.

- A **Iris** la diferència és de **0,0017** (amb `max_depth=3`) i **0,0022** (sense
  límit). Són dues dècimes de punt percentual: els dos criteris són indistingibles.
- A **Wine** l'entropia guanya per **0,0222** i **0,0167**, és a dir, entre un punt i
  mig i dos punts i mig. No és zero.

Ara, comparem-ho amb la columna de la desviació típica, que és el que varia l'exactitud
només per canviar quines files cauen a l'examen: **0,031** a Iris i **0,040-0,049** a
Wine. La diferència entre criteris és, en tots quatre casos, **més petita que el soroll
de la partició**. Amb 40 particions no en podem concloure que l'entropia sigui millor a
Wine: el que podem concloure és que si hi ha un efecte, és petit.

La conclusió pràctica és que triar `criterion` és una de les decisions menys importants
que prendreu sobre un arbre. `max_depth`, `min_samples_leaf` o passar a un bosc mouen la
exactitud molt més que això. I la conclusió teòrica és la que interessa en aquest
quadern: dues fórmules amb els mateixos zeros, el mateix màxim i la mateixa concavitat
mesuren **essencialment la mateixa cosa**, encara que els arbres que en surtin es vegin
diferents.
"""))

# ---------------------------------------------------------------- 4 guany
A(md(r"""
## 4. El guany d'informació

Al quadern d'arbres vau calcular el guany amb Gini. La versió amb entropia té el
mateix esquelet i un nom propi: **guany d'informació** (*information gain*). Per a un
node pare amb $n$ mostres que es parteix en fills amb $n_j$ mostres cadascun:

$$IG \;=\; H(\text{pare}) \;-\; \sum_j \frac{n_j}{n}\, H(\text{fill}_j)$$

La lectura en bits és literal i val la pena aturar-s'hi: $H(\text{pare})$ és quants
bits d'incertesa tenim sobre la classe d'una flor abans de conèixer el resultat del
tall, el segon terme és quants n'hi queden després, i $IG$ és **quants bits
d'informació sobre la classe ens ha donat el tall**. El terme $\sum_j \frac{n_j}{n}
H(\text{fill}_j)$ té nom propi, **entropia condicional** $H(Y \mid \text{tall})$, i
llavors $IG = H(Y) - H(Y \mid \text{tall})$.

Aquesta mateixa quantitat, quan les dues coses són variables aleatòries qualssevol, es
diu **informació mútua**, i la retrobarem a la secció 8.

Implementem-ho i recorrem tots els talls possibles de `petal_llarg`, com vau fer amb
Gini.
"""))

A(code(r'''
def guany_informacio(columna, y, llindar):
    """IG en bits de partir y pel tall columna <= llindar."""
    columna = np.asarray(columna, dtype=float)
    y = np.asarray(y)
    esq = columna <= llindar
    n = len(y)
    n_esq, n_dre = int(esq.sum()), int((~esq).sum())
    if n_esq == 0 or n_dre == 0:
        return 0.0
    condicional = (n_esq / n) * entropia_etiquetes(y[esq]) \
                + (n_dre / n) * entropia_etiquetes(y[~esq])
    return entropia_etiquetes(y) - condicional


def llindars_candidats(columna):
    """Punts mitjos entre valors consecutius que apareixen a les dades."""
    valors = np.unique(np.asarray(columna, dtype=float))
    return (valors[:-1] + valors[1:]) / 2


col = X["petal_llarg"].to_numpy()
llindars = llindars_candidats(col)
guanys = np.array([guany_informacio(col, y, t) for t in llindars])

i_max = int(np.argmax(guanys))
millor_llindar = llindars[i_max]
millor_guany = guanys[i_max]

print(f"H(pare) sobre les 150 flors = {entropia_etiquetes(y):.4f} bits")
print(f"log2(3)                     = {np.log2(3):.4f} bits")
print(f"Llindars provats            = {len(llindars)}")
print(f"Millor llindar              = {millor_llindar:.4f}")
print(f"Guany d'informació màxim    = {millor_guany:.4f} bits")
'''))

A(code(r'''
plt.figure(figsize=(8, 5))
plt.plot(llindars, guanys, color="tab:blue")
plt.axvline(millor_llindar, color="tab:red", linestyle="--",
            label=f"màxim a {millor_llindar:.2f} ({millor_guany:.3f} bits)")
plt.xlabel("Llindar de tall sobre petal_llarg (cm)")
plt.ylabel("Guany d'informació (bits)")
plt.title("Guany d'informació de cada llindar possible, columna petal_llarg")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
La corba té la mateixa forma que la del guany de Gini del quadern d'arbres: un replà
ample entre 2 i 2,5 cm i baixades als dos costats. La diferència és l'escala de
l'eix vertical, que ara està en bits. Ara comprovem que el llindar que troba el nostre
codi és el que tria `DecisionTreeClassifier`.
"""))

A(code(r'''
arbre_ig = DecisionTreeClassifier(max_depth=1, criterion="entropy", random_state=42)
arbre_ig.fit(X, y)

columna_sk = X.columns[arbre_ig.tree_.feature[0]]
llindar_sk = float(arbre_ig.tree_.threshold[0])

print(f"el nostre càlcul : petal_llarg <= {millor_llindar:.4f}")
print(f"scikit-learn     : {columna_sk} <= {llindar_sk:.4f}")
print("coincideixen:", np.isclose(millor_llindar, llindar_sk))
print()

# en quina base calcula el logaritme scikit-learn? ho podem llegir de la impuresa
# que desa a l'arrel, que ha de ser H de les 150 flors senceres
impuresa_arrel = float(arbre_ig.tree_.impurity[0])
print(f"impuresa de l'arrel segons sklearn = {impuresa_arrel:.12f}")
print(f"log2(3)                            = {np.log2(3):.12f}")
print(f"ln(3)                              = {np.log(3):.12f}")
print("sklearn fa servir base 2:", np.isclose(impuresa_arrel, np.log2(3)))
'''))

A(md(r"""
Coincideix, i de passada hem comprovat en quina base treballa scikit-learn sense obrir-ne
el codi font: `tree_.impurity[0]` guarda la impuresa de l'arrel, que és $H$ de les 150
flors senceres, i val 1,584962…, que és $\log_2 3$ i no $\ln 3$. Base 2, igual que
nosaltres.

Però tant se val, i això és el detall que importa de debò. El llindar
que surt del `argmax` **no depèn de la base del logaritme**, perquè canviar de base
multiplica tota la corba de guanys per una constant positiva ($\log_b x =
\log_2 x / \log_2 b$) i una constant positiva no mou l'`argmax`. Si implementéssiu tot
el quadern amb `np.log` en lloc de `np.log2` triaríeu exactament els mateixos talls,
i els números sortirien en *nats* en lloc de bits.
"""))

# ---------------------------------------------------------------- 5 gain ratio
A(md(r"""
## 5. El problema del guany d'informació, i la ràtio de guany

El guany d'informació té un defecte greu i ben conegut: **premia les columnes amb
molts valors diferents**, encara que no signifiquin res. Vegem-ho amb el cas més
incòmode possible.

Afegim a Iris una columna d'identificadors únics: 0, 1, 2, …, 149. És un número de
fitxa, no té cap relació causal amb l'espècie de la flor. Ara, per mesurar el defecte
en la seva forma pura, hem de fer servir la formulació original d'ID3: un tall que
crea **un fill per cada valor diferent** de la columna (una partició multivia), no un
tall binari. Amb la columna d'identificadors, cada fill conté exactament una flor, i
una flor sola sempre és un grup pur: $H = 0$. L'entropia condicional és 0 i el guany
és el màxim possible, $H(Y) = \log_2 3$ bits.
"""))

A(code(r'''
def guany_multivia(columna, y):
    """IG d'un tall que crea un fill per cada valor diferent de la columna (ID3)."""
    columna = np.asarray(columna)
    y = np.asarray(y)
    n = len(y)
    condicional = 0.0
    for v in np.unique(columna):
        fill = y[columna == v]
        condicional += (len(fill) / n) * entropia_etiquetes(fill)
    return entropia_etiquetes(y) - condicional


def informacio_del_tall(columna):
    """Split information: entropia de la mida dels fills. SI = -sum (nj/n) log2(nj/n)."""
    _, comptes = np.unique(np.asarray(columna), return_counts=True)
    return entropia(comptes / comptes.sum())


X_amb_id = X.copy()
X_amb_id["id_fitxa"] = np.arange(len(X_amb_id))

resum = []
for c in X_amb_id.columns:
    col_c = X_amb_id[c].to_numpy()
    ig = guany_multivia(col_c, y)
    si = informacio_del_tall(col_c)
    resum.append({
        "columna": c,
        "valors diferents": len(np.unique(col_c)),
        "IG multivia (bits)": round(ig, 4),
        "split info (bits)": round(si, 4),
        "ràtio de guany": round(ig / si, 4) if si > 0 else np.nan,
    })

taula_ig = pd.DataFrame(resum).sort_values("IG multivia (bits)", ascending=False)
print("H(especie) =", round(entropia_etiquetes(y), 4), "bits  (= log2(3))")
print()
print(taula_ig.to_string(index=False))
'''))

A(md(r"""
La columna d'identificadors guanya per davant de tot: **1,585 bits**, que és tota
l'entropia de l'etiqueta, i per tant l'entropia condicional és exactament 0. Els pètals,
que són les columnes que de debò diuen alguna cosa sobre l'espècie, es queden a
**1,446** (`petal_llarg`) i **1,436** (`petal_ample`). Un algorisme que triï per guany
d'informació tria `id_fitxa`, construeix un arbre amb 150 fulles d'una flor cadascuna,
encerta el 100 % de l'entrenament i **no serveix per a res**: davant d'una flor nova
amb identificador 150, l'arbre no té cap branca on posar-la.

**Aquesta és una fuita d'informació**, del mateix tipus que vau treballar a
`EX_05_dades_brutes`. La columna funciona en el laboratori per un motiu que no té res a
veure amb el fenomen que voleu modelar: en aquest cas, perquè el dataset Iris ve ordenat
per espècie i l'identificador codifica aquest ordre. La manera de detectar-ho no és
mirar l'exactitud (que és perfecta) sinó preguntar-se **d'on surt la columna**.

### La ràtio de guany

La correcció clàssica de Quinlan a C4.5 és dividir el guany per una mesura de com de
fragmentada queda la partició. Aquesta mesura es diu **informació del tall** (*split
information*) i és l'entropia de les **mides dels fills**, no de les classes:

$$SI = -\sum_j \frac{n_j}{n}\log_2 \frac{n_j}{n}
\qquad\qquad
GR = \frac{IG}{SI}$$

Amb 150 fills d'una mostra cadascun, $SI = \log_2 150 = 7{,}229$ bits: la partició és
caríssima en termes de fragmentació. Dividir-hi el guany enfonsa la columna
d'identificadors. Mirem la mateixa taula ordenada per ràtio de guany.
"""))

A(code(r'''
print(taula_ig.sort_values("ràtio de guany", ascending=False).to_string(index=False))
'''))

A(md(r"""
Amb la ràtio de guany els dos pètals passen al davant (0,3546 i 0,2873) i `id_fitxa`
cau a 0,2193. Fixeu-vos que no cau a l'últim lloc: els dos sèpals, que són columnes
legítimes però mediocres, queden encara més avall. La ràtio de guany no és perfecta (es dispara quan $SI$ és molt petit, i C4.5 hi posa
salvaguardes que aquí ens saltem), però la idea és la correcta: el guany d'informació
en brut no té en compte el preu de fragmentar les dades.

### Com s'ho fa scikit-learn

`DecisionTreeClassifier` no implementa la ràtio de guany, i no li fa falta de la
mateixa manera: fa servir **només talls binaris** sobre columnes numèriques. Un tall
binari sempre crea 2 fills, i per tant el nombre de valors diferents de la columna no
infla mecànicament el guany. Comparem les dues formulacions sobre la mateixa columna.
"""))

A(code(r'''
def millor_guany_binari(columna, y):
    """Millor IG entre tots els talls binaris possibles de la columna."""
    ts = llindars_candidats(columna)
    if len(ts) == 0:
        return 0.0, np.nan
    g = np.array([guany_informacio(columna, y, t) for t in ts])
    k = int(np.argmax(g))
    return float(g[k]), float(ts[k])


for c in ("id_fitxa", "petal_llarg", "petal_ample", "sepal_ample"):
    col_c = X_amb_id[c].to_numpy(dtype=float)
    g_bin, t_bin = millor_guany_binari(col_c, y)
    print(f"{c:13s} IG binari = {g_bin:.4f} bits (tall <= {t_bin:7.3f})   "
          f"IG multivia = {guany_multivia(col_c, y):.4f} bits")
'''))

A(md(r"""
Amb talls binaris el guany de `id_fitxa` baixa d'1,585 a 0,9183 bits i ja no domina:
**empata** amb els dos pètals, que donen exactament el mateix, 0,9183 bits. L'empat no
és casualitat: `id_fitxa <= 49.5` separa les 50 setosa de les 100 restants, i
`petal_llarg <= 2.45` fa exactament la mateixa partició, perquè el dataset ve ordenat per
espècie. Dos talls que produeixen els mateixos dos grups tenen per força el mateix guany.

L'arbre binari, doncs, no cau en la trampa de la **cardinalitat**, però **sí que cau en
la fuita**. Vegem què passa si li deixem la columna i el deixem créixer.
"""))

A(code(r'''
Xtr, Xte, ytr, yte = train_test_split(
    X_amb_id, y, test_size=0.3, random_state=42, stratify=y)

arbre_fuita = DecisionTreeClassifier(criterion="entropy", random_state=42)
arbre_fuita.fit(Xtr, ytr)

importancies = pd.Series(arbre_fuita.feature_importances_,
                         index=X_amb_id.columns).sort_values(ascending=False)
print("exactitud d'examen amb la columna id_fitxa:",
      f"{arbre_fuita.score(Xte, yte):.4f}")
print("arrel:", X_amb_id.columns[arbre_fuita.tree_.feature[0]],
      "<=", round(float(arbre_fuita.tree_.threshold[0]), 3))
print()
print("importància de cada columna:")
print(importancies.round(4).to_string())
'''))

A(md(r"""
Llegiu bé el resultat, perquè no és el que es podria esperar. L'arbre **no** parteix per
`id_fitxa` a l'arrel: hi posa `petal_ample <= 0.7`, que empata amb el tall de
l'identificador i guanya el desempat. Però a partir del segon nivell sí que fa servir
`id_fitxa`, i li acaba donant el **42 %** de la importància total, repartint-se-la amb
`petal_ample`. Les altres tres columnes es queden a zero: l'arbre les ha descartat totes
a favor del número de fitxa.

I l'exactitud d'examen és del **100 %**. Aquí hi ha el punt de la secció: la fuita no
empitjora l'exactitud, la **millora**. El `train_test_split` reparteix files del mateix
dataset ordenat, així que l'examen conté identificadors intercalats amb els
d'entrenament i confirma la fuita en lloc de delatar-la. Cap mètrica d'aquest quadern us
avisarà de res. El que us ha d'avisar és saber **d'on surt la columna**: davant d'una
flor recollida demà, l'identificador serà un número nou i no dirà absolutament res de
l'espècie.
"""))

# ---------------------------------------------------------------- 6 KL
A(md(r"""
## 6. Divergència de Kullback-Leibler i entropia creuada

Fins ara hem mesurat la incertesa d'**una** distribució. Ara en necessitem dues: la
distribució **real** $p$ i la que el nostre model **creu** que és certa, $q$. Aquesta
és la situació de qualsevol classificador probabilístic.

Dues definicions. L'**entropia creuada**:

$$H(p, q) = -\sum_i p_i \log_2 q_i$$

Compareu-la amb l'entropia: $H(p) = -\sum_i p_i \log_2 p_i$. L'única diferència és que
els pesos de la mitjana venen de $p$ (el món real) i les sorpreses de $q$ (el que creu
el model). Llegit com a longitud de codi: és la mitjana de bits que gastem si
dissenyem el codi pensant que la distribució és $q$ quan de debò és $p$.

I la **divergència de Kullback-Leibler**:

$$D_{KL}(p \,\|\, q) = \sum_i p_i \log_2 \frac{p_i}{q_i}$$

que és el **sobrecost** d'aquest error. Que sigui exactament el sobrecost es veu
separant el logaritme del quocient en una resta:

$$D_{KL}(p\|q) = \sum_i p_i \log_2 p_i - \sum_i p_i \log_2 q_i = -H(p) + H(p,q)$$

i reordenant queda la relació que ho lliga tot:

$$\boxed{\;H(p,q) = H(p) + D_{KL}(p\,\|\,q)\;}$$

En paraules: **el que gastes = el mínim inevitable + el que perds per equivocar-te**.
El primer terme, $H(p)$, no depèn del model: és la incertesa del món. El segon sí. I
aquí hi ha la clau de tot el que ve després: **minimitzar l'entropia creuada respecte
al model és exactament el mateix que minimitzar la divergència KL**, perquè els dos es
diferencien en una constant que el model no pot tocar.

Comprovem la identitat amb distribucions concretes.
"""))

A(code(r'''
def entropia_creuada(p, q):
    """H(p, q) = -sum p_i log2(q_i), en bits."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = p > 0                      # els termes amb p_i = 0 no compten (0*log q = 0)
    return float(-np.sum(p[m] * np.log2(q[m])))


def kl(p, q):
    """D_KL(p || q) = sum p_i log2(p_i / q_i), en bits."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = p > 0
    return float(np.sum(p[m] * np.log2(p[m] / q[m])))


p1 = np.array([0.70, 0.20, 0.10])
q1 = np.array([0.50, 0.30, 0.20])

print("p =", p1)
print("q =", q1)
print()
print(f"H(p)            = {entropia(p1):.6f} bits")
print(f"D_KL(p || q)    = {kl(p1, q1):.6f} bits")
print(f"H(p) + D_KL     = {entropia(p1) + kl(p1, q1):.6f} bits")
print(f"H(p, q) directe = {entropia_creuada(p1, q1):.6f} bits")
print()
print("identitat verificada:",
      np.isclose(entropia_creuada(p1, q1), entropia(p1) + kl(p1, q1)))
'''))

A(md(r"""
En un dibuix: la barra de l'entropia creuada fa exactament la mateixa alçada que la pila
de $H(p)$ (el mínim inevitable) i $D_{KL}$ (el que es perd per creure $q$).
"""))

A(code(r'''
fig, ax = plt.subplots(figsize=(7, 4.8))
ax.bar(0, entropia_creuada(p1, q1), width=0.55, color="tab:purple", label="H(p, q)")
ax.bar(1, entropia(p1), width=0.55, color="tab:blue", label="H(p): el mínim inevitable")
ax.bar(1, kl(p1, q1), bottom=entropia(p1), width=0.55, color="tab:red",
       label="D_KL(p || q): el sobrecost del model")
for x, alcada in [(0, entropia_creuada(p1, q1)), (1, entropia(p1) + kl(p1, q1))]:
    ax.text(x, alcada + 0.03, f"{alcada:.4f} bits", ha="center")
ax.set_xticks([0, 1], ["entropia creuada", "H(p) + D_KL"])
ax.set_ylim(0, 1.75)
ax.set_ylabel("bits")
ax.set_title("p = (0,7; 0,2; 0,1) i q = (0,5; 0,3; 0,2)")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3, axis="y")
plt.show()
'''))

A(md(r"""
### $D_{KL}$ és 0 si i només si les distribucions són iguals, i positiva sempre

Aquesta propietat es diu desigualtat de Gibbs i es demostra amb la concavitat del
logaritme (aquí ens saltem la demostració i la comprovem numèricament). Generem 5.000
parells de distribucions a l'atzar amb el simplex de Dirichlet i mirem el mínim de tots
els $D_{KL}$.
"""))

A(code(r'''
# D_KL(p || p) = 0 per a qualsevol p
for _ in range(3):
    p_r = np.random.dirichlet(np.ones(5))
    print(f"D_KL(p || p) = {kl(p_r, p_r):.2e}")

print()
# 5000 parells a l'atzar: cap D_KL ha de ser negatiu
n_proves = 5000
divergencies = np.empty(n_proves)
for i in range(n_proves):
    pa = np.random.dirichlet(np.ones(4))
    qa = np.random.dirichlet(np.ones(4))
    divergencies[i] = kl(pa, qa)

print(f"{n_proves} parells a l'atzar:")
print(f"  mínim  D_KL = {divergencies.min():.6f}")
print(f"  mitjana D_KL = {divergencies.mean():.4f}")
print(f"  màxim  D_KL = {divergencies.max():.4f}")
print(f"  algun negatiu? {bool((divergencies < 0).any())}")
'''))

A(md(r"""
Cap negatiu. El mínim és positiu i petit, i correspon al parell que per casualitat ha
sortit més semblant. La comprovació no és una demostració, però si la desigualtat fos
falsa, 5.000 proves l'haurien trencat.

### No és simètrica, i per tant no és una distància

$D_{KL}(p\|q) \ne D_{KL}(q\|p)$. Malgrat el costum d'anomenar-la «distància», no ho és:
una distància ha de ser simètrica, i aquesta no ho és. Per això el nom correcte és
*divergència*.
"""))

A(code(r'''
p2 = np.array([0.90, 0.10])
q2 = np.array([0.50, 0.50])

print("p =", p2, "  q =", q2)
print(f"D_KL(p || q) = {kl(p2, q2):.6f} bits")
print(f"D_KL(q || p) = {kl(q2, p2):.6f} bits")
print(f"diferència   = {abs(kl(p2, q2) - kl(q2, p2)):.6f} bits")
print("simètrica:", np.isclose(kl(p2, q2), kl(q2, p2)))
'''))

A(md(r"""
Els dos números són diferents, i la asimetria té un sentit concret: $D_{KL}(p\|q)$
pondera els errors amb $p$, o sigui que **castiga que $q$ doni poca probabilitat allà
on $p$ en té molta**. Al límit, si $q_i = 0$ en un lloc on $p_i > 0$, la divergència es
dispara a infinit. Al revés no: que $q$ reparteixi probabilitat on $p$ no en té surt
més barat. Això explica per què, en entrenar un classificador, l'ordre importa: es
minimitza sempre $D_{KL}(\text{real} \,\|\, \text{model})$, que és el que penalitza
duríssimament assignar probabilitat gairebé zero a la classe certa.
"""))

# ---------------------------------------------------------------- 7 la tesi
A(md(r"""
## 7. La tesi: la log-loss **és** l'entropia creuada

Aquí tanquem el quadern. Prenem un problema de classificació binària de debò i
demostrem que la funció de pèrdua que minimitza una regressió logística és, terme a
terme, l'entropia creuada de la secció anterior.

**La construcció.** Per a cada fila $i$ del dataset tenim dues distribucions sobre les
dues classes:

- La **real**, $p^{(i)}$: sabem del cert quina és la classe, així que és un 1 a la
  classe certa i un 0 a l'altra. Si $y_i = 1$, $p^{(i)} = (0, 1)$; si $y_i = 0$,
  $p^{(i)} = (1, 0)$. Això és un *one-hot*.
- La **predita**, $q^{(i)} = (1 - \hat{y}_i,\; \hat{y}_i)$, que és el que dona
  `predict_proba`.

L'entropia creuada d'aquesta fila és $H(p^{(i)}, q^{(i)}) = -\sum_c p^{(i)}_c \log
q^{(i)}_c$. Com que $p^{(i)}$ és un one-hot, de la suma només en sobreviu **un** terme,
el de la classe certa, i els altres desapareixen pel conveni $0\log 0 = 0$:

$$H(p^{(i)}, q^{(i)}) = -\log q^{(i)}_{y_i}
= \begin{cases} -\log \hat{y}_i & \text{si } y_i = 1\\[2pt]
-\log(1 - \hat{y}_i) & \text{si } y_i = 0\end{cases}$$

Els dos casos es poden escriure en una sola línia sense `if`, aprofitant que un dels
dos factors queda multiplicat per zero:

$$H(p^{(i)}, q^{(i)}) = -\big[\, y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i) \,\big]$$

I la mitjana sobre totes les files:

$$\mathcal{L} = -\frac{1}{n}\sum_{i=1}^{n}
\big[\, y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i)\,\big]$$

Aquesta última expressió és, literalment, la **log-loss** (o *binary cross-entropy*)
que minimitza `LogisticRegression`. No s'assembla a l'entropia creuada: **és**
l'entropia creuada, amb el one-hot substituït i la suma col·lapsada.

Ho implementem dues vegades, amb noms diferents i per camins diferents, i ho comparem
amb scikit-learn. Fem servir logaritme **natural**, perquè és el que fa servir
`sklearn.metrics.log_loss`; la unitat passa de bits a *nats* i tota la resta és igual.
"""))

A(code(r'''
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss

cancer = load_breast_cancer()
Xc, yc = cancer.data, cancer.target
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(
    Xc, yc, test_size=0.3, random_state=42, stratify=yc)

model = make_pipeline(StandardScaler(),
                      LogisticRegression(max_iter=5000, random_state=42))
model.fit(Xc_tr, yc_tr)

probes = model.predict_proba(Xc_te)      # forma (n, 2): [P(classe 0), P(classe 1)]
y_hat = probes[:, 1]                     # probabilitat de la classe 1

print("files d'examen:", len(yc_te))
print("exactitud:", f"{model.score(Xc_te, yc_te):.4f}")
print("probes.shape:", probes.shape, " suma per fila:", np.unique(probes.sum(axis=1).round(10)))
'''))

A(md(r"""
Camí 1: la log-loss, escrita tal com apareix als llibres d'estadística.

Un detall imprescindible: si el model prediu exactament 0 o exactament 1 i s'equivoca,
$\log 0 = -\infty$ i la pèrdua es dispara. `sklearn.metrics.log_loss` retalla les
probabilitats a $[\varepsilon, 1-\varepsilon]$ amb $\varepsilon$ molt petit per evitar-ho.
Fem el mateix retall, amb el mateix $\varepsilon$, perquè els números siguin comparables
fins a l'últim decimal.
"""))

A(code(r'''
EPSILON = np.finfo(float).eps    # el mateix que fa servir sklearn.metrics.log_loss


def la_nostra_log_loss(y_cert, y_prob):
    """Log-loss binaria: -mitjana[ y*ln(p) + (1-y)*ln(1-p) ]."""
    y_cert = np.asarray(y_cert, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), EPSILON, 1 - EPSILON)
    perdua_per_fila = -(y_cert * np.log(p) + (1 - y_cert) * np.log(1 - p))
    return float(np.mean(perdua_per_fila))


valor_log_loss = la_nostra_log_loss(yc_te, y_hat)
print(f"la nostra log-loss      = {valor_log_loss:.12f} nats")
'''))

A(md(r"""
Camí 2: l'entropia creuada de la secció 6, sense passar per cap fórmula de log-loss.
Construïm la matriu one-hot de les etiquetes reals, la matriu de probabilitats
predites, i apliquem $-\sum_c p_c \log q_c$ fila per fila. No hi apareix cap
`y*log(p) + (1-y)*log(1-p)`: és la definició general d'entropia creuada, per a
$C$ classes.
"""))

A(code(r'''
def la_nostra_entropia_creuada(y_cert, matriu_probes, n_classes=None):
    """Mitjana de H(p_i, q_i) amb p_i one-hot de l'etiqueta certa. En nats."""
    y_cert = np.asarray(y_cert, dtype=int)
    Q = np.clip(np.asarray(matriu_probes, dtype=float), EPSILON, 1 - EPSILON)
    C = n_classes or Q.shape[1]

    P = np.zeros((len(y_cert), C))       # one-hot: 1 a la classe certa, 0 a la resta
    P[np.arange(len(y_cert)), y_cert] = 1.0

    mascara = P > 0                      # conveni 0*log(q) = 0 per als zeros del one-hot
    per_fila = np.zeros(len(y_cert))
    np.add.at(per_fila, np.where(mascara)[0], -(P[mascara] * np.log(Q[mascara])))
    return float(np.mean(per_fila))


valor_entropia_creuada = la_nostra_entropia_creuada(yc_te, probes)
valor_sklearn = log_loss(yc_te, probes)

print(f"la nostra log-loss         = {valor_log_loss:.12f}")
print(f"la nostra entropia creuada = {valor_entropia_creuada:.12f}")
print(f"sklearn.metrics.log_loss   = {valor_sklearn:.12f}")
print()
print("log-loss == entropia creuada :",
      np.isclose(valor_log_loss, valor_entropia_creuada, rtol=0, atol=1e-12))
print("entropia creuada == sklearn  :",
      np.isclose(valor_entropia_creuada, valor_sklearn, rtol=0, atol=1e-12))
print("diferència màxima            :",
      max(abs(valor_log_loss - valor_entropia_creuada),
          abs(valor_entropia_creuada - valor_sklearn)))
'''))

A(md(r"""
**Les tres xifres coincideixen.** Aquesta cel·la és la conclusió del quadern.

L'arbre de decisió mesura el desordre d'un node amb $H(p) = -\sum p_i\log p_i$ i busca
els talls que el redueixen. La regressió logística mesura el desordre de les seves
prediccions amb $H(p, q) = -\sum p_i\log q_i$ i mou els pesos per reduir-lo. La
segona fórmula és la primera amb una distribució diferent dins del logaritme. Els dos
models minimitzen entropia; el que canvia és què poden tocar per fer-la baixar: l'arbre
mou el llindar d'un tall, la logística mou un vector de pesos.

I encara hi ha un pont més. A la secció 6 hem vist que
$H(p,q) = H(p) + D_{KL}(p\|q)$, i que $H(p)$ no depèn del model. Per a un one-hot,
$H(p) = 0$ (no hi ha cap incertesa sobre l'etiqueta certa: la sabem), i per tant en
aquest cas concret

$$\mathcal{L} = \frac{1}{n}\sum_i H(p^{(i)}, q^{(i)})
= \frac{1}{n}\sum_i D_{KL}(p^{(i)} \,\|\, q^{(i)})$$

Entrenar una regressió logística és **minimitzar la divergència de Kullback-Leibler
entre el món i el model**. Comprovem-ho, perquè és una afirmació prou forta per no
deixar-la sense codi.
"""))

A(code(r'''
Q = np.clip(probes, EPSILON, 1 - EPSILON)
kl_per_fila = np.empty(len(yc_te))
H_per_fila = np.empty(len(yc_te))

for i, etiqueta in enumerate(yc_te):
    p_fila = np.zeros(2)
    p_fila[etiqueta] = 1.0
    # kl() i entropia() treballen en bits; passem a nats multiplicant per ln(2)
    kl_per_fila[i] = kl(p_fila, Q[i]) * np.log(2)
    H_per_fila[i] = entropia(p_fila) * np.log(2)

print(f"mitjana de H(p_i)          = {H_per_fila.mean():.12f} nats  (one-hot: 0)")
print(f"mitjana de D_KL(p_i || q_i) = {kl_per_fila.mean():.12f} nats")
print(f"la nostra entropia creuada  = {valor_entropia_creuada:.12f} nats")
print()
print("log-loss == KL mitjana:",
      np.isclose(kl_per_fila.mean(), valor_entropia_creuada, rtol=0, atol=1e-12))
'''))

A(md(r"""
### La tesi en un dibuix

A l'esquerra, cada punt és una fila de l'examen. A l'eix horitzontal, el seu terme de
log-loss, $-[y\ln\hat y + (1-y)\ln(1-\hat y)]$; al vertical, el seu terme d'entropia creuada
amb el one-hot, $-\sum_c p_c \ln q_c$. Tots cauen sobre la diagonal: no és que les mitjanes
coincideixin, és que **fila a fila** són el mateix número. A la dreta, d'on surten: les
dues branques de la pèrdua, $-\ln \hat y$ per a les files de classe 1 i $-\ln(1-\hat y)$ per
a les de classe 0, amb cada fila col·locada a la seva.
"""))

A(code(r'''
p_tall = np.clip(y_hat, EPSILON, 1 - EPSILON)
terme_logloss = -(yc_te * np.log(p_tall) + (1 - yc_te) * np.log(1 - p_tall))
one_hot = np.eye(2)[yc_te]
terme_creuada = -(one_hot * np.log(np.clip(probes, EPSILON, 1 - EPSILON))).sum(axis=1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ax1.loglog(terme_logloss, terme_creuada, "o", color="tab:blue", alpha=0.5, markersize=5)
lim = [terme_logloss.min() / 2, terme_logloss.max() * 2]
ax1.plot(lim, lim, color="tab:red", linestyle="--", label="diagonal: els dos valen igual")
ax1.set_xlabel("terme de log-loss de la fila (nats)")
ax1.set_ylabel("terme d'entropia creuada de la fila (nats)")
ax1.set_title(f"Fila a fila. Mitjanes: {terme_logloss.mean():.6f} i {terme_creuada.mean():.6f}")
ax1.legend(loc="upper left")
ax1.grid(alpha=0.3)

yh = np.linspace(0.001, 0.999, 500)
ax2.plot(yh, -np.log(yh), color="tab:blue", label="classe certa 1: $-\\ln \\hat{y}$")
ax2.plot(yh, -np.log(1 - yh), color="tab:red", label="classe certa 0: $-\\ln(1-\\hat{y})$")
u = yc_te == 1
ax2.scatter(y_hat[u], -np.log(p_tall[u]), color="tab:blue", edgecolor="k", s=22, zorder=3)
ax2.scatter(y_hat[~u], -np.log(1 - p_tall[~u]), color="tab:red", edgecolor="k", s=22, zorder=3)
ax2.set_ylim(0, 5)
ax2.set_xlabel("$\\hat{y}$ = probabilitat de la classe 1 segons el model")
ax2.set_ylabel("pèrdua de la fila (nats)")
ax2.set_title("Les files d'examen sobre les dues branques")
ax2.legend(loc="upper center")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
'''))

A(md(r"""
Gairebé totes les files són a prop de zero: el model hi dona molta probabilitat a la classe
certa. Les poques que pugen per les branques són les que s'equivoca, o encerta amb poca
convicció, i són les que pesen a la mitjana. Això és el que fa la log-loss i el que no fa
l'exactitud: castigar **quant** s'equivoca, no només **si** s'equivoca.
"""))

# ---------------------------------------------------------------- 8 MI
A(md(r"""
## 8. Informació mútua com a eina pràctica

A la secció 4 hem definit $IG = H(Y) - H(Y \mid \text{tall})$ per a un tall concret. Si
en lloc d'un tall hi posem una variable sencera $X$, la mateixa quantitat es diu
**informació mútua**:

$$I(X; Y) = H(Y) - H(Y \mid X)$$

És, en bits (o nats), **quanta informació sobre l'etiqueta us dona conèixer aquesta
columna**. Val 0 si i només si $X$ i $Y$ són independents, i és simètrica:
$I(X;Y) = I(Y;X)$. Es pot escriure també com una divergència KL, entre la distribució
conjunta i el producte de les marginals: $I(X;Y) = D_{KL}\big(P(X,Y) \,\|\,
P(X)P(Y)\big)$, és a dir, com de lluny està la realitat de la hipòtesi que les dues
variables no tenen res a veure.

`mutual_info_classif` de scikit-learn l'estima per a cada columna. Per a columnes
contínues l'estimació es fa amb un mètode basat en distàncies als $k$ veïns més
propers, i té un component aleatori: cal fixar `random_state` si voleu números
reproduïbles. Aquí ens saltem com funciona l'estimador i ens quedem amb què mesura, i
amb el fet que retorna **nats**, no bits.
"""))

A(code(r'''
from sklearn.feature_selection import mutual_info_classif, SelectKBest

mi_nats = mutual_info_classif(X_vi, y_vi, random_state=42)
mi_bits = mi_nats / np.log(2)

ranquing = pd.DataFrame({
    "columna": X_vi.columns,
    "I(X;Y) nats": mi_nats.round(4),
    "I(X;Y) bits": mi_bits.round(4),
}).sort_values("I(X;Y) nats", ascending=False).reset_index(drop=True)

print("H(target) de Wine =", round(entropia_etiquetes(y_vi), 4), "bits")
print("cap columna pot superar aquest valor en bits: I(X;Y) <= H(Y)")
print()
print(ranquing.to_string(index=False))
'''))

A(md(r"""
El rànquing és interpretable en bits, directament. `flavanoids` encapçala amb **0,963
bits**, contra els **1,567 bits** que té l'etiqueta de Wine: aquesta columna, sola,
resol el **61 %** de la incertesa sobre el celler. I cap columna supera $H(Y)$, com ha
de ser: una columna no pot donar més informació sobre l'etiqueta que la que l'etiqueta
té. Aquesta fita, $I(X;Y) \le H(Y)$, us serveix de comprovació de sanitat sobre
qualsevol estimació d'informació mútua que veieu.

### La connexió amb `SelectKBest`

A `EX_03_digits` vau fer servir `SelectKBest(f_classif, k=20)`. `f_classif` és un test
F d'ANOVA: mesura si les mitjanes de la columna difereixen entre classes. Això detecta
bé les relacions **lineals i monòtones** i se li escapen les que no ho són.
`mutual_info_classif` no assumeix cap forma: detecta qualsevol dependència, també les
no monòtones, al preu de ser una estimació més sorollosa i més lenta. Els dos
s'endollen a `SelectKBest` exactament igual.
"""))

A(code(r'''
from sklearn.ensemble import RandomForestClassifier

Xv_tr, Xv_te, yv_tr, yv_te = train_test_split(
    X_vi, y_vi, test_size=0.3, random_state=42, stratify=y_vi)

def puntua_mi(Xa, ya):
    return mutual_info_classif(Xa, ya, random_state=42)


for k in (1, 2, 3, 5, 8, 13):
    seleccio = SelectKBest(puntua_mi, k=k).fit(Xv_tr, yv_tr)
    triades = list(X_vi.columns[seleccio.get_support()])
    # mitjana sobre 20 particions, que una sola no distingeix res en aquest dataset
    puntuacions = []
    for llavor in range(20):
        Xa, Xb, ya, yb = train_test_split(
            X_vi[triades], y_vi, test_size=0.3, random_state=llavor, stratify=y_vi)
        bosc = RandomForestClassifier(n_estimators=200, random_state=42)
        bosc.fit(Xa, ya)
        puntuacions.append(bosc.score(Xb, yb))
    print(f"k={k:2d}  exactitud mitjana = {np.mean(puntuacions):.4f}  "
          f"± {np.std(puntuacions):.4f}   {triades if k <= 5 else ''}")
'''))

A(md(r"""
Aquesta taula diu dues coses, i cap de les dues és òbvia.

**Primera: la millor columna, sola, no serveix.** `flavanoids` és la que té més
informació mútua, però un bosc entrenat només amb ella es queda al **71,7 %**. La
informació mútua es calcula **columna a columna**, i per tant no diu res de com es
combinen: 0,963 bits és molt per a una columna sola, i encara falten 0,6 bits per cobrir
l'etiqueta.

**Segona: la informació es repeteix.** Amb 3 columnes ja hi ha **96,9 %**, amb 5 un
**97,6 %** i amb les 13 un **98,6 %**. Les 8 columnes addicionals valen **1 punt**. Això
no vol dir que siguin inútils: vol dir que el que aporten està en bona part **repetit**
en les que ja hi són. `total_phenols` i `flavanoids`, per exemple, són dues mesures de
compostos fenòlics i estan molt correlacionades; les dues tenen una $I(X;Y)$ alta, les
dues surten amunt al rànquing, i la segona gairebé no afegeix res a la primera.

Aquesta és **la limitació important del mètode**, i és estructural: `SelectKBest` puntua
cada columna contra l'etiqueta i mai dues columnes entre elles. Tractar-ho bé demana
informació mútua **condicional**, $I(X_2; Y \mid X_1)$, que mesura què aporta una columna
**donat** que ja teniu l'altra. Aquí no hi entrem.
"""))

# ---------------------------------------------------------------- exercicis
A(md(r"""
## 9. Pràctica

Quatre exercicis. Treballeu sobre el que ja hi ha en aquest quadern: `sorpresa`,
`entropia`, `entropia_etiquetes`, `gini`, `guany_informacio`, `guany_multivia`,
`informacio_del_tall`, `kl`, `entropia_creuada`, `llindars_candidats`, i les dades
`X`, `y`, `X_amb_id`, `X_vi`, `y_vi`.

Abans de cada exercici hi ha un dibuix amb **dades inventades** que ensenya la idea;
els números de debò els heu de treure vosaltres.
"""))

A(md(r"""
### Exercici 1 — L'entropia d'un dau trucat

Teniu un dau de 6 cares trucat amb aquestes probabilitats:

$$p = (0{,}5,\; 0{,}1,\; 0{,}1,\; 0{,}1,\; 0{,}1,\; 0{,}1)$$

1. Comproveu que les probabilitats sumen 1 (si no, la fórmula no vol dir res).
2. Calculeu-ne l'entropia en bits amb `entropia`.
3. Compareu-la amb l'entropia d'un dau just de 6 cares i digueu, en una frase, per què
   la del trucat és més petita.
4. Calculeu la sorpresa de cada cara amb `sorpresa` i comproveu a mà que la mitjana
   ponderada d'aquestes sorpreses (pesant cada una per la seva $p_i$) dona el mateix
   número que `entropia`. És la definició, però val la pena veure-ho.
5. Trobeu, provant valors, quina probabilitat de la primera cara fa que l'entropia
   baixi per sota d'1,5 bits, mantenint les altres cinc repartides a parts iguals.

**Com saps que ho has fet bé:** l'entropia del dau just ha de ser exactament
$\log_2 6$ (`np.log2(6)`), perquè amb $n$ cares equiprobables $H = \log_2 n$; si no et
surt, `entropia` no està ben cridada. La del trucat ha de quedar per sobre de 0 i **per
sota** de la del just: cap dau de 6 cares passa de $\log_2 6$. La mitjana ponderada de les
sorpreses ha de coincidir amb el que retorna `entropia` fins als últims decimals
(`np.isclose`); si no coincideix, no has pesat amb les $p_i$. Al punt 5, a cada valor que
provis les sis probabilitats han de sumar 1, i a partir de $1/6$ l'entropia ha de baixar
cada vegada que puges la primera: si et puja, has repartit malament la resta. El valor
que trobis és la teva resposta.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix, amb un **dau de 4 cares inventat**. A l'esquerra,
l'entropia com a àrea: amplada $p_i$, alçada la sorpresa de cada cara. A la dreta, com es
busca un llindar provant valors: l'entropia quan la primera cara s'emporta cada cop més
probabilitat i les altres tres es reparteixen la resta, i el primer valor que baixa d'1 bit.
El vostre dau té 6 cares i el llindar és 1,5 bits.
"""))

A(code(r'''
dau4_il = np.array([0.4, 0.3, 0.2, 0.1])
esq_il = np.concatenate([[0], np.cumsum(dau4_il)[:-1]])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))
ax1.bar(esq_il, sorpresa(dau4_il), width=dau4_il, align="edge", edgecolor="white",
        color=["tab:blue", "tab:orange", "tab:green", "tab:red"])
for x0, p_i in zip(esq_il, dau4_il):
    ax1.text(x0 + p_i / 2, sorpresa(p_i) + 0.08, f"p = {p_i:g}", ha="center", fontsize=9)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 3.8)
ax1.set_xlabel("amplada = $p_i$")
ax1.set_ylabel("alçada = sorpresa (bits)")
ax1.set_title(f"Dau de 4 cares inventat: àrea = H = {entropia(dau4_il):.3f} bits")
ax1.grid(alpha=0.3, axis="y")

p1_il = np.round(np.arange(0.25, 0.991, 0.01), 2)
H_il = np.array([entropia([a] + [(1 - a) / 3] * 3) for a in p1_il])
k_il = int(np.argmax(H_il < 1.0))
ax2.plot(p1_il, H_il, color="tab:blue")
ax2.axhline(1.0, color="gray", linestyle="--", label="llindar d'1 bit")
ax2.scatter([p1_il[k_il]], [H_il[k_il]], color="tab:red", s=60, zorder=3,
            label=f"primer per sota: p = {p1_il[k_il]:.2f}")
ax2.set_xlabel("probabilitat de la primera cara")
ax2.set_ylabel("H (bits)")
ax2.set_title("Dau de 4 cares: l'entropia baixa quan una cara domina")
ax2.legend()
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
'''))

A(code(r'''
# TODO 1: definiu p_trucat i comproveu que suma 1

# TODO 2: entropia en bits del dau trucat

# TODO 3: entropia del dau just de 6 cares, i comparacio

# TODO 4: sorpresa de cada cara, i mitjana ponderada per p_i
#         pista: np.sum(p * sorpresa(p)) ha de donar el mateix que entropia(p)

# TODO 5: recorreu p_primera de 0.2 a 0.95 repartint (1 - p_primera) entre les
#         altres 5 cares, i trobeu on H baixa de 1.5 bits
'''))

A(md(r"""
### Exercici 2 — La ràtio de guany completa

A la secció 5 la ràtio de guany ja està calculada dins de la taula. Ara escriviu-la
vosaltres com una funció, i feu-la servir per mesurar la columna d'identificadors.

1. Escriviu `ratio_de_guany(columna, y)` que retorni $GR = IG / SI$, fent servir
   `guany_multivia` i `informacio_del_tall`. Tracteu el cas $SI = 0$ (passa quan la
   columna té un únic valor diferent: llavors no hi ha partició i la ràtio no està
   definida); retorneu `np.nan`.
2. Apliqueu-la a totes les columnes de `X_amb_id` i imprimiu el rànquing.
3. Digueu quina columna guanya amb $IG$ i quina amb $GR$, i quina de les dues
   ordenacions us sembla útil.
4. Afegiu a `X_amb_id` una segona columna inventada, `id_parell = id_fitxa // 2`, que
   té 75 valors diferents en lloc de 150. Mesureu-li l'$IG$ i la $GR$. Expliqueu per què
   l'$IG$ surt com surt: penseu què conté cada fill de 2 flors, tenint en compte que
   Iris ve ordenat per espècie.

**Com saps que ho has fet bé:** per a les columnes de `X_amb_id`, la teva funció ha de
reproduir, columna per columna, la columna «ràtio de guany» de `taula_ig` de la secció 5
(fins al quart decimal, que és com està arrodonida). Si no hi coincideix, `ratio_de_guany`
no crida bé `guany_multivia` o `informacio_del_tall`. Per a `id_parell` no hi ha taula,
però sí dues comprovacions de cap: com que té 75 valors amb 2 flors cadascun, el seu $SI$ ha
de ser exactament $\log_2 75$ (`np.log2(75)`), i el seu $IG$ no pot passar de $H(Y)$
d'Iris, $\log_2 3$. Quin $IG$ li surt, per què, i on queda al rànquing, és la teva
resposta.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix: columnes **inventades de soroll pur**, sense cap
relació amb una etiqueta també inventada, amb cada cop més valors diferents. El guany
d'informació multivia puja tot sol cap a $H(Y)$ només perquè hi ha més fills; la
informació del tall també puja, com $\log_2$ del nombre de valors. La ràtio fa servir
precisament que la segona creix més de pressa.
"""))

A(code(r'''
rng = np.random.default_rng(8)
y_il = rng.integers(0, 3, 150)
ks_il = [2, 3, 5, 10, 20, 50, 100, 150]
ig_il, si_il = [], []
for k in ks_il:
    col_il = rng.permutation(np.arange(150) % k)     # k valors, cap relacio amb y_il
    ig_il.append(guany_multivia(col_il, y_il))
    si_il.append(informacio_del_tall(col_il))

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot(ks_il, ig_il, marker="o", color="tab:blue", label="IG multivia (columna de soroll)")
ax.plot(ks_il, si_il, marker="s", color="tab:orange", label="informació del tall SI")
ax.axhline(entropia_etiquetes(y_il), color="gray", linestyle="--", label="H(Y) de l'etiqueta inventada")
ax.set_xscale("log")
ax.set_xticks(ks_il, [str(k) for k in ks_il])
ax.set_xlabel("valors diferents de la columna (escala logarítmica)")
ax.set_ylabel("bits")
ax.set_title("Dades inventades: el guany creix amb els valors, encara que sigui soroll")
ax.legend()
ax.grid(alpha=0.3)
plt.show()
'''))

A(code(r'''
def ratio_de_guany(columna, y):
    # TODO: IG / SI, fent servir guany_multivia i informacio_del_tall
    # retorneu np.nan si SI == 0
    pass


# TODO: apliqueu-la a totes les columnes de X_amb_id i imprimiu el ranquing

# TODO: afegiu id_parell = id_fitxa // 2 i mesureu-li IG i GR
'''))

A(md(r"""
### Exercici 3 — L'asimetria de la KL, amb números

Preneu aquestes dues distribucions sobre tres resultats:

$$p = (0{,}8,\; 0{,}15,\; 0{,}05) \qquad\qquad q = (0{,}2,\; 0{,}4,\; 0{,}4)$$

1. Calculeu $D_{KL}(p\|q)$ i $D_{KL}(q\|p)$ amb `kl` i comproveu que són diferents.
2. Verifiqueu la identitat $H(p,q) = H(p) + D_{KL}(p\|q)$ per a aquest parell, i també
   la versió amb els papers intercanviats: $H(q,p) = H(q) + D_{KL}(q\|p)$.
3. Expliqueu en dues frases **quina de les dues divergències és més gran i per què**,
   mirant on cada distribució posa la seva massa i on l'altra en posa poca.
4. Ara feu $q_3 \to 0$: construïu $q_\epsilon = (0{,}2,\; 0{,}8-\epsilon,\; \epsilon)$
   per a $\epsilon = 10^{-1}, 10^{-3}, 10^{-6}, 10^{-12}$ i mireu què li passa a
   $D_{KL}(p\|q_\epsilon)$. Expliqueu per què creix sense límit, i relacioneu-ho amb el
   retall a $[\varepsilon, 1-\varepsilon]$ que hem fet a la secció 7.

**Com saps que ho has fet bé:** les dues divergències han de ser positives (la KL mai
és negativa) i diferents entre elles; si et surten iguals, has passat les dues
distribucions en el mateix ordre. Pots validar `kl` amb scipy:
`scipy.stats.entropy(p, q, base=2)` calcula exactament $D_{KL}(p\|q)$. Les identitats del
punt 2 són la comprovació forta: calcula els dos costats per separat i han de coincidir
fins als últims decimals (`np.isclose`). Al punt 4, mira la diferència entre cada
$D_{KL}(p\|q_\epsilon)$ i l'anterior: com que els $\epsilon$ es divideixen sempre per mil,
aquestes diferències s'han d'anar acostant a un valor fix. Quin és i d'on surt forma part
de l'explicació que et demanem.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix, amb dues distribucions **inventades** (no són les
de l'exercici). A l'esquerra, on posa la massa cadascuna. A la dreta, el **terme** de cada
resultat dins de cada divergència, $p_i\log_2(p_i/q_i)$ i $q_i\log_2(q_i/p_i)$: n'hi ha de
negatius, però la suma (a la llegenda) mai no ho és, i les dues sumes no coincideixen.
"""))

A(code(r'''
pa_il = np.array([0.7, 0.25, 0.05])
qa_il = np.array([0.3, 0.3, 0.4])
x_il = np.arange(3)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))
ax1.bar(x_il - 0.2, pa_il, width=0.4, color="tab:blue", label="p")
ax1.bar(x_il + 0.2, qa_il, width=0.4, color="tab:orange", label="q")
ax1.set_xticks(x_il, ["resultat 1", "resultat 2", "resultat 3"])
ax1.set_ylabel("probabilitat")
ax1.set_title("Dues distribucions inventades")
ax1.legend()
ax1.grid(alpha=0.3, axis="y")

terme_pq = pa_il * np.log2(pa_il / qa_il)
terme_qp = qa_il * np.log2(qa_il / pa_il)
ax2.bar(x_il - 0.2, terme_pq, width=0.4, color="tab:blue",
        label=f"terme de D_KL(p || q), suma = {terme_pq.sum():.3f}")
ax2.bar(x_il + 0.2, terme_qp, width=0.4, color="tab:orange",
        label=f"terme de D_KL(q || p), suma = {terme_qp.sum():.3f}")
ax2.axhline(0, color="black", linewidth=0.8)
ax2.set_xticks(x_il, ["resultat 1", "resultat 2", "resultat 3"])
ax2.set_ylabel("bits")
ax2.set_title("Cada resultat aporta a la divergència")
ax2.set_ylim(-0.5, 1.65)
ax2.legend(loc="upper left", fontsize=9)
ax2.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.show()
'''))

A(code(r'''
# TODO 1: definiu p3 i q3, i calculeu kl(p3, q3) i kl(q3, p3)

# TODO 2: comproveu H(p,q) = H(p) + D_KL(p||q) i la versio amb els papers canviats

# TODO 3: la resposta va en una cel.la de text, no en codi

# TODO 4: construiu q_epsilon per a diversos epsilon i mireu D_KL(p || q_epsilon)
'''))

A(md(r"""
### Exercici 4 — L'entropia de l'etiqueta i el desequilibri de classes

Carregueu `load_breast_cancer` (ja el teniu a `cancer`, `yc`).

1. Compteu quantes mostres hi ha de cada classe i calculeu-ne les proporcions.
2. Calculeu $H(Y)$ en bits amb `entropia_etiquetes`.
3. Compareu-la amb 1 bit, que és el màxim per a dues classes, i digueu quin percentatge
   del màxim és. Aquest percentatge és una manera de quantificar el desequilibri.
4. Calculeu quina exactitud obtindria un classificador que sempre digués la classe
   majoritària, sense mirar cap columna. Relacioneu els dos números: com més baixa és
   $H(Y)$, més alta és aquesta exactitud trivial, i menys informativa és l'exactitud com
   a mètrica.
5. Repetiu els punts 1-4 amb `y_vi` (Wine, 3 classes) i amb `y` (Iris, 3 classes). A
   Iris les tres classes estan perfectament equilibrades: comproveu que $H(Y)$ dona
   exactament $\log_2 3$.

**Com saps que ho has fet bé:** els recomptes de cada dataset han de sumar el total de
files (569 a càncer, 178 a Wine, 150 a Iris) i les proporcions, 1. Cap $H(Y)$ de dues
classes pot passar d'1 bit, ni cap de tres classes de $\log_2 3$. L'exactitud del
classificador trivial ha de ser exactament la proporció de la classe majoritària, i la
pots contrastar amb un `DummyClassifier(strategy="most_frequent")` de `sklearn.dummy`
entrenat i avaluat sobre les mateixes etiquetes: han de coincidir. A Iris, $H(Y)$ ha de
donar `np.log2(3)` i el trivial, $1/3$. Els números de càncer i de Wine, i la relació
entre tots dos, són la teva resposta.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix. A l'esquerra, per a dues classes: quan una classe
domina, $H(Y)$ baixa i l'exactitud del classificador que sempre diu la majoritària puja.
A la dreta, un conjunt **inventat** amb un 95 % d'una classe i un 5 % de l'altra: el
classificador trivial té una exactitud altíssima i no troba **cap** cas de la classe
petita. Per això l'exactitud sola enganya. Al costat hi ha la **precisió** (*precision*)
i la sensibilitat de la classe petita, que la miren a ella sola (les tens a `EX_00`, §7).
"""))

A(code(r'''
from sklearn.metrics import accuracy_score, precision_score, recall_score

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
p_maj = np.linspace(0.5, 1, 101)
ax1.plot(p_maj, [entropia([a, 1 - a]) for a in p_maj], color="tab:blue", label="H(Y) (bits)")
ax1.plot(p_maj, p_maj, color="tab:orange", label="exactitud de dir sempre la majoritària")
ax1.set_xlabel("proporció de la classe majoritària")
ax1.set_title("Dues classes: menys entropia, més exactitud trivial")
ax1.legend()
ax1.grid(alpha=0.3)

y_il = np.array([1] * 10 + [0] * 190)                      # 5 % de la classe petita (1)
trivial_il = np.zeros(200, dtype=int)                      # sempre la majoritaria
model_il = np.array([1] * 7 + [0] * 3 + [1] * 8 + [0] * 182)   # un model inventat
noms_metriques = ["exactitud", "precisió (classe 1)", "sensibilitat (classe 1)"]
x_il = np.arange(3)
for desp, (nom, pred, color) in zip([-0.2, 0.2], [("sempre la majoritària", trivial_il, "tab:gray"),
                                                 ("un model inventat", model_il, "tab:green")]):
    valors = [accuracy_score(y_il, pred),
              precision_score(y_il, pred, zero_division=0),   # sense cap 1 predit: 0
              recall_score(y_il, pred)]
    ax2.bar(x_il + desp, valors, width=0.4, color=color, label=nom)
    for xx, v in zip(x_il + desp, valors):
        ax2.text(xx, v + 0.02, f"{v:.0%}", ha="center", fontsize=9)
ax2.set_xticks(x_il, noms_metriques)
ax2.set_ylim(0, 1.12)
ax2.set_title("Dades inventades 95/5: l'exactitud sola enganya")
ax2.legend(loc="upper right")
ax2.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.show()
'''))

A(code(r'''
# TODO 1: comptes i proporcions de les classes de yc
#         pista: np.unique(yc, return_counts=True)

# TODO 2: H(Y) en bits

# TODO 3: percentatge respecte a 1 bit

# TODO 4: exactitud del classificador que sempre diu la classe majoritaria

# TODO 5: el mateix amb y_vi i amb y, comparant contra log2(3)
'''))

# ---------------------------------------------------------------- resum
A(md(r"""
## Resum

Què s'ha demostrat en aquest quadern, amb codi:

- La informació d'un esdeveniment ha de ser $-\log_2 p$ si volem que valgui 0 per als
  esdeveniments segurs i que se **sumi** sobre esdeveniments independents. El logaritme
  no és una tria estètica: és l'única funció que converteix productes en sumes.
- L'entropia és la sorpresa mitjana, i el bit és literal: 1 bit per a una moneda justa,
  3 bits exactes per a un dau de 8 cares, que són les preguntes de sí o no que calen.
- El conveni $0\log 0 = 0$ és l'única extensió contínua de la fórmula, no un pegat:
  $\lim_{p\to 0^+} p\log p = 0$, comprovat numèricament.
- Entropia i Gini comparteixen zeros, màxim i concavitat, i per això **no** donen els
  mateixos arbres però sí la mateixa exactitud: a l'arrel d'Iris trien el mateix tall, a
  l'arrel de Wine ja discrepen, els arbres sencers divergeixen als nodes petits, i les
  exactituds mitjanes sobre 40 particions es diferencien en **0,002** a Iris i **0,017-
  0,022** a Wine, en tots dos casos per sota de la desviació típica entre particions
  (0,031 i 0,040-0,049). Els arbres sencers d'Iris surten idèntics tall a tall; els de
  Wine no comparteixen ni un tall.
- El guany d'informació calculat a mà sobre `petal_llarg` troba el llindar **2,45** amb
  **0,9183 bits** de guany, el mateix que
  `DecisionTreeClassifier(max_depth=1, criterion="entropy")`.
- Amb una columna d'identificadors 0…149, el guany d'informació multivia la tria per
  damunt dels pètals (**1,585** bits contra 1,446 i 1,436) i produeix un model
  inservible. És una **fuita d'informació**, i l'exactitud d'examen no la delata: puja
  al 100 %. La ràtio de guany, dividint pel *split information* $\log_2 150 = 7{,}229$,
  la baixa a 0,2193 i deixa els pètals al davant.
- $H(p,q) = H(p) + D_{KL}(p\|q)$ es compleix fins als últims decimals; $D_{KL}$ és 0 en
  la diagonal, no negativa en 5.000 parells a l'atzar, i **no simètrica**.
- **La tesi**: la log-loss que minimitza `LogisticRegression`, l'entropia creuada entre
  el one-hot de l'etiqueta i `predict_proba`, i `sklearn.metrics.log_loss` donen el
  **mateix número**. I com que el one-hot té $H(p) = 0$, aquest número també és la
  divergència KL mitjana entre el món i el model. L'arbre i la logística mesuren el
  desordre amb la mateixa vara.
- La informació mútua és aquesta mateixa magnitud aplicada a una columna sencera, i
  serveix per ordenar columnes: `flavanoids` sola val **0,963** dels **1,567** bits de
  l'etiqueta de Wine. Però ordenar-les no és seleccionar-les: amb la millor sola el bosc
  es queda al 71,7 %, amb 3 columnes arriba al 96,9 % i amb les 13 al 98,6 %. Les 8
  columnes de més valen 1 punt, perquè la seva informació està repetida, i
  $I(X;Y)$ calculada columna a columna no veu aquesta redundància.

### Què hem deixat fora

- El **teorema de la codificació de Shannon**: que l'entropia sigui assolible com a
  longitud mitjana de codi, i no només una fita.
- La **demostració de la desigualtat de Gibbs** ($D_{KL} \ge 0$), que surt de la
  concavitat del logaritme. L'hem comprovada, no demostrada.
- Com **estima** la informació mútua `mutual_info_classif` per a columnes contínues
  (veïns més propers), i la informació mútua **condicional**, que és el que caldria per
  tractar la redundància entre columnes.
- Les salvaguardes de C4.5 sobre la ràtio de guany quan el *split information* és molt
  petit.
"""))

info = escriu(cells, "Machine Learning/03_matematiques/MA_04_entropia_informacio.ipynb",
              titol_colab="MA_04_entropia_informacio.ipynb")
print(info)
