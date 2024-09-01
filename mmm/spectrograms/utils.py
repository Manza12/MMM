import torch
import numpy as np
from .parameters import EPS, FS


def to_db(x, library='torch'):
    if library == 'torch':
        return 20 * torch.log10(x + EPS)
    elif library == 'numpy':
        return 20 * np.log10(x + EPS)


def from_db(x, library='torch'):
    if library == 'torch':
        return torch.pow(10, x / 20)
    elif library == 'numpy':
        return np.pow(10, x / 20)


def get_duration(data):
    return len(data) / FS
