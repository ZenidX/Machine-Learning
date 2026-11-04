# -*- coding: utf-8 -*-
"""Afegeix els grafics de teoria i els il.lustratius d'exercici a ML_05_svm.ipynb.

El quadern no te generador: aquest script el llegeix, treu les cel.les que ell
mateix havia afegit abans (marcades amb metadata["grafic"] = "ML_05") i les
torna a inserir darrere de les cel.les d'ancoratge. Es pot executar tantes
vegades com calgui.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_ML_05.py
"""
import io
import json
import sys

sys.path.insert(0, "_eines")
from nbgen import md, code  # noqa: E402

RUTA = "Machine Learning/01_teoria/ML_05_svm.ipynb"
MARCA = "ML_05"


def marca(c):
    c["metadata"]["grafic"] = MARCA
    return c


def M(s):
    return marca(md(s))


def C(s):
    return marca(code(s))


# ------------------------------------------------------------------ cel.les
# Cada entrada: (inici del text de la cel.la d'ancoratge, cel.les a posar darrere)
INSERCIONS = []

# 1. Moltes rectes a l'atzar: el marge com a problema d'optimitzacio
INSERCIONS.append(("**Recta C guanya**", [
    M(r"""
Fem-ho a la força bruta, per veure el problema amb els ulls: tirem **3.000 rectes a
l'atzar** pel buit entre les dues espècies, ens quedem només amb les que separen bé
les dues classes i calculem el marge de cadascuna amb la mateixa funció `distancia`.
"""),
    C(r"""
rng = np.random.default_rng(0)
angles = rng.uniform(0, np.pi, 3000)
punts_pas = np.column_stack([rng.uniform(1.9, 3.0, 3000), rng.uniform(0.0, 1.2, 3000)])

rectes_atzar = []                                   # (w, b, marge) de les que separen
for th, p in zip(angles, punts_pas):
    w_r = np.array([np.cos(th), np.sin(th)])
    b_r = -w_r @ p                                  # la recta passa per p
    costat = np.sign(X @ w_r + b_r)
    if abs(costat[y == 0].sum()) == (y == 0).sum() and \
       abs(costat[y == 1].sum()) == (y == 1).sum() and \
       costat[y == 0][0] != costat[y == 1][0]:      # cada classe a un costat
        rectes_atzar.append((w_r, b_r, distancia(w_r, b_r, X).min()))

marges_atzar = np.array([r[2] for r in rectes_atzar])
print(f"Rectes que separen bé: {len(rectes_atzar)} de 3000")
print(f"Marge de la millor: {marges_atzar.max():.3f}   (Recta C: "
      f"{distancia(rectes['Recta C']['w'], rectes['Recta C']['b'], X).min():.3f})")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ordre = np.argsort(marges_atzar)                    # les millors, dibuixades al damunt
cmap = plt.cm.viridis
x1_l = np.linspace(0.5, 5.5, 2)
for k in ordre[::6]:
    w_r, b_r, m_r = rectes_atzar[k]
    if abs(w_r[1]) > 1e-3:
        ax1.plot(x1_l, (-b_r - w_r[0] * x1_l) / w_r[1],
                 color=cmap(m_r / marges_atzar.max()), alpha=0.5, linewidth=1)
ax1.scatter(X[y == 0, 0], X[y == 0, 1], color="tab:blue", edgecolor="k", s=25, zorder=3, label="setosa")
ax1.scatter(X[y == 1, 0], X[y == 1, 1], color="tab:orange", edgecolor="k", s=25, zorder=3, label="versicolor")
ax1.set_xlim(0.5, 5.5)
ax1.set_ylim(-0.1, 2.0)
ax1.set_xlabel("Llargada del pètal (cm)")
ax1.set_ylabel("Amplada del pètal (cm)")
ax1.set_title("Rectes que separen bé, pintades pel seu marge\n(groc = marge gran, lila = petit)")
ax1.legend(loc="upper left")
ax1.grid(alpha=0.3)

ax2.hist(marges_atzar, bins=40, color="tab:gray", edgecolor="white")
for nom, r in rectes.items():
    ax2.axvline(distancia(r["w"], r["b"], X).min(), color=r["color"], linewidth=2, label=nom)
ax2.set_xlabel("marge (cm)")
ax2.set_ylabel("quantes rectes")
ax2.set_title("Com més marge, menys rectes l'aconsegueixen")
ax2.legend()
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),
    M(r"""
Totes les rectes del dibuix de l'esquerra encerten el 100 %. El que les diferencia és el
marge, i l'histograma diu que com més marge, menys rectes l'aconsegueixen: les bones
són rares, i la millor de les 3.000 amb prou feines supera la Recta C. Provar a
l'atzar és una manera molt cara de buscar-les. L'SVM no prova: **resol** el problema.
"""),
]))

# 2. D'on surt 1/||w||, i el carrer
INSERCIONS.append(("El marge de l'SVM (calculat resolent", [
    M(r"""
D'on surt `1 / np.linalg.norm(w)`? La recta $w \cdot x + b = 0$ és la mateixa si
multipliques $w$ i $b$ per qualsevol número, així que l'SVM tria una escala concreta:
la que fa que **els punts més propers donin exactament** $w \cdot x + b = \pm 1$. Amb
aquesta escala, la fórmula de distància del punt 2 dona, per a aquests punts,

$$d = \frac{|w \cdot x + b|}{\|w\|} = \frac{1}{\|w\|}$$

Comprovem-ho: `decision_function` calcula $w \cdot x + b$.
"""),
    C(r"""
valors_sv = model.decision_function(model.support_vectors_)
print("w.x + b als vectors de suport:", np.round(valors_sv, 4))
print("distància dels vectors de suport a la frontera:",
      np.round(distancia(w, b, model.support_vectors_), 4))
print(f"1 / ||w|| = {1 / np.linalg.norm(w):.4f}")
"""),
]))

INSERCIONS.append(('dibuixa_frontera_lineal(model, X, y, "Frontera', [
    M(r"""
De més a prop, al buit entre les dues espècies. La franja ombrejada és el **carrer**: la
zona on $-1 < w \cdot x + b < 1$, on no hi ha cap flor. Hi tornem a posar les rectes a
l'atzar d'abans, en gris: totes passen pel buit, però cap deixa un carrer tan ample.
La fletxa lila travessa el carrer d'un vector de suport a l'altre: és el doble del marge.
La fletxa és $w$: perpendicular a la frontera, com al quadern d'àlgebra.
"""),
    C(r"""
fig, ax = plt.subplots(figsize=(8, 6))
g1, g2 = np.meshgrid(np.linspace(1.0, 3.6, 300), np.linspace(-0.1, 1.4, 300))
valor = model.decision_function(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape)
ax.contourf(g1, g2, valor, levels=[-1, 1], colors=["gold"], alpha=0.35)
ax.contour(g1, g2, valor, levels=[-1, 0, 1], colors="k", linestyles=["--", "-", "--"])

x1_l = np.linspace(1.0, 3.6, 2)
for w_r, b_r, m_r in rectes_atzar[::40]:
    if abs(w_r[1]) > 1e-3:
        ax.plot(x1_l, (-b_r - w_r[0] * x1_l) / w_r[1], color="tab:gray", alpha=0.25, linewidth=1)

ax.scatter(X[y == 0, 0], X[y == 0, 1], color="tab:blue", edgecolor="k", s=35, zorder=3, label="setosa")
ax.scatter(X[y == 1, 0], X[y == 1, 1], color="tab:orange", edgecolor="k", s=35, zorder=3, label="versicolor")
ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=250,
           facecolors="none", edgecolors="tab:red", linewidths=2, zorder=4, label="vectors de suport")

# w, dibuixat des d'un punt de la frontera
mig = model.support_vectors_.mean(axis=0)         # entre els vectors de suport...
p0 = mig - (w @ mig + b) / (w @ w) * w              # ...portat a sobre de la frontera
u = w / np.linalg.norm(w)
t = np.array([-u[1], u[0]])                         # direcció de la frontera
pw = p0 - 0.40 * t                                  # una mica més amunt, per no tapar res
ax.annotate("", xy=pw + 0.35 * u, xytext=pw,
            arrowprops=dict(arrowstyle="->", color="tab:green", lw=2.5))
ax.annotate("$w$", pw + 0.38 * u + np.array([0, 0.03]), color="tab:green", fontsize=13)
# amplada del carrer
marge_m = 1 / np.linalg.norm(w)
ax.annotate("", xy=p0 + marge_m * u, xytext=p0 - marge_m * u,
            arrowprops=dict(arrowstyle="<->", color="tab:purple", lw=1.5))
ax.annotate(r"amplada $= 2/\|w\|$" + f" = {2 * marge_m:.2f}", p0 + np.array([0.12, -0.08]),
            color="tab:purple", fontsize=11,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="none", alpha=0.8))

ax.set_xlim(1.0, 3.6)
ax.set_ylim(-0.1, 1.4)
ax.set_aspect("equal")
ax.set_xlabel("Llargada del pètal (cm)")
ax.set_ylabel("Amplada del pètal (cm)")
ax.set_title("El carrer de l'SVM: el més ample que hi cap")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
plt.show()
"""),
]))

# 3. Treure flors no mou la frontera, dibuixat
INSERCIONS.append(("Hem tret 40 de les 100 flors", [
    M(r"""
El mateix, dibuixat. A la dreta, les 40 flors eliminades surten com a creuetes grises:
ja no hi són, i la frontera i el carrer no s'han mogut.
"""),
    C(r"""
fig, axs = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
g1, g2 = np.meshgrid(np.linspace(0.5, 5.5, 300), np.linspace(-0.1, 2.0, 300))
for ax, m, Xd, yd, titol in [(axs[0], model, X, y, f"{len(X)} flors"),
                              (axs[1], model_retallat, X_retallat, y_retallat,
                               f"{len(X_retallat)} flors (40 fora)")]:
    valor = m.decision_function(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape)
    ax.contourf(g1, g2, valor, levels=[-1, 1], colors=["gold"], alpha=0.35)
    ax.contour(g1, g2, valor, levels=[-1, 0, 1], colors="k", linestyles=["--", "-", "--"])
    ax.scatter(Xd[yd == 0, 0], Xd[yd == 0, 1], color="tab:blue", edgecolor="k", s=25, label="setosa")
    ax.scatter(Xd[yd == 1, 0], Xd[yd == 1, 1], color="tab:orange", edgecolor="k", s=25, label="versicolor")
    ax.scatter(m.support_vectors_[:, 0], m.support_vectors_[:, 1], s=200, facecolors="none",
               edgecolors="tab:red", linewidths=2, label="vectors de suport")
    ax.set_title(titol)
    ax.set_xlabel("Llargada del pètal (cm)")
    ax.grid(alpha=0.3)
axs[1].scatter(X[elimina, 0], X[elimina, 1], marker="x", color="tab:gray", s=30, label="eliminades")
axs[0].set_ylabel("Amplada del pètal (cm)")
axs[1].legend(loc="upper left", fontsize=9)
fig.suptitle("Treure flors que no són vectors de suport no mou res")
plt.tight_layout()
plt.show()
"""),
]))

# 4. El truc del kernel: el pla en 3D torna a 2D com un cercle
INSERCIONS.append(("x3 = Xc[:, 0]**2 + Xc[:, 1]**2", [
    M(r"""
No cal fiar-se de l'ull: entrenem un SVM **lineal** (sense kernel) sobre les tres
columnes $(x_1, x_2, x_3)$. Si en 3D hi ha un pla que separa, l'ha de trobar.
"""),
    C(r"""
X3 = np.column_stack([Xc, x3])
model_3d = SVC(kernel="linear", C=10).fit(X3, yc)
w3, b3 = model_3d.coef_[0], model_3d.intercept_[0]
print(f"Exactitud de l'SVM lineal en 3D: {model_3d.score(X3, yc):.1%}")
print(f"El pla: {w3[0]:.2f}·x1 {w3[1]:+.2f}·x2 {w3[2]:+.2f}·x3 {b3:+.2f} = 0")
"""),
    M(r"""
El pla és gairebé horitzontal: el pes de $x_3$ mana i els de $x_1, x_2$ són petits. Ara
el pas que ho lliga tot. Si a l'equació del pla hi tornem a posar
$x_3 = x_1^2 + x_2^2$, queda

$$w_1 x_1 + w_2 x_2 + w_3\,(x_1^2 + x_2^2) + b = 0$$

que és **l'equació d'un cercle** al pla original. Un pla en 3D, mirat des de dalt, és
una frontera circular en 2D.
"""),
    C(r"""
fig = plt.figure(figsize=(13, 5.5))

ax = fig.add_subplot(1, 2, 1, projection="3d")
ax.scatter(Xc[yc == 0, 0], Xc[yc == 0, 1], x3[yc == 0], color="tab:blue", s=10, label="classe 0")
ax.scatter(Xc[yc == 1, 0], Xc[yc == 1, 1], x3[yc == 1], color="tab:orange", s=10, label="classe 1")
p1, p2 = np.meshgrid(np.linspace(-1.3, 1.3, 20), np.linspace(-1.3, 1.3, 20))
ax.plot_surface(p1, p2, (-b3 - w3[0] * p1 - w3[1] * p2) / w3[2], color="tab:green", alpha=0.3)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_zlabel("$x_3 = x_1^2 + x_2^2$")
ax.set_title("En 3D: un pla (verd) separa les dues classes")
ax.view_init(elev=12, azim=-55)
ax.legend(loc="upper left")

ax2 = fig.add_subplot(1, 2, 2)
g1, g2 = np.meshgrid(np.linspace(-1.4, 1.4, 300), np.linspace(-1.4, 1.4, 300))
pla_en_2d = w3[0] * g1 + w3[1] * g2 + w3[2] * (g1**2 + g2**2) + b3
ax2.contour(g1, g2, pla_en_2d, levels=[0], colors="tab:green", linewidths=2.5)
ax2.scatter(Xc[yc == 0, 0], Xc[yc == 0, 1], color="tab:blue", s=10)
ax2.scatter(Xc[yc == 1, 0], Xc[yc == 1, 1], color="tab:orange", s=10)
ax2.plot([], [], color="tab:green", linewidth=2.5, label="el mateix pla, en 2D")
ax2.set_aspect("equal")
ax2.set_xlabel("$x_1$")
ax2.set_ylabel("$x_2$")
ax2.set_title("Tornat a 2D: el pla és un cercle")
ax2.legend(loc="upper right")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),
    M(r"""
I una versió que **es pot girar amb el ratolí** (Plotly; a Colab ja hi és). Mireu-la
arran de terra, de costat: es veu el pla passant entre els dos pisos de punts. Després
mireu-la des de dalt: torna el cercle.
"""),
    C(r"""
import plotly.graph_objects as go

fig3d = go.Figure()
for classe, color in [(0, "#1f77b4"), (1, "#ff7f0e")]:
    sel = yc == classe
    fig3d.add_trace(go.Scatter3d(x=Xc[sel, 0], y=Xc[sel, 1], z=x3[sel], mode="markers",
                                 marker=dict(size=3, color=color), name=f"classe {classe}"))
fig3d.add_trace(go.Surface(x=p1, y=p2, z=(-b3 - w3[0] * p1 - w3[1] * p2) / w3[2],
                           colorscale=[[0, "green"], [1, "green"]], opacity=0.35,
                           showscale=False, name="pla"))
fig3d.update_layout(scene=dict(xaxis_title="x1", yaxis_title="x2", zaxis_title="x3 = x1² + x2²"),
                    width=750, height=550, margin=dict(l=0, r=0, t=40, b=0),
                    title="Gira'm: el pla que separa els dos cercles")
fig3d.show()
"""),
]))

