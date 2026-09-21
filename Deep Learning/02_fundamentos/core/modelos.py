"""
Deep Learning - Modelos Base
============================
Implementaciones de arquitecturas fundamentales de Deep Learning.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Optional


# =============================================================================
# PERCEPTRÓN MULTICAPA (MLP)
# =============================================================================

class MLP(nn.Module):
    """
    Perceptrón Multicapa (Multi-Layer Perceptron).

    Red neuronal fully connected básica para clasificación o regresión.

    Arquitectura:
        Input → [Linear → Activation → Dropout] × N → Output

    Args:
        input_size: Dimensión de entrada
        hidden_sizes: Lista con tamaños de capas ocultas [128, 64, 32]
        output_size: Dimensión de salida (clases o valores)
        dropout: Probabilidad de dropout (0.0 a 1.0)
        activation: Función de activación ('relu', 'leaky_relu', 'tanh', 'sigmoid')

    Ejemplo:
        >>> modelo = MLP(784, [256, 128], 10, dropout=0.3)
        >>> x = torch.randn(32, 784)  # batch de 32
        >>> out = modelo(x)  # shape: (32, 10)
    """

    def __init__(
        self,
        input_size: int,
        hidden_sizes: List[int],
        output_size: int,
        dropout: float = 0.2,
        activation: str = 'relu'
    ):
        super().__init__()

        self.input_size = input_size
        self.output_size = output_size

        # Seleccionar función de activación
        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(0.1),
            'tanh': nn.Tanh(),
            'sigmoid': nn.Sigmoid(),
            'gelu': nn.GELU()
        }
        self.activation = activations.get(activation, nn.ReLU())

        # Construir capas dinámicamente
        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.BatchNorm1d(hidden_size),  # Normalización para estabilidad
                self.activation,
                nn.Dropout(dropout)
            ])
            prev_size = hidden_size

        # Capa de salida (sin activación, se aplica en loss)
        layers.append(nn.Linear(prev_size, output_size))

        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass del MLP.

        Args:
            x: Tensor de entrada (batch_size, input_size)

        Returns:
            Logits de salida (batch_size, output_size)
        """
        # Aplanar si viene de imagen
        if x.dim() > 2:
            x = x.view(x.size(0), -1)
        return self.network(x)

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Predicción con probabilidades (softmax aplicado)."""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            return F.softmax(logits, dim=1)

    def count_parameters(self) -> int:
        """Cuenta parámetros entrenables."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# =============================================================================
# RED NEURONAL CONVOLUCIONAL (CNN)
# =============================================================================

