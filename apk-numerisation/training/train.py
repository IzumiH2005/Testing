"""Entraînement des 3 IA sur les pages synthétiques.

  python train.py paper   DATA OUT --minutes 15   # IA 1
  python train.py cache1  DATA OUT                # garde les prédictions de l'IA 1 pour chaque page
  python train.py select  DATA OUT --minutes 40   # IA 2
  python train.py cache2  DATA OUT
  python train.py print   DATA OUT --minutes 60   # IA 3
"""
import argparse
import glob
import math
import os
import time

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

from common import print_t, t_lin2srgb, t_srgb2lin
from models import PaperNet, PrintNet, SelectNet, sel_probs

ap = argparse.ArgumentParser()
ap.add_argument("stage")
ap.add_argument("data")
ap.add_argument("out")
ap.add_argument("--minutes", type=float, default=20)
ap.add_argument("--bs", type=int, default=8)
ap.add_argument("--crop", type=int, default=192)
ap.add_argument("--lr", type=float, default=2e-3)
ap.add_argument("--resume", action="store_true")
ap.add_argument("--pretrained", default=None, help="poids ImageNet de MobileNetV3 (IA 1)")
args = ap.parse_args()
torch.set_num_threads(4)
os.makedirs(args.out, exist_ok=True)

pages = sorted(p for p in glob.glob(os.path.join(args.data, "*")) if os.path.exists(os.path.join(p, "meta.npz")))
val, train = pages[-60:], pages[:-60]
print(len(train), "pages d'entraînement,", len(val), "de contrôle", flush=True)


def read_photo(p):
    return cv2.imread(os.path.join(p, "photo.jpg"))[..., ::-1].astype(np.float32) / 255


def read_lab(p):
    lab = cv2.imread(os.path.join(p, "lab.png"), cv2.IMREAD_UNCHANGED)
    return lab % 4, lab // 4


def lin(x):
    return torch.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def srgb(x):
    return torch.where(x <= 0.0031308, 12.92 * x, 1.055 * x.clamp(min=1e-8) ** (1 / 2.4) - 0.055)


def rsz(a, size, interpolation):
    if a.ndim == 3 and a.shape[2] > 4:
        return np.dstack([rsz(a[..., i:i + 4], size, interpolation) for i in range(0, a.shape[2], 4)])
    r = cv2.resize(a, size, interpolation=interpolation)
    return r[..., None] if a.ndim == 3 and r.ndim == 2 else r


def to_t(a):
    return torch.from_numpy(np.ascontiguousarray(a)).permute(2, 0, 1).float()


def run(model, loader_fn, loss_fn, minutes, name, val_fn=None, groups=None):
    opt = torch.optim.AdamW(groups or model.parameters(), lr=args.lr, weight_decay=1e-4)
    ck = os.path.join(args.out, name + ".pt")
    if args.resume and os.path.exists(ck):
        model.load_state_dict(torch.load(ck))
    t0, step, avg = time.time(), 0, None
    budget = minutes * 60
    model.train()
    while True:
        for batch in loader_fn():
            el = time.time() - t0
            if el > budget:
                break
            lr = args.lr * (0.03 + 0.97 * 0.5 * (1 + math.cos(math.pi * el / budget)))
            for g in opt.param_groups:
                g["lr"] = lr * g.get("k", 1)
            loss = loss_fn(model, batch)
            opt.zero_grad()
            loss.backward()
            opt.step()
            avg = loss.item() if avg is None else 0.98 * avg + 0.02 * loss.item()
            step += 1
            if step % 100 == 0:
                print(f"{name} pas {step} perte {avg:.4f} lr {lr:.5f} {el/60:.1f} min", flush=True)
                torch.save(model.state_dict(), ck)
        else:
            continue
        break
    torch.save(model.state_dict(), ck)
    model.eval()
    if val_fn:
        with torch.no_grad():
            val_fn(model)
    return model


