# -*- coding: utf-8 -*-
"""
Jutge del Concurs de RL — Gran Premi Racing
=============================================
Carrega agents entrenats pels alumnes (xarxes CarDQN de racing_game.py),
els avalua contra la pista i genera el marcador. També organitza la
Gran Cursa Final: tots els cotxes classificats corrent alhora en pantalla.

Format de lliurament (obligatori):
    Cada alumne entrega un fitxer "agent.pth" amb l'state_dict d'una
    xarxa CarDQN(state_size=6, n_acciones=9) tal com la defineix
    03_proyectos_dqn/racing/racing_game.py. No es toca l'arquitectura
    (6 -> 128 -> 128 -> 9): si es canvia, el jutge no podrà carregar-lo.

    torch.save(agent.q_network.state_dict(), "agent.pth")

Estructura esperada per als comandaments --marcador i --cursa-final:
    lliuraments/
      alba/agent.pth
      bernat/agent.pth
      ...

Ús:
    # Avaluar un sol agent (l'alumne, per provar abans d'entregar)
    python avalua_agent.py --model lliuraments/alba/agent.pth

    # Generar el marcador de tota la classe
    python avalua_agent.py --marcador lliuraments/ --sortida marcador.csv

    # Gran Cursa Final amb els 6 millors + professor + agent aleatori
    python avalua_agent.py --cursa-final lliuraments/ --top 6 --render

Veure el README.md d'aquesta carpeta per al reglament complet.
"""
import argparse
import csv
import random
import sys
from pathlib import Path

import numpy as np
import torch

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # sys.stdout ja no és un TextIOWrapper (p.ex. dins d'un notebook)

AQUI = Path(__file__).resolve().parent
RACING_DIR = AQUI.parent / "03_proyectos_dqn" / "racing"
MODELOS_DIR = AQUI.parent / "modelos"
sys.path.insert(0, str(RACING_DIR))

import racing_game as rg  # noqa: E402 (necessita el sys.path.insert d'abans)

ARXIU_AGENT = "agent.pth"              # nom fix que ha de tenir el lliurament de cada alumne
STATE_SIZE = 6
N_ACCIONS = 9
EPISODIS_DEFECTE = 5
LLAVORS_DEFECTE = (0, 1, 2, 3, 4)
MAX_PASSOS_DEFECTE = 2000              # mateix límit que fa servir l'entrenament original
TOP_DEFECTE = 6                        # + professor + aleatori = 8 cotxes (colors definits al joc)
AGENT_PROFESSOR = MODELOS_DIR / "car_agent_0.pth"   # línia base; substituir per un de millor si cal


def sembra(llavor):
    """Sembra tots els generadors d'atzar. L'avaluació és determinista (epsilon=0,
    física sense atzar), així que això és més aviat una xarxa de seguretat: si
    algú fa servir mostreig estocàstic en lloc d'argmax, els episodis seguiran
    sent reproduïbles i comparables."""
    random.seed(llavor)
    np.random.seed(llavor)
    torch.manual_seed(llavor)


class AgentEntrenat:
    """Embolcalla una xarxa CarDQN ja entrenada amb política determinista (argmax)."""

    def __init__(self, path, device="cpu"):
        self.origen = str(path)
        self.device = torch.device(device)
        self.xarxa = rg.CarDQN(STATE_SIZE, N_ACCIONS).to(self.device)
        estat = torch.load(path, map_location=self.device)
        self.xarxa.load_state_dict(estat)
        self.xarxa.eval()

    def act(self, state):
        with torch.no_grad():
            t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            return int(self.xarxa(t).argmax().item())


class AgentAleatori:
    """Referència del marcador: tria accions a l'atzar, sense aprendre res."""

    origen = "(aleatori)"

    def act(self, state):
        return random.randint(0, N_ACCIONS - 1)


def carregar_agent(path):
    try:
        return AgentEntrenat(path)
    except Exception as e:
        raise RuntimeError(
            f"No s'ha pogut carregar '{path}' com CarDQN({STATE_SIZE}, {N_ACCIONS}). "
            f"Comprova que sigui un state_dict fet amb "
            f"torch.save(xarxa.state_dict(), ...) i que no s'hagi tocat "
            f"l'arquitectura de la xarxa. Error original: {e}"
        ) from e