# 5. C (lineal) i gamma (paisatge 3D)
INSERCIONS.append(("Fixa't en la cantonada `C=100, gamma=50`", [
    M(r"""
Separem els dos efectes. Primer `C` sol, amb un SVM lineal i unes dades inventades on les dues classes es toquen
una mica. Amb `C` petit, l'SVM accepta punts dins del carrer (i algun al costat
equivocat) a canvi d'un carrer ample. Amb `C` gran, el carrer s'estreny fins que
gairebé no hi queda ningú a dins. Els cercles vermells són els vectors de suport: amb
marge tou, també ho són els punts que han entrat al carrer.
"""),
    C(r"""
rng = np.random.default_rng(5)
X_il = np.vstack([rng.normal([0, 0], 0.9, (40, 2)), rng.normal([2.6, 2.2], 0.9, (40, 2))])
y_il = np.array([0] * 40 + [1] * 40)

fig, axs = plt.subplots(1, 3, figsize=(15, 4.8), sharey=True)
g1, g2 = np.meshgrid(np.linspace(-2.5, 5, 300), np.linspace(-2.5, 4.5, 300))
for ax, C_il in zip(axs, [0.01, 1, 100]):
    m_il = SVC(kernel="linear", C=C_il).fit(X_il, y_il)
    valor = m_il.decision_function(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape)
    ax.contourf(g1, g2, valor, levels=[-1, 1], colors=["gold"], alpha=0.35)
    ax.contour(g1, g2, valor, levels=[-1, 0, 1], colors="k", linestyles=["--", "-", "--"])
    ax.scatter(X_il[y_il == 0, 0], X_il[y_il == 0, 1], color="tab:blue", edgecolor="k", s=25)
    ax.scatter(X_il[y_il == 1, 0], X_il[y_il == 1, 1], color="tab:orange", edgecolor="k", s=25)
    ax.scatter(m_il.support_vectors_[:, 0], m_il.support_vectors_[:, 1], s=130,
               facecolors="none", edgecolors="tab:red", linewidths=1.5)
    ax.set_title(f"C = {C_il}: {len(m_il.support_)} vectors de suport\n"
                 f"amplada del carrer = {2 / np.linalg.norm(m_il.coef_[0]):.2f}")
    ax.set_xlabel("$x_1$")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("$x_2$")
fig.suptitle("Dades inventades: com més gran és C, més estret és el carrer")
plt.tight_layout()
plt.show()
"""),
    M(r"""
I ara `gamma`. Per veure què fa per dins, mirem la funció de decisió com un **paisatge**:
l'altura de cada punt del pla és el valor que el model hi calcula
(`decision_function`), i la frontera és la corba on el paisatge creua l'altura 0. Cada
punt d'entrenament hi aporta un turó (o un clot) amb forma de campana; `gamma` diu com
d'estreta és la campana. Amb `gamma` petit, les campanes són amples i se sumen en un
paisatge suau. Amb `gamma` gran, cada punt fa la seva agulla i el paisatge s'arruga.
"""),
    C(r"""
g1, g2 = np.meshgrid(np.linspace(-1.6, 1.6, 120), np.linspace(-1.6, 1.6, 120))
fig = plt.figure(figsize=(14, 5.5))
for k, gamma in enumerate([0.1, 50]):
    m = SVC(kernel="rbf", C=1, gamma=gamma).fit(Xg_tr, yg_tr)
    alt = m.decision_function(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape)
    ax = fig.add_subplot(1, 2, k + 1, projection="3d")
    ax.plot_surface(g1, g2, alt, cmap="coolwarm", alpha=0.85, linewidth=0)
    ax.contour(g1, g2, alt, levels=[0], colors="k", offset=alt.min() - 0.3, linewidths=2)
    ax.contourf(g1, g2, alt, levels=[alt.min() - 1, 0, alt.max() + 1], colors=["tab:blue", "tab:red"],
                alpha=0.15, offset=alt.min() - 0.3)
    ax.set_zlim(alt.min() - 0.3, alt.max())
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_zlabel("funció de decisió")
    ax.set_title(f"gamma = {gamma}\n(a terra, la frontera: on el paisatge val 0)")
    ax.view_init(elev=30, azim=-60)
    ax.set_box_aspect(None, zoom=0.85)
plt.tight_layout()
plt.show()
"""),
]))

