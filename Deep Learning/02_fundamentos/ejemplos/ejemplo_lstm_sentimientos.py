"""
Ejemplo: Análisis de Sentimientos con LSTM
==========================================
Clasificación de texto usando redes recurrentes.
"""

import sys
sys.path.append('..')

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from collections import Counter
import numpy as np

from core import LSTM, Entrenador, EarlyStopping
from core.utils import visualizar_metricas, guardar_modelo, set_seed, get_device
from core.entrenamiento import crear_optimizador


# =============================================================================
# DATASET PERSONALIZADO PARA TEXTO
# =============================================================================

class TextDataset(Dataset):
    """Dataset para texto con tokenización simple."""

    def __init__(self, texts, labels, vocab=None, max_len=100):
        self.texts = texts
        self.labels = labels
        self.max_len = max_len

        # Construir vocabulario si no existe
        if vocab is None:
            self.vocab = self._build_vocab(texts)
        else:
            self.vocab = vocab

    def _build_vocab(self, texts, min_freq=2):
        """Construye vocabulario a partir de textos."""
        counter = Counter()
        for text in texts:
            counter.update(text.lower().split())

        vocab = {'<PAD>': 0, '<UNK>': 1}
        for word, count in counter.items():
            if count >= min_freq:
                vocab[word] = len(vocab)

        print(f"Vocabulario construido: {len(vocab)} palabras")
        return vocab

    def _tokenize(self, text):
        """Convierte texto a secuencia de índices."""
        tokens = text.lower().split()
        indices = [self.vocab.get(t, self.vocab['<UNK>']) for t in tokens]

        # Padding/truncating
        if len(indices) < self.max_len:
            indices = indices + [0] * (self.max_len - len(indices))
        else:
            indices = indices[:self.max_len]

        return indices

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        tokens = torch.LongTensor(self._tokenize(text))
        label = torch.LongTensor([label])

        return tokens, label.squeeze()


# =============================================================================
# DATOS DE EJEMPLO (En producción usar IMDB, SST, etc.)
# =============================================================================

def crear_datos_ejemplo():
    """Crea dataset de ejemplo para demostración."""

    # Ejemplos positivos
    positivos = [
        "This movie is amazing and wonderful I loved it",
        "Great film with excellent acting and story",
        "Absolutely fantastic a must watch movie",
        "Beautiful cinematography and great performances",
        "One of the best films I have ever seen",
        "Incredible movie with stunning visuals",
        "Loved every minute of this masterpiece",
        "Perfect film nothing could be better",
        "Amazing story with great characters",
        "Wonderful experience highly recommended",
    ] * 50  # Multiplicar para tener más datos

    # Ejemplos negativos
    negativos = [
        "This movie is terrible and boring I hated it",
        "Awful film with bad acting and poor story",
        "Completely disappointing waste of time",
        "Terrible cinematography and bad performances",
        "One of the worst films I have ever seen",
        "Horrible movie with ugly visuals",
        "Hated every minute of this disaster",
        "Terrible film nothing could be worse",
        "Awful story with terrible characters",
        "Bad experience not recommended at all",
    ] * 50

    texts = positivos + negativos
    labels = [1] * len(positivos) + [0] * len(negativos)

    # Mezclar datos
    indices = np.random.permutation(len(texts))
    texts = [texts[i] for i in indices]
    labels = [labels[i] for i in indices]

    return texts, labels


