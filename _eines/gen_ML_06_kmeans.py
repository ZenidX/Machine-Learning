# -*- coding: utf-8 -*-
"""Genera el quadern ML_06: k-means, agrupar sense etiquetes.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_ML_06_kmeans.py

Els numeros que apareixen al text son els de l'execucio real del quadern
(numpy 2.3, scikit-learn 1.8); si es canvia el codi, cal tornar a executar-lo
amb _eines/executa_nb.py i actualitzar-los.

Els exercicis d'aquesta sessio son a 02_practica/EX_06_kmeans.ipynb. El seu
solucionari NO es genera des d'aqui: es a 02_practica/solucions/, que esta al
.gitignore.
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# Agrupar sense etiquetes: k-means

**Optativa d'Aprenentatge automàtic · DAM/DAW 2n**

Fins ara cada dataset venia amb la resposta: la columna `y` deia quina espècie era cada flor,
quin vi era cada ampolla, quina xifra era cada imatge. Els models aprenien a **imitar** aquesta
resposta. És l'aprenentatge **supervisat**.

Al quadern del PCA vas veure la primera cosa que no mirava `y`: buscava direccions de màxima
variància i, de rebot, les espècies d'Iris sortien separades. Aquí fem un pas més:

> **Si ningú et diu quins grups hi ha, els pots trobar?**

L'algorisme més conegut per fer-ho és **k-means**. És tan senzill que el pots escriure en deu
línies de NumPy: assignar cada punt al centre més proper, moure cada centre a la mitjana dels
seus punts, i repetir. El que el fa interessant no és el codi, és la pregunta que hi ha a sota:
**per què aquests dos passos, i no uns altres?** La resposta és que cadascun és la solució
exacta d'un problema de minimització, i ho demostrarem. No amb fe: amb una deducció de quatre
línies i amb el número que la comprova.

Del curs fem servir tres coses que ja tens:

- la **distància euclidiana** del quadern de k-NN (és Pitàgores);
- els **eixos** de NumPy (`axis=0`, `axis=1`) i el *broadcasting* de `FO_01_numpy`;
- la **mitjana** com a vector, i el PCA de `MA_06` per dibuixar dades de moltes columnes.
"""))

A(code("""
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, load_iris, make_moons

np.set_printoptions(precision=4, suppress=True)

print("numpy", np.__version__)
"""))

# ---------------------------------------------------------------- 1
A(md(r"""
## 1. Unes dades sense resposta

Comencem amb dades fabricades, perquè així **nosaltres** sabem la veritat i el model no.
`make_blobs` genera núvols de punts al voltant d'uns quants centres. En demanem 300 punts en
2 columnes, al voltant de 3 centres, i **llencem les etiquetes**: les guardem en una variable
que l'algorisme no veurà, només per comprovar-ho al final.
"""))

A(code("""
X, y_veritat = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=42)
n, d = X.shape

print("Forma de X:", X.shape)
print("Primeres 5 files:")
print(X[:5])

plt.figure(figsize=(6, 5.5))
plt.scatter(X[:, 0], X[:, 1], s=15, color="gray", alpha=0.7)
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.title("El que veu l'algorisme: punts, sense cap color")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
A ull, els grups es veuen. El problema és que «a ull» no és un algorisme, i amb 13 columnes
(Wine) o 64 (digits) ja no hi ha ull que valgui. Cal convertir «els grups es veuen» en un
número que es pugui minimitzar.
"""))

# ---------------------------------------------------------------- 2
A(md(r"""
## 2. Què vol dir «un bon agrupament»: la inèrcia

Volem partir els $n$ punts en $k$ grups i donar a cada grup un **centre** (o *centroide*)
$\mu_1, \dots, \mu_k$. Cada punt $x_i$ pertany a un grup, que escrivim $c(i) \in \{1,\dots,k\}$.

Un agrupament és bo si cada punt queda **a prop del centre del seu grup**. La manera de mesurar
això que fa servir k-means és la suma de les distàncies al quadrat, que s'anomena **inèrcia**:

$$J(c, \mu) = \sum_{i=1}^{n} \left\| x_i - \mu_{c(i)} \right\|^2$$

Dues coses s'hi poden triar: **a quin grup va cada punt** ($c$) i **on són els centres** ($\mu$).
Tot k-means és minimitzar $J$ respecte d'aquestes dues coses.

Per calcular-la necessitem la distància de **cada** punt a **cada** centre: una matriu $D$ de
$n \times k$ on

$$D_{ij} = \|x_i - \mu_j\|^2 = \sum_{l=1}^{d} (x_{il} - \mu_{jl})^2$$

Sense bucles. `X[:, None, :]` té forma $(n, 1, d)$ i `M[None, :, :]` té forma $(1, k, d)$: el
*broadcasting* les estira a $(n, k, d)$, restem, elevem al quadrat i sumem sobre l'últim eix,
el de les columnes. És la mateixa idea que `axis=` de `FO_01_numpy`, amb un eix més.
"""))

