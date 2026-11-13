#!/usr/bin/env python3
"""situation.py : planche « en situation » des FX F2/F4/F5 sur le décor du jeu (critère 9).
Compose les PNG déjà rendus (aucun pixel nouveau) ; sortie art/out/fx/situation_fx.png (×4).
"""
import os
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
A = os.path.join(ROOT, "game", "assets")


def cell(name, i, w, h, sub="fx"):
    im = Image.open(os.path.join(A, sub, name + ".png")).convert("RGBA")
    return im.crop((i * w, 0, i * w + w, h))


def main():
    S = Image.new("RGBA", (192, 176), (35, 32, 61, 255))
    back = Image.open(os.path.join(A, "env", "back.png")).convert("RGBA")
    wall = Image.open(os.path.join(A, "env", "wall.png")).convert("RGBA")
    for y in range(0, 176, 16):
        for x in range(16, 176, 16):
            S.alpha_composite(back.crop((((x // 16 + y // 16) % 7) * 16, 0, ((x // 16 + y // 16) % 7) * 16 + 16, 16)), (x, y))
        S.alpha_composite(wall.crop((0, 0, 16, 16)), (0, y))
        S.alpha_composite(wall.crop((16, 0, 32, 16)).transpose(Image.FLIP_LEFT_RIGHT), (176, y))
    player = Image.open(os.path.join(A, "sprites", "player.png")).convert("RGBA").crop((0, 0, 16, 16))
    S.alpha_composite(player, (16, 40))
    S.alpha_composite(cell("fx_dust_wall", 1, 16, 16), (16, 44))
    S.alpha_composite(cell("fx_land", 1, 16, 16), (16, 70))
    S.alpha_composite(cell("fx_turn", 0, 16, 16), (60, 30))
    S.alpha_composite(cell("fx_turn_echo", 0, 16, 16), (96, 30))
    for k, x in enumerate((44, 56, 68)):
        S.alpha_composite(cell("shard", k, 8, 8), (x, 64))
    S.alpha_composite(cell("shard_big", 2, 16, 16), (90, 58))
    S.alpha_composite(cell("powerup_bubble", 0, 16, 16), (120, 56))
    S.alpha_composite(cell("pu_burin", 0, 8, 8), (124, 60))
    S.alpha_composite(cell("feather_gold", 0, 16, 16), (148, 56))
    S.alpha_composite(cell("echo_shard", 0, 8, 8), (40, 90))
    S.alpha_composite(cell("grave", 2, 16, 16), (60, 86))
    S.alpha_composite(cell("fx_engrave_seal", 1, 16, 16), (80, 86))
    S.alpha_composite(cell("shard_pop", 2, 16, 16), (100, 86))
    S.alpha_composite(cell("fx_graze", 1, 16, 16), (120, 86))
    S.alpha_composite(cell("fx_echo_recharge", 2, 16, 16), (140, 86))
    S.alpha_composite(cell("altar", 1, 32, 32), (100, 104))
    S.alpha_composite(cell("altar_flame", 0, 8, 16), (112, 99))
    S.alpha_composite(cell("altar", 0, 32, 32), (40, 104))
    glow = Image.open(os.path.join(A, "tide", "tide_glow.png")).convert("RGBA")
    crest = cell("tide_crest", 0, 32, 16, "tide")
    body = Image.open(os.path.join(A, "tide", "tide_body.png")).convert("RGBA")
    for x in range(0, 192, 32):
        # additif : on ajoute RVB × alpha
        reg = S.crop((x, 132, x + 32, 148))
        px, gp = reg.load(), glow.load()
        for j in range(16):
            for i in range(32):
                r, g, b, a = gp[i, j]
                R, Gg, B, _ = px[i, j]
                px[i, j] = (min(255, R + r * a // 255), min(255, Gg + g * a // 255), min(255, B + b * a // 255), 255)
        S.paste(reg, (x, 132))
        S.alpha_composite(crest, (x, 148))
        S.alpha_composite(body.crop((0, 0, 32, 12)), (x, 164))
    S = S.resize((S.width * 4, S.height * 4), Image.NEAREST)
    S.save(os.path.join(ROOT, "art", "out", "fx", "situation_fx.png"))
    S.save(os.path.join(ROOT, "art", "out", "tide", "situation_fx.png"))


if __name__ == "__main__":
    main()
