"""Exporte les 3 IA au format ONNX pour l'appli web.

  python export.py CKPT_DIR ../web/models
"""
import os
import sys

import torch

from models import PaperNet, PrintNet, SelectNet

ck, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)


def load(m, name):
    m.load_state_dict(torch.load(os.path.join(ck, name + ".pt")))
    return m.eval()


class SelectOut(torch.nn.Module):  # renvoie directement les probabilités
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, photo, paperE):
        o = self.m(photo, paperE)
        return torch.cat([torch.softmax(o[:, :4], 1), torch.sigmoid(o[:, 4:5])], 1)


def exp(m, args, names, outs, file, dyn):
    torch.onnx.export(m, args, os.path.join(out, file), input_names=names, output_names=outs,
                      dynamic_axes=dyn, opset_version=17, dynamo=False)
    print(file, os.path.getsize(os.path.join(out, file)) // 1024, "Ko")


with torch.no_grad():
    exp(load(PaperNet(), "paper"), (torch.rand(1, 3, 256, 256),), ["photo"], ["paper", "E"], "ia1_papier.onnx", None)
    hw = {0: "b", 2: "h", 3: "w"}
    exp(SelectOut(load(SelectNet(), "select")), (torch.rand(1, 3, 384, 512), torch.rand(1, 3, 384, 512)),
        ["photo", "E"], ["sel"], "ia2_trieur.onnx", {"photo": hw, "E": hw, "sel": hw})
    exp(load(PrintNet(), "print"), (torch.rand(1, 3, 256, 256), torch.rand(1, 3, 256, 256), torch.rand(1, 5, 256, 256)),
        ["photo", "E", "sel"], ["cov"], "ia3_imprimante.onnx", {"photo": hw, "E": hw, "sel": hw, "cov": hw})
