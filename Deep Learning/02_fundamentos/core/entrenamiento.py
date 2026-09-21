"""
Deep Learning - Módulo de Entrenamiento
========================================
Clases y funciones para entrenar modelos de Deep Learning.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List, Callable, Optional, Tuple
from tqdm import tqdm
import copy
import time


class EarlyStopping:
    """
    Early Stopping para detener entrenamiento cuando no hay mejora.

    Previene overfitting deteniendo el entrenamiento cuando la métrica
    de validación deja de mejorar.

    Args:
        patience: Épocas a esperar sin mejora antes de parar
        min_delta: Cambio mínimo para considerar mejora
        mode: 'min' para loss, 'max' para accuracy
        restore_best: Si restaurar mejores pesos al parar

    Ejemplo:
        >>> early_stop = EarlyStopping(patience=5)
        >>> for epoch in range(100):
        ...     val_loss = entrenar_epoca()
        ...     if early_stop(val_loss, modelo):
        ...         print("Early stopping!")
        ...         break
    """

    def __init__(
        self,
        patience: int = 7,
        min_delta: float = 0.0001,
        mode: str = 'min',
        restore_best: bool = True
    ):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.restore_best = restore_best

        self.counter = 0
        self.best_score = None
        self.best_weights = None
        self.early_stop = False

        # Función de comparación según modo
        if mode == 'min':
            self.is_better = lambda score, best: score < best - min_delta
        else:
            self.is_better = lambda score, best: score > best + min_delta

    def __call__(self, score: float, model: nn.Module) -> bool:
        """
        Evalúa si debe parar el entrenamiento.

        Args:
            score: Métrica actual (loss o accuracy)
            model: Modelo para guardar pesos

        Returns:
            True si debe parar, False en caso contrario
        """
        if self.best_score is None:
            self.best_score = score
            self.best_weights = copy.deepcopy(model.state_dict())
            return False

        if self.is_better(score, self.best_score):
            self.best_score = score
            self.best_weights = copy.deepcopy(model.state_dict())
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
                if self.restore_best:
                    model.load_state_dict(self.best_weights)
                return True

        return False

    def reset(self):
        """Reinicia el estado del early stopping."""
        self.counter = 0
        self.best_score = None
        self.best_weights = None
        self.early_stop = False


class Entrenador:
    """
    Clase para gestionar el entrenamiento de modelos PyTorch.

    Encapsula el ciclo de entrenamiento completo con soporte para:
    - Early stopping
    - Learning rate scheduling
    - Logging de métricas
    - Checkpointing

    Args:
        modelo: Modelo PyTorch (nn.Module)
        optimizador: Optimizador de PyTorch
        loss_fn: Función de pérdida
        device: Dispositivo ('cuda' o 'cpu')
        scheduler: Learning rate scheduler (opcional)

    Ejemplo:
        >>> modelo = MLP(784, [256, 128], 10)
        >>> optimizer = torch.optim.Adam(modelo.parameters(), lr=0.001)
        >>> loss_fn = nn.CrossEntropyLoss()
        >>>
        >>> entrenador = Entrenador(modelo, optimizer, loss_fn)
        >>> historial = entrenador.fit(train_loader, val_loader, epochs=50)
    """

    def __init__(
        self,
        modelo: nn.Module,
        optimizador: torch.optim.Optimizer,
        loss_fn: nn.Module,
        device: str = None,
        scheduler: torch.optim.lr_scheduler._LRScheduler = None
    ):
        # Detectar dispositivo automáticamente
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.device = torch.device(device)
        self.modelo = modelo.to(self.device)
        self.optimizador = optimizador
        self.loss_fn = loss_fn
        self.scheduler = scheduler

        # Historial de entrenamiento
        self.historial = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': [],
            'lr': []
        }

    def _train_epoch(self, dataloader: DataLoader) -> Tuple[float, float]:
        """Ejecuta una época de entrenamiento."""
        self.modelo.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch_x, batch_y in dataloader:
            batch_x = batch_x.to(self.device)
            batch_y = batch_y.to(self.device)

            # Forward pass
            self.optimizador.zero_grad()
            outputs = self.modelo(batch_x)
            loss = self.loss_fn(outputs, batch_y)

            # Backward pass
            loss.backward()

            # Gradient clipping (previene explosión de gradientes)
            torch.nn.utils.clip_grad_norm_(self.modelo.parameters(), max_norm=1.0)

            self.optimizador.step()

            # Métricas
            total_loss += loss.item() * batch_x.size(0)
            _, predicted = outputs.max(1)
            total += batch_y.size(0)
            correct += predicted.eq(batch_y).sum().item()

        avg_loss = total_loss / total
        accuracy = 100.0 * correct / total

        return avg_loss, accuracy

    def _validate_epoch(self, dataloader: DataLoader) -> Tuple[float, float]:
        """Ejecuta validación en una época."""
        self.modelo.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch_x, batch_y in dataloader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                outputs = self.modelo(batch_x)
                loss = self.loss_fn(outputs, batch_y)

                total_loss += loss.item() * batch_x.size(0)
                _, predicted = outputs.max(1)
                total += batch_y.size(0)
                correct += predicted.eq(batch_y).sum().item()

        avg_loss = total_loss / total
        accuracy = 100.0 * correct / total

        return avg_loss, accuracy

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader = None,
        epochs: int = 100,
        early_stopping: EarlyStopping = None,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """
        Entrena el modelo.

        Args:
            train_loader: DataLoader de entrenamiento
            val_loader: DataLoader de validación (opcional)
            epochs: Número máximo de épocas
            early_stopping: Instancia de EarlyStopping (opcional)
            verbose: Si mostrar progreso

        Returns:
            Diccionario con historial de métricas
        """
        start_time = time.time()

        # Barra de progreso
        epoch_iter = tqdm(range(epochs), desc="Entrenamiento") if verbose else range(epochs)

        for epoch in epoch_iter:
            # Entrenamiento
            train_loss, train_acc = self._train_epoch(train_loader)
            self.historial['train_loss'].append(train_loss)
            self.historial['train_acc'].append(train_acc)

            # Validación
            if val_loader is not None:
                val_loss, val_acc = self._validate_epoch(val_loader)
                self.historial['val_loss'].append(val_loss)
                self.historial['val_acc'].append(val_acc)
            else:
                val_loss, val_acc = None, None

            # Learning rate actual
            current_lr = self.optimizador.param_groups[0]['lr']
            self.historial['lr'].append(current_lr)

            # Scheduler step
            if self.scheduler is not None:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_loss if val_loss else train_loss)
                else:
                    self.scheduler.step()

            # Logging
            if verbose:
                msg = f"Epoch {epoch+1}/{epochs} | "
                msg += f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%"
                if val_loss is not None:
                    msg += f" | Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%"
                msg += f" | LR: {current_lr:.2e}"
                tqdm.write(msg)

            # Early stopping
            if early_stopping is not None and val_loader is not None:
                if early_stopping(val_loss, self.modelo):
                    if verbose:
                        print(f"\nEarly stopping en época {epoch+1}")
                        print(f"Mejor val_loss: {early_stopping.best_score:.4f}")
                    break

        elapsed = time.time() - start_time
        if verbose:
            print(f"\nEntrenamiento completado en {elapsed:.2f} segundos")

        return self.historial

    def evaluate(self, dataloader: DataLoader) -> Dict[str, float]:
        """
        Evalúa el modelo en un dataset.

        Args:
            dataloader: DataLoader con datos de evaluación

        Returns:
            Diccionario con loss y accuracy
        """
        loss, acc = self._validate_epoch(dataloader)
        return {'loss': loss, 'accuracy': acc}

    def predict(self, dataloader: DataLoader) -> torch.Tensor:
        """
        Genera predicciones para un dataset.

        Args:
            dataloader: DataLoader con datos

        Returns:
            Tensor con predicciones
        """
        self.modelo.eval()
        predictions = []

        with torch.no_grad():
            for batch_x, _ in dataloader:
                batch_x = batch_x.to(self.device)
                outputs = self.modelo(batch_x)
                _, preds = outputs.max(1)
                predictions.append(preds.cpu())

        return torch.cat(predictions)

    def predict_proba(self, dataloader: DataLoader) -> torch.Tensor:
        """
        Genera probabilidades de predicción.

        Returns:
            Tensor con probabilidades por clase
        """
        self.modelo.eval()
        probas = []

        with torch.no_grad():
            for batch_x, _ in dataloader:
                batch_x = batch_x.to(self.device)
                outputs = self.modelo(batch_x)
                probs = torch.softmax(outputs, dim=1)
                probas.append(probs.cpu())

        return torch.cat(probas)


def crear_optimizador(
    modelo: nn.Module,
    tipo: str = 'adam',
    lr: float = 0.001,
    weight_decay: float = 0.0,
    **kwargs
) -> torch.optim.Optimizer:
    """
    Factory function para crear optimizadores.

    Args:
        modelo: Modelo PyTorch
        tipo: Tipo de optimizador ('adam', 'sgd', 'adamw', 'rmsprop')
        lr: Learning rate
        weight_decay: Regularización L2
        **kwargs: Argumentos adicionales para el optimizador

    Returns:
        Optimizador configurado
    """
    optimizadores = {
        'adam': torch.optim.Adam,
        'adamw': torch.optim.AdamW,
        'sgd': torch.optim.SGD,
        'rmsprop': torch.optim.RMSprop
    }

    if tipo not in optimizadores:
        raise ValueError(f"Optimizador '{tipo}' no soportado. Opciones: {list(optimizadores.keys())}")

    # SGD necesita momentum
    if tipo == 'sgd' and 'momentum' not in kwargs:
        kwargs['momentum'] = 0.9

    return optimizadores[tipo](
        modelo.parameters(),
        lr=lr,
        weight_decay=weight_decay,
        **kwargs
    )


def crear_scheduler(
    optimizador: torch.optim.Optimizer,
    tipo: str = 'plateau',
    **kwargs
) -> torch.optim.lr_scheduler._LRScheduler:
    """
    Factory function para crear learning rate schedulers.

    Args:
        optimizador: Optimizador PyTorch
        tipo: Tipo de scheduler ('plateau', 'step', 'cosine', 'exponential')
        **kwargs: Argumentos adicionales

    Returns:
        Scheduler configurado
    """
    schedulers = {
        'plateau': lambda: torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizador, mode='min', factor=0.5, patience=5, **kwargs
        ),
        'step': lambda: torch.optim.lr_scheduler.StepLR(
            optimizador, step_size=kwargs.get('step_size', 10), gamma=0.1
        ),
        'cosine': lambda: torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizador, T_max=kwargs.get('T_max', 50)
        ),
        'exponential': lambda: torch.optim.lr_scheduler.ExponentialLR(
            optimizador, gamma=kwargs.get('gamma', 0.95)
        ),
        'onecycle': lambda: torch.optim.lr_scheduler.OneCycleLR(
            optimizador,
            max_lr=kwargs.get('max_lr', 0.01),
            epochs=kwargs.get('epochs', 100),
            steps_per_epoch=kwargs.get('steps_per_epoch', 100)
        )
    }

    if tipo not in schedulers:
        raise ValueError(f"Scheduler '{tipo}' no soportado. Opciones: {list(schedulers.keys())}")

    return schedulers[tipo]()