A(code("""
def distancies2(X, M):
    \"\"\"Matriu (n, k) de distàncies AL QUADRAT entre cada fila de X i cada fila de M.\"\"\"
    dif = X[:, None, :] - M[None, :, :]      # (n, 1, d) - (1, k, d) -> (n, k, d)
    return (dif ** 2).sum(axis=2)            # sumem sobre les d columnes -> (n, k)


def inercia(X, etiquetes, M):
    \"\"\"J = suma de ||x_i - mu_c(i)||^2.\"\"\"
    return ((X - M[etiquetes]) ** 2).sum()


# Comprovació a mà amb un punt i un centre qualssevol
M_prova = np.array([[0.0, 0.0], [5.0, 5.0], [-5.0, 5.0]])
D_prova = distancies2(X, M_prova)
print("Forma de D:", D_prova.shape)
print(f"D[0, 1] amb la funció:    {D_prova[0, 1]:.6f}")
print(f"D[0, 1] amb Pitàgores:    {(X[0, 0] - 5) ** 2 + (X[0, 1] - 5) ** 2:.6f}")
"""))

A(md(r"""
Fixa't en `M[etiquetes]` a la funció `inercia`: és indexar un array **amb un altre array**.
Si `etiquetes` és `[2, 0, 0, 1, ...]`, `M[etiquetes]` és una matriu de $n$ files on la fila $i$
és el centre del grup del punt $i$. Una línia, i és exactament el $\mu_{c(i)}$ de la fórmula.
"""))

# ---------------------------------------------------------------- 3
A(md(r"""
## 3. El primer pas, deduït: amb els centres fixos, on va cada punt?

Suposem que algú ens dona els centres $\mu_1,\dots,\mu_k$ i no els podem tocar. Quina
assignació $c$ fa $J$ mínima?

Mira la fórmula: $J$ és una **suma de $n$ termes**, i el terme $i$ només depèn de $c(i)$, no de
l'assignació de cap altre punt. Per tant minimitzar la suma és minimitzar cada terme pel seu
compte:

$$c(i) = \arg\min_{j} \|x_i - \mu_j\|^2$$

**Cada punt va al centre més proper.** No és una regla raonable que algú es va inventar: és
l'única assignació que minimitza $J$ amb aquests centres. En codi és una línia, `D.argmin(axis=1)`:
la posició del mínim de cada fila.

Una deducció tan curta convé comprovar-la. Amb 8 punts i 2 centres hi ha $2^8 = 256$ maneres
d'assignar-los; les provem **totes** i mirem si la millor és la del centre més proper.
"""))

A(code("""
rng = np.random.default_rng(1)
X_petit = rng.normal(size=(8, 2)) * 2
M_petit = np.array([[-1.0, 0.0], [1.5, 0.5]])

# Força bruta: totes les 2^8 assignacions possibles
millor_J, millor_c = np.inf, None
for c in itertools.product([0, 1], repeat=len(X_petit)):
    J = inercia(X_petit, np.array(c), M_petit)
    if J < millor_J:
        millor_J, millor_c = J, np.array(c)

# La regla: cada punt al centre més proper
c_proper = distancies2(X_petit, M_petit).argmin(axis=1)

print("Assignacions provades:", 2 ** len(X_petit))
print("Millor per força bruta:", millor_c, f"  J = {millor_J:.6f}")
print("Centre més proper:     ", c_proper, f"  J = {inercia(X_petit, c_proper, M_petit):.6f}")
print("Són la mateixa?", np.array_equal(millor_c, c_proper))
"""))

A(md(r"""
De les 256 assignacions, la millor és exactament la del centre més proper, amb el mateix $J$.
La força bruta convenç; la deducció explica per què no calia provar-les.
"""))

# ---------------------------------------------------------------- 4
A(md(r"""
## 4. El segon pas, deduït: amb els grups fixos, on va cada centre?

Ara a l'inrevés: els grups estan fixats i podem moure els centres. Com que cada centre només
apareix als termes dels seus punts, el problema es parteix en $k$ problemes independents. Per a
un grup $G$ amb $m$ punts, volem el $\mu$ que minimitza

$$f(\mu) = \sum_{i \in G} \|x_i - \mu\|^2$$

La resposta és la **mitjana** $\bar{x} = \frac{1}{m}\sum_{i\in G} x_i$, i ho podem demostrar de
dues maneres. Les dues valen la pena.

### Primera manera: sumar i restar la mitjana

El truc és escriure $x_i - \mu = (x_i - \bar{x}) + (\bar{x} - \mu)$ i desenvolupar el quadrat,
igual que $(a+b)^2 = a^2 + 2ab + b^2$ però amb vectors:

$$f(\mu) = \sum_{i\in G} \|x_i - \bar{x}\|^2 \;+\; 2\,(\bar{x}-\mu)\cdot\sum_{i\in G}(x_i - \bar{x}) \;+\; m\,\|\bar{x} - \mu\|^2$$

El terme del mig és zero, perquè $\sum_{i}(x_i - \bar{x}) = \sum_i x_i - m\bar{x} = 0$: les
desviacions respecte de la mitjana sumen zero (és la mateixa propietat que fa que les dades
centrades del PCA tinguin mitjana zero). Queda

$$\boxed{f(\mu) = f(\bar{x}) + m\,\|\bar{x} - \mu\|^2}$$

El segon terme és un quadrat multiplicat per $m > 0$: és $\geq 0$, i només val 0 quan
$\mu = \bar{x}$. **Qualsevol altre centre és pitjor que la mitjana, i sabem exactament quant
pitjor.** Comprovem la igualtat amb punts i centres a l'atzar.
"""))