# ------------------------------------------------------- exercicis
INSERCIONS.append(("### Exercici 1 — Calcula un marge", [
    M(r"""
Abans de començar, la idea en un dibuix (dades inventades): una recta qualsevol, la
distància de **cada** punt a la recta (els segments) i el marge, que és **la més curta
de totes**. És el que fa `distancia(...).min()`.
"""),
    C(r"""
rng = np.random.default_rng(11)
X_il = np.vstack([rng.normal([1, 1], 0.45, (12, 2)), rng.normal([3.5, 3], 0.45, (12, 2))])
w_il, b_il = np.array([1.0, 0.6]), -3.6               # una recta inventada

d_il = distancia(w_il, b_il, X_il)
peus_il = X_il - ((X_il @ w_il + b_il) / (w_il @ w_il))[:, None] * w_il
k_il = d_il.argmin()

fig, ax = plt.subplots(figsize=(7, 6))
for p, q in zip(X_il, peus_il):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="tab:gray", alpha=0.5)
ax.plot([X_il[k_il, 0], peus_il[k_il, 0]], [X_il[k_il, 1], peus_il[k_il, 1]],
        color="tab:red", linewidth=3, label=f"la més curta = marge = {d_il[k_il]:.2f}")
ax.scatter(X_il[:12, 0], X_il[:12, 1], color="tab:blue", edgecolor="k", zorder=3)
ax.scatter(X_il[12:, 0], X_il[12:, 1], color="tab:orange", edgecolor="k", zorder=3)
x1_l = np.linspace(-0.5, 5, 2)
ax.plot(x1_l, (-b_il - w_il[0] * x1_l) / w_il[1], color="black", label="la recta")
ax.set_aspect("equal")
ax.set_xlim(-0.5, 5)
ax.set_ylim(-0.5, 4.5)
ax.set_title("Dades inventades: el marge és la distància més curta")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.show()
"""),
]))

