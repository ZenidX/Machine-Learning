"""
DEMO DE CLASE - Launcher visual (Tkinter)
==========================================

Ventana con botones grandes que lanzan cada agente RL en una ventana
separada. Pensado para presentar la asignatura en clase.

Uso:
    cd "Reinforcement Learning"
    python demo_launcher.py
"""

from __future__ import annotations

import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk


ROOT = Path(__file__).parent.resolve()


# Cada entrada: (titulo_corto, descripcion, nombre_funcion_en_demo_clase)
JUEGOS = [
    ("CartPole",    "Palo equilibrista  -  el 'hola mundo' del RL",   "demo_cartpole"),
    ("FlappyBird",  "Pajaro que esquiva tuberias",                    "demo_flappybird"),
    ("Nibbler",     "Snake autonomo - aprende a comer sin morir",     "demo_nibbler"),
    ("LunarLander", "Aterrizaje lunar - control con motores",         "demo_lunarlander"),
    ("Racing",      "4 coches aprendiendo en paralelo",               "demo_racing"),
]


# Estado global: solo permitimos UNA demo abierta a la vez (Pygame OOM si no).
_proceso_activo: subprocess.Popen | None = None
_botones: list[tk.Button] = []
_textos_originales: dict[tk.Button, str] = {}


def _bloquear_todos(boton_activo: tk.Button) -> None:
    for b in _botones:
        if b is boton_activo:
            b.config(state="disabled", text=_textos_originales[b] + "  (corriendo...)")
        else:
            b.config(state="disabled")


def _desbloquear_todos() -> None:
    for b in _botones:
        b.config(state="normal", text=_textos_originales[b])


def lanzar(nombre_funcion: str, boton: tk.Button) -> None:
    """Lanza la demo en un subprocess y bloquea los demas botones."""
    global _proceso_activo
    if _proceso_activo is not None and _proceso_activo.poll() is None:
        return  # ya hay una demo corriendo, ignorar

    _bloquear_todos(boton)

    # Subprocess para que la ventana Pygame/Gym no choque con Tkinter.
    _proceso_activo = subprocess.Popen(
        [sys.executable, "-c", f"from demo_clase import {nombre_funcion}; {nombre_funcion}()"],
        cwd=str(ROOT),
    )

    def vigilar():
        global _proceso_activo
        if _proceso_activo is not None and _proceso_activo.poll() is None:
            boton.after(500, vigilar)
        else:
            _proceso_activo = None
            _desbloquear_todos()

    boton.after(500, vigilar)


def construir_ventana() -> tk.Tk:
    root = tk.Tk()
    root.title("Demo Machine Learning & Reinforcement Learning")
    root.geometry("640x520")
    root.configure(bg="#1e1e2e")
    root.resizable(False, False)

    # Cabecera
    cabecera = tk.Frame(root, bg="#1e1e2e")
    cabecera.pack(fill="x", padx=30, pady=(30, 10))

    tk.Label(
        cabecera,
        text="Demo  ML  &  Reinforcement Learning",
        font=("Segoe UI", 18, "bold"),
        fg="#cdd6f4",
        bg="#1e1e2e",
    ).pack()

    tk.Label(
        cabecera,
        text="Cinco agentes que han aprendido solos a jugar",
        font=("Segoe UI", 11, "italic"),
        fg="#a6adc8",
        bg="#1e1e2e",
    ).pack(pady=(4, 0))

    # Separador
    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=30, pady=10)

    # Botones grandes para cada juego
    contenedor = tk.Frame(root, bg="#1e1e2e")
    contenedor.pack(fill="both", expand=True, padx=30, pady=(0, 10))

    estilo_btn = dict(
        font=("Segoe UI", 12),
        bg="#313244",
        fg="#cdd6f4",
        activebackground="#45475a",
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=15,
        pady=12,
        anchor="w",
        cursor="hand2",
    )

    for titulo, descripcion, funcion in JUEGOS:
        texto = f"  {titulo}   -   {descripcion}"
        boton = tk.Button(contenedor, text=texto, **estilo_btn)
        boton.config(command=lambda f=funcion, b=boton: lanzar(f, b))
        boton.pack(fill="x", pady=4)
        _botones.append(boton)
        _textos_originales[boton] = texto

    # Pie con boton de salir
    pie = tk.Frame(root, bg="#1e1e2e")
    pie.pack(fill="x", padx=30, pady=(0, 20))

    tk.Button(
        pie,
        text="Salir",
        font=("Segoe UI", 11),
        bg="#f38ba8",
        fg="#1e1e2e",
        activebackground="#eba0ac",
        relief="flat",
        bd=0,
        padx=20,
        pady=6,
        cursor="hand2",
        command=root.destroy,
    ).pack(side="right")

    return root


def main() -> int:
    root = construir_ventana()
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