A(code("""
G = X[:40]                      # un grup qualsevol de 40 punts
m = len(G)
mitjana = G.mean(axis=0)


def f(mu):
    return ((G - mu) ** 2).sum()


# El terme del mig és zero: les desviacions sumen zero
print("Suma de les desviacions (x_i - mitjana):", (G - mitjana).sum(axis=0))

# La igualtat f(mu) = f(mitjana) + m ||mitjana - mu||^2, amb cinc mu a l'atzar
rng = np.random.default_rng(2)
for _ in range(5):
    mu = rng.normal(size=2) * 5
    esquerra = f(mu)
    dreta = f(mitjana) + m * ((mitjana - mu) ** 2).sum()
    print(f"mu = {mu}   f(mu) = {esquerra:12.6f}   f(mitjana) + m||mitjana-mu||^2 = {dreta:12.6f}")
"""))

A(md(r"""
### Segona manera: la derivada, com al descens de gradient

Si recordes `MA_02`, el mínim d'una funció és on la derivada val zero. Derivem $f$ respecte de
$\mu$. Cada terme $\|x_i - \mu\|^2 = \sum_l (x_{il} - \mu_l)^2$ té derivada respecte de $\mu_l$
igual a $-2(x_{il} - \mu_l)$, per la regla de la cadena. Sumant:

$$\nabla f(\mu) = -2\sum_{i\in G}(x_i - \mu) = -2m\,(\bar{x} - \mu)$$

que val zero si i només si $\mu = \bar{x}$. El mateix resultat per un altre camí. I com al
quadern del gradient, la derivada analítica es comprova amb **diferències finites**.
"""))

A(code("""
def gradient_analitic(mu):
    return -2 * m * (mitjana - mu)


def gradient_numeric(mu, h=1e-6):
    g = np.zeros_like(mu)
    for l in range(len(mu)):
        e = np.zeros_like(mu)
        e[l] = h
        g[l] = (f(mu + e) - f(mu - e)) / (2 * h)
    return g


mu = np.array([3.0, -2.0])
print("Gradient analític a mu = [3, -2]:", gradient_analitic(mu))
print("Gradient numèric  a mu = [3, -2]:", gradient_numeric(mu))
print("\\nGradient analític a la mitjana:  ", gradient_analitic(mitjana))
print("Gradient numèric  a la mitjana:  ", gradient_numeric(mitjana))
"""))

A(md(r"""
A $\mu = (3, -2)$ el gradient analític i el numèric coincideixen, i a la mitjana tots dos són
zero (el numèric, a l'ordre de l'error d'arrodoniment). **El centre òptim d'un grup és la seva
mitjana**, i per això l'algorisme es diu *k-means*: *means* vol dir mitjanes.

Fixa't també en la diferència entre les dues demostracions. La derivada diu que la mitjana és
un punt on el pendent és zero. La primera manera diu més: que és el mínim **global** i que
qualsevol altre punt costa exactament $m\|\bar{x}-\mu\|^2$ més.
"""))

# ---------------------------------------------------------------- 5
A(md(r"""
## 5. L'algorisme de Lloyd: alternar els dos passos

Ja tenim les dues peces. Minimitzar $J$ respecte de $c$ i $\mu$ **alhora** és difícil, però
minimitzar-la respecte d'un **amb l'altre fix** és fàcil, i ho acabem de resoldre. La idea
d'en Stuart Lloyd (1957) és alternar:

1. **Inicialitzar**: triar $k$ centres, per exemple $k$ punts de les dades a l'atzar.
2. **Assignar**: cada punt al centre més proper (secció 3).
3. **Actualitzar**: cada centre a la mitjana dels seus punts (secció 4).
4. Repetir 2 i 3 fins que cap punt canviï de grup.

**Per què s'acaba, i per què $J$ no puja mai.** El pas 2 tria, amb els centres actuals, la
millor assignació possible: $J$ no pot pujar. El pas 3 tria, amb els grups actuals, els millors
centres possibles: $J$ tampoc pot pujar. Per tant $J$ és una seqüència que **no creix mai**. I
com que hi ha un nombre finit de maneres de repartir $n$ punts en $k$ grups (com a molt $k^n$),
i l'algorisme no pot tornar a una partició on ja ha estat sense que $J$ s'hagi quedat igual,
en algun moment les assignacions deixen de canviar i s'atura.

Això és el que cal comprovar al codi: guardem $J$ **després de cada mig pas** i mirem que no
pugi ni una sola vegada.
"""))

A(code("""
def kmeans_a_ma(X, centres_inicials, max_iter=100):
    \"\"\"Algorisme de Lloyd. Retorna (etiquetes, centres, historial_J, iteracions, historial_centres).

    historial_J guarda J després de cada mig pas: assignar, actualitzar, assignar...
    \"\"\"
    M = centres_inicials.astype(float).copy()
    historial_J = []
    historial_M = [M.copy()]
    etiquetes_abans = None

    for it in range(1, max_iter + 1):
        # pas 2: assignar cada punt al centre més proper
        etiquetes = distancies2(X, M).argmin(axis=1)
        historial_J.append(inercia(X, etiquetes, M))

        if etiquetes_abans is not None and np.array_equal(etiquetes, etiquetes_abans):
            break                                   # ningú ha canviat de grup: hem acabat

        # pas 3: cada centre a la mitjana dels seus punts
        M = np.array([X[etiquetes == j].mean(axis=0) for j in range(len(M))])
        historial_J.append(inercia(X, etiquetes, M))
        historial_M.append(M.copy())
        etiquetes_abans = etiquetes

    return etiquetes, M, historial_J, it, historial_M


# Inicialització: 3 punts de les dades triats a l'atzar
rng = np.random.default_rng(6)
M0 = X[rng.choice(n, size=3, replace=False)]

etiquetes, M_final, hist_J, iteracions, hist_M = kmeans_a_ma(X, M0)

print("Centres inicials:")
print(M0)
print("Centres finals:")
print(M_final)
print("\\nJ després de cada mig pas:", np.round(hist_J, 2))
print("Rondes d'assignació:", iteracions)
print("J no puja mai?", bool(np.all(np.diff(hist_J) <= 1e-9)))
print("Punts per grup:", np.bincount(etiquetes), " suma:", np.bincount(etiquetes).sum())
"""))

