import torch

DEVICE = 'cuda:0'

# Thinning templates
C = torch.Tensor([[1]]).to(torch.bool).to(DEVICE)

C_W = torch.Tensor([
    [0, 0, 0],
    [0, 1, 1],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_W = torch.Tensor([
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0]
]).to(torch.bool).to(DEVICE)

C_E = torch.Tensor([
    [0, 0, 0],
    [1, 1, 0],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_E = torch.Tensor([
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1]
]).to(torch.bool).to(DEVICE)

C_N = torch.Tensor([
    [0, 0, 0],
    [0, 1, 0],
    [0, 1, 0]
]).to(torch.bool).to(DEVICE)

D_N = torch.Tensor([
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

C_S = torch.Tensor([
    [0, 1, 0],
    [0, 1, 0],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_S = torch.Tensor([
    [0, 0, 0],
    [0, 0, 0],
    [1, 1, 1]
]).to(torch.bool).to(DEVICE)

# Restoring
C_WE = torch.Tensor([
    [0, 1, 1, 0],
]).to(torch.bool).to(DEVICE)

D_WE = torch.Tensor([
    [1, 0, 0, 1],
]).to(torch.bool).to(DEVICE)

ORIGIN_WE = (0, 1)
ORIGIN_WE_DIL = (0, 2)

C_NS = torch.Tensor([
    [0],
    [1],
    [1],
    [0],
]).to(torch.bool).to(DEVICE)

D_NS = torch.Tensor([
    [1],
    [0],
    [0],
    [1],
]).to(torch.bool).to(DEVICE)

ORIGIN_NS = (1, 0)
ORIGIN_NS_DIL = (2, 0)

# Trimming
C_NE = torch.Tensor([
    [0, 0, 0],
    [1, 1, 0],
    [0, 1, 0]
]).to(torch.bool).to(DEVICE)

D_NE = torch.Tensor([
    [0, 1, 1],
    [0, 0, 1],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

C_NW = torch.Tensor([
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 0]
]).to(torch.bool).to(DEVICE)

D_NW = torch.Tensor([
    [1, 1, 0],
    [1, 0, 0],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

C_SW = torch.Tensor([
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_SW = torch.Tensor([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0]
]).to(torch.bool).to(DEVICE)

C_SE = torch.Tensor([
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_SE = torch.Tensor([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 1]
]).to(torch.bool).to(DEVICE)

C_WT = torch.Tensor([
    [0, 0, 0],
    [0, 1, 1],
    [0, 0, 0]
]).to(torch.bool).to(DEVICE)

D_WT = torch.Tensor([
    [1, 1, 0],
    [1, 0, 0],
    [1, 1, 0]
]).to(torch.bool).to(DEVICE)

D_ET = torch.Tensor([
    [0, 1, 1],
    [0, 0, 1],
    [0, 1, 1]
]).to(torch.bool).to(DEVICE)

C_NT = torch.Tensor([
    [0, 0, 0],
    [0, 1, 0],
    [0, 1, 0]
]).to(torch.bool).to(DEVICE)

D_NT = torch.Tensor([
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1]
]).to(torch.bool).to(DEVICE)

B_O = torch.Tensor([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]).to(torch.bool).to(DEVICE)
