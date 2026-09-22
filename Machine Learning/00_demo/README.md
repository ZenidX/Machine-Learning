# Demostració d'arrencada — «El que sabreu fer al gener»

Quadern per passar a classe just després del bloc de condicionals, quan l'alumnat encara
no sap res de machine learning. No és una activitat: és una demostració que fa el docent
executant les cel·les, i dura uns 20-25 minuts.

**Fitxer:** `ML_00_demo_iris.ipynb` · 19 cel·les, 7 de codi · funciona a Google Colab sense instal·lar res.

## La idea

El gancho és el bloc anterior. Acaben de veure `if`, `elif` i `else`, i un arbre de
decisió és exactament això: condicionals encadenats. La diferència és qui els escriu.

El quadern els fa fer el recorregut sencer en aquest ordre:

1. Miren les dades i un gràfic de les tres espècies.
2. **Classifiquen les flors a mà**, amb tres condicionals dels d'ahir. Encerten un 96 %.
3. Entrenen un arbre de decisió, que arriba al 97,8 % sense que ningú li digui cap número.
4. **Dibuixen l'arbre** i descobreixen que els llindars que ha trobat sol (2,45 i 1,75)
   són pràcticament els que ells havien triat a ull mirant el gràfic.
5. Comparen cinc models amb tres línies cadascun.
6. Miren la matriu de confusió, per veure on falla.

El punt 4 és el moment de la sessió. La resta hi porta.

## Què hi ha de dir el docent

**Al pas 2**, quan surti el 96 %: que això ho han aconseguit mirant un gràfic i triant dos
números a ull, amb 4 columnes i 150 files. Que amb 500 columnes i un milió de files ja no
poden mirar-s'ho.

**Al pas 4**, deixar-los llegir el node de dalt de l'arbre abans de dir res.

**Al pas 5**, el bosc aleatori surt *pitjor* que l'arbre sol (91 % contra 97,8 %). Està
avisat dins del quadern, però convé dir-ho en veu alta: no és cap error, és que amb un
conjunt tan petit i fàcil un model més complicat no ajuda. I que canviant el
`random_state` aquests números ballen, perquè 45 flors d'examen són molt poques.

## Comprovat

Les 7 cel·les de codi s'han executat en ordre amb scikit-learn 1.8 i pandas 2.3, sense cap
error. Els percentatges que apareixen al text del quadern són els que surten de debò.

## D'on ve

Adaptat de `intro ML - Iris Dataset.ipynb` del CE d'IA i Big Data, que cobreix els mateixos
models però en anglès, amb més profunditat i plantejat com a exercici per omplir. Aquell
servirà per al bloc 3 del curs; aquest només és l'aperitiu.