A(code("""
plt.figure(figsize=(7.5, 4.2))
plt.plot(range(len(hist_J)), hist_J, "o-", color="tab:blue")
plt.yscale("log")
plt.xlabel("Mig pas (assignar, actualitzar, assignar...)")
plt.ylabel("Inèrcia $J$ (escala log)")
plt.title("La inèrcia no puja mai")
plt.grid(alpha=0.3)
plt.show()
"""))

A(code("""
quins = [0, 2, 4, len(hist_M) - 1]
fig, axs = plt.subplots(1, 4, figsize=(16, 4.2), sharex=True, sharey=True)
for ax, t in zip(axs, quins):
    M_t = hist_M[t]
    etiq_t = distancies2(X, M_t).argmin(axis=1)
    ax.scatter(X[:, 0], X[:, 1], c=etiq_t, cmap="tab10", vmin=0, vmax=9, s=12, alpha=0.6)
    ax.scatter(M_t[:, 0], M_t[:, 1], c="black", marker="X", s=180, edgecolor="white")
    ax.set_title(f"centres després de {t} actualitzacions\\nJ = {inercia(X, etiq_t, M_t):.1f}")
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
En aquesta execució la inèrcia comença a **19089.49** i durant unes quantes rondes baixa a poc a
poc. Mira els quatre dibuixos: dos dels centres inicials han caigut al mateix núvol de dalt i
se'l reparteixen, mentre el tercer ha de cobrir els dos núvols de baix i acaba a mig camí entre
tots dos. Ronda a ronda, un dels centres de dalt va perdent punts i baixa cap al núvol de la
dreta; quan hi arriba, el centre de mig camí es queda amb el núvol de baix sol, la inèrcia cau de
cop fins a **566.86**, i a la sisena ronda ja ningú canvia de grup. Els grups finals tenen 100
punts cadascun, que és com els havíem fabricat.

La seqüència sencera és no creixent, com havíem deduït: cada mig pas, o baixa, o es queda igual.
I aquesta execució ja avisa d'una cosa que la secció 7 farà explícita: ha anat d'un pèl que no
es quedés encallada.
"""))

# ---------------------------------------------------------------- 6
A(md(r"""
## 6. Comparació amb scikit-learn

`sklearn.cluster.KMeans` fa el mateix. Per comparar-ho de veritat li hem de donar **les mateixes
condicions**:

- `init=M0`: els mateixos centres inicials (per defecte en tria ell, amb un mètode que veurem a
  la secció 7);
- `n_init=1`: una sola execució (per defecte en fa diverses i es queda la millor);
- `algorithm="lloyd"`: el mateix algorisme (hi ha una variant, `"elkan"`, que dona el mateix
  resultat estalviant distàncies);
- `tol=0`: que s'aturi quan ningú canviï de grup, com el nostre, i no abans.
"""))

A(code("""
from sklearn.cluster import KMeans

km = KMeans(n_clusters=3, init=M0, n_init=1, algorithm="lloyd", tol=0)
km.fit(X)

print("Centres de scikit-learn (cluster_centers_):")
print(km.cluster_centers_)
print("Els nostres:")
print(M_final)
print()
print(f"Diferència màxima entre centres:   {np.abs(km.cluster_centers_ - M_final).max():.2e}")
print(f"Etiquetes idèntiques?              {np.array_equal(km.labels_, etiquetes)}")
print(f"inertia_ de scikit-learn:          {km.inertia_:.6f}")
print(f"La nostra J final:                 {hist_J[-1]:.6f}")
print(f"Iteracions (n_iter_):              {km.n_iter_}  (les nostres rondes: {iteracions})")
"""))

A(md(r"""
Centres iguals fins a $10^{-15}$, les 300 etiquetes idèntiques i la mateixa inèrcia, **566.86**,
a totes les xifres. Les deu línies de `kmeans_a_ma` són el que fa `KMeans.fit`.

Dos atributs que surten d'aquí i faràs servir als exercicis:

- `.transform(X)` retorna la matriu de distàncies de cada punt a cada centre, **sense elevar
  al quadrat**. És l'arrel de la nostra `distancies2`.
- `.predict(X_nou)` assigna punts nous al centre més proper. És el pas 2 sol, sense moure cap
  centre.
"""))

A(code("""
print("transform == arrel de distancies2?",
      np.allclose(km.transform(X), np.sqrt(distancies2(X, km.cluster_centers_))))
print("predict == argmin de la distància?",
      np.array_equal(km.predict(X), distancies2(X, km.cluster_centers_).argmin(axis=1)))
"""))

# ---------------------------------------------------------------- 7
A(md(r"""
## 7. El parany: mínims locals, i com s'esquiven

L'argument de la secció 5 garanteix que $J$ baixa i que l'algorisme s'atura. **No garanteix que
s'aturi al millor agrupament possible.** S'atura quan cap dels dos passos pot millorar, i això
pot passar en un lloc dolent. Provem la mateixa funció amb 200 inicialitzacions diferents.
"""))

