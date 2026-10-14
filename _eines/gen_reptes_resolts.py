# -*- coding: utf-8 -*-
"""Genera els reptes resolts públics (04_reptes/resolts/) a partir dels solucionaris privats.

Decisió del 14-oct-2026: la versió resolta de cada repte es publica i s'enllaça des de la pàgina
de Recursos. Els solucionaris de `04_reptes/solucions/` continuen fora del repositori (hi ha els
generadors i, de vegades, notes per al professor); aquest script en fa una còpia neta:

- treu el bàner de «no publicar», la caixa d'eines, les pistes plegades, les comprovacions, les
  caixes «Quan cridar en Xavi», el lliurament i les tasques obertes «La teva pregunta»;
- posa al costat de cada resultat l'enunciat de la tasca (de la versió amb bastida, que es guarda
  a `solucions/bastides/`), perquè el resolt s'entengui sol;
- canvia la veu de professor («Per al professor», «Solucionari», «han de descobrir...») per la
  d'un quadern resolt;
- afegeix una conclusió als reptes que no en tenien;
- i comprova que no queda cap rastre privat (proves, notes privades, datasets reservats).

Cal executar-lo en local, amb els solucionaris al seu lloc:

    python _eines/gen_reptes_resolts.py
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_reptes_enunciat import REPTES  # noqa: E402

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPTES_DIR = os.path.join(ARREL, "Machine Learning", "04_reptes")
SOL = os.path.join(REPTES_DIR, "solucions")
BASTIDES = os.path.join(SOL, "bastides")
DESTI = os.path.join(REPTES_DIR, "resolts")

PER_ID = {r["id"]: r for r in REPTES}

BANNER = ("> **Repte resolt.** Una manera de resoldre'l, no l'única. Els números del text surten d'una "
          "execució real del quadern.")

# Frases amb veu de professor -> veu de quadern resolt
SUBSTITUCIONS = [
    ("**Per al professor.** Coses que haurien de sortir:", "**Comentari.** El que hi ha:"),
    ("**Per al professor.**", "**Comentari.**"),
    ("> **Solucionari.**", "> **Resultat.**"),
    ("Al 2023 hi havia zeros explícits (fitxa 3.4).", "Al 2023 hi havia zeros explícits (ho veuràs al RE_302)."),
    (" És la discussió de la caixa del Xavi.", ""),
    (" Que la variable més útil sigui l'olor és la troballa que han de fer ells; no se'ls diu.", ""),
    ("Aquí hi ha la discussió que volem:", "Aquí hi ha la discussió de fons:"),
    (" Que l'ordre entre models canviï (o no) amb la quantitat de dades és el que han de descobrir: "
     "els números són a la sortida de la cel·la.", ""),
    ("ve d'una sola columna: és bo que ho vegin ells mateixos en la descomposició.",
     "ve d'una sola columna, com es veu a la descomposició."),
    ("Aquesta és la troballa del repte: no se'ls dona.", "Aquesta és la troballa del repte."),
    ("El solucionari els deixa:", "Aquí es deixen:"),
    ("Que ho vegin al gràfic és la clau", "El gràfic és la clau"),
    ("Si algú ho troba, cal felicitar-lo per no haver «forçat» la conclusió esperada.",
     "Trobar-ho i dir-ho, sense forçar la conclusió esperada, també és part de la feina."),
    ("El que es valora és l'argument.", "El que compta és l'argument."),
    ("Cada alumne ha de fer-ho amb el seu municipi.", "Fes-ho amb el teu municipi."),
    ("Si no treuen les repetides", "Si no es treuen les repetides"),
    ("Si no normalitzen", "Si no es normalitza"),
    ("el test deixa de ser un examen", "el test ja no mesura res de nou"),
]

# Rastres que no poden arribar mai a un resolt públic
PROHIBIT = re.compile(
    r"Pp\s?\d|notes-privades|notes privades|privad|professor|NO PUBLICAR|no es publica|solucionari|"
    r"se'ls|alumn|Incendis|Pima|Diamonds|Telco|dataset reservat|datasets reservats|recuperació|examen",
    re.IGNORECASE)

CONCLUSIONS = {
    "RE_201": """Sí que es pot decidir amb un model: els 22 trets separen les dues classes gairebé del tot. Un
