"""Construction des prismes du grand cristal (gabarit des facettes, B6-D étapes 1 à 3).
Chaque prisme est décidé par des nombres choisis à la main : position du pied, largeur des
trois faces (gauche éclairée, avant, droite dans l'ombre), hauteur, pente (1 px tous les n
rangs, une pente propre), hauteur et décalage de la pointe."""

W = H = 32

def prisme(nom, x0, ybas, faces, haut_corps, sens, tous_les, haut_pointe, pointe_dx):
    """Renvoie {(x, y): étiquette}. Étiquettes : nom+'g' / 'a' / 'd' pour les faces,
    nom+'G' / 'A' / 'D' pour les facettes de la pointe, 'O' pour le contour."""
    lignes = {}  # y -> (gauche, droite) bords extérieurs (contour compris)
    larg = 1 + sum(faces) + 1
    for k in range(haut_corps):
        y = ybas - k
        off = sens * (k // tous_les)
        lignes[y] = (x0 + off, x0 + off + larg - 1)
    ytop = ybas - haut_corps + 1
    Lt, Rt = lignes[ytop]
    P = Lt + pointe_dx
    for t in range(1, haut_pointe + 1):
        y = ytop - t
        f = t / haut_pointe
        lignes[y] = (round(Lt + (P - Lt) * f), round(Rt + (P - Rt) * f))
    ypointe = ytop - haut_pointe
    b1 = Lt + 1 + faces[0]          # premier px de la face avant au sommet du corps
    b2 = b1 + faces[1]              # premier px de la face droite
    out = {}
    ys = sorted(lignes)
    for y in ys:
        L, R = lignes[y]
        for x in range(L, R + 1):
            if y >= ytop:  # corps
                k = ybas - y; off = sens * (k // tous_les)
                fx = x - (x0 + off)
                e = 'g' if fx <= faces[0] else ('a' if fx <= faces[0] + faces[1] else 'd')
            else:          # pointe : arêtes du haut des faces jusqu'à la pointe
                f = (ytop - y) / haut_pointe
                r1 = b1 + (P - b1) * f
                r2 = b2 + (P + 1 - b2) * f
                e = 'G' if x < r1 else ('A' if x < r2 else 'D')
            out[(x, y)] = nom + e
    # contour : extrémités de chaque rang, prolongées jusqu'au rang du dessus (trait 8-connexe)
    prev = None
    for y in ys:
        L, R = lignes[y]
        if prev is None:
            for x in range(L, R + 1): out[(x, y)] = 'O'
        else:
            pL, pR = prev
            for x in range(L, max(L, pL - 1) + 1): out[(x, y)] = 'O'
            for x in range(min(R, pR + 1), R + 1): out[(x, y)] = 'O'
        prev = (L, R)
    return out

# Les quatre prismes (A4b : grand, moyen, petit, minuscule ; chacun penché autrement)
P1 = prisme('1', 11, 28, (3, 3, 3), 20, -1, 6, 8, 4)   # grand, penche à gauche
P2 = prisme('2', 18, 28, (2, 2, 2), 16, +1, 5, 6, 5)   # moyen derrière, penche à droite
P3 = prisme('3', 5, 28, (2, 2, 2), 9, -1, 4, 5, 2)     # petit devant à gauche, penche à gauche
P4 = prisme('4', 24, 26, (1, 2, 1), 4, +1, 3, 3, 3)    # minuscule devant à droite
ORDRE = [P2, P1, P4, P3]  # du fond vers l'avant