A(code("""
J_finals = []
for llavor in range(200):
    r = np.random.default_rng(llavor)
    M_ini = X[r.choice(n, size=3, replace=False)]
    J_finals.append(kmeans_a_ma(X, M_ini)[2][-1])
J_finals = np.array(J_finals)

valors, vegades = np.unique(np.round(J_finals, 1), return_counts=True)
print("Inèrcia final i quantes vegades surt (de 200):")
for v, c in zip(valors, vegades):
    print(f"  J = {v:8.1f}   {c:3d} vegades")
print(f"\\nExecucions que NO arriben a 566.9: {np.mean(J_finals > 600):.0%}")
"""))

A(code("""
r = np.random.default_rng(0)                          # una llavor que cau al parany
M_dolent = X[r.choice(n, size=3, replace=False)]
etiq_dolent, M_dol_final, hist_dol, _, _ = kmeans_a_ma(X, M_dolent)

fig, axs = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)
for ax, et, M_, titol in [(axs[0], etiquetes, M_final, f"Bon mínim: J = {hist_J[-1]:.1f}"),
                         (axs[1], etiq_dolent, M_dol_final, f"Mínim local: J = {hist_dol[-1]:.1f}")]:
    ax.scatter(X[:, 0], X[:, 1], c=et, cmap="tab10", vmin=0, vmax=9, s=12, alpha=0.6)
    ax.scatter(M_[:, 0], M_[:, 1], c="black", marker="X", s=180, edgecolor="white")
    ax.set_title(titol)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
Gairebé una de cada quatre inicialitzacions acaba en un agrupament on **dos núvols comparteixen
un centre i un altre núvol se'n queda dos**. La inèrcia és deu vegades més alta, però l'algorisme
no en pot sortir: cap punt vol canviar de grup i cap centre es vol moure. És un **mínim local**,
la mateixa idea que al descens de gradient.

Hi ha dos remeis, i `KMeans` fa servir tots dos per defecte.

**Remei 1: repetir.** Executar l'algorisme diverses vegades i quedar-se la de menor $J$. Això és
`n_init`. Si una execució falla amb probabilitat 0.24, deu execucions fallen totes amb
probabilitat $0.24^{10} \approx 6\cdot10^{-7}$ (si fossin independents, que ho són perquè cada
una tria la seva llavor).

**Remei 2: començar millor.** La inicialització **k-means++** (Arthur i Vassilvitskii, 2007) tria
el primer centre a l'atzar i cada centre següent **amb probabilitat proporcional a la distància
al quadrat al centre més proper ja triat**. Els punts lluny de tots els centres tenen més
números a la rifa, i així és difícil que dos centres caiguin al mateix núvol. Són sis línies.
"""))

A(code("""
def kmeanspp(X, k, rng):
    \"\"\"Inicialització k-means++: cada centre nou, amb probabilitat proporcional a D^2.\"\"\"
    centres = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        D2 = distancies2(X, np.array(centres)).min(axis=1)    # distància al centre més proper
        centres.append(X[rng.choice(len(X), p=D2 / D2.sum())])
    return np.array(centres)


J_pp = np.array([kmeans_a_ma(X, kmeanspp(X, 3, np.random.default_rng(s)))[2][-1]
                 for s in range(200)])

print(f"Inicialització a l'atzar: {np.mean(J_finals > 600):.1%} de les execucions al mínim local")
print(f"Inicialització k-means++: {np.mean(J_pp > 600):.1%} de les execucions al mínim local")
"""))

A(md(r"""
De **24 %** a **5 %**, només canviant com es trien els centres de sortida. El que **no** fem aquí
és la demostració que hi ha a l'article: que k-means++ dona, de mitjana, una inèrcia com a molt
$O(\log k)$ vegades l'òptima. La deixem fora, i ho diem; el que sí que hem fet és mesurar-ne
l'efecte.

Amb tots dos remeis junts (`init="k-means++"`, que és el valor per defecte, i `n_init` > 1), a
la pràctica el parany desapareix. Per això, a partir d'aquí fem servir `KMeans` amb
`n_init=10` i `random_state=42`.
"""))

# ---------------------------------------------------------------- 8
A(md(r"""
## 8. Quants grups? La $k$ que no ens diu ningú

Fins ara hem fet trampa: sabíem que eren 3 núvols perquè els havíem fabricat. Amb dades de
veritat, $k$ és la pregunta.

### Per què la inèrcia no serveix per triar $k$

La temptació és provar diverses $k$ i quedar-se la de menor $J$. No funciona, i es pot
demostrar: **la inèrcia òptima amb $k+1$ grups és sempre menor o igual que amb $k$**. Agafa la
millor solució amb $k$ centres i afegeix-hi un centre nou just a sobre d'un punt de les dades.
Aquell punt passa a tenir distància 0 (abans en tenia més), i cap altre punt queda més lluny
del seu centre més proper (com a molt, n'hi ha un de nou més a prop). Per tant ja hi ha una
solució amb $k+1$ centres que no és pitjor, i l'òptima encara ho és menys. Al límit, amb
$k = n$, cada punt és el seu propi centre i $J = 0$.

Minimitzar $J$ sobre $k$ dona sempre «tants grups com punts». Cal un altre criteri.
"""))