class CNN(nn.Module):
    """
    Red Neuronal Convolucional para clasificación de imágenes.

    Arquitectura:
        [Conv2d → BatchNorm → Activation → MaxPool] × N → Flatten → MLP

    Args:
        in_channels: Canales de entrada (1 para grayscale, 3 para RGB)
        num_classes: Número de clases a clasificar
        conv_channels: Lista de canales para capas conv [32, 64, 128]
        fc_sizes: Lista de tamaños para capas fully connected [256, 128]
        dropout: Probabilidad de dropout
        input_size: Tamaño de imagen (asume cuadrada)

    Ejemplo:
        >>> modelo = CNN(in_channels=3, num_classes=10, input_size=32)
        >>> x = torch.randn(16, 3, 32, 32)  # batch de 16 imágenes RGB 32x32
        >>> out = modelo(x)  # shape: (16, 10)
    """

    def __init__(
        self,
        in_channels: int = 3,
        num_classes: int = 10,
        conv_channels: List[int] = [32, 64, 128],
        fc_sizes: List[int] = [256],
        dropout: float = 0.3,
        input_size: int = 32
    ):
        super().__init__()

        self.in_channels = in_channels
        self.num_classes = num_classes

        # Construir capas convolucionales
        conv_layers = []
        prev_channels = in_channels

        for channels in conv_channels:
            conv_layers.extend([
                nn.Conv2d(prev_channels, channels, kernel_size=3, padding=1),
                nn.BatchNorm2d(channels),
                nn.ReLU(inplace=True),
                nn.Conv2d(channels, channels, kernel_size=3, padding=1),
                nn.BatchNorm2d(channels),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2, 2),  # Reduce tamaño a la mitad
                nn.Dropout2d(dropout * 0.5)
            ])
            prev_channels = channels

        self.conv_layers = nn.Sequential(*conv_layers)

        # Calcular tamaño después de convs (cada MaxPool divide por 2)
        final_size = input_size // (2 ** len(conv_channels))
        flatten_size = conv_channels[-1] * final_size * final_size

        # Capas fully connected
        fc_layers = [nn.Flatten()]
        prev_size = flatten_size

        for fc_size in fc_sizes:
            fc_layers.extend([
                nn.Linear(prev_size, fc_size),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout)
            ])
            prev_size = fc_size

        fc_layers.append(nn.Linear(prev_size, num_classes))

        self.fc_layers = nn.Sequential(*fc_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass de la CNN.

        Args:
            x: Tensor de imagen (batch, channels, height, width)

        Returns:
            Logits de clasificación (batch, num_classes)
        """
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extrae features de las capas convolucionales."""
        return self.conv_layers(x)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# =============================================================================
# RED RECURRENTE (LSTM)
# =============================================================================

class LSTM(nn.Module):
    """
    Red LSTM para procesamiento de secuencias.

    Arquitectura:
        [Embedding] → LSTM → Dropout → Linear

    Args:
        vocab_size: Tamaño del vocabulario (para NLP)
        embedding_dim: Dimensión de embeddings
        hidden_dim: Dimensión del estado oculto LSTM
        output_dim: Dimensión de salida
        num_layers: Número de capas LSTM apiladas
        bidirectional: Si usar LSTM bidireccional
        dropout: Probabilidad de dropout
        use_embedding: Si usar capa de embedding (False para datos numéricos)
        input_dim: Dimensión de entrada si no usa embedding

    Ejemplo NLP:
        >>> modelo = LSTM(vocab_size=10000, embedding_dim=128, hidden_dim=256, output_dim=2)
        >>> x = torch.randint(0, 10000, (32, 100))  # batch de 32, secuencia de 100
        >>> out = modelo(x)  # shape: (32, 2)

    Ejemplo Series Temporales:
        >>> modelo = LSTM(input_dim=5, hidden_dim=64, output_dim=1, use_embedding=False)
        >>> x = torch.randn(32, 50, 5)  # batch 32, secuencia 50, 5 features
        >>> out = modelo(x)
    """

    def __init__(
        self,
        vocab_size: int = None,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
        output_dim: int = 1,
        num_layers: int = 2,
        bidirectional: bool = True,
        dropout: float = 0.3,
        use_embedding: bool = True,
        input_dim: int = None
    ):
        super().__init__()

        self.use_embedding = use_embedding
        self.bidirectional = bidirectional
        self.num_directions = 2 if bidirectional else 1

        # Capa de embedding para texto
        if use_embedding:
            assert vocab_size is not None, "vocab_size requerido con use_embedding=True"
            self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
            lstm_input_dim = embedding_dim
        else:
            assert input_dim is not None, "input_dim requerido con use_embedding=False"
            self.embedding = None
            lstm_input_dim = input_dim

        # Capa LSTM
        self.lstm = nn.LSTM(
            input_size=lstm_input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
            dropout=dropout if num_layers > 1 else 0
        )

        # Capas de salida
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * self.num_directions, output_dim)

    def forward(
        self,
        x: torch.Tensor,
        lengths: torch.Tensor = None
    ) -> torch.Tensor:
        """
        Forward pass del LSTM.

        Args:
            x: Secuencia de entrada
               - Con embedding: (batch, seq_len) con índices
               - Sin embedding: (batch, seq_len, input_dim)
            lengths: Longitudes reales de cada secuencia (para padding)

        Returns:
            Salida del modelo (batch, output_dim)
        """
        # Embedding si es necesario
        if self.use_embedding:
            x = self.embedding(x)  # (batch, seq_len, embedding_dim)

        # LSTM forward
        # output: (batch, seq_len, hidden_dim * num_directions)
        # hidden: (num_layers * num_directions, batch, hidden_dim)
        output, (hidden, cell) = self.lstm(x)

        # Usar último estado oculto
        if self.bidirectional:
            # Concatenar últimos estados de ambas direcciones
            hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        else:
            hidden = hidden[-1,:,:]

        # Dropout y capa final
        hidden = self.dropout(hidden)
        out = self.fc(hidden)

        return out

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# =============================================================================
# AUTOENCODER
# =============================================================================

