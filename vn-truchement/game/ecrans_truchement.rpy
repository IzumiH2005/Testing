## Écrans propres à Truchement : compte à rebours et Journal de la nuit.

init python:
    def note(moment, langue, original, dit, altere):
        """Consigne une traduction dans le journal de la nuit.

        langue : "n" si la phrase d'origine est en nordique, "v" si en valléen.
        altere : True si Ilan a changé, coupé ou inventé quelque chose.
        """
        store.journal_lignes.append((moment, langue, original, dit, altere))
        store.nb_trad += 1
        if altere:
            store.nb_alt += 1
        renpy.fix_rollback()

    def fins_trouvees():
        return len(set(persistent.fins or ()))


## Barre qui se vide pendant le dernier choix. Quand elle est vide, Ilan se tait.
screen compte_a_rebours(duree, cible):
    zorder 100
    timer duree action [Hide("compte_a_rebours"), Jump(cible)]
    bar:
        value AnimatedValue(0, duree, duree, duree)
        xalign 0.5
        ypos 48
        xsize 960
        ysize 6
        left_bar Solid("#c8913a")
        right_bar Solid("#ffffff1a")
        thumb None


style journal_texte is default:
    font "fonts/CrimsonPro.ttf"
    size 29
    line_spacing 4

style journal_moment is journal_texte:
    size 22
    color "#8a857c"
    italic True

screen journal():
    modal True
    add Solid("#0c0d10")

    vbox:
        xalign 0.5
        ypos 64
        xsize 1560
        spacing 14

        text "Journal de la nuit" size 68 color "#c8913a" font "fonts/CrimsonPro.ttf"
        text "Cette nuit, vous avez transmis [nb_trad] répliques. Vous en avez changé [nb_alt]." style "journal_texte" color "#dcd8d0"

        null height 10
        hbox:
            spacing 60
            text "Ce qui a été dit" style "journal_texte" size 24 color "#8a857c" xsize 720
            text "Ce que vous avez dit" style "journal_texte" size 24 color "#8a857c" xsize 720

        viewport:
            ysize 680
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 30
                for moment, langue, original, dit, altere in journal_lignes:
                    vbox:
                        spacing 6
                        text (moment + ("   ·   modifié" if altere else "   ·   fidèle")) style "journal_moment" color ("#d9a25a" if altere else "#8a857c")
                        hbox:
                            spacing 60
                            text original style "journal_texte" xsize 720 color (C_NORD_TXT if langue == "n" else C_VAL_TXT)
                            text dit style "journal_texte" xsize 720 color (C_VAL_TXT if langue == "n" else C_NORD_TXT)

    hbox:
        xalign 0.5
        yalign 0.97
        spacing 80
        text "Fins découvertes : [fins_trouvees()] sur 6" style "journal_texte" size 24 color "#8a857c" yalign 0.5
        textbutton "Continuer" action Return() text_size 34 text_font "fonts/CrimsonPro.ttf"