A(code("""
from sklearn.metrics import silhouette_score

ks = range(1, 9)
inercies = []
for k in ks:
    model = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inercies.append(model.inertia_)

for k, J in zip(ks, inercies):
    print(f"k = {k}   inèrcia = {J:9.2f}")
print("\\nNo creix mai amb k?", bool(np.all(np.diff(inercies) <= 1e-9)))

# I al límit, k = n: cada punt és el seu centre
print("Inèrcia amb k = n, calculada:", inercia(X, np.arange(n), X))
"""))

A(md(r"""
### El colze

El primer criteri és mirar **on deixa de compensar** afegir grups. Dibuixant $J$ contra $k$,
la corba baixa de pressa mentre cada grup nou separa núvols de veritat, i després s'aplana:
afegir grups només parteix núvols que ja estaven bé. El punt on es doblega és el **colze**.
"""))

A(code("""
plt.figure(figsize=(7, 4.2))
plt.plot(list(ks), inercies, "o-", color="tab:blue")
plt.xlabel("Nombre de grups $k$")
plt.ylabel("Inèrcia $J$")
plt.title("El mètode del colze sobre els tres núvols")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Aquí el colze és clar perquè les dades són de joguina. Amb dades reals sovint no n'hi ha cap de
clar, i fa falta un número.

### La silueta, implementada a mà

Per a cada punt $i$ es calculen dues mitjanes de distàncies (sense elevar al quadrat):

- $a(i)$: la distància mitjana als **altres punts del seu grup**. Com de ben acompanyat està.
- $b(i)$: la distància mitjana als punts del **grup veí més proper** (el grup aliè amb la
  mitjana més petita). Com de lluny té l'alternativa.

I la silueta del punt és

$$s(i) = \frac{b(i) - a(i)}{\max\big(a(i),\, b(i)\big)}$$

que val entre $-1$ i $1$. A prop d'1: el punt és molt més a prop dels seus que dels veïns. A
prop de 0: és a la frontera. Negativa: estaria millor a l'altre grup. La silueta de
l'agrupament és la **mitjana** de $s(i)$ de tots els punts, i a diferència de la inèrcia **no
millora sola amb $k$**: partir un núvol bo en dos fa que els punts tinguin el «veí» molt a prop,
i $b(i)$ cau.

Una convenció: si un punt està sol al seu grup, $a(i)$ no es pot calcular i scikit-learn hi
posa $s(i)=0$. Amb $k=1$ no hi ha grup veí i la silueta no està definida.
"""))

A(code("""
def silueta_a_ma(X, etiquetes):
    \"\"\"Silueta mitjana, punt a punt, amb la definició.\"\"\"
    D = np.sqrt(distancies2(X, X))                # (n, n) distàncies entre tots els punts
    grups = np.unique(etiquetes)
    s = np.zeros(len(X))
    for i in range(len(X)):
        meu = etiquetes == etiquetes[i]
        if meu.sum() == 1:
            continue                              # sol al seu grup: s(i) = 0
        a = D[i, meu].sum() / (meu.sum() - 1)     # el propi punt (distància 0) no compta
        b = min(D[i, etiquetes == g].mean() for g in grups if g != etiquetes[i])
        s[i] = (b - a) / max(a, b)
    return s.mean()


print(" k   silueta a mà   silhouette_score   diferència")
siluetes = []
for k in range(2, 9):
    et = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
    propia, sk = silueta_a_ma(X, et), silhouette_score(X, et)
    siluetes.append(sk)
    print(f" {k}      {propia:.6f}        {sk:.6f}        {abs(propia - sk):.1e}")
"""))

A(code("""
plt.figure(figsize=(7, 4.2))
plt.plot(range(2, 9), siluetes, "o-", color="tab:green")
plt.xlabel("Nombre de grups $k$")
plt.ylabel("Silueta mitjana")
plt.title("La silueta sí que té un màxim")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
La implementació pròpia coincideix amb `silhouette_score` a totes les $k$, i la silueta té un
màxim clar a $k = 3$, amb **0.848**: el número que coneixíem perquè havíem fabricat les dades.
Amb dades reals no el coneixeràs, i aquests dos gràfics són les eines per decidir-lo. Sovint no
es posen d'acord, i llavors decidir és feina teva, no de l'algorisme.
"""))

# ---------------------------------------------------------------- 9
A(md(r"""
## 9. Iris sense etiquetes

Ara amb dades de veritat. Agafem les 150 flors d'Iris, **llencem l'espècie**, i demanem 3 grups.
Les quatre columnes són centímetres, així que no cal escalar (és el mateix raonament que al PCA:
quan totes les columnes van a la mateixa unitat, la diferència de variància és informació).

Després comparem els grups amb les espècies, que l'algorisme no ha vist.
"""))

A(code("""
iris = load_iris()
X_iris = iris.data
especie = iris.target_names[iris.target]

km_iris = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_iris)

taula = pd.crosstab(km_iris.labels_, especie, rownames=["grup"], colnames=["espècie"])
taula
"""))

A(md(r"""
`pd.crosstab` compta quantes flors hi ha a cada combinació de grup i espècie. Si k-means hagués
recuperat les espècies perfectament, cada fila tindria un sol número diferent de zero.

### El número del grup no vol dir res

Abans de llegir la taula, un parany que ja vas veure al PCA amb el signe dels vectors propis.
**Els grups 0, 1 i 2 no tenen cap relació amb les espècies 0, 1 i 2.** k-means numera els grups
segons l'ordre en què li han sortit, i amb una altra llavor els mateixos grups poden sortir amb
els números permutats. Per això no té sentit calcular una «precisió» comparant `labels_` amb
`target` directament.

La mesura que s'usa és l'**índex de Rand ajustat** (`adjusted_rand_score`): mira **parelles de
punts** i compta si l'agrupament i les etiquetes coincideixen a l'hora de dir «aquests dos van
junts» o «aquests dos van separats». Com que mira parelles, no números de grup, **no li afecta
permutar els noms**. Val 1 si les dues particions són idèntiques i al voltant de 0 si
l'agrupament és a l'atzar. No en deduïm la fórmula; en comprovem les dues propietats.
"""))

