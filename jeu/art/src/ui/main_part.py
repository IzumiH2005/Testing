

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render_only = "--render" in sys.argv
    names = args or list(REGISTRY)
    for n in names:
        fn, frames, doc = REGISTRY[n]
        if not render_only:
            c = fn()
            write_grid(n, c, frames, doc)
        img, fr = render(n)
        print(f"ok {n}: {img.width}x{img.height} ({fr} images)")
    contact()


def contact():
    """Planche générale : tous les assets ×2 sur d, étiquetés."""
    from build_fonts import text_strip
    items = []
    for n in REGISTRY:
        p = os.path.join(OUT_GAME, n + ".png")
        if os.path.exists(p):
            items.append((n, Image.open(p).convert("RGBA")))
    W = 1200
    x = y = 0
    rowh = 0
    placed = []
    for n, im in items:
        s = 2 if im.width * 2 <= W else 1
        w, h = im.width * s, im.height * s + 12
        if x + w > W:
            x, y = 0, y + rowh + 6
            rowh = 0
        placed.append((n, im, s, x, y))
        x += w + 8
        rowh = max(rowh, h)
    sheet = Image.new("RGBA", (W, y + rowh + 6), hex_to_rgba(PAL["d"]))
    for n, im, s, x, y in placed:
        sheet.alpha_composite(text_strip("font_5", n.upper(), "d"), (x, y))
        sheet.alpha_composite(im.resize((im.width * s, im.height * s), Image.NEAREST), (x, y + 12))
    sheet.save(os.path.join(OUT_ART, "planche_ui.png"))
    print("planche_ui.png", sheet.size)


if __name__ == "__main__":
    main()
