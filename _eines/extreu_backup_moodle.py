# -*- coding: utf-8 -*-
"""Reconstrueix els fitxers d'un backup de Moodle (.mbz ja extret).

Moodle desa els fitxers a `files/<2 primers caracters del hash>/<hash>` i el
mapatge hash -> nom real es a `files.xml`. Aquest script el desfa i copia cada
fitxer amb el seu nom, organitzat per activitat.

    python extreu_backup_moodle.py <carpeta_extreta> <carpeta_desti>
"""
import io
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def net(s, maxlen=90):
    """Nom de fitxer segur a Windows."""
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", (s or "").strip())
    s = re.sub(r"\s+", " ", s).strip(". ")
    return (s or "sense_nom")[:maxlen]


def titols_activitats(arrel):
    """cmid/contextid -> (tipus, titol) llegint els module.xml i els .xml propis."""
    per_context = {}
    dir_act = os.path.join(arrel, "activities")
    if not os.path.isdir(dir_act):
        return per_context
    for carpeta in os.listdir(dir_act):
        ruta = os.path.join(dir_act, carpeta)
        if not os.path.isdir(ruta):
            continue
        tipus = carpeta.split("_")[0]
        ctx = None
        titol = None
        fmod = os.path.join(ruta, "module.xml")
        if os.path.isfile(fmod):
            try:
                r = ET.parse(fmod).getroot()
                ctx = r.get("contextid")
            except ET.ParseError:
                pass
        for f in os.listdir(ruta):
            if f.endswith(".xml") and f != "module.xml":
                try:
                    r = ET.parse(os.path.join(ruta, f)).getroot()
                    n = r.find(".//name")
                    if n is not None and n.text:
                        titol = n.text
                        break
                except ET.ParseError:
                    continue
        if ctx:
            per_context[ctx] = (tipus, titol or carpeta)
    return per_context


def main(arrel, desti):
    fitxers_xml = os.path.join(arrel, "files.xml")
    if not os.path.isfile(fitxers_xml):
        print("No hi ha files.xml a", arrel)
        return 1

    contextos = titols_activitats(arrel)
    root = ET.parse(fitxers_xml).getroot()

    copiats, saltats, perduts = 0, 0, 0
    resum = defaultdict(list)

    for f in root.findall("file"):
        def camp(n):
            e = f.find(n)
            return e.text if e is not None and e.text else ""

        nom = camp("filename")
        if not nom or nom == ".":
            saltats += 1
            continue
        chash = camp("contenthash")
        ctx = camp("contextid")
        component = camp("component")
        mida = int(camp("filesize") or 0)
        if mida == 0:
            saltats += 1
            continue

        origen = os.path.join(arrel, "files", chash[:2], chash)
        if not os.path.isfile(origen):
            perduts += 1
            continue

        tipus, titol = contextos.get(ctx, (component or "altres", "context_" + ctx))
        carpeta = net(f"{tipus} - {titol}", 70)
        dir_final = os.path.join(desti, carpeta)
        os.makedirs(dir_final, exist_ok=True)

        final = os.path.join(dir_final, net(nom))
        base, ext = os.path.splitext(final)
        i = 2
        while os.path.exists(final):
            final = f"{base} ({i}){ext}"
            i += 1

        shutil.copy2(origen, final)
        copiats += 1
        resum[carpeta].append((net(nom), mida))

    print(f"Copiats: {copiats} | saltats (buits): {saltats} | sense contingut: {perduts}\n")
    for carpeta in sorted(resum):
        tot = sum(m for _, m in resum[carpeta])
        print(f"{carpeta}  ({len(resum[carpeta])} fitxers, {tot/1024:.0f} KB)")
        for n, m in sorted(resum[carpeta])[:6]:
            print(f"    {n}  ({m/1024:.0f} KB)")
        if len(resum[carpeta]) > 6:
            print(f"    ... i {len(resum[carpeta]) - 6} mes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
