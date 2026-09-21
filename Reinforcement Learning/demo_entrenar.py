"""
Entrenamiento rápido para la demo de clase.

Entrena dos agentes con Stable-Baselines3 y guarda los modelos en `modelos/`:
  - FlappyBird (DQN, ~50k steps)
  - LunarLander (PPO, ~150k steps)

Uso:
    python demo_entrenar.py flappybird
    python demo_entrenar.py lunarlander
    python demo_entrenar.py all
"""

import sys
from pathlib import Path

import gymnasium as gym
from stable_baselines3 import DQN, PPO
import flappy_bird_gymnasium  # noqa: F401  registra FlappyBird-v0


ROOT = Path(__file__).parent
MODELOS = ROOT / "modelos"
MODELOS.mkdir(exist_ok=True)


def entrenar_flappybird(timesteps: int = 400_000) -> Path:
    """FlappyBird PPO. DQN se atasca en minimos locales; PPO converge mejor."""
    print(f"\n=== Entrenando FlappyBird PPO ({timesteps:,} steps) ===")
    env = gym.make("FlappyBird-v0", use_lidar=False)
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=2.5e-4,
        n_steps=1024,
        batch_size=256,
        n_epochs=4,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        policy_kwargs={"net_arch": [128, 128]},
        verbose=1,
    )
    model.learn(total_timesteps=timesteps, progress_bar=False)
    out = MODELOS / "flappybird_ppo.zip"
    model.save(str(out))
    env.close()
    print(f"Guardado: {out}")
    return out


def entrenar_lunarlander(timesteps: int = 150_000) -> Path:
    print(f"\n=== Entrenando LunarLander PPO ({timesteps:,} steps) ===")
    env = gym.make("LunarLander-v3")
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.999,
        gae_lambda=0.98,
        ent_coef=0.01,
        verbose=1,
    )
    model.learn(total_timesteps=timesteps, progress_bar=False)
    out = MODELOS / "lunarlander_ppo.zip"
    model.save(str(out))
    env.close()
    print(f"Guardado: {out}")
    return out


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("flappybird", "all"):
        entrenar_flappybird()
    if target in ("lunarlander", "all"):
        entrenar_lunarlander()
    print("\nEntrenamiento completado.")


if __name__ == "__main__":
    main()