# ------------------------------------------------------------------ IA 1
if args.stage == "paper":
    def load(ps):
        X, E, P = [], [], []
        for p in ps:
            m = np.load(os.path.join(p, "meta.npz"))
            X.append(cv2.resize(read_photo(p), (256, 256), interpolation=cv2.INTER_AREA))
            E.append(m["E"])
            P.append(m["paper"])
        return (torch.from_numpy(np.stack(X)).permute(0, 3, 1, 2), torch.from_numpy(np.stack(E)).permute(0, 3, 1, 2),
                torch.from_numpy(np.stack(P)))
    Xt, Et, Pt = load(train)
    Xv, Ev, Pv = load(val)
    print("chargé", flush=True)

    def loader():
        idx = torch.randperm(len(Xt))
        for i in range(0, len(idx) - 31, 32):
            b = idx[i:i + 32]
            x, e = Xt[b], Et[b]
            if torch.rand(1) < 0.5:
                x, e = x.flip(3), e.flip(3)
            if torch.rand(1) < 0.5:
                x, e = x.flip(2), e.flip(2)
            # autre éclairage (couleur de lampe, exposition) : la photo change, pas la couleur du papier
            n = len(b)
            t = (torch.rand(n) * 2 - 1) * torch.where(torch.rand(n) < 0.35, 1.6, 1.0)
            g = torch.stack([1 + 0.35 * t, torch.ones(n), 1 - 0.45 * t], 1).clamp(min=0.12)
            g[:, 1] *= 1 + 0.06 * torch.randn(n)
            g = g / g.amax(1, keepdim=True) * torch.empty(n, 1).uniform_(0.45, 1.25)
            keep = torch.rand(n) < 0.3
            g[keep] = 1
            g = g[:, :, None, None]
            x = srgb((lin(x) * g).clamp(0, 1))
            e = srgb((lin(e) * g).clamp(0, 1))
            yield x, e, Pt[b]

    def loss_fn(m, b):
        x, e, p = b
        pp, ee = m(x)
        return 3 * (pp - p).abs().mean() + (ee - e).abs().mean()

    def val_fn(m):
        pp, ee = m(Xv)
        err = (pp - Pv).abs() * 255
        print("contrôle : erreur couleur papier moyenne %.1f / 255 (max %.1f), carte papier %.1f / 255"
              % (err.mean(), err.max(), (ee - Ev).abs().mean() * 255), flush=True)

    net = PaperNet(args.pretrained)
    base = list(net.f.parameters())
    ids = {id(p) for p in base}
    groups = [{"params": base, "k": 0.2}, {"params": [p for p in net.parameters() if id(p) not in ids], "k": 1.0}]
    run(net, loader, loss_fn, args.minutes, "paper", val_fn, groups)

elif args.stage == "cache1":
    m = PaperNet()
    m.load_state_dict(torch.load(os.path.join(args.out, "paper.pt")))
    m.eval()
    with torch.no_grad():
        for p in pages:
            x = torch.from_numpy(cv2.resize(read_photo(p), (256, 256), interpolation=cv2.INTER_AREA)).permute(2, 0, 1)[None]
            pp, ee = m(x)
            np.save(os.path.join(p, "Ep.npy"), ee[0].permute(1, 2, 0).numpy().astype(np.float32))
    print("ok")