class Autoencoder(nn.Module):
    """
    Autoencoder para reducción de dimensionalidad y generación.

    Arquitectura:
        Encoder: Input → [Linear → Activation] × N → Latent
        Decoder: Latent → [Linear → Activation] × N → Output

    Args:
        input_dim: Dimensión de entrada
        latent_dim: Dimensión del espacio latente
        hidden_dims: Lista de dimensiones para encoder [512, 256, 128]
        activation: Función de activación

    Ejemplo:
        >>> ae = Autoencoder(784, latent_dim=32, hidden_dims=[256, 128])
        >>> x = torch.randn(32, 784)
        >>> reconstructed = ae(x)  # shape: (32, 784)
        >>> latent = ae.encode(x)  # shape: (32, 32)
    """

    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 32,
        hidden_dims: List[int] = [256, 128],
        activation: str = 'relu'
    ):
        super().__init__()

        self.input_dim = input_dim
        self.latent_dim = latent_dim

        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(0.1),
            'tanh': nn.Tanh()
        }
        act = activations.get(activation, nn.ReLU())

        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                act,
            ])
            prev_dim = hidden_dim
        encoder_layers.append(nn.Linear(prev_dim, latent_dim))
        self.encoder = nn.Sequential(*encoder_layers)

        # Decoder (espejo del encoder)
        decoder_layers = []
        prev_dim = latent_dim
        for hidden_dim in reversed(hidden_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                act,
            ])
            prev_dim = hidden_dim
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        decoder_layers.append(nn.Sigmoid())  # Salida entre 0 y 1
        self.decoder = nn.Sequential(*decoder_layers)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Codifica entrada al espacio latente."""
        if x.dim() > 2:
            x = x.view(x.size(0), -1)
        return self.encoder(x)

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """Decodifica del espacio latente."""
        return self.decoder(z)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass completo (encode + decode)."""
        z = self.encode(x)
        return self.decode(z)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# =============================================================================
# VARIATIONAL AUTOENCODER (VAE)
# =============================================================================

class VAE(nn.Module):
    """
    Variational Autoencoder para generación de datos.

    Similar al Autoencoder pero con espacio latente probabilístico.
    Aprende una distribución, no un punto fijo.

    Args:
        input_dim: Dimensión de entrada
        latent_dim: Dimensión del espacio latente
        hidden_dims: Lista de dimensiones ocultas
    """

    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 32,
        hidden_dims: List[int] = [256, 128]
    ):
        super().__init__()

        self.latent_dim = latent_dim

        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.LeakyReLU(0.1)
            ])
            prev_dim = h_dim
        self.encoder = nn.Sequential(*encoder_layers)

        # Capas para media y varianza
        self.fc_mu = nn.Linear(hidden_dims[-1], latent_dim)
        self.fc_var = nn.Linear(hidden_dims[-1], latent_dim)

        # Decoder
        decoder_layers = []
        prev_dim = latent_dim
        for h_dim in reversed(hidden_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.LeakyReLU(0.1)
            ])
            prev_dim = h_dim
        decoder_layers.extend([
            nn.Linear(prev_dim, input_dim),
            nn.Sigmoid()
        ])
        self.decoder = nn.Sequential(*decoder_layers)

    def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Retorna media y log-varianza del espacio latente."""
        if x.dim() > 2:
            x = x.view(x.size(0), -1)
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_var(h)

    def reparameterize(self, mu: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
        """
        Reparametrization trick: z = mu + std * epsilon
        Permite backpropagation a través del sampling.
        """
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        return self.decoder(z)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Returns:
            reconstruction: Reconstrucción de x
            mu: Media del espacio latente
            log_var: Log-varianza del espacio latente
        """
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        return self.decode(z), mu, log_var

    def sample(self, num_samples: int, device: str = 'cpu') -> torch.Tensor:
        """Genera muestras del espacio latente."""
        z = torch.randn(num_samples, self.latent_dim).to(device)
        return self.decode(z)

    @staticmethod
    def loss_function(
        recon_x: torch.Tensor,
        x: torch.Tensor,
        mu: torch.Tensor,
        log_var: torch.Tensor,
        kld_weight: float = 0.0005
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        VAE Loss = Reconstruction Loss + KL Divergence

        Args:
            recon_x: Reconstrucción
            x: Original
            mu: Media latente
            log_var: Log-varianza latente
            kld_weight: Peso del término KL

        Returns:
            total_loss, recon_loss, kld_loss
        """
        # Reconstruction loss (BCE)
        recon_loss = F.binary_cross_entropy(
            recon_x.view(-1, x.size(-1)),
            x.view(-1, x.size(-1)),
            reduction='sum'
        )

        # KL Divergence
        kld_loss = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())

        total_loss = recon_loss + kld_weight * kld_loss

        return total_loss, recon_loss, kld_loss
