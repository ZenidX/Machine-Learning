"""
Deep Learning - Utilidades
==========================
Funciones auxiliares para carga de datos, visualización y gestión de modelos.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List, Optional
import os


# =============================================================================
# CARGA DE DATOS
# =============================================================================

def cargar_datos(
    nombre: str = 'mnist',
    batch_size: int = 64,
    val_split: float = 0.2,
    num_workers: int = 0,
    data_dir: str = './data'
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Carga datasets comunes de forma sencilla.

    Args:
        nombre: Nombre del dataset ('mnist', 'cifar10', 'fashion_mnist')
        batch_size: Tamaño del batch
        val_split: Proporción de datos para validación
        num_workers: Workers para carga paralela
        data_dir: Directorio para guardar datos

    Returns:
        train_loader, val_loader, test_loader

    Ejemplo:
        >>> train, val, test = cargar_datos('mnist', batch_size=32)
    """
    from torchvision import datasets, transforms

    # Transformaciones según dataset
    if nombre in ['mnist', 'fashion_mnist']:
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        in_channels = 1
        input_size = 28
    else:  # cifar10, cifar100
        transform_train = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(32, padding=4),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        transform = transform_train
        in_channels = 3
        input_size = 32

    # Cargar dataset
    datasets_map = {
        'mnist': datasets.MNIST,
        'fashion_mnist': datasets.FashionMNIST,
        'cifar10': datasets.CIFAR10,
        'cifar100': datasets.CIFAR100
    }

    if nombre not in datasets_map:
        raise ValueError(f"Dataset '{nombre}' no soportado. Opciones: {list(datasets_map.keys())}")

    dataset_class = datasets_map[nombre]

    # Descargar y cargar
    train_full = dataset_class(data_dir, train=True, download=True, transform=transform)
    test_data = dataset_class(
        data_dir, train=False, download=True,
        transform=transform_test if nombre.startswith('cifar') else transform
    )

    # Split train/val
    val_size = int(len(train_full) * val_split)
    train_size = len(train_full) - val_size
    train_data, val_data = random_split(train_full, [train_size, val_size])

    # Crear DataLoaders
    train_loader = DataLoader(
        train_data, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    val_loader = DataLoader(
        val_data, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_data, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )

    # Info del dataset
    print(f"Dataset: {nombre.upper()}")
    print(f"  Train: {train_size} muestras")
    print(f"  Val: {val_size} muestras")
    print(f"  Test: {len(test_data)} muestras")
    print(f"  Input: {in_channels}x{input_size}x{input_size}")

    return train_loader, val_loader, test_loader


def crear_dataloader_numpy(
    X: np.ndarray,
    y: np.ndarray,
    batch_size: int = 32,
    shuffle: bool = True,
    val_split: float = 0.0
) -> DataLoader:
    """
    Crea DataLoader a partir de arrays NumPy.

    Args:
        X: Features (N, features) o (N, channels, height, width)
        y: Labels (N,)
        batch_size: Tamaño del batch
        shuffle: Si mezclar datos
        val_split: Si > 0, retorna tupla (train_loader, val_loader)

    Returns:
        DataLoader o tupla de DataLoaders
    """
    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.LongTensor(y)

    dataset = TensorDataset(X_tensor, y_tensor)

    if val_split > 0:
        val_size = int(len(dataset) * val_split)
        train_size = len(dataset) - val_size
        train_data, val_data = random_split(dataset, [train_size, val_size])

        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=shuffle)
        val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
        return train_loader, val_loader

    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


# =============================================================================
# VISUALIZACIÓN
# =============================================================================