def jugar_solo(controlador, llavor, max_passos=MAX_PASSOS_DEFECTE, render=False):
    """Fa competir un sol agent contra la pista durant com a molt max_passos."""
    sembra(llavor)
    joc = rg.RacingGame(n_cars=1, render=render)
    estats = joc.reset()
    passos = 0
    aturat = False
    try:
        while passos < max_passos and not aturat:
            if render:
                for event in rg.pygame.event.get():
                    if event.type == rg.pygame.QUIT:
                        aturat = True
            accio = controlador.act(estats[0])
            estats, _, _, all_done = joc.step([accio])
            passos += 1
            if render:
                joc.render()
                joc.clock.tick(60)
            if all_done:
                break
        cotxe = joc.cars[0]
        resultat = {
            "fitness": cotxe.fitness,
            "distancia": cotxe.distance,
            "voltes": cotxe.laps,
            "checkpoint": cotxe.checkpoint,
            "passos_viu": passos,
            "va_xocar": not cotxe.alive,
        }
    finally:
        joc.close()
    return resultat


def avaluar_agent(path_o_controlador, nom=None, n_episodis=EPISODIS_DEFECTE,
                   llavors=LLAVORS_DEFECTE, max_passos=MAX_PASSOS_DEFECTE, render=False):
    """Avalua un agent (ruta a .pth, o un controlador ja instanciat com AgentAleatori)."""
    if isinstance(path_o_controlador, (str, Path)):
        controlador = carregar_agent(path_o_controlador)
        nom = nom or Path(path_o_controlador).parent.name
    else:
        controlador = path_o_controlador
        nom = nom or "agent"

    llavors_us = list(llavors)[:n_episodis]
    while len(llavors_us) < n_episodis:
        llavors_us.append((llavors_us[-1] + 1) if llavors_us else 0)

    episodis = [jugar_solo(controlador, ll, max_passos=max_passos, render=render)
                for ll in llavors_us]

    return {
        "nom": nom,
        "fitness_mitjana": float(np.mean([e["fitness"] for e in episodis])),
        "voltes_max": max(e["voltes"] for e in episodis),
        "passos_viu_mitjana": float(np.mean([e["passos_viu"] for e in episodis])),
        "n_xocs": sum(e["va_xocar"] for e in episodis),
        "episodis": episodis,
    }


def imprimeix_resultat(resultat):
    print(f"\n--- {resultat['nom']} ---")
    for i, ep in enumerate(resultat["episodis"]):
        estat = "XOC" if ep["va_xocar"] else "TEMPS ESGOTAT"
        print(f"  Episodi {i + 1}: fitness={ep['fitness']:8.1f}  voltes={ep['voltes']}  "
              f"passos={ep['passos_viu']:4d}  ({estat})")
    print(f"  Fitness mitjana: {resultat['fitness_mitjana']:.1f}  |  "
          f"Voltes (millor): {resultat['voltes_max']}  |  "
          f"Xocs: {resultat['n_xocs']}/{len(resultat['episodis'])}")


def avaluar_lliuraments(carpeta_lliuraments, n_episodis=EPISODIS_DEFECTE,
                         max_passos=MAX_PASSOS_DEFECTE):
    """Avalua totes les subcarpetes amb agent.pth. Retorna la llista ordenada
    (només alumnes, sense les referències del professor/aleatori)."""
    carpeta = Path(carpeta_lliuraments)
    resultats = []
    for subcarpeta in sorted(p for p in carpeta.iterdir() if p.is_dir()):
        model = subcarpeta / ARXIU_AGENT
        if not model.exists():
            print(f"[AVÍS] {subcarpeta.name}: no té {ARXIU_AGENT}, es descarta")
            continue
        try:
            r = avaluar_agent(model, nom=subcarpeta.name, n_episodis=n_episodis,
                               max_passos=max_passos)
        except Exception as e:
            print(f"[ERROR] {subcarpeta.name}: {e}")
            continue
        resultats.append(r)
    resultats.sort(key=_clau_ordre)
    return resultats


