"""
Ejemplo: Clasificación de dígitos MNIST con MLP
===============================================
Ejemplo completo de entrenamiento de un Perceptrón Multicapa.
"""

import sys
sys.path.append('..')

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from core import MLP, Entrenador, EarlyStopping
from core.utils import visualizar_metricas, guardar_modelo, set_seed, get_device
from core.entrenamiento import crear_optimizador, crear_scheduler


def main():
    # =========================================================================
    # 1. CONFIGURACIÓN
    # =========================================================================
    set_seed(42)
    device = get_device()

    # Hiperparámetros
    BATCH_SIZE = 64
    EPOCHS = 30
    LEARNING_RATE = 0.001
    HIDDEN_SIZES = [256, 128, 64]
    DROPOUT = 0.3

    # =========================================================================
    # 2. CARGAR DATOS
    # =========================================================================
    print("\n" + "="*50)
    print("CARGANDO DATOS MNIST")
    print("="*50)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # Media y std de MNIST
    ])

    train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_data = datasets.MNIST('./data', train=False, download=True, transform=transform)

    # Split train/val
    train_size = int(0.8 * len(train_data))
    val_size = len(train_data) - train_size
    train_data, val_data = torch.utils.data.random_split(train_data, [train_size, val_size])

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)

    print(f"Train: {len(train_data)} muestras")
    print(f"Val: {len(val_data)} muestras")
    print(f"Test: {len(test_data)} muestras")

    # =========================================================================
    # 3. CREAR MODELO
    # =========================================================================
    print("\n" + "="*50)
    print("CREANDO MODELO MLP")
    print("="*50)

    # MNIST: 28x28 = 784 pixels de entrada, 10 clases de salida
    modelo = MLP(
        input_size=784,
        hidden_sizes=HIDDEN_SIZES,
        output_size=10,
        dropout=DROPOUT,
        activation='relu'
    )
    modelo = modelo.to(device)

    print(f"\nArquitectura:")
    print(f"  Input: 784 (28x28 pixels)")
    print(f"  Hidden: {HIDDEN_SIZES}")
    print(f"  Output: 10 (dígitos 0-9)")
    print(f"  Dropout: {DROPOUT}")
    print(f"\nParámetros totales: {modelo.count_parameters():,}")

    # =========================================================================
    # 4. CONFIGURAR ENTRENAMIENTO
    # =========================================================================
    print("\n" + "="*50)
    print("CONFIGURANDO ENTRENAMIENTO")
    print("="*50)

    # Loss function
    loss_fn = nn.CrossEntropyLoss()

    # Optimizador
    optimizador = crear_optimizador(
        modelo,
        tipo='adam',
        lr=LEARNING_RATE,
        weight_decay=1e-5
    )

    # Scheduler
    scheduler = crear_scheduler(
        optimizador,
        tipo='plateau',
        factor=0.5,
        patience=3
    )

    # Early stopping
    early_stopping = EarlyStopping(
        patience=7,
        min_delta=0.001,
        mode='min',
        restore_best=True
    )

    print(f"Optimizador: Adam (lr={LEARNING_RATE})")
    print(f"Scheduler: ReduceLROnPlateau")
    print(f"Early Stopping: patience=7")

    # =========================================================================
    # 5. ENTRENAR
    # =========================================================================
    print("\n" + "="*50)
    print("INICIANDO ENTRENAMIENTO")
    print("="*50)

    entrenador = Entrenador(
        modelo=modelo,
        optimizador=optimizador,
        loss_fn=loss_fn,
        device=device,
        scheduler=scheduler
    )

    historial = entrenador.fit(
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=EPOCHS,
        early_stopping=early_stopping,
        verbose=True
    )

    # =========================================================================
    # 6. EVALUAR
    # =========================================================================
    print("\n" + "="*50)
    print("EVALUACIÓN EN TEST SET")
    print("="*50)

    test_metrics = entrenador.evaluate(test_loader)
    print(f"Test Loss: {test_metrics['loss']:.4f}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.2f}%")

    # =========================================================================
    # 7. VISUALIZAR Y GUARDAR
    # =========================================================================
    print("\n" + "="*50)
    print("GUARDANDO RESULTADOS")
    print("="*50)

    # Visualizar curvas
    visualizar_metricas(historial, save_path='../../modelos/mnist_mlp_training.png')

    # Guardar modelo
    guardar_modelo(
        modelo,
        '../../modelos/mnist_mlp.pth',
        optimizador=optimizador,
        historial=historial,
        test_accuracy=test_metrics['accuracy']
    )

    print("\n¡Entrenamiento completado!")


if __name__ == "__main__":
    main()