A(code("""
from sklearn.metrics import adjusted_rand_score

ari = adjusted_rand_score(iris.target, km_iris.labels_)
print(f"ARI de k-means contra les espècies:                {ari:.4f}")

# Propietat 1: permutar els noms dels grups no canvia res
permutacio = np.array([2, 0, 1])
print(f"ARI amb els grups renombrats (0->2, 1->0, 2->1):   "
      f"{adjusted_rand_score(iris.target, permutacio[km_iris.labels_]):.4f}")

# Propietat 2: unes etiquetes a l'atzar donen un ARI proper a zero
rng = np.random.default_rng(42)
print(f"ARI d'unes etiquetes a l'atzar:                     "
      f"{adjusted_rand_score(iris.target, rng.integers(0, 3, len(X_iris))):.4f}")

# Propietat 3: una partició contra ella mateixa dona 1
print(f"ARI de les espècies contra elles mateixes:          "
      f"{adjusted_rand_score(iris.target, iris.target):.4f}")
"""))

A(code("""
from sklearn.decomposition import PCA

Z = PCA(n_components=2).fit_transform(X_iris)
centres_Z = PCA(n_components=2).fit(X_iris).transform(km_iris.cluster_centers_)

fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
axs[0].scatter(Z[:, 0], Z[:, 1], c=iris.target, cmap="tab10", vmin=0, vmax=9, s=20, alpha=0.8)
axs[0].set_title("Les espècies (k-means no les ha vist)")
axs[1].scatter(Z[:, 0], Z[:, 1], c=km_iris.labels_, cmap="tab10", vmin=0, vmax=9, s=20, alpha=0.8)
axs[1].scatter(centres_Z[:, 0], centres_Z[:, 1], c="black", marker="X", s=180, edgecolor="white")
axs[1].set_title("Els grups de k-means")
for ax in axs:
    ax.set_xlabel("1a component principal")
    ax.set_ylabel("2a component principal")
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
Els colors dels dos dibuixos no es corresponen (és el parany de la numeració), però la
**forma** sí que es pot comparar. Les dades tenen 4 columnes i les dibuixem amb el PCA de
`MA_06`; els centres de k-means, que també són punts de 4 columnes, es projecten amb la mateixa
transformació.

El que surt: la *setosa* la troba sencera, en un grup net de 50 flors. *Versicolor* i
*virginica* les barreja a la frontera: un grup es queda 48 *versicolor* i 14 *virginica*, i
l'altre 36 *virginica* i 2 *versicolor*. L'ARI és **0.7302**.

I la lectura bona no és «k-means s'equivoca en 16 flors». **k-means no s'ha equivocat de res:
ningú li ha demanat que trobés espècies.** Ha trobat els tres grups que fan mínima la inèrcia, i
resulta que dues espècies se solapen en mides de pètal i de sèpal. El que mesura l'ARI és fins a
quin punt l'estructura geomètrica de les dades coincideix amb una classificació que hi ha fet
un botànic. Aquí, molt però no del tot.
"""))

# ---------------------------------------------------------------- 10
A(md(r"""
## 10. On k-means falla

k-means fa una suposició que no diu en veu alta: que cada grup és **un núvol arrodonit al voltant
del seu centre**. És el que implica minimitzar distàncies al centre: la frontera entre dos grups
és sempre la recta (o el pla) a mig camí entre els dos centres. Si els grups tenen una altra
forma, no hi ha $k$ ni llavor que ho arregli.

### Formes que no són núvols

Dues mitges llunes encaixades, amb `make_moons`.
"""))

A(code("""
X_ll, y_ll = make_moons(n_samples=300, noise=0.05, random_state=42)
km_ll = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X_ll)

from sklearn.cluster import DBSCAN
db_ll = DBSCAN(eps=0.2).fit(X_ll)

print(f"k-means: ARI = {adjusted_rand_score(y_ll, km_ll.labels_):.4f}")
print(f"DBSCAN:  ARI = {adjusted_rand_score(y_ll, db_ll.labels_):.4f}")

fig, axs = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True, sharey=True)
axs[0].scatter(X_ll[:, 0], X_ll[:, 1], c=km_ll.labels_, cmap="tab10", vmin=0, vmax=9, s=14)
axs[0].scatter(*km_ll.cluster_centers_.T, c="black", marker="X", s=180, edgecolor="white")
axs[0].set_title("k-means: talla per la recta entre els dos centres")
axs[1].scatter(X_ll[:, 0], X_ll[:, 1], c=db_ll.labels_, cmap="tab10", vmin=0, vmax=9, s=14)
axs[1].set_title("DBSCAN: segueix la densitat de punts")
for ax in axs:
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
k-means talla les llunes per la meitat amb una recta, i l'ARI cau a **0.2475**. No és qüestió de
llavor ni de `n_init`: amb dos centres, la frontera **és** una recta, per definició. És el mateix
límit que tenia el PCA amb els anells: una eina lineal davant d'una estructura que no ho és.

La solució és **canviar d'eina, no de paràmetres**. `DBSCAN` agrupa per densitat (punts que
tenen prou veïns a prop van junts) i recupera les dues llunes. No l'expliquem en aquest quadern:
el posem aquí només perquè es vegi que el problema és de la suposició, no de les dades.

### Unitats diferents

El segon límit ja el coneixes del k-NN i l'SVM, i aquí és igual de greu: k-means treballa amb
distàncies euclidianes, i una columna amb números grans domina la distància. Fem la prova amb els
tres núvols: hi afegim una tercera columna que **no té res a veure amb els grups** (soroll pur),
però mesurada en unitats grans, com un import en cèntims o una distància en mil·límetres. I
tornem a agrupar.
"""))

