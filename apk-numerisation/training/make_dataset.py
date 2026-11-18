"""Génère N pages d'entraînement (photo simulée + vérité terrain) dans un dossier."""
import os
import sys
from multiprocessing import Pool

import torch

from synth import make_sample, save_sample

OUT = sys.argv[1]
N = int(sys.argv[2])
START = int(sys.argv[3]) if len(sys.argv) > 3 else 0


def job(i):
    torch.set_num_threads(1)
    p = os.path.join(OUT, f"{i:05d}")
    if os.path.exists(os.path.join(p, "meta.npz")):
        return
    try:
        save_sample(make_sample(1000 + i), p)
    except Exception as e:  # une page ratée n'arrête pas tout
        print("erreur", i, e, flush=True)


if __name__ == "__main__":
    from common import get_lut
    get_lut()
    with Pool(4) as pool:
        for k, _ in enumerate(pool.imap_unordered(job, range(START, START + N), chunksize=4)):
            if k % 100 == 0:
                print(k, flush=True)