# ------------------------------------------------------------------ IA 2
elif args.stage in ("select", "cache2"):
    def page512(p):
        ph = read_photo(p)
        H, W = ph.shape[:2]
        s = 512 / max(H, W)
        h, w = round(H * s), round(W * s)
        x = cv2.resize(ph, (w, h), interpolation=cv2.INTER_AREA)
        E = cv2.resize(np.load(os.path.join(p, "Ep.npy")), (w, h), interpolation=cv2.INTER_LINEAR)
        return x, E

    if args.stage == "cache2":
        m = SelectNet()
        m.load_state_dict(torch.load(os.path.join(args.out, "select.pt")))
        m.eval()
        with torch.no_grad():
            for p in pages:
                x, E = page512(p)
                pr = sel_probs(m(to_t(x)[None], to_t(E)[None]))[0].permute(1, 2, 0).numpy()
                np.save(os.path.join(p, "sel.npy"), (pr * 255 + 0.5).astype(np.uint8))
        print("ok")
    else:
        class DS(Dataset):
            def __init__(self, ps):
                self.ps = ps

            def __len__(self):
                return len(self.ps) * 4

            def __getitem__(self, i):
                p = self.ps[i % len(self.ps)]
                x, E = page512(p)
                cls, dfc = read_lab(p)
                h, w = x.shape[:2]
                cls = cv2.resize(cls, (w, h), interpolation=cv2.INTER_NEAREST)
                dfc = cv2.resize(dfc.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
                c = args.crop
                y0, x0 = np.random.randint(0, h - c + 1), np.random.randint(0, w - c + 1)
                sl = (slice(y0, y0 + c), slice(x0, x0 + c))
                return to_t(x[sl]), to_t(E[sl]), torch.from_numpy(cls[sl].astype(np.int64)), torch.from_numpy(dfc[sl])

        dl = DataLoader(DS(train), batch_size=args.bs, shuffle=True, num_workers=3, drop_last=True,
                        persistent_workers=True)
        cw = torch.tensor([1.0, 2.0, 2.0, 1.0])
        pw = torch.tensor(5.0)  # les défauts sont rares : on les compte plus

        def loss_fn(m, b):
            x, E, cls, dfc = b
            o = m(x, E)
            return F.cross_entropy(o[:, :4], cls, weight=cw) + \
                F.binary_cross_entropy_with_logits(o[:, 4], (dfc > 0.3).float(), pos_weight=pw)

        def val_fn(m):
            conf = np.zeros((4, 4))
            tp = fp = fn = 0
            for p in val[:30]:
                x, E = page512(p)
                cls, dfc = read_lab(p)
                h, w = x.shape[:2]
                cls = cv2.resize(cls, (w, h), interpolation=cv2.INTER_NEAREST)
                dfc = cv2.resize(dfc.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) > 0.3
                o = m(to_t(x)[None], to_t(E)[None])[0]
                pc = o[:4].argmax(0).numpy()
                np.add.at(conf, (cls.ravel(), pc.ravel()), 1)
                pd = (o[4] > 0).numpy()
                tp += (pd & dfc).sum(); fp += (pd & ~dfc).sum(); fn += (~pd & dfc).sum()
            acc = conf.diagonal() / conf.sum(1).clip(1)
            print("contrôle : bonne classe papier %.2f texte %.2f aplat %.2f image %.2f ; défauts rappel %.2f précision %.2f"
                  % (*acc, tp / max(1, tp + fn), tp / max(1, tp + fp)), flush=True)

        net = SelectNet(args.pretrained)
        base = list(net.f.parameters())
        ids = {id(p) for p in base}
        groups = [{"params": base, "k": 0.3}, {"params": [p for p in net.parameters() if id(p) not in ids], "k": 1.0}]
        run(net, lambda: dl, loss_fn, args.minutes, "select", val_fn, groups)

# ------------------------------------------------------------------ IA 3
elif args.stage == "print":
    class DS(Dataset):
        def __init__(self, ps, k=4):
            self.ps, self.k = ps, k

        def __len__(self):
            return len(self.ps)

        def __getitem__(self, i):
            p = self.ps[i]
            ph = read_photo(p)
            H, W = ph.shape[:2]
            cov = cv2.imread(os.path.join(p, "cov.png"), cv2.IMREAD_UNCHANGED).astype(np.float32) / 255
            wp = os.path.join(p, "w.png")
            w = cv2.imread(wp, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255 if os.path.exists(wp) else np.zeros((H, W), np.float32)
            cov = np.dstack([cov, w])  # C, M, J, N, blanc
            paper = torch.from_numpy(np.load(os.path.join(p, "meta.npz"))["paper"]).float()
            cls, _ = read_lab(p)
            E = cv2.resize(np.load(os.path.join(p, "Ep.npy")), (W, H), interpolation=cv2.INTER_LINEAR)
            sel = rsz(np.load(os.path.join(p, "sel.npy")).astype(np.float32) / 255, (W, H), cv2.INTER_LINEAR)
            s = np.random.uniform(0.75, 1.4)
            if abs(s - 1) > 0.05:  # varie la taille des caractères
                sz = (round(W * s), round(H * s))
                it = cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR
                ph, cov, E, sel = [rsz(a, sz, it) for a in (ph, cov, E, sel)]
                cls = cv2.resize(cls, sz, interpolation=cv2.INTER_NEAREST)
            H, W = ph.shape[:2]
            c = args.crop
            out = []
            for _ in range(self.k):
                # préfère les zones avec de l'encre
                for _t in range(5):
                    y0, x0 = np.random.randint(0, H - c + 1), np.random.randint(0, W - c + 1)
                    if (cls[y0:y0 + c, x0:x0 + c] > 0).mean() > 0.08 or _t == 4:
                        break
                sl = (slice(y0, y0 + c), slice(x0, x0 + c))
                out.append((to_t(ph[sl]), to_t(E[sl]), to_t(sel[sl]), to_t(cov[sl]),
                            torch.from_numpy(cls[sl].astype(np.int64)), paper))
            return [torch.stack(z) for z in zip(*out)]

    dl = DataLoader(DS(train), batch_size=max(1, args.bs // 4), shuffle=True, num_workers=3, drop_last=True,
                    persistent_workers=True, collate_fn=lambda b: [torch.cat(z) for z in zip(*b)])

    def printed(cov, paper):  # page imprimée sur un papier de la couleur trouvée par l'IA 1
        return t_lin2srgb(print_t(t_srgb2lin(paper), cov))

    def loss_fn(m, b):
        x, E, sel, cov, cls, paper = b
        pc = m(x, E, sel)
        w = 1 + (cls == 1).float()[:, None] * 2  # le texte compte plus
        l_cov = ((pc - cov).abs() * w).mean()
        l_rgb = ((printed(pc, paper) - printed(cov, paper)).abs() * w).mean()
        # encre blanche : rare et invisible sur fond pâle, donc notée à part et fortement
        l_w = ((pc[:, 4] - cov[:, 4]).abs() * (1 + 20 * cov[:, 4])).mean()
        return l_cov + 2 * l_rgb + 3 * l_w

    def val_fn(m):
        errs = []
        ds = DS(val[:20], k=2)
        for i in range(len(ds)):
            x, E, sel, cov, cls, paper = ds[i]
            pc = m(x, E, sel)
            errs.append(((printed(pc, paper) - printed(cov, paper)).abs().mean() * 255).item())
        print("contrôle : écart moyen page réimprimée / page d'origine %.1f / 255" % np.mean(errs), flush=True)
        wv, wp = [], []
        for i in range(len(ds)):
            x, E, sel, cov, cls, paper = ds[i]
            m_ = cov[:, 4] > 0.5
            if m_.any():
                wv.append(((m(x, E, sel)[:, 4] > 0.5) & m_).sum().item() / m_.sum().item())
        print("contrôle : encre blanche retrouvée %.2f" % (np.mean(wv) if wv else -1), flush=True)

    run(PrintNet(), lambda: dl, loss_fn, args.minutes, "print", val_fn)