A(code("""
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
soroll = rng.normal(0, 1, n) * 100              # no diu res dels grups, però va per centenars
X_unitats = np.column_stack([X, soroll])
print("Desviació típica de cada columna:", X_unitats.std(axis=0))

et_bo = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(X)
et_unitats = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(X_unitats)
et_escalat = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(
    StandardScaler().fit_transform(X_unitats))

print(f"Dades originals:                    ARI = {adjusted_rand_score(y_veritat, et_bo):.4f}")
print(f"Amb la columna de soroll:           ARI = {adjusted_rand_score(y_veritat, et_unitats):.4f}")
print(f"Soroll + StandardScaler:            ARI = {adjusted_rand_score(y_veritat, et_escalat):.4f}")
"""))

A(md(r"""
Les dues columnes bones tenen una desviació típica de 4.9 i 6.6; la de soroll, de 92.9. Amb ella,
l'ARI cau de **1.0000** a **0.0043**: k-means parteix les dades en franges de la columna de
soroll i els núvols de veritat li passen per alt. Amb `StandardScaler` les tres columnes pesen
igual i l'ARI torna a **1.0000**: el soroll hi és, però ja no mana. **Abans de k-means, escala**, llevat que
totes les columnes vagin a la mateixa unitat i la diferència de variància signifiqui alguna cosa.
"""))

# ---------------------------------------------------------------- resum
A(md(r"""
## 11. Resum

- **k-means minimitza la inèrcia** $J = \sum_i \|x_i - \mu_{c(i)}\|^2$, la suma de distàncies al
  quadrat de cada punt al centre del seu grup. En NumPy, `((X - M[etiquetes]) ** 2).sum()`.
- **Assignar cada punt al centre més proper no és una regla inventada**: és l'única assignació
  que minimitza $J$ amb els centres fixos, perquè cada terme depèn només del seu punt. Ho hem
  deduït i comprovat contra les 256 assignacions possibles d'un cas petit.
- **El millor centre d'un grup és la seva mitjana.** Per dos camins: sumant i restant la
  mitjana, $f(\mu) = f(\bar{x}) + m\|\bar{x}-\mu\|^2$; i amb la derivada,
  $\nabla f = -2m(\bar{x}-\mu)$, comprovada amb diferències finites.
- **L'algorisme de Lloyd alterna els dos passos**, cadascun òptim amb l'altre fix. Per això $J$
  no puja mai i l'algorisme s'acaba. La nostra implementació coincideix amb `KMeans` (mateixa
  `init`, `n_init=1`, `tol=0`) fins a $10^{-15}$ en els centres, i amb les 300 etiquetes iguals.
- **S'acaba, però no necessàriament al millor lloc.** Amb inicialització a l'atzar, el 24 % de
  les execucions queden en un mínim local; amb k-means++, el 5 %. `n_init` repeteix i es queda
  la millor.
- **La inèrcia no serveix per triar $k$**: l'òptima no creix mai amb $k$, i amb $k = n$ val 0.
  El colze i la silueta (implementada a mà, igual que `silhouette_score`) són els criteris.
- **El número d'un grup no vol dir res.** Per comparar amb etiquetes reals cal una mesura
  invariant a permutacions, com l'ARI. A Iris, k-means troba la *setosa* neta i barreja les
  altres dues: ARI 0.7302, sense haver vist cap etiqueta.
- **k-means suposa núvols arrodonits i distàncies comparables.** Amb llunes falla (ARI 0.2475) i
  cal una altra eina; amb una columna de soroll en unitats grans cau a ARI 0.0043, i escalant
  torna a 1.

### Què hem deixat fora

- Que trobar l'agrupament **òptim** de veritat és un problema NP-difícil: no es coneix cap manera
  de fer-ho essencialment millor que provant particions, i n'hi ha un nombre astronòmic. Lloyd
  troba un mínim local, i és el que tothom fa servir.
- La **garantia** de k-means++ (inèrcia esperada com a molt $O(\log k)$ vegades l'òptima). L'hem
  mesurada, no demostrada.
- La fórmula de l'**ARI**, que és un recompte de parelles corregit per l'atzar. N'hem comprovat
  les propietats, no la fórmula.
- **DBSCAN** i la resta d'algorismes d'agrupament. Hi és només per ensenyar que el límit de
  k-means és de la seva suposició.

## Pràctica

Els exercicis d'aquesta sessió són a `02_practica/EX_06_kmeans.ipynb`: el vi sense etiquetes, el
model per dins, els dígits agrupats sense saber quina xifra és cada imatge, i (opcional) una foto
reduïda a pocs colors.
"""))

info = escriu(cells, "Machine Learning/01_teoria/ML_06_kmeans.ipynb",
              titol_colab="ML_06_kmeans.ipynb")
print(info)