arbre de profunditat 5 ja encerta el 99,9 % del test i amb profunditat 7 arriba al 100 %; el kNN
també hi arriba, però no s'explica a ningú. El primer tall és l'olor (`odor_n`, «sense olor») i treu
el 62 % de la impuresa de l'arrel (Gini 0,4994 → 0,1897). L'error perillós és dir comestible un
bolet verinós: l'arbre de profunditat 3 en fa 3 al test (*recall* 0,9969), i en una app això no és
acceptable. Cal la profunditat més petita que en faci zero, i dir clar que zero al test no és zero
al bosc.""",
    "RE_202": """La logística supera el model que no diu mai «compra» (0,884 contra 0,845 de precisió), i la
millora es veu molt més clara amb la log-loss (0,305 contra 0,431). La probabilitat calculada a mà,
$z = Xw + b$ i la sigmoide, coincideix amb `predict_proba`. Una sola variable fa gairebé tota la
feina: `PageValues` (pes 1,54, *odds* × 4,7 per desviació típica), i `ExitRates` és la que més empeny
en contra (*odds* × 0,45). Sense `PageValues` el model cau per sota de la línia de sortida, i com
que es calcula amb les pàgines vistes abans d'una transacció, no es coneix a mitja sessió: abans de
posar el model en un tauler, cal decidir si es pot fer servir en el moment d'actuar.""",
    "RE_203": """Només un 11,7 % dels clients contracta, i per això la precisió no serveix: el model que no truca
mai ja en fa 0,883. Amb el llindar de 0,5, la logística i el bosc empaten (F1 0,28, *recall* 0,18) i
gairebé no truquen ningú. La diferència surt a la corba *precision-recall* (AP 0,413 el bosc i
0,380 la logística; l'atzar, 0,124), que és la que parla el llenguatge de la directora. Amb 5 € per
trucada i 50 € per contracte, el benefici màxim surt amb un llindar de 0,15: unes 2.400 trucades,
més de la meitat dels «sí» trobats i uns 25.000 € al test, contra uns 9.600 € trucant a tothom. Si
canvien els costos, canvia el llindar, no el model.""",
    "RE_204": """Es pot prometre un error d'uns 4,4 MPa: és el MAE de test de l'arbre amb la profunditat triada
per validació creuada (15), mesurat una sola vegada al final. L'arbre sense límit s'equivoca 0,06 MPa
a l'entrenament i gairebé 5 al test: aquesta distància és memòria, no aprenentatge. El kNN queda per
darrere (6,8 MPa), i escalar-lo gairebé no canvia res perquè sense escalar ja manava l'edat, que és
la columna més útil (deixar-la sense escalar el baixa a 5,37). La recta fa 7,99 MPa perquè la
resistència no creix en línia recta amb l'edat; amb `log(age)` baixa a 5,54.""",
    "RE_205": """El millor model és el bosc, amb un MAE d'unes 89 bicis per hora quan s'entrena amb el 2011 i es
prova amb el 2012. La recta amb l'hora com a número es queda a 130, i amb l'hora en one-hot a 110:
els laborables tenen dos pics (8 h i 17-18 h) que una recta amb un sol pes per a l'hora no pot
dibuixar. La partició aleatòria donaria la meitat d'error (45), però és enganyosa, perquè el model
veu dies veïns dels del test i no ha de preveure el futur. L'error té signe: el model es queda curt
tots els mesos del 2012 (+84 bicis per hora de mitjana), perquè el servei va créixer i només ha vist
el 2011. La xifra per a logística és la temporal, amb l'avís que cal reentrenar amb dades recents.""",
    "RE_206": """Hem auditat una regressió logística que encerta el 85,5 % (el model que diu sempre «no», el
76,1 %). El model no tracta igual dones i homes: de les persones que sí que guanyen més de 50K, en
troba el 50,6 % de les dones i el 61,3 % dels homes. Treure `sex` i `race` gairebé no canvia res
(TPR 0,525 contra 0,604), perquè el sexe es dedueix d'altres columnes, sobretot de `relationship`
(es prediu amb un 85 % d'encert). Per grups ètnics, la diferència del grup `Black` (TPR 0,49 contra
0,61 de `White`) és sòlida, però `Other` i `Amer-Indian-Eskimo` tenen massa pocs casos per treure'n
conclusions. Recomanació: no engegar el model sense decidir quina mesura d'equitat s'exigeix,
mesurar-la per grups amb la mida al costat, i no confiar que amagar l'atribut protegit ho resol.""",
    "RE_401": """Proposem **dos tipus de clients**, fets amb k-means sobre la despesa amb logaritme i
estandarditzada: un que compra sobretot frescos i congelats (el perfil d'un restaurant o un hotel) i
un altre que compra ultramarins, llet i detergents (el perfil d'una botiga). Sense logaritme la
silueta és més alta (0,57), però els grups són 49 «grans clients» contra 391, i amb més grups en
surten d'1 a 4 clients: k-means separa *outliers*, no tipus de client. Els grups amb logaritme
s'assemblen força a `Channel` (ARI 0,51) i els de sense logaritme, no (0,21). La preparació de les
dades ha pesat més que la tria de k; k = 3 seria una alternativa raonable.""",
    "RE_402": """Hi ha molta informació diferent, però no s'organitza en pocs eixos: amb les dades
estandarditzades la primera component explica només un 18 % i calen 8 de 12 components per arribar
al 80 %. Sense escalar, el PCA diu el contrari (una component amb gairebé el 100 %), però només
perquè `duration_ms` va en mil·lisegons. Els grups de k-means no són estils clars: la silueta no
passa de 0,15 per a cap k, i amb 6 grups cap no és un gènere (ARI ≈ 0,06). El gènere és de la
playlist, una etiqueta cultural que el so només explica en part; el més semblant a un gènere són un
grup de veu parlada (rap) i un d'instrumental (edm).""",
    "RE_403": """Amb 13 indicadors relatius del 2024 (947 municipis, sense la fila del total de Catalunya), els
municipis formen un continu més que no pas grups nets (silueta màxima 0,19). Les dues primeres
components expliquen el 42 %: la primera va de ciutat dormitori densa a poble de segona residència,
i la segona, de turisme de masses a micropoble agrari. Amb k = 4 surten quatre tipus: micropobles en
declivi, pobles rurals, municipis turístics i municipis urbans i metropolitans. Sant Cugat del Vallès
cau al grup urbà, però els seus veïns al mapa de dues components no s'hi assemblen; amb tots els
indicadors, sí. El mapa de dues components és per mirar, no per mesurar.""",
}