INSERCIONS.append(("### Exercici 2 — Quants vectors de suport?", [
    M(r"""
Abans de començar, la idea en un dibuix (dades inventades, dues columnes perquè es
pugui dibuixar): els vectors de suport són les files de `support_vectors_`, i comptar-los
és mirar quantes files té. El percentatge és sobre el total de mostres amb què has
entrenat.
"""),
    C(r"""
rng = np.random.default_rng(21)
X_il = np.vstack([rng.normal([0, 0], 0.8, (30, 2)), rng.normal([3, 2], 0.8, (30, 2))])
y_il = np.array([0] * 30 + [1] * 30)
m_il = SVC(kernel="linear").fit(X_il, y_il)
n_sv_il = m_il.support_vectors_.shape[0]

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.scatter(X_il[y_il == 0, 0], X_il[y_il == 0, 1], color="tab:blue", edgecolor="k")
ax.scatter(X_il[y_il == 1, 0], X_il[y_il == 1, 1], color="tab:orange", edgecolor="k")
ax.scatter(m_il.support_vectors_[:, 0], m_il.support_vectors_[:, 1], s=200,
           facecolors="none", edgecolors="tab:red", linewidths=2, label="support_vectors_")
ax.set_title(f"Dades inventades: support_vectors_.shape = {m_il.support_vectors_.shape}\n"
             f"{n_sv_il} de {len(X_il)} mostres = {n_sv_il / len(X_il):.0%}")
ax.legend()
ax.grid(alpha=0.3)
plt.show()
"""),
]))

