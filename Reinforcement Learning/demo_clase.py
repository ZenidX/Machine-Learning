"""
DEMO DE CLASE — Machine Learning y Reinforcement Learning
==========================================================

Launcher con menu interactivo que abre 5 agentes ya entrenados jugando.

Pensado para la sesion de presentacion de la asignatura:
sin slides, sin teoria. Solo agentes en accion.

Uso:
    cd "Reinforcement Learning"
    python demo_clase.py

Pulsa 1..5 para abrir cada juego. ESC dentro del juego para cerrar y
volver al menu. 'q' en el menu para salir.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.resolve()
MODELOS = ROOT / "modelos"


# ---------- utilidades de presentacion ----------

def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu() -> None:
    limpiar_pantalla()
    print(
        r"""
+==============================================================+
|                                                              |
|       DEMO  -  MACHINE LEARNING & REINFORCEMENT LEARNING     |
|                                                              |
|       Cinco agentes que han aprendido solos a jugar.         |
|       Nadie les ha programado las reglas.                    |
|                                                              |
+==============================================================+
|                                                              |
|   [1]  CartPole     -  Palo equilibrista  (el "hola mundo")  |
|                                                              |
|   [2]  FlappyBird   -  Pajaro entre tuberias                 |
|                                                              |
|   [3]  Nibbler      -  Snake autonomo                        |
|                                                              |
|   [4]  LunarLander  -  Aterrizaje lunar                      |
|                                                              |
|   [5]  Racing       -  4 coches aprendiendo en paralelo      |
|                                                              |
|   [q]  Salir                                                 |
|                                                              |
+==============================================================+
"""
    )


def pausa(msg: str = "Pulsa ENTER para volver al menu...") -> None:
    try:
        input(f"\n{msg}")
    except (EOFError, KeyboardInterrupt):
        pass


# ---------- demo 1: CartPole (Gymnasium + DQN cargado a mano) ----------

def demo_cartpole() -> None:
    """CartPole-v1 con la red entrenada en modelos/cartpole_dqn.pth."""
    import torch
    import torch.nn as nn
    import gymnasium as gym

    modelo = MODELOS / "cartpole_dqn.pth"
    if not modelo.exists():
        print(f"[ERROR] Falta {modelo}")
        pausa()
        return

    class DQNetwork(nn.Module):
        def __init__(self):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(4, 128), nn.ReLU(),
                nn.Linear(128, 128), nn.ReLU(),
                nn.Linear(128, 2),
            )

        def forward(self, x):
            return self.network(x)

    net = DQNetwork()
    checkpoint = torch.load(str(modelo), map_location="cpu", weights_only=False)
    # El .pth guarda {'q_network': state_dict, 'target_network': ..., ...}
    state_dict = checkpoint["q_network"] if isinstance(checkpoint, dict) and "q_network" in checkpoint else checkpoint
    net.load_state_dict(state_dict)
    net.eval()

    print("\n>>> CartPole - El palo equilibrista")
    print("    Cierra la ventana o pulsa Ctrl+C para volver al menu.\n")

    env = gym.make("CartPole-v1", render_mode="human")
    try:
        for episodio in range(1, 11):
            obs, _ = env.reset()
            total = 0
            done = False
            while not done:
                with torch.no_grad():
                    q = net(torch.from_numpy(obs).float().unsqueeze(0))
                    accion = int(q.argmax(dim=1).item())
                obs, recompensa, term, trunc, _ = env.step(accion)
                total += recompensa
                done = term or trunc
            print(f"  Episodio {episodio}: {total:.0f} pasos sin caer")
    except KeyboardInterrupt:
        pass
    finally:
        env.close()
    pausa()


# ---------- demo 2: FlappyBird (SB3 DQN) ----------

def demo_flappybird() -> None:
    """FlappyBird-v0 con el PPO entrenado por demo_entrenar.py."""
    import gymnasium as gym
    import flappy_bird_gymnasium  # noqa: F401
    from stable_baselines3 import PPO

    modelo = MODELOS / "flappybird_ppo.zip"
    if not modelo.exists():
        print(f"[ERROR] Falta {modelo}")
        print("    Ejecuta: python demo_entrenar.py flappybird")
        pausa()
        return

    print("\n>>> FlappyBird - El pajaro que esquiva tuberias")
    print("    Cierra la ventana o pulsa Ctrl+C para volver al menu.\n")

    env = gym.make("FlappyBird-v0", render_mode="human", use_lidar=False)
    model = PPO.load(str(modelo), env=env)
    try:
        for episodio in range(1, 6):
            obs, _ = env.reset()
            total = 0.0
            done = False
            while not done:
                accion, _ = model.predict(obs, deterministic=True)
                obs, recompensa, term, trunc, _ = env.step(int(accion))
                total += float(recompensa)
                done = term or trunc
            print(f"  Episodio {episodio}: recompensa {total:.1f}")
    except KeyboardInterrupt:
        pass
    finally:
        env.close()
    pausa()


# ---------- demo 3: Nibbler (subprocess al script existente) ----------

def demo_nibbler() -> None:
    """Llama al script nibbler_game.py --demo (necesita el .pth en su carpeta)."""
    carpeta = ROOT / "03_proyectos_dqn" / "nibbler"
    origen = MODELOS / "nibbler_best.pth"
    destino = carpeta / "nibbler_best.pth"

    if not origen.exists():
        print(f"[ERROR] Falta {origen}")
        pausa()
        return

    if not destino.exists():
        shutil.copy(origen, destino)

    print("\n>>> Nibbler - Snake autonomo")
    print("    ESC en la ventana para volver al menu.\n")

    subprocess.run(
        [sys.executable, "nibbler_game.py", "--demo"],
        cwd=str(carpeta),
    )
    pausa()


# ---------- demo 4: LunarLander (SB3 PPO) ----------

def demo_lunarlander() -> None:
    """LunarLander-v3 con el PPO entrenado por demo_entrenar.py."""
    import gymnasium as gym
    from stable_baselines3 import PPO

    modelo = MODELOS / "lunarlander_ppo.zip"
    if not modelo.exists():
        print(f"[ERROR] Falta {modelo}")
        print("    Ejecuta: python demo_entrenar.py lunarlander")
        pausa()
        return

    print("\n>>> LunarLander - Aterrizaje lunar")
    print("    Cierra la ventana o pulsa Ctrl+C para volver al menu.\n")

    env = gym.make("LunarLander-v3", render_mode="human")
    model = PPO.load(str(modelo), env=env)
    try:
        for episodio in range(1, 6):
            obs, _ = env.reset()
            total = 0.0
            done = False
            while not done:
                accion, _ = model.predict(obs, deterministic=True)
                obs, recompensa, term, trunc, _ = env.step(int(accion))
                total += float(recompensa)
                done = term or trunc
            veredicto = "aterrizaje" if total > 100 else "estrellado" if total < 0 else "regular"
            print(f"  Episodio {episodio}: recompensa {total:.1f}  ({veredicto})")
    except KeyboardInterrupt:
        pass
    finally:
        env.close()
    pausa()


# ---------- demo 5: Racing (subprocess al script existente) ----------

def demo_racing() -> None:
    """Llama al script racing_game.py --demo con los 4 .pth copiados."""
    carpeta = ROOT / "03_proyectos_dqn" / "racing"

    for i in range(4):
        origen = MODELOS / f"car_agent_{i}.pth"
        destino = carpeta / f"car_agent_{i}.pth"
        if origen.exists() and not destino.exists():
            shutil.copy(origen, destino)

    print("\n>>> Racing - 4 coches aprendiendo en paralelo")
    print("    ESC en la ventana para volver al menu.\n")

    subprocess.run(
        [sys.executable, "racing_game.py", "--demo"],
        cwd=str(carpeta),
    )
    pausa()


# ---------- bucle principal ----------

OPCIONES = {
    "1": ("CartPole", demo_cartpole),
    "2": ("FlappyBird", demo_flappybird),
    "3": ("Nibbler", demo_nibbler),
    "4": ("LunarLander", demo_lunarlander),
    "5": ("Racing", demo_racing),
}


def main() -> int:
    while True:
        mostrar_menu()
        try:
            eleccion = input("  Elige una opcion: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if eleccion in ("q", "quit", "exit", "salir"):
            print("\nFin de la demo. Hasta la proxima.")
            return 0

        if eleccion not in OPCIONES:
            print("  Opcion no valida.")
            pausa()
            continue

        nombre, funcion = OPCIONES[eleccion]
        try:
            funcion()
        except Exception as exc:
            print(f"\n[ERROR] La demo de {nombre} ha fallado: {exc}")
            pausa()


if __name__ == "__main__":
    sys.exit(main())