def visualizar_metricas(historial: Dict[str, List[float]], save_path: str = None):
    """
    Visualiza el historial de entrenamiento.

    Args:
        historial: Diccionario con 'train_loss', 'val_loss', 'train_acc', 'val_acc'
        save_path: Ruta para guardar la figura (opcional)

    Ejemplo:
        >>> historial = entrenador.fit(train_loader, val_loader)
        >>> visualizar_metricas(historial, 'training_curves.png')
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    epochs = range(1, len(historial['train_loss']) + 1)

    # Loss
    axes[0].plot(epochs, historial['train_loss'], 'b-', label='Train')
    if 'val_loss' in historial and historial['val_loss']:
        axes[0].plot(epochs, historial['val_loss'], 'r-', label='Validation')
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Curva de Pérdida')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Accuracy
    axes[1].plot(epochs, historial['train_acc'], 'b-', label='Train')
    if 'val_acc' in historial and historial['val_acc']:
        axes[1].plot(epochs, historial['val_acc'], 'r-', label='Validation')
    axes[1].set_xlabel('Época')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Curva de Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Learning Rate
    if 'lr' in historial and historial['lr']:
        axes[2].plot(epochs, historial['lr'], 'g-')
        axes[2].set_xlabel('Época')
        axes[2].set_ylabel('Learning Rate')
        axes[2].set_title('Learning Rate Schedule')
        axes[2].set_yscale('log')
        axes[2].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figura guardada en: {save_path}")

    plt.show()


def visualizar_predicciones(
    modelo: nn.Module,
    dataloader: DataLoader,
    class_names: List[str] = None,
    num_images: int = 16,
    device: str = 'cpu'
):
    """
    Visualiza predicciones del modelo en una cuadrícula.

    Args:
        modelo: Modelo entrenado
        dataloader: DataLoader con imágenes
        class_names: Lista de nombres de clases
        num_images: Número de imágenes a mostrar
        device: Dispositivo del modelo
    """
    modelo.eval()
    images, labels = next(iter(dataloader))
    images, labels = images[:num_images], labels[:num_images]

    with torch.no_grad():
        outputs = modelo(images.to(device))
        _, preds = outputs.max(1)
        preds = preds.cpu()

    # Calcular grid
    cols = int(np.ceil(np.sqrt(num_images)))
    rows = int(np.ceil(num_images / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2.5))
    axes = axes.flatten()

    for idx in range(num_images):
        ax = axes[idx]
        img = images[idx].cpu()

        # Desnormalizar
        img = img * 0.5 + 0.5

        # Mostrar imagen
        if img.shape[0] == 1:  # Grayscale
            ax.imshow(img.squeeze(), cmap='gray')
        else:  # RGB
            ax.imshow(img.permute(1, 2, 0))

        # Título con predicción
        true_label = labels[idx].item()
        pred_label = preds[idx].item()

        if class_names:
            title = f"True: {class_names[true_label]}\nPred: {class_names[pred_label]}"
        else:
            title = f"True: {true_label}\nPred: {pred_label}"

        color = 'green' if true_label == pred_label else 'red'
        ax.set_title(title, fontsize=8, color=color)
        ax.axis('off')

    # Ocultar ejes vacíos
    for idx in range(num_images, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()


def visualizar_filtros_conv(modelo: nn.Module, layer_name: str = None, max_filters: int = 64):
    """
    Visualiza los filtros de una capa convolucional.

    Args:
        modelo: Modelo con capas convolucionales
        layer_name: Nombre de la capa (si None, usa la primera conv)
        max_filters: Máximo número de filtros a mostrar
    """
    # Encontrar la primera capa convolucional
    conv_layer = None
    for name, module in modelo.named_modules():
        if isinstance(module, nn.Conv2d):
            if layer_name is None or name == layer_name:
                conv_layer = module
                layer_name = name
                break

    if conv_layer is None:
        print("No se encontró capa convolucional")
        return

    # Obtener pesos
    weights = conv_layer.weight.data.cpu()
    num_filters = min(weights.shape[0], max_filters)

    # Calcular grid
    cols = int(np.ceil(np.sqrt(num_filters)))
    rows = int(np.ceil(num_filters / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(cols, rows))
    axes = axes.flatten()

    for idx in range(num_filters):
        ax = axes[idx]
        # Tomar primer canal si hay múltiples
        kernel = weights[idx, 0].numpy()
        ax.imshow(kernel, cmap='viridis')
        ax.axis('off')

    for idx in range(num_filters, len(axes)):
        axes[idx].axis('off')

    plt.suptitle(f'Filtros de {layer_name}', fontsize=12)
    plt.tight_layout()
    plt.show()


def matriz_confusion(
    y_true: torch.Tensor,
    y_pred: torch.Tensor,
    class_names: List[str] = None,
    normalize: bool = True
):
    """
    Muestra matriz de confusión.

    Args:
        y_true: Labels verdaderos
        y_pred: Predicciones
        class_names: Nombres de clases
        normalize: Si normalizar por fila
    """
    from sklearn.metrics import confusion_matrix
    import seaborn as sns

    y_true = y_true.cpu().numpy() if isinstance(y_true, torch.Tensor) else y_true
    y_pred = y_pred.cpu().numpy() if isinstance(y_pred, torch.Tensor) else y_pred

    cm = confusion_matrix(y_true, y_pred)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1, keepdims=True)

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='.2f' if normalize else 'd',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names
    )
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión')
    plt.tight_layout()
    plt.show()


# =============================================================================
# GESTIÓN DE MODELOS
# =============================================================================

def guardar_modelo(
    modelo: nn.Module,
    ruta: str,
    optimizador: torch.optim.Optimizer = None,
    historial: Dict = None,
    **metadata
):
    """
    Guarda modelo con checkpoint completo.

    Args:
        modelo: Modelo a guardar
        ruta: Ruta del archivo .pth
        optimizador: Optimizador (opcional)
        historial: Historial de entrenamiento (opcional)
        **metadata: Información adicional (epoch, accuracy, etc.)

    Ejemplo:
        >>> guardar_modelo(
        ...     modelo, 'best_model.pth',
        ...     optimizador=optimizer,
        ...     historial=historial,
        ...     epoch=50,
        ...     val_acc=95.5
        ... )
    """
    checkpoint = {
        'model_state_dict': modelo.state_dict(),
        'model_class': modelo.__class__.__name__,
    }

    if optimizador is not None:
        checkpoint['optimizer_state_dict'] = optimizador.state_dict()

    if historial is not None:
        checkpoint['historial'] = historial

    checkpoint.update(metadata)

    # Crear directorio si no existe
    os.makedirs(os.path.dirname(ruta) if os.path.dirname(ruta) else '.', exist_ok=True)

    torch.save(checkpoint, ruta)
    print(f"Modelo guardado en: {ruta}")


def cargar_modelo(
    modelo: nn.Module,
    ruta: str,
    optimizador: torch.optim.Optimizer = None,
    device: str = 'cpu'
) -> Dict:
    """
    Carga modelo desde checkpoint.

    Args:
        modelo: Instancia del modelo (arquitectura)
        ruta: Ruta del archivo .pth
        optimizador: Optimizador para restaurar (opcional)
        device: Dispositivo destino

    Returns:
        Diccionario con metadata del checkpoint

    Ejemplo:
        >>> modelo = MLP(784, [256, 128], 10)
        >>> metadata = cargar_modelo(modelo, 'best_model.pth')
        >>> print(f"Época: {metadata.get('epoch')}")
    """
    checkpoint = torch.load(ruta, map_location=device)

    modelo.load_state_dict(checkpoint['model_state_dict'])
    modelo.to(device)

    if optimizador is not None and 'optimizer_state_dict' in checkpoint:
        optimizador.load_state_dict(checkpoint['optimizer_state_dict'])

    print(f"Modelo cargado desde: {ruta}")

    # Retornar metadata
    metadata = {k: v for k, v in checkpoint.items()
                if k not in ['model_state_dict', 'optimizer_state_dict']}

    return metadata


def contar_parametros(modelo: nn.Module, verbose: bool = True) -> int:
    """
    Cuenta parámetros del modelo.

    Args:
        modelo: Modelo PyTorch
        verbose: Si mostrar desglose por capa

    Returns:
        Total de parámetros entrenables
    """
    total_params = 0
    trainable_params = 0

    if verbose:
        print(f"\n{'Capa':<40} {'Params':>15} {'Trainable':>10}")
        print("-" * 65)

    for name, param in modelo.named_parameters():
        num_params = param.numel()
        total_params += num_params

        if param.requires_grad:
            trainable_params += num_params

        if verbose:
            trainable = "Sí" if param.requires_grad else "No"
            print(f"{name:<40} {num_params:>15,} {trainable:>10}")

    if verbose:
        print("-" * 65)
        print(f"{'Total':<40} {total_params:>15,}")
        print(f"{'Entrenables':<40} {trainable_params:>15,}")
        print(f"{'No entrenables':<40} {total_params - trainable_params:>15,}")

    return trainable_params


def set_seed(seed: int = 42):
    """Establece semilla para reproducibilidad."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)

    # Para reproducibilidad completa (puede afectar rendimiento)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    print(f"Semilla establecida: {seed}")


def get_device(prefer_gpu: bool = True) -> torch.device:
    """
    Obtiene el dispositivo óptimo disponible.

    Args:
        prefer_gpu: Si preferir GPU cuando esté disponible

    Returns:
        torch.device
    """
    if prefer_gpu and torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"Usando GPU: {torch.cuda.get_device_name(0)}")
        print(f"  Memoria: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    elif prefer_gpu and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = torch.device('mps')
        print("Usando Apple Silicon MPS")
    else:
        device = torch.device('cpu')
        print("Usando CPU")

    return device
