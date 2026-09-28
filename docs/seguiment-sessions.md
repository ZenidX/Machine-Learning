# Seguiment de sessions — Optativa de Machine Learning

Diari del curs 2026-27: què s'ha fet de veritat a cada sessió i on es reprèn. **No és el pla, és
el registre.**

El pla és a [`diagnostic-i-programacio-2627.md`](diagnostic-i-programacio-2627.md) i els guions
de sessió als fitxers `guions-bloc-*.md`.

**Calendari:** 33 sessions de 2 h, dilluns i dimarts, del **21 de setembre de 2026** al **2 de
febrer de 2027**. Descomptats el 12 d'octubre, el 8 de desembre i les vacances de Nadal.

> **Correcció del 29 de setembre.** Aquest diari i tot el calendari donaven per fet que les
> classes havien començat el **14 de setembre**. Van començar el **21**. Ho ha corregit en Xavi, i
> ha canviat la numeració de totes les sessions i les dates de tot el curs: el que abans era la
> S06 és ara la S04, i el concurs passa del 26 de gener al 2 de febrer.

---

## S01 · dilluns 21 de setembre · Presentació i bases de Python

Presentació de com anirà el mòdul, i introducció teòrica a les bases de Python amb una mica de
pràctica. **Es van repartir els primers enunciats d'exercicis de Python.**

Materials del curs passat, a `_moodle-25-26/teoria-python/` (carpeta local, no publicada):
`tipus_dades_variables.pdf`, `cadenes_de_text_llibreries.pdf` i `condicionals.pdf`.

**Un fet del primer dia que condiciona la programació sencera:** l'optativa es va anunciar com a
**difícil**, a posta, i tot i això s'hi han quedat **15 alumnes**. És un grup que ve pel nivell, i
el que els enganxa és entendre la matemàtica de sota. Hi ha el raonament a la secció 1.4 del
diagnòstic.

## S02 · dimarts 22 de setembre · Els models de machine learning, explorats

**Les dues hores senceres** explorant els diferents models de machine learning, perquè es
quedessin amb **les formes del comportament** de cadascun. El quadern d'Iris ho ensenya molt bé, i
va ser el fil de la sessió.

**Conseqüència que s'arrossega:** van sortir amb la intuïció dels models i sense l'eina per
fer-los servir. És el diagnòstic del curs, i el que justifica que el bloc següent siguin els
fonaments de dades i no més models.

## S03 · dilluns 28 de setembre · Pràctica de Python i primer contacte amb els exercicis

Pràctica de Python amb una mica de teoria dels models, i llançar-los contra els exercicis de
`02_practica/`.

**No va acabar de funcionar, i val la pena tenir les dues raons separades**, perquè les dues han
provocat canvis al material:

1. **Els faltava el manual per gestionar dades.** No sabien que `dades.data` existeix, ni que
   `df.shape` va sense parèntesis, ni que un model entrenat guarda el que ha après en atributs
   acabats en guió baix. I sobretot no sabien **com esbrinar-ho**: que a un objecte de Python se
   li pot preguntar què té a dins. D'aquí surt la sessió del 29.
2. **Van pensar que les solucions eren dins del mateix enunciat.** I hi eren: les línies de «com
   saps que ho has fet bé» donaven el resultat que havien de descobrir. Arreglat, amb el criteri
   escrit a [`didactica-matematica-ml.md`](didactica-matematica-ml.md).

I una tercera cosa que va sortir d'aquí: **fer-los endevinar quina funció fer servir no ensenya
res.** L'enunciat diu quina eina toca; el que no diu és quin resultat surt.

---

## S04 · dimarts 29 de setembre · Objectes de Python i primera anàlisi de dades — *la d'avui*

**Toca:** `Machine Learning/01_fonaments/FO_00_objectes_i_autocompletar.ipynb`. Guió a
[`guions-bloc-1-fonaments.md`](guions-bloc-1-fonaments.md), que porta la frase per obrir la
sessió reconeixent què va passar dilluns.

**Fet:** _(per omplir després de la sessió)_

---

## Com omplir aquest diari

Una entrada per sessió, amb tres coses i prou:

- **Fet:** què es va cobrir de veritat, no què estava previst.
- **On es reprèn:** el punt exacte del quadern o del PDF.
- **Observació:** només si hi ha alguna cosa que canviï el pla. Si no, no cal.

Quan una sessió es desvia del pla, **anota-ho aquí i mira si cal tocar el pla**, no només el
diari. Les tres primeres sessions d'aquest curs són l'exemple: cadascuna ha canviat alguna cosa
del material. Els punts on la programació es pot trencar, i què fer en cada cas, són a la secció
2.5 del diagnòstic.

---

## Encara pendent de resoldre

**La data de final del mòdul.** Amb 66 h a 4 h setmanals des del 21 de setembre, el curs arriba
al **2 de febrer**. Si ha d'acabar el gener, hi caben 31 sessions, o sigui **62 h**, i falten 4 h.
**Cal confirmar-ho abans d'anunciar el concurs a l'alumnat**, perquè les dues últimes sessions de
taller són les que es perdrien.

**Els pesos de l'avaluació.** La fitxa oficial diu 10 % proves escrites, 10 % activitats i 80 %
proves pràctiques; la presentació que es va passar al grup el curs 25-26 deia 60 % proves escrites
en paper i 40 % projectes. **Mentre no es confirmi, ni la web ni cap document donen percentatges.**

La contradicció de les hores **està resolta**: són 66 h a 4 h setmanals, o sigui 33 sessions.

**Material de la docent anterior.** Les seves presentacions de Google viuen al seu Drive i els
enllaços funcionen mentre ella els mantingui compartits. Convé demanar-li'n còpia abans de
dependre'n. La llista és a `_moodle-25-26/ENLLACOS.md`.

**La sessió de k-means (S25)** és l'únic forat de material que queda a la programació.
