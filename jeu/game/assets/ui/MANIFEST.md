# MANIFEST — assets d'interface (famille F9, UI_UX §7), palette v2

Tous les PNG de ce dossier n'utilisent que les couleurs de `studio/palette_v2.txt`, sans alpha partiel
(vérifié par script). Import Godot : filtre **Nearest**, pas de mipmaps, compression Lossless.

- **Sources** : `art/src/ui/build_ui.py` (dessin) + `uicore.py` (outils) → grilles texte éditables
  `art/src/ui/grids/<nom>.txt` ; icônes dessinées à la main dans `icons12.txt` / `icons16.txt` ;
  polices dans `font_5/7/8/l.font` (`build_fonts.py`). Une grille qui contient une ligne `# manuel`
  seule n'est plus réécrite par le script (retouche à la main possible).
- **Rebuild** : `cd art/src/ui && python3 build_fonts.py && python3 build_ui.py` (`--render` = rendre les
  grilles sans les régénérer ; on peut passer des noms d'assets).
- **Contrôle** : `art/out/ui/<nom>@8.png` (x8) et `<nom>_planche.png` (sur b, sur p, en gris, silhouette) ;
  planche générale `art/out/ui/planche_ui.png`.
- Convention des bandes : les images d'un asset sont côte à côte de gauche à droite, image i en
  `x = i * largeur_image`. « 9-patch marges N » = marges de `StyleBoxTexture` / `NinePatchRect`.

## Polices (BMFont texte .fnt + .png, chargeables en `FontFile` / police bitmap Godot)

| Fichier | Cellule | lineHeight / base | Avance | Glyphes | Crénage |
|---|---|---|---|---|---|
| font_5(.fnt/.png) | 5x8 | 8 / 7 | chasse 4 (M W N Æ Œ plus larges), espace 3 | capitales seulement (minuscules = alias), chiffres, ponctuation, accents FR, ◆ ▶ ★ … (142) | aucun |
| font_7 | 6x10 | 10 / 9 | chasse fixe 6 (largeur 5 + 1), espace 4 | capitales (minuscules = alias), accents FR, « » ’ … – — ◆ ◇ ▶ ↻ ↑ ↓ ← → ▮ ✕ ★ ☆ ∞ (142) | aucun |
| font_8 | 7x12 | 12 / 10 | proportionnelle (largeur + 1, de 2 à 7), espace 3 | casse mixte complète, accents FR, Œ œ Æ æ, symboles (142) | 12 paires à -1 : Te To Ta Ve Vo Ya Tu Tr Ty Vu Yo… |
| font_l | 10x16 | 16 / 15 | chasse 10 (M W : 12), trait 2 px, espace 4 | chiffres + capitales + accents FR, ponctuation de score, ▶ ◆ ★ (118) | aucun |
| font_*_outline | +2 px | idem | même xadvance que la police de base | idem | idem |
| font.fnt/.png | = font_7 | 10 / 9 | — | ancien nom gardé pour `assets.gd` | — |

Les variantes `_outline` ont un contour k de 1 px intégré au glyphe : `xoffset`/`yoffset` = -1 pour que
le tracé reste aligné sur la police de base. Couleur des glyphes : w (teinter avec `font_color`).
Les tailles Godot (`font_size`) doivent être celles du .fnt (8, 10, 12, 16) ou leurs multiples entiers.

## Assets

Les assets marqués P1/P2 sont hors du lot P0. `icons.png` est un atlas de compatibilité.

### panel.png — 24x24, 1 image(s)
panel 24x24 · 9-patch marges 8 (content_margin 8). Fond d ; bordure pierre 3 px : anneau 1 l (haut-gauche, arête éclairée) / n (bas-droite), anneau 2 s, anneau 3 creux n (haut-gauche) / m (bas-droite) ; sceaux d'écho t aux coins ; contour k.

### panel_echo.png — 24x24, 1 image(s)
panel_echo 24x24 · 9-patch marges 8. Panneau « écho » (vidéo, confirmation, record). Fond d ; bordure q t c : anneau 1 c / q, anneau 2 t, anneau 3 q / c ; sceaux e aux coins ; contour k.

### panel_inset.png — 24x24, 1 image(s)
panel_inset 24x24 · 9-patch marges 6. Creux (listes, cases, champs). Fond b ; anneau creux k en haut-gauche / n en bas-droite ; ombre portée intérieure d sur la 2e rangée et la 2e colonne ; pas de contour extérieur.

### btn_main.png — 144x24, 3 image(s)
btn_main 144x24 = 3 images 48x24 : 0 normal · 1 enfoncé · 2 désactivé. 9-patch marges gauche 8, droite 8, haut 6, bas 8 (zone étirée : colonnes 8-39, rangées 6-15). Normal : contour k arrondi, biseau haut a (2 rangées) + reflet A, face o, bord droit r, épaisseur R (2 rangées) + pied r. Enfoncé : la face descend de 2 px, plus d'épaisseur. Désactivé : position enfoncée, face n, biseau s, libellé m. Libellé font_7 k, y 7 (9 enfoncé).

### btn_alt.png — 144x24, 3 image(s)
btn_alt 144x24 = 3 images 48x24 : 0 normal · 1 enfoncé · 2 désactivé. 9-patch marges gauche 8, droite 8, haut 6, bas 8 (zone étirée : colonnes 8-39, rangées 6-15). Normal : contour k arrondi, biseau haut m (2 rangées) + reflet l, face s, bord droit d, épaisseur n (2 rangées) + pied d. Enfoncé : la face descend de 2 px, plus d'épaisseur. Désactivé : position enfoncée, face n, biseau s, libellé m. Libellé font_7 w, y 7 (9 enfoncé).

### btn_echo.png — 144x24, 3 image(s)
btn_echo 144x24 = 3 images 48x24 : 0 normal · 1 enfoncé · 2 désactivé. 9-patch marges gauche 8, droite 8, haut 6, bas 8 (zone étirée : colonnes 8-39, rangées 6-15). Normal : contour k arrondi, biseau haut e (2 rangées) + reflet W, face c, bord droit q, épaisseur t (2 rangées) + pied q. Enfoncé : la face descend de 2 px, plus d'épaisseur. Désactivé : position enfoncée, face n, biseau s, libellé m. Libellé font_7 k, y 7 (9 enfoncé). Seule face cyan autorisée hors écho (ARBITRAGES A12 : face c, texte k).

### tab.png — 72x20, 3 image(s)
tab 72x20 = 3 images 24x20 : 0 inactif · 1 actif · 2 enfoncé. 9-patch marges 6. Inactif : face d, bord n, libellé l. Actif : face s, haut m, trait a de 2 px en bas, libellé w. Enfoncé : face n. Coins hauts arrondis, base droite (l'onglet se pose sur le panneau).

### bar.png — 40x6, 5 image(s)
bar 40x6 = 5 images 8x6, 9-patch marges 2. 0 cadre (contour k, fond b) · 1 remplissage XP j/J · 2 or G/y · 3 écho c/e · 4 danger z/Z. Les remplissages se posent dans le cadre (même 9-patch), rangée 1 claire, rangées 2-4 base.

### badge_new.png — 28x7, 4 image(s)
badge_new 28x7 = 4 images 7x7 (pop en boucle, 120 ms) : 7x7 · 7x7 + reflet y · 5x5 · 7x7. Rond G, « ! » k 1x4 (barre 3 + point), contour k.

### hud_pip.png — 4x2, 2 image(s)
hud_pip 4x2 = 2 images 2x2 : 0 vide n · 1 plein G (compteur de vies / combo du HUD).

### diff_pips.png — 12x4, 3 image(s)
diff_pips 12x4 = 3 images 4x4 : 0 facile rond l · 1 moyen losange a · 2 dur triangle o. Contour k ; les trois formes diffèrent aussi en silhouette (lecture sans couleur).

### icons12.png — 288x12, 24 image(s)
icons12 288x12 = 24 icônes 12x12 (source à la main : art/src/ui/icons12.txt). Index : 0=pause 1=shard 2=prism 3=xp 4=volte 5=rythme 6=tide 7=burin 8=plume 9=calme 10=aimant 11=lanterne 12=elan 13=lock 14=check 15=cross 16=video 17=flame 18=ice 19=trophy 20=grave 21=altar 22=arrow_down 23=chest_mini

### icons16.png — 256x16, 16 image(s)
icons16 256x16 = 16 icônes 16x16 (source à la main : art/src/ui/icons16.txt). Index : 0=play 1=replay 2=home 3=share 4=video 5=shop 6=journal 7=codex 8=trophy 9=gear 10=daily 11=back 12=sound 13=music 14=vibration 15=shield

### hud_bar.png — 180x20, 1 image(s)
hud_bar 180x20 : bandeau haut du HUD. Rangées 0-15 k plein ; 16-17 trame Bayer 50 % k ; 18-19 trame 25 % k (fondu vers le jeu sans alpha).

### ui_lantern.png — 48x12, 4 image(s)
ui_lantern 48x12 = 4 images 12x12 (vies du HUD). 0 allumée (verre o a A, cœur W) · 1 flamme alternée (vacille, 2 images à 200 ms) · 2 s'éteint (verre n, braise a, fumée l) · 3 éteinte = écho (verre q t c e, la vie devient écho). Chapeau m l, socle n, contour k.

### banner.png — 96x16, 2 image(s)
banner 96x16 = 2 images 48x16, 9-patch marges 6 (gauche/droite), 4 (haut/bas). 0 or : face G, biseau y, ombre g, contour k, encoches en V aux deux bouts (record, niveau). 1 pierre : face s, biseau m, ombre n, contour k (titres de section).

### toast.png — 24x16, 1 image(s)
toast 24x16, 9-patch marges 6. Fond k, bordure n, arête m en haut (1 px). Coins coupés.

### banner_tuto.png — 64x24, 1 image(s)
banner_tuto 64x24, 9-patch marges 6. Bandeau tutoriel court : fond d, bordure n s (anneau s éclairé en haut-gauche, n en bas-droite), contour k. Le pictogramme tuto16 se pose à x 4, y 4.

### tuto16.png — 96x32, 6 image(s)
tuto16 96x32 = 6 pictogrammes 16x16 x 2 poses. Rangée 0 = pose A, rangée 1 = pose B (alterner 400 ms). Colonnes : 0 tap · 1 maintenir (doigt + arc qui s'allonge) · 2 volte (tap en l'air, arc de demi-tour) · 3 glisser · 4 danger (triangle + dents) · 5 autel (flamme qui grandit). Couleurs w + l, contour k. Pictogrammes sans texte.

### tap.png — 64x32, 2 image(s)
tap 64x32 = 2 images 32x32 (400 ms par image) : main posée sur le mur, à côté du héros. 0 doigt levé · 1 doigt appuyé (main descendue de 3 px, impacts I). Couleurs i I (+ H pour l'ombre du poignet), contour k. Remplace sprites/tap.png (32x16, v1), qui reste en place pour main.gd.

### stamp_frame.png — 320x24, 5 image(s)
stamp_frame 320x24 = 5 images 64x24 (pop du tampon « RECORD », 50 ms/image) : 0 50 % (27x10) · 1 115 % (62x23) · 2 écrasé (60x18) · 3 final (54x20) · 4 final + étincelle e. Plaque d, double filet or G/g + reflet y, contour k. Texte posé par-dessus en font_l_outline.

### card.png — 96x24, 4 image(s)
card 96x24 = 4 images 24x24, 9-patch marges 6 (cartes de boutique / tenues). 0 normal : creux (panel_inset) + bordure n · 1 sélectionnée : bordure w 1 px + coins a · 2 équipée : bordure G (+ reflet y) · 3 verrouillée : fond k, bordure n, trame d.

### shop_pedestal.png — 64x16, 1 image(s)
shop_pedestal 64x16 : socle de pierre de la boutique (la tenue se pose dessus, y 0). Plateau l (arête) / m, devant s avec joints n, pied n, contour k.

### chest.png — 256x32, 8 image(s)
chest 256x32 = 8 images 32x32 (coffre de palier) : 0-1 secousse ±1 px · 2-4 ouverture (couvercle qui bascule, lueur G, pic W sur l'image 3 seulement) · 5-6 lueur ouverte en boucle (étincelles y) · 7 ouvert, final. Pierre s/m/n, cerclages et serrure G/g/y, contour k.

### popup_reward.png — 384x64, 6 image(s)
popup_reward 384x64 = 6 images 64x64, 83 ms par image, en boucle (rotation de 7,5° par image : 8 rayons = période 45°, la 7e image retombe sur la 1re). Rayons G (y près du centre, pointes tramées) sur disque d ; anneau n puis contour k. L'objet gagné se pose au centre.

### shard_mini.png — 24x6, 4 image(s)
shard_mini 24x6 = 4 images 6x6 : éclat qui tourne (100 ms/image). 0 face · 1 trois-quarts · 2 tranche · 3 trois-quarts inversé. Or g G y + o, contour k.

### dither.png — 16x4, 4 image(s)
dither 16x4 = 4 images 4x4 : trame Bayer k à 25 / 50 / 75 / 100 % (fondus d'écran sans alpha, 4 pas de 50 ms). Se répète en mosaïque (TextureRect tile).

### xp_badge.png — 40x20, 2 image(s)
xp_badge 40x20 = 2 images 20x20 : pastille de niveau (le nombre est écrit par-dessus en font_7_outline). 0 normal : disque u, anneau U/j, reflet J, contour k · 1 montée de niveau : anneau G/g, reflets y, étincelles y aux coins.

### cal_cell.png — 60x28, 3 image(s)
cal_cell 60x28 = 3 images 20x28 (case du calendrier de la tour du jour). 0 à venir : creux b (k haut-gauche, n bas-droite), chiffre écrit en s · 1 aujourd'hui : bordure a 1 px + fond d, chiffre w · 2 obtenu : fond n, coche f/F en bas.

### codex_cell.png — 108x40, 3 image(s)
codex_cell 108x40 = 3 images 36x40 (case du codex : le piège 32x32 se pose en x 2, y 2). 0 inconnu : fond k, trame d, bordure n, « ? » s · 1 vu : creux b, bordure s · 2 maîtrisé : creux b, bordure G/g, reflet y, coins y.

### star5.png — 10x5, 2 image(s)
star5 10x5 = 2 images 5x5 : étoile de niveau 0 vide n · 1 pleine G (pointe y). Sans contour : posée sur fond sombre.

### toggle.png — 96x16, 3 image(s)
toggle 96x16 = 3 images 32x16 (bascules des réglages). 0 coupé : rail n, bouton m à gauche · 1 actif : rail f, bouton w à droite avec coche f · 2 barre « coupé » z 2 px en diagonale, 16x16 calée à gauche (posée par-dessus une icône 16 teintée s).

### slider.png — 24x12, 3 image(s)
slider 24x12 : x 0-7 = rail (rangées 0-3 vide : contour k, fond n ; rangées 4-7 rempli : contour k, l + reflet p), 9-patch marges 2 · x 8-15 = curseur 8x12 normal (m, arête l) · x 16-23 = curseur enfoncé (l, arête w).

### logo.png — 960x48, 6 image(s)
logo 960x48 = 6 images 160x48 (100 ms/image ; l'image 0 est le logo fixe). Lettres de art/src/ui/logo.txt (dessin v1 à la main, lettres p w l k + échos c t) rendues en palette v2, centrées dans 160x48. Images 1-5 : reflet W qui balaie les lettres en diagonale (bande de 3 px).

### icons.png — 252x12, 21 image(s)
icons 252x12 = 21 icônes 12x12 : atlas de COMPATIBILITÉ pour ui_kit.gd (ordre UIK : 0=LIFE 1=LIFE_USED 2=SHARD 3=PLAY 4=SHARE 5=VIDEO 6=GEAR 7=SOUND_ON 8=SOUND_OFF 9=BACK 10=TROPHY 11=CALENDAR 12=LOCK 13=CHECK 14=PAUSE 15=FLAME 16=VIBRATION 17=HOME 18=SKULL 19=CROWN 20=SCARF). LIFE/LIFE_USED = ui_lantern 0/3 ; SHARD, LOCK, CHECK, PAUSE, FLAME, TROPHY, VIDEO = icons12 ; les autres = anciennes grilles de art/src/ui/icons.txt rendues en palette v2. À abandonner quand le code utilisera icons12/icons16.

### confetti.png — 24x3, 8 image(s)
confetti 24x3 = 8 images 3x3 : 4 couleurs (G o c j) x 2 orientations (plat, tranche). Pas de contour (particules de 1-3 px).

### star8.png — 24x8, 3 image(s)
star8 24x8 = 3 images 8x8 : étoile de fin de niveau 0 vide (n, contour k) · 1 pleine (G y, contour k) · 2 éclat (pleine + cœur W, 1 image de flash).

### level_node.png — 64x16, 4 image(s)
level_node 64x16 = 4 images 16x16 (carte des niveaux) : 0 verrouillé (pierre n s, cadenas k) · 1 disponible (pierre m l, cœur a) · 2 réussi (or G y) · 3 actuel (anneau c pulsé : 1 image).

### focus_ring.png — 8x8, 1 image(s)
focus_ring 8x8, 9-patch marges 3 (P2) : anneau de focus clavier / manette, c 1 px, coins e. Posé autour du contrôle avec 1 px d'écart.

## Index d'icônes (rappel)

- icons12 : 0 pause · 1 shard · 2 prism · 3 xp · 4 volte · 5 rythme · 6 tide · 7 burin · 8 plume · 9 calme ·
  10 aimant · 11 lanterne · 12 elan · 13 lock · 14 check · 15 cross · 16 video · 17 flame · 18 ice ·
  19 trophy · 20 grave · 21 altar · 22 arrow_down · 23 chest_mini.
- icons16 : 0 play · 1 replay · 2 home · 3 share · 4 video · 5 shop · 6 journal · 7 codex · 8 trophy ·
  9 gear · 10 daily · 11 back · 12 sound · 13 music · 14 vibration · 15 shield.
  play, replay et video sont en k sans contour : à poser sur une face claire (btn_main / btn_echo).
  Son, musique, vibration « coupés » : teinter l'icône en s et poser `toggle.png` image 2 par-dessus.

## Changements .gd nécessaires (non faits : hors périmètre F9)

1. **ui_kit.gd `button()`** : les boutons font maintenant 3 images de **48x24** (et non 24x24).
   `sb_tex(name, frame, 48, ...)` ; marges 9-patch gauche 8, haut 6, droite 8, bas 8 ;
   content_margin normal ≈ (8, 5, 8, 7), enfoncé ≈ (8, 7, 8, 5) (le libellé descend de 2 px) ;
   style `disabled` = **image 2** (aujourd'hui `normal`), `font_disabled_color` = m.
2. **ui_kit.gd `icon()`** : l'atlas `ui/icons` (21 icônes, ordre UIK) reste valable et a été refait en v2.
   Pour passer aux nouvelles icônes : `ui/icons12` (Rect2(i*12,0,12,12)) et `ui/icons16`
   (Rect2(i*16,0,16,16)) avec les index ci-dessus ; `icons.png` pourra alors être supprimé.
3. **ui_kit.gd `panel()`** : inchangé (24x24, marges 8). Prévoir `panel_inset` (marges 6) pour les listes.
4. **main.gd logo** : `logo.png` est une bande de 6 images 160x48 → utiliser une `AtlasTexture`
   Rect2(0,0,160,48) (ou animer les 6 images à 100 ms pour le reflet). Aujourd'hui la texture
   entière (960x48) est affichée.
5. **main.gd main tap** : `sprites/tap.png` (32x16, régions 16x16) a été refait en v2 et reste
   compatible. La version §7 est `ui/tap.png` (2 images 32x32) : région Rect2(i*32,0,32,32).
6. Nouveaux assets sans code : HUD (hud_bar, ui_lantern, hud_pip), bandeaux, toast, tuto16, tampon,
   coffre, popup, xp_badge, calendrier, codex, toggle, slider, etc. Durées conseillées dans chaque entrée.

## Manquant

- P1 non produits : `countdown` (216x32, à faire avec font_l), `biome16`, `share_card`, `splash`,
  `icon_adaptive`. P1 produits : confetti, star8, level_node ; P2 : focus_ring.