RE_TASCA = re.compile(r"^(#{2,3}) (\d\.\d) · (.*)$")


def font(c):
    return "".join(c["source"])


def posa(c, text):
    c["source"] = text.splitlines(True)
    return c


def neteja_enunciat(text):
    """Treu les pistes plegades i les comprovacions d'un enunciat de tasca."""
    text = re.sub(r"<details>.*?</details>\s*", "", text, flags=re.S)
    text = re.sub(r"\*\*Comprova(?:ció:\*\*|\.\*\*).*?(?=\n\n|\Z)", "", text, flags=re.S)
    return text.strip()


def enunciats_bastida(rid):
    """{'1.1': text de la tasca} de la versió antiga amb bastida."""
    rutes = glob.glob(os.path.join(BASTIDES, rid + "_*.ipynb"))
    if not rutes:
        return {}
    nb = json.load(open(rutes[0], encoding="utf-8"))
    tasques = {}
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        s = font(c)
        m = RE_TASCA.match(s.splitlines()[0]) if s else None
        if m:
            tasques[m.group(2)] = neteja_enunciat(s)
    return tasques


def converteix(ruta):
    rid = os.path.basename(ruta)[:6]
    r = PER_ID[rid]
    nb = json.load(open(ruta, encoding="utf-8"))
    tasques = enunciats_bastida(rid)
    sortida = []
    saltant = False
    titol_fet = False

    for c in nb["cells"]:
        s = font(c)
        if c["cell_type"] == "code":
            if not saltant:
                c["outputs"], c["execution_count"] = [], None
                sortida.append(c)
            continue

        primera = s.splitlines()[0] if s else ""
        # Cel.les que no van mai al resolt
        if (primera.startswith("# SOLUCIONARI") or primera.startswith("## Caixa d'eines")
                or primera.startswith("> **Quan cridar") or primera.startswith("## Lliurament")
                or primera.startswith("**La teva resposta:**")
                or (primera.startswith("## Conclusió") and "Escriu-la aquí" in s)):
            continue

        m = RE_TASCA.match(primera)
        if m:
            saltant = "La teva pregunta" in m.group(3)
            if saltant:
                continue
            if r["bloc"] == 2:
                s = neteja_enunciat(s)
            elif m.group(2) in tasques:
                cos = tasques[m.group(2)].split("\n", 1)
                s = primera + ("\n\n" + cos[1].strip() if len(cos) > 1 else "")
        elif primera.startswith("#"):
            saltant = False
        if saltant:
            continue

        # El resolt és un nivell més avall (resolts/): els enllaços relatius han de pujar un nivell més
        s = s.replace("](../", "](../../")
        s = re.sub(r"\]\((RE_\d{3}_[^)]+\.ipynb)\)", r"](../\1)", s)

        # Títol i bàner
        if primera.startswith(f"# {rid}") and not titol_fet:
            titol_fet = True
            s = s.replace(" · solucionari", " · resolt")
            s = re.sub(r"> \*\*SOLUCIONARI[^\n]*", BANNER, s)
            if BANNER not in s:
                linies = s.split("\n\n", 2)
                linies.insert(2 if len(linies) > 2 else len(linies), BANNER)
                s = "\n\n".join(linies)
            if r["bloc"] in (3, 4):
                s += f"\n\n{r['encarrec'].strip()}\n\n**La pregunta:** {r['pregunta'].strip()}"
            s += (f"\n\nL'enunciat complet, amb el diccionari de columnes, és a "
                  f"[{r['id']}](../{r['fitxer']}). Si encara no l'has fet, fes-lo abans de llegir això.")

        for vell, nou in SUBSTITUCIONS:
            s = s.replace(vell, nou)
        sortida.append(posa(c, s))

    if rid in CONCLUSIONS:
        sortida.append({"cell_type": "markdown", "metadata": {},
                        "source": ("## Conclusió\n\n" + CONCLUSIONS[rid]).splitlines(True)})

    nom = os.path.basename(ruta).replace("_solucions.ipynb", "_resolt.ipynb")
    nb["cells"] = sortida
    nb["metadata"].setdefault("colab", {})["name"] = nom

    # Comprovació de fuites: cap rastre privat a cap cel.la
    for c in sortida:
        trobat = PROHIBIT.search(font(c))
        if trobat:
            raise SystemExit(f"{nom}: rastre privat «{trobat.group(0)}» a:\n{font(c)[:300]}")
    return nom, nb


def main():
    os.makedirs(DESTI, exist_ok=True)
    rutes = sorted(glob.glob(os.path.join(SOL, "RE_*_solucions.ipynb")))
    if not rutes:
        raise SystemExit("No hi ha solucionaris a " + SOL)
    for ruta in rutes:
        nom, nb = converteix(ruta)
        with open(os.path.join(DESTI, nom), "w", encoding="utf-8", newline="\n") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("escrit resolts/" + nom)


if __name__ == "__main__":
    main()
