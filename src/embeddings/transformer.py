import torch
import torch.nn as nn

class TransformerEncoderModel(nn.Module):
    def __init__(self, dim=128):
        super().__init__()
        layer = nn.TransformerEncoderLayer(d_model=dim, nhead=4)
        self.encoder = nn.TransformerEncoder(layer, num_layers=2)

    def forward(self, x):
        return self.encoder(x)

model = TransformerEncoderModel()

def tokenize(text):
    return [ord(c) % 128 for c in text[:128]]

def get_embedding(text):
    tokens = tokenize(text)

    # Force fixed length = 128
    tokens = tokens[:128]
    if len(tokens) < 128:
        tokens += [0] * (128 - len(tokens))

    tensor = torch.tensor(tokens).float()

    # 🔥 NO transformer needed (fix for now)
    embedding = tensor.numpy()

    return embedding