def avaluar_referencies(n_episodis=EPISODIS_DEFECTE, max_passos=MAX_PASSOS_DEFECTE):
    """Puntua la línia base del professor i l'agent aleatori, per situar el
    marcador: qui no els supera encara no ha après res útil."""
    refs = []
    if AGENT_PROFESSOR.exists():
        refs.append(avaluar_agent(AGENT_PROFESSOR, nom="Professor (línia base)",
                                   n_episodis=n_episodis, max_passos=max_passos))
    else:
        print(f"[AVÍS] No es troba la línia base del professor a {AGENT_PROFESSOR}")
    refs.append(avaluar_agent(AgentAleatori(), nom="Agent aleatori",
                               n_episodis=n_episodis, max_passos=max_passos))
    return refs


def _clau_ordre(r):
    return (-r["fitness_mitjana"], -r["voltes_max"], -r["passos_viu_mitjana"])


def _imprimeix_taula(resultats, titol):
    print("\n" + "=" * 74)
    print(f"  {titol}")
    print("=" * 74)
    print(f"{'#':>3} {'Nom':<28} {'Fitness':>10} {'Voltes':>7} {'Passos viu':>11} {'Xocs':>6}")
    for i, r in enumerate(resultats, 1):
        print(f"{i:>3} {r['nom']:<28} {r['fitness_mitjana']:>10.1f} {r['voltes_max']:>7} "
              f"{r['passos_viu_mitjana']:>11.1f} {r['n_xocs']:>6}")


def construir_marcador(carpeta_lliuraments, n_episodis=EPISODIS_DEFECTE,
                        max_passos=MAX_PASSOS_DEFECTE, sortida_csv=None):
    resultats = avaluar_lliuraments(carpeta_lliuraments, n_episodis, max_passos)
    resultats += avaluar_referencies(n_episodis, max_passos)
    resultats.sort(key=_clau_ordre)

    _imprimeix_taula(resultats, "MARCADOR")

    if sortida_csv:
        with open(sortida_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["posicio", "nom", "fitness_mitjana", "voltes_max",
                        "passos_viu_mitjana", "n_xocs"])
            for i, r in enumerate(resultats, 1):
                w.writerow([i, r["nom"], f"{r['fitness_mitjana']:.1f}", r["voltes_max"],
                            f"{r['passos_viu_mitjana']:.1f}", r["n_xocs"]])
        print(f"\nMarcador desat a: {sortida_csv}")

    return resultats


def _dibuixa_noms(joc, noms):
    """Afegeix a la finestra un rètol amb el nom de cada alumne (RacingGame ja
    dibuixa 'Car N: ...' a l'esquerra; això és la llegenda de la dreta)."""
    for i, (nom, cotxe) in enumerate(zip(noms, joc.cars)):
        color = cotxe.color if cotxe.alive else (100, 100, 100)
        text = f"{i + 1}. {nom}"
        rendered = joc.font.render(text, True, color)
        joc.screen.blit(rendered, (joc.screen.get_width() - 260, 10 + i * 20))
    rg.pygame.display.flip()