INSERCIONS.append(("### Exercici 3 — Compara kernels", [
    M(r"""
Abans de començar, la idea en un dibuix: com es mesura l'**exactitud de test** que
posareu a la taula. Dades inventades i un sol model: s'entrena amb els punts petits
(entrenament) i es puntua amb els grans (test). Les creus negres són els punts de test
on el model s'equivoca; l'exactitud és la fracció de punts de test sense creu.
"""),
    C(r"""
rng = np.random.default_rng(31)
X_il = np.vstack([rng.normal([0, 0], 1.0, (60, 2)), rng.normal([2.2, 1.8], 1.0, (60, 2))])
y_il = np.array([0] * 60 + [1] * 60)
Xi_tr, Xi_te, yi_tr, yi_te = train_test_split(X_il, y_il, test_size=0.3, random_state=0, stratify=y_il)
m_il = SVC(kernel="linear").fit(Xi_tr, yi_tr)
mal_il = m_il.predict(Xi_te) != yi_te

fig, ax = plt.subplots(figsize=(7, 6))
g1, g2 = np.meshgrid(np.linspace(-3, 5, 200), np.linspace(-3, 5, 200))
ax.contourf(g1, g2, m_il.predict(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape),
            alpha=0.15, cmap="coolwarm")
ax.scatter(Xi_tr[:, 0], Xi_tr[:, 1], c=yi_tr, cmap="coolwarm", s=12, alpha=0.6, label="entrenament")
ax.scatter(Xi_te[:, 0], Xi_te[:, 1], c=yi_te, cmap="coolwarm", s=70, edgecolors="k", label="test")
ax.scatter(Xi_te[mal_il, 0], Xi_te[mal_il, 1], marker="x", color="black", s=120, linewidths=2,
           label="errors de test")
ax.set_title(f"Dades inventades: {mal_il.sum()} errors de {len(yi_te)} -> "
             f"exactitud de test = {m_il.score(Xi_te, yi_te):.1%}")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.show()
"""),
]))