def main():
    # =========================================================================
    # 1. CONFIGURACIÓN
    # =========================================================================
    set_seed(42)
    device = get_device()

    # Hiperparámetros
    BATCH_SIZE = 32
    EPOCHS = 30
    LEARNING_RATE = 0.001
    MAX_LEN = 50
    EMBEDDING_DIM = 128
    HIDDEN_DIM = 128

    # =========================================================================
    # 2. PREPARAR DATOS
    # =========================================================================
    print("\n" + "="*50)
    print("PREPARANDO DATOS DE TEXTO")
    print("="*50)

    texts, labels = crear_datos_ejemplo()

    # Split train/val/test
    n = len(texts)
    train_texts, train_labels = texts[:int(0.7*n)], labels[:int(0.7*n)]
    val_texts, val_labels = texts[int(0.7*n):int(0.85*n)], labels[int(0.7*n):int(0.85*n)]
    test_texts, test_labels = texts[int(0.85*n):], labels[int(0.85*n):]

    # Crear datasets
    train_dataset = TextDataset(train_texts, train_labels, max_len=MAX_LEN)
    vocab = train_dataset.vocab  # Usar mismo vocabulario para val/test

    val_dataset = TextDataset(val_texts, val_labels, vocab=vocab, max_len=MAX_LEN)
    test_dataset = TextDataset(test_texts, test_labels, vocab=vocab, max_len=MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    print(f"Train: {len(train_dataset)} textos")
    print(f"Val: {len(val_dataset)} textos")
    print(f"Test: {len(test_dataset)} textos")
    print(f"Vocabulario: {len(vocab)} palabras")

    # =========================================================================
    # 3. CREAR MODELO LSTM
    # =========================================================================
    print("\n" + "="*50)
    print("CREANDO MODELO LSTM")
    print("="*50)

    modelo = LSTM(
        vocab_size=len(vocab),
        embedding_dim=EMBEDDING_DIM,
        hidden_dim=HIDDEN_DIM,
        output_dim=2,  # Positivo/Negativo
        num_layers=2,
        bidirectional=True,
        dropout=0.3,
        use_embedding=True
    )
    modelo = modelo.to(device)

    print("\nArquitectura:")
    print(f"  Vocabulario: {len(vocab)}")
    print(f"  Embedding: {EMBEDDING_DIM}")
    print(f"  Hidden: {HIDDEN_DIM}")
    print(f"  Capas LSTM: 2 (bidireccional)")
    print(f"  Output: 2 (positivo/negativo)")
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
        tipo='adam',
        lr=LEARNING_RATE,
        weight_decay=1e-5
    )

    early_stopping = EarlyStopping(
        patience=5,
        min_delta=0.001,
        mode='min',
        restore_best=True
    )

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
        device=device
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
    # 7. PREDICCIONES DE EJEMPLO
    # =========================================================================
    print("\n" + "="*50)
    print("PREDICCIONES DE EJEMPLO")
    print("="*50)

    ejemplos = [
        "This is a great and wonderful movie",
        "Terrible film I really hated it",
        "Not bad but could be better",
        "Amazing performance by the actors"
    ]

    modelo.eval()
    with torch.no_grad():
        for texto in ejemplos:
            # Tokenizar
            tokens = [vocab.get(t, vocab['<UNK>']) for t in texto.lower().split()]
            if len(tokens) < MAX_LEN:
                tokens = tokens + [0] * (MAX_LEN - len(tokens))
            else:
                tokens = tokens[:MAX_LEN]

            tokens = torch.LongTensor(tokens).unsqueeze(0).to(device)

            # Predecir
            output = modelo(tokens)
            probs = torch.softmax(output, dim=1)
            pred = output.argmax(dim=1).item()

            sentimiento = "POSITIVO" if pred == 1 else "NEGATIVO"
            confianza = probs[0, pred].item() * 100

            print(f"\nTexto: '{texto}'")
            print(f"  → {sentimiento} ({confianza:.1f}% confianza)")

    # Guardar
    visualizar_metricas(historial, save_path='../../modelos/sentiment_lstm_training.png')
    guardar_modelo(
        modelo,
        '../../modelos/sentiment_lstm.pth',
        optimizador=optimizador,
        historial=historial,
        vocab=vocab,
        test_accuracy=test_metrics['accuracy']
    )

    print("\n¡Entrenamiento completado!")


if __name__ == "__main__":
    main()
