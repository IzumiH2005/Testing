#!/usr/bin/env python3
"""sfx.py : synthétise les bruitages et la musique d'ÉCHO en WAV 16 bits mono (22 050 Hz).
Usage : python3 sfx.py dossier_sortie/
"""
import math
import os
import random
import struct
import sys
import wave

SR = 22050
random.seed(7)


def write(path, samples):
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples))


def env(i, n, a=0.005, r=None):
    t = i / SR
    dur = n / SR
    r = dur if r is None else r
    e = min(1.0, t / a) if a > 0 else 1.0
    return e * max(0.0, 1.0 - t / r) ** 2


def square(ph, duty=0.5):
    return 1.0 if (ph % 1.0) < duty else -1.0


def tri(ph):
    p = ph % 1.0
    return 4 * p - 1 if p < 0.5 else 3 - 4 * p


def sweep(f0, f1, dur, wave_f=square, vol=0.3, duty=0.5):
    n = int(SR * dur)
    out, ph = [], 0.0
    for i in range(n):
        f = f0 + (f1 - f0) * i / n
        ph += f / SR
        v = wave_f(ph, duty) if wave_f is square else wave_f(ph)
        out.append(v * vol * env(i, n))
    return out


def noise(dur, vol=0.3, lp=0.5):
    n = int(SR * dur)
    out, last = [], 0.0
    for i in range(n):
        last = last + lp * (random.uniform(-1, 1) - last)
        out.append(last * vol * env(i, n))
    return out


def mix(*parts):
    n = max(len(p) for p in parts)
    return [sum(p[i] for p in parts if i < len(p)) for i in range(n)]


def notes(seq, dur, wave_f=square, vol=0.25, duty=0.25):
    out = []
    for f in seq:
        n = int(SR * dur)
        ph = 0.0
        for i in range(n):
            ph += f / SR
            v = wave_f(ph, duty) if wave_f is square else wave_f(ph)
            out.append(v * vol * env(i, n, 0.003))
    return out


def music():
    # boucle calme : basse triangle + arpège doux, la mineur, 96 bpm, 8 mesures
    bpm = 96
    beat = 60 / bpm
    prog = [(220.0, [440, 523.25, 659.25]), (174.61, [349.23, 440, 523.25]),
            (196.0, [392, 493.88, 587.33]), (164.81, [329.63, 415.3, 493.88])]
    total = int(SR * beat * 4 * 8)
    out = [0.0] * total
    pos = 0
    for bar in range(8):
        root, chord = prog[bar % 4]
        # basse : 2 blanches
        for k in range(2):
            n = int(SR * beat * 2)
            ph = 0.0
            for i in range(n):
                ph += root / 2 / SR
                out[pos + k * n + i] += tri(ph) * 0.16 * env(i, n, 0.02)
        # arpège en croches
        for s in range(8):
            f = chord[[0, 1, 2, 1, 0, 2, 1, 2][s]] * (2 if bar % 2 and s >= 4 else 1)
            n = int(SR * beat / 2)
            ph = 0.0
            st = pos + s * n
            for i in range(n):
                ph += f / SR
                out[st + i] += square(ph, 0.125) * 0.045 * env(i, n, 0.004, beat * 0.45)
        pos += int(SR * beat * 4)
    # écho simple (le thème du jeu)
    d = int(SR * beat * 0.75)
    for i in range(d, total):
        out[i] += out[i - d] * 0.28
    return out


def main():
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    s = {
        "jump": sweep(330, 660, 0.09, vol=0.18, duty=0.25),
        "turn": sweep(660, 990, 0.08, vol=0.16, duty=0.125),
        "land": noise(0.05, 0.25, 0.3),
        "shard": notes([1318.5, 1975.5], 0.06, vol=0.16, duty=0.25),
        "die": mix(sweep(440, 70, 0.4, vol=0.25, duty=0.5), noise(0.3, 0.3, 0.6)),
        "engrave": mix(notes([523.25, 783.99, 1046.5, 1567.98], 0.07, wave_f=tri, vol=0.3),
                       [0.0] * 600 + notes([1046.5], 0.25, wave_f=tri, vol=0.12)),
        "click": sweep(900, 700, 0.03, vol=0.15, duty=0.25),
        "record": notes([523.25, 659.25, 783.99, 1046.5, 783.99, 1046.5], 0.08, vol=0.18, duty=0.25),
        "reward": notes([659.25, 830.61, 987.77, 1318.5], 0.07, wave_f=tri, vol=0.3),
        "laser": sweep(1400, 1500, 0.12, vol=0.06, duty=0.5),
        "start": notes([392, 523.25, 659.25], 0.07, vol=0.16, duty=0.25),
        "deny": notes([220, 185], 0.08, vol=0.18, duty=0.5),
    }
    for k, v in s.items():
        write(os.path.join(od, k + ".wav"), v)
    write(os.path.join(od, "music.wav"), music())
    print("ok", len(s) + 1, "fichiers")


if __name__ == "__main__":
    main()
