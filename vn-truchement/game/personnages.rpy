## Personnages, couleurs des langues, images.
##
## Code couleur (règle de lecture du jeu) :
##   bleu-gris = nordique (la langue de l'occupant)
##   ocre      = valléen (la langue de la vallée de Sauve)
##   gris clair = narration (Ilan)

define C_NORD = "#9db4cc"
define C_NORD_TXT = "#d6e2ef"
define C_VAL = "#d9a25a"
define C_VAL_TXT = "#f2dcb5"
define C_NARR = "#dcd8d0"

define TAG_NORD = "  {size=-20}{i}nordique{/i}{/size}"
define TAG_VAL = "  {size=-20}{i}valléen{/i}{/size}"

define narrator = Character(None, what_color=C_NARR)
define pense = Character(None, what_color="#a9a49b", what_italic=True)

define v = Character("Capitaine Vey", image="vey", color=C_NORD, what_color=C_NORD_TXT, who_suffix=TAG_NORD)
define m = Character("Mara Lenz", image="mara", color=C_VAL, what_color=C_VAL_TXT, who_suffix=TAG_VAL)
## Mara quand elle parle nordique (à partir de la révélation).
define mn = Character("Mara Lenz", image="mara", color=C_NORD, what_color=C_NORD_TXT, who_suffix=TAG_NORD)

## Ilan parle toujours dans la langue de celui à qui il s'adresse.
define inn = Character("Ilan", color=C_NORD, what_color=C_NORD_TXT, who_suffix=TAG_NORD)
define iv = Character("Ilan", color=C_VAL, what_color=C_VAL_TXT, who_suffix=TAG_VAL)

define lettre = Character(None, what_color=C_VAL_TXT, what_italic=True)
define voix = Character("Une voix, derrière le mur", color=C_VAL, what_color=C_VAL_TXT, who_suffix=TAG_VAL)

init python:
    ## Italique : utiliser la vraie fonte italique plutôt qu'une italique simulée.
    config.font_replacement_map["fonts/CrimsonPro.ttf", False, True] = ("fonts/CrimsonPro-Italic.ttf", False, False)


## Portraits ------------------------------------------------------------------
##
## Remplacez simplement les PNG de images/persos/ par les vrais portraits,
## en gardant exactement les mêmes noms de fichiers. Le transform « portrait »
## les met à l'échelle automatiquement (ils tiennent dans 820 x 1000 px,
## posés sur le bas de l'écran), donc la résolution exacte importe peu tant que
## tous les portraits d'un même personnage ont le même cadrage.

transform portrait:
    fit "contain"
    xysize (820, 1000)

transform gauche:
    xcenter 0.25
    yalign 1.0

transform droite:
    xcenter 0.75
    yalign 1.0

define EXPR_MARA = ["neutre", "inquiete", "dure", "triste", "sourire", "determinee", "surprise"]
define EXPR_VEY = ["neutre", "las", "agace", "rire", "grave", "emu"]

init 1 python:
    for _e in EXPR_MARA:
        renpy.image(("mara", _e), At("images/persos/mara_%s.png" % _e, portrait))
    for _e in EXPR_VEY:
        renpy.image(("vey", _e), At("images/persos/vey_%s.png" % _e, portrait))


## Décors ---------------------------------------------------------------------

image bg poste = "images/decors/bg_poste.png"
image bg poste_sombre = "images/decors/bg_poste_sombre.png"
image bg poste_aube = "images/decors/bg_poste_aube.png"
image bg col = "images/decors/bg_col.png"
image bg cellule = "images/decors/bg_cellule.png"