INSERCIONS.append(("### Exercici 4 — La millor combinació de C i gamma", [
    M(r"""
Abans de començar, la idea en un dibuix: com es llegeix el resultat d'una graella.
Cada casella és una combinació de `C` i `gamma`, i el número és la mitjana de la
validació creuada (`cv_results_["mean_test_score"]`). Els números d'aquest dibuix
**són inventats**: només serveixen per veure on mirar. La casella guanyadora és la que
`GridSearchCV` posa a `best_params_`.
"""),
    C(r"""
rng = np.random.default_rng(41)
Cs_il = [0.1, 1, 10, 100]
gammes_il = [0.01, 0.1, 1, 10]
# una muntanya inventada amb soroll: no té res a veure amb els cercles
lc, lg = np.meshgrid(np.log10(Cs_il), np.log10(gammes_il), indexing="ij")
notes_il = 0.9 - 0.04 * (lc - 0.6) ** 2 - 0.05 * (lg + 0.4) ** 2 + rng.normal(0, 0.01, lc.shape)
i_il, j_il = np.unravel_index(notes_il.argmax(), notes_il.shape)

fig, ax = plt.subplots(figsize=(7, 5.5))
im = ax.imshow(notes_il, cmap="viridis")
for i in range(len(Cs_il)):
    for j in range(len(gammes_il)):
        ax.text(j, i, f"{notes_il[i, j]:.3f}", ha="center", va="center",
                color="white" if notes_il[i, j] < notes_il.mean() else "black")
ax.add_patch(plt.Rectangle((j_il - 0.5, i_il - 0.5), 1, 1, fill=False, edgecolor="tab:red", linewidth=3))
ax.set_xticks(range(len(gammes_il)), [str(g) for g in gammes_il])
ax.set_yticks(range(len(Cs_il)), [str(c) for c in Cs_il])
ax.set_xlabel("gamma")
ax.set_ylabel("C")
ax.set_title("Números inventats: la casella vermella seria best_params_")
fig.colorbar(im, ax=ax, label="exactitud mitjana (validació creuada)")
plt.show()
"""),
]))


# ------------------------------------------------------------------ inserir
def text(c):
    return "".join(c["source"])


def main():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    cells = [c for c in nb["cells"] if c.get("metadata", {}).get("grafic") != MARCA]
    for ancora, noves in INSERCIONS:
        idx = [i for i, c in enumerate(cells) if ancora in text(c)]
        if len(idx) != 1:
            raise SystemExit(f"Ancoratge no trobat o repetit ({len(idx)}): {ancora!r}")
        cells[idx[0] + 1:idx[0] + 1] = noves
    nb["cells"] = cells
    io.open(RUTA, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    print(f"{RUTA}: {len(cells)} cel.les ({sum(len(n) for _, n in INSERCIONS)} afegides)")


if __name__ == "__main__":
    main()
