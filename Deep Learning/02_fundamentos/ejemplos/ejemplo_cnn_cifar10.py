"""
Ejemplo: Clasificación CIFAR-10 con CNN
=======================================
Red Convolucional para clasificación de imágenes en color.
"""

import sys
sys.path.append('..')

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from core import CNN, Entrenador, EarlyStopping
from core.utils import (
    visualizar_metricas, visualizar_predicciones, guardar_modelo,
    set_seed, get_device
)
from core.entrenamiento import crear_optimizador, crear_scheduler


# Nombres de las clases CIFAR-10
CIFAR10_CLASSES = [
    'avión', 'automóvil', 'pájaro', 'gato', 'ciervo',
    'perro', 'rana', 'caballo', 'barco', 'camión'
]


def main():
    # =========================================================================
    # 1. CONFIGURACIÓN
    # =========================================================================
    set_seed(42)
    device = get_device()

    # Hiperparámetros
    BATCH_SIZE = 128
    EPOCHS = 50
    LEARNING_RATE = 0.001

    # =========================================================================
    # 2. CARGAR DATOS CON DATA AUGMENTATION
    # =========================================================================
    print("\n" + "="*50)
    print("CARGANDO DATOS CIFAR-10")
    print("="*50)

    # Data augmentation para entrenamiento
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
    ])

    # Sin augmentation para test
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
    ])

    train_full = datasets.CIFAR10('./data', train=True, download=True, transform=transform_train)
    test_data = datasets.CIFAR10('./data', train=False, download=True, transform=transform_test)

    # Split train/val
    train_size = int(0.9 * len(train_full))
    val_size = len(train_full) - train_size
    train_data, val_data = torch.utils.data.random_split(train_full, [train_size, val_size])

    # Para validación usar transform sin augmentation
    val_data.dataset.transform = transform_test

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print(f"Train: {len(train_data)} imágenes")
    print(f"Val: {len(val_data)} imágenes")
    print(f"Test: {len(test_data)} imágenes")
    print(f"Clases: {CIFAR10_CLASSES}")

    # =========================================================================
    # 3. CREAR MODELO CNN
    # =========================================================================
    print("\n" + "="*50)
    print("CREANDO MODELO CNN")
    print("="*50)

    modelo = CNN(
        in_channels=3,        # RGB
        num_classes=10,       # 10 categorías
        conv_channels=[32, 64, 128],  # 3 bloques convolucionales
        fc_sizes=[256],       # 1 capa fully connected
        dropout=0.3,
        input_size=32         # Imágenes 32x32
    )
    modelo = modelo.to(device)

    print("\nArquitectura:")
    print("  Input: 3x32x32 (RGB)")
    print("  Conv Blocks: [32, 64, 128] canales")
    print("  FC: [256, 10]")
    print(f"\nParámetros totales: {modelo.count_parameters():,}")

    # =========================================================================
    # 4. CONFIGURAR ENTRENAMIENTO
    # =========================================================================
    print("\n" + "="*50)
    print("CONFIGURANDO ENTRENAMIENTO")
    print("="*50)

    loss_fn = nn.CrossEntropyLoss()

    optimizador = crear_optimizador(
        modelo,
        tipo='adamw',  # AdamW mejor para CNNs
        lr=LEARNING_RATE,
        weight_decay=1e-4
    )

    scheduler = crear_scheduler(
        optimizador,
        tipo='cosine',
        T_max=EPOCHS
    )

    early_stopping = EarlyStopping(
        patience=10,
        min_delta=0.001,
        mode='min',
        restore_best=True
    )

    print(f"Optimizador: AdamW (lr={LEARNING_RATE})")
    print(f"Scheduler: CosineAnnealing")
    print(f"Early Stopping: patience=10")

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
    # 7. VISUALIZAR RESULTADOS
    # =========================================================================
    print("\n" + "="*50)
    print("VISUALIZANDO RESULTADOS")
    print("="*50)

    # Curvas de entrenamiento
    visualizar_metricas(historial, save_path='../../modelos/cifar10_cnn_training.png')

    # Predicciones
    visualizar_predicciones(
        modelo,
        test_loader,
        class_names=CIFAR10_CLASSES,
        num_images=16,
        device=device
    )

    # Guardar modelo
    guardar_modelo(
        modelo,
        '../../modelos/cifar10_cnn.pth',
        optimizador=optimizador,
        historial=historial,
        test_accuracy=test_metrics['accuracy'],
        classes=CIFAR10_CLASSES
    )

    print("\n¡Entrenamiento completado!")


if __name__ == "__main__":
    main()