def cursa_final(participants, max_passos=MAX_PASSOS_DEFECTE, render=True):
    """participants: llista de (nom, controlador) ja carregats. Els fa competir
    tots alhora en una sola cursa i imprimeix la classificació final."""
    if len(participants) > len(rg.CAR_COLORS):
        sobren = len(participants) - len(rg.CAR_COLORS)
        print(f"[AVÍS] Només es distingeixen {len(rg.CAR_COLORS)} colors; "
              f"es descarten els {sobren} últims classificats.")
        participants = participants[:len(rg.CAR_COLORS)]

    noms = [n for n, _ in participants]
    controladors = [c for _, c in participants]
    n_cars = len(participants)

    print("\n" + "=" * 74)
    print("  GRAN CURSA FINAL")
    print("=" * 74)
    for i, nom in enumerate(noms, 1):
        print(f"  Cotxe {i}: {nom}")

    joc = rg.RacingGame(n_cars=n_cars, render=render)
    estats = joc.reset()
    passos = 0
    aturat = False

    while passos < max_passos and not aturat:
        if render:
            for event in rg.pygame.event.get():
                if event.type == rg.pygame.QUIT:
                    aturat = True
                elif event.type == rg.pygame.KEYDOWN and event.key == rg.pygame.K_ESCAPE:
                    aturat = True

        accions = [c.act(s) for c, s in zip(controladors, estats)]
        estats, _, _, all_done = joc.step(accions)
        passos += 1

        if render:
            joc.render()
            _dibuixa_noms(joc, noms)
            joc.clock.tick(60)

        if all_done:
            break

    classificacio = sorted(
        zip(noms, joc.cars),
        key=lambda nc: (-nc[1].fitness, -nc[1].laps, -nc[1].time_alive),
    )

    print("\n" + "-" * 74)
    print("  CLASSIFICACIÓ")
    print("-" * 74)
    for pos, (nom, cotxe) in enumerate(classificacio, 1):
        estat = "viu" if cotxe.alive else "fora de pista"
        print(f"  {pos:>2}. {nom:<28} fitness={cotxe.fitness:8.1f}  "
              f"voltes={cotxe.laps}  ({estat})")

    joc.close()
    return classificacio


def gran_cursa_final(carpeta_lliuraments, top=TOP_DEFECTE, max_passos=MAX_PASSOS_DEFECTE,
                      render=True, n_episodis_classificacio=EPISODIS_DEFECTE):
    """Classifica tots els lliuraments i fa competir els `top` millors alumnes
    contra la línia base del professor i l'agent aleatori."""
    carpeta = Path(carpeta_lliuraments)
    classificats = avaluar_lliuraments(carpeta, n_episodis_classificacio, max_passos)[:top]

    participants = [
        (r["nom"], carregar_agent(carpeta / r["nom"] / ARXIU_AGENT))
        for r in classificats
    ]
    if AGENT_PROFESSOR.exists():
        participants.append(("Professor (línia base)", carregar_agent(AGENT_PROFESSOR)))
    participants.append(("Agent aleatori", AgentAleatori()))

    return cursa_final(participants, max_passos=max_passos, render=render)


def main():
    parser = argparse.ArgumentParser(
        description="Jutge del concurs de RL (Racing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    grup = parser.add_mutually_exclusive_group(required=True)
    grup.add_argument("--model", type=str, help="Avalua un sol agent .pth")
    grup.add_argument("--marcador", type=str,
                       help="Carpeta amb una subcarpeta per alumne, cadascuna amb agent.pth")
    grup.add_argument("--cursa-final", type=str,
                       help="Carpeta de lliuraments: classifica i fa la Gran Cursa Final")
    parser.add_argument("--episodis", type=int, default=EPISODIS_DEFECTE,
                         help=f"Episodis per agent (per defecte {EPISODIS_DEFECTE})")
    parser.add_argument("--max-passos", type=int, default=MAX_PASSOS_DEFECTE,
                         help=f"Límit de passos per episodi (per defecte {MAX_PASSOS_DEFECTE})")
    parser.add_argument("--top", type=int, default=TOP_DEFECTE,
                         help=f"Nombre d'alumnes que passen a la Gran Cursa Final (per defecte {TOP_DEFECTE})")
    parser.add_argument("--sortida", type=str, default=None, help="Fitxer CSV per al marcador")
    parser.add_argument("--render", action="store_true",
                         help="Mostra la finestra de pygame (cal pantalla; a la classificació "
                              "per lot normalment es deixa apagat)")
    args = parser.parse_args()

    if args.model:
        r = avaluar_agent(args.model, n_episodis=args.episodis, max_passos=args.max_passos,
                           render=args.render)
        imprimeix_resultat(r)
    elif args.marcador:
        construir_marcador(args.marcador, n_episodis=args.episodis, max_passos=args.max_passos,
                            sortida_csv=args.sortida)
    elif args.cursa_final:
        gran_cursa_final(args.cursa_final, top=args.top, max_passos=args.max_passos,
                          render=args.render, n_episodis_classificacio=args.episodis)


if __name__ == "__main__":
    main()
