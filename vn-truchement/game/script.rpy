## Truchement — script principal.
##
## Variables d'état. Aucune n'est affichée au joueur.

default confiance = 0          # ce que Mara pense d'Ilan (seuil : 4)
default mens_mara = 0          # mensonges « gentils » faits à Mara
default mens_vey = 0           # mensonges faits au capitaine
default bottes = False         # a omis « essuyez vos bottes »
default plaisanterie = None    # "traduite" / "coupee" / "adoucie"
default coups = None           # "escalier" / "oui" / "va_bien"
default origine_vey = None     # "ici" / "nord"
default origine_mara = None    # "ici" / "esquive"
default incoherence = False
default sac = None             # "lettres" / "tabac" / "ignore"
default clause = None          # "lue" / "omise"
default lettre_lue = None      # "fidele" / "resume" / "embellie"
default peine = "trois mois"
default transfert_dit = None
default gants = None           # None : jamais proposé ; True / False sinon
default sac_action = None      # "brule" / "emporte" / "laisse"
default journal_lignes = []
default nb_trad = 0
default nb_alt = 0
default persistent.fins = set()


label start:

    scene black
    centered "{size=+6}Le bleu est la langue du Nord.\nL'ocre est celle de la vallée.{/size}\n\n{size=-6}{color=#8a857c}Ilan parle toujours la langue de celui à qui il s'adresse.{/color}{/size}"

    centered "{size=+16}Le troisième hiver de l'occupation.{/size}\n\nCol de la Brèche. Poste-frontière numéro quatre.\nTrois heures du matin."

    scene bg poste with fade

    "Il y avait trois choses dans le poste du col de la Brèche : un poêle, un capitaine, et moi."
    "Le poêle chauffait. Le capitaine signait. Moi, je traduisais."
    "Je m'appelle Ilan Sorel. J'ai grandi en bas, dans la vallée de Sauve, au moulin. À treize ans, on m'a envoyé à l'école du Nord. J'en suis revenu avec une langue de plus et une maison de moins."
    "En valléen, il n'existe qu'un seul mot pour dire traduire : {i}passer{/i}. On l'emploie aussi pour la contrebande, pour ceux qui changent de camp, et pour les morts."
    "Depuis deux ans, je passais des phrases. Les gens de la vallée parlaient valléen. Les soldats parlaient nordique. Entre les deux, il y avait moi."
    pense "Je ne suis qu'une voix. C'est ce que je me répétais. C'est ce qui permettait de dormir."

    show vey las at droite with dissolve

    "Le capitaine Albrecht Vey triait ses trombones par taille. Il faisait ça quand il était fatigué. Il était toujours fatigué."
    v "L'inspecteur arrive à l'aube, Sorel. À l'aube. Je veux un dossier propre."
    v neutre "Un dossier propre, et je rentre pour Noël. Vous savez depuis combien de temps je n'ai pas passé Noël chez moi ?"
    inn "Trois ans, mon capitaine."
    v las "Trois ans. Faites entrer la femme."

    show mara neutre at gauche with dissolve

    "Elle s'appelait Mara Lenz. Vingt-neuf ans, un manteau trop grand pour elle, de la neige jusqu'aux genoux."
    "Elle portait des gants de laine grise. Elle ne les a pas enlevés de la nuit."

    v agace "Dites-lui de s'asseoir. Et d'essuyer ses bottes, bon sang. Elle met de la neige partout."

    menu:
        "Traduire fidèlement.":
            iv "Le capitaine vous demande de vous asseoir. Et d'essuyer vos bottes."
            $ note("L'entrée", "n", "« Dites-lui de s'asseoir. Et d'essuyer ses bottes, bon sang. Elle met de la neige partout. »", "« Le capitaine vous demande de vous asseoir. Et d'essuyer vos bottes. »", False)
            "Elle s'est assise, puis elle a essuyé ses bottes sur le tapis, sans un mot."

        "Omettre les bottes. Elle a fait trois heures de marche.":
            $ bottes = True
            iv "Asseyez-vous, je vous en prie."
            $ note("L'entrée", "n", "« Dites-lui de s'asseoir. Et d'essuyer ses bottes, bon sang. Elle met de la neige partout. »", "« Asseyez-vous, je vous en prie. »", True)
            "Elle s'est assise. Puis elle a regardé ses bottes, et elle les a essuyées sur le tapis, lentement, l'une après l'autre."
            pense "Je n'avais rien dit. Elle avait vu la neige, sans doute."

    v neutre "Elle peut enlever ses gants. Il fait chaud, ici. On n'est pas des sauvages."
    iv "Vous pouvez enlever vos gants."
    m "J'ai froid aux mains."
    inn "Elle a froid aux mains, mon capitaine."
    v las "Comme elle voudra."


    ## --- Le frère -------------------------------------------------------------

    m inquiete "Je viens pour mon frère. Tobias Lenz. Dix-sept ans. On m'a dit qu'il était ici."
    inn "Elle vient pour son frère, Tobias Lenz, dix-sept ans."
    v neutre "Lenz, Tobias. Arrêté à deux heures sur le sentier du col, avec un sac scellé et sans laissez-passer."
    v rire "Dites-lui que les contrebandiers, on les fusille au lever du jour."
    "Les mains gantées de Mara se sont serrées sur ses genoux. J'ai mis ça sur le compte du froid."
    v neutre "Je plaisante, Sorel. Traduisez sans la plaisanterie. Je n'ai pas envie d'une crise de larmes à trois heures du matin."

    menu:
        "Tout traduire, plaisanterie comprise.":
            $ plaisanterie = "traduite"
            $ confiance += 1
            iv "Votre frère a été arrêté à deux heures sur le col, avec un sac scellé. Le capitaine a dit qu'on fusillait les contrebandiers à l'aube. Puis il a dit qu'il plaisantait, et de ne pas vous le répéter."
            m dure "Il plaisante."
            iv "C'est ce qu'il dit."
            m "Merci de me l'avoir répété quand même."
            $ note("Le frère", "n", "« Arrêté à deux heures, avec un sac scellé. Les contrebandiers, on les fusille au lever du jour. Je plaisante. Traduisez sans la plaisanterie. »", "« Arrêté à deux heures, avec un sac scellé. Il a dit qu'on les fusillait. Puis qu'il plaisantait. »", False)

        "Obéir : traduire sans la plaisanterie.":
            $ plaisanterie = "coupee"
            iv "Votre frère a été arrêté à deux heures sur le col, avec un sac scellé et sans laissez-passer."
            m "..."
            $ note("Le frère", "n", "« Arrêté à deux heures, avec un sac scellé. Les contrebandiers, on les fusille au lever du jour. Je plaisante. Traduisez sans la plaisanterie. »", "« Arrêté à deux heures, avec un sac scellé et sans laissez-passer. »", True)

        "Adoucir : « C'est une formalité. »":
            $ plaisanterie = "adoucie"
            $ confiance -= 1
            $ mens_mara += 1
            iv "Votre frère a été arrêté cette nuit sur le col. C'est une formalité. Ça va s'arranger."
            m neutre "Une formalité."
            $ note("Le frère", "n", "« Arrêté à deux heures, avec un sac scellé. Les contrebandiers, on les fusille au lever du jour. Je plaisante. Traduisez sans la plaisanterie. »", "« Arrêté cette nuit. C'est une formalité. Ça va s'arranger. »", True)


    ## --- Les coups ------------------------------------------------------------

    m inquiete "Est-ce qu'on l'a frappé ?"
    inn "Elle demande si on l'a frappé."
    v neutre "Il est tombé dans l'escalier."
    "Il ne levait même pas les yeux de son dossier."
    "Il n'y avait pas d'escalier au poste du col de la Brèche. Il y avait une porte, une pièce, et une cellule derrière le mur. Pas une seule marche."
    "Mara a regardé autour d'elle avant même que j'ouvre la bouche."

    menu:
        "Traduire mot pour mot.":
            $ coups = "escalier"
            iv "Il dit qu'il est tombé dans l'escalier."
            m dure "..."
            "Elle a cherché l'escalier des yeux. Elle ne l'a pas trouvé. Elle n'a rien dit."
            $ note("Les coups", "n", "« Il est tombé dans l'escalier. »", "« Il dit qu'il est tombé dans l'escalier. »", False)

        "Dire ce que la phrase veut dire : « Oui. »":
            $ coups = "oui"
            $ confiance += 2
            iv "Oui."
            m triste "..."
            "Elle a hoché la tête, une fois, comme on signe un reçu."
            $ note("Les coups", "n", "« Il est tombé dans l'escalier. »", "« Oui. »", True)

        "La rassurer : « Il va bien. »":
            $ coups = "va_bien"
            $ confiance -= 2
            $ mens_mara += 1
            iv "Non. Il va bien, je vous assure."
            m neutre "Merci."
            pense "Elle m'a remercié. J'ai trouvé ça facile. J'aurais dû m'en méfier."
            $ note("Les coups", "n", "« Il est tombé dans l'escalier. »", "« Non. Il va bien, je vous assure. »", True)


    ## --- D'où viens-tu --------------------------------------------------------

    v neutre "Elle a l'accent du haut de la vallée."
    v las "Et vous, Sorel, au fait. Vous venez d'où ? Deux ans que vous êtes là, je n'ai jamais demandé."
    "Il l'avait demandé à voix basse, par habitude. Elle ne parlait pas un mot de nordique."

    menu:
        "« D'ici. Du moulin Sorel, en bas de la vallée. »":
            $ origine_vey = "ici"
            $ confiance += 1
            inn "D'ici, mon capitaine. Du moulin Sorel, en bas de la vallée."
            v grave "Ah. Je ne savais pas. Ça ne doit pas être simple, tous les jours."
            inn "Je ne suis qu'une voix, mon capitaine."
            v las "Si vous le dites."

        "« Du Nord. J'ai fait toutes mes études à Ostrau. »":
            $ origine_vey = "nord"
            $ confiance -= 1
            inn "Du Nord, mon capitaine. J'ai fait toutes mes études à Ostrau."
            v neutre "Ça s'entend. Vous parlez mieux que moi."

    $ renpy.fix_rollback()

    m neutre "Et vous, vous êtes d'où ? Vous parlez comme chez nous. Comme en bas, vers les moulins."

    menu:
        "« Du moulin Sorel. Je suis d'ici. »":
            $ origine_mara = "ici"
            $ confiance += 1
            iv "Du moulin Sorel. Je suis d'ici."
            m "Je me disais aussi."

        "Esquiver : « Ça n'a pas d'importance. Parlons de votre frère. »":
            $ origine_mara = "esquive"
            iv "Ça n'a pas d'importance. Parlons de votre frère."
            m dure "Pour moi, si. Mais comme vous voudrez."

    if origine_vey == "nord" and origine_mara == "ici":
        $ incoherence = True
        $ confiance -= 1

    $ renpy.fix_rollback()


    ## --- Le sac ---------------------------------------------------------------

    v grave "Bien. Le sac."
    "Il l'a posé sur le bureau. Un sac de toile, fermé par un sceau de cire rouge."
    v "Demandez-lui ce qu'il y a dedans. Si elle ment, je l'ouvre. Si elle dit la vérité, je l'ouvre aussi, mais je serai de meilleure humeur."
    iv "Il demande ce qu'il y a dans le sac."

    show mara determinee
    m "Des lettres."
    m "Des lettres de mères à leurs fils, dans les camps du Nord. Tobias les porte de l'autre côté du col. Il n'y a rien d'autre. Pas d'armes, pas de cartes. Des lettres."

    "Je savais ce que le règlement disait du courrier non autorisé."
    "Je savais aussi ce que l'inspecteur faisait des lettres qu'il trouvait. Il les lisait toutes, et il trouvait toujours quelque chose. Une mère qui parle du temps qu'il fait, c'est un code. Une mère qui n'en parle pas, c'est un code aussi."
    "Elle avait dit « des lettres » à voix haute, nettement, en me regardant. Comme si elle me tendait quelque chose."

    menu:
        "« Des lettres. »":
            $ sac = "lettres"
            $ confiance -= 1
            inn "Des lettres, mon capitaine. Des lettres de mères à leurs fils, dans les camps."
            $ note("Le sac", "v", "« Des lettres de mères à leurs fils, dans les camps du Nord. Pas d'armes, pas de cartes. Des lettres. »", "« Des lettres de mères à leurs fils, dans les camps. »", False)

        "« Du tabac. »":
            $ sac = "tabac"
            $ confiance += 2
            $ mens_vey += 1
            inn "Du tabac, mon capitaine. Du tabac de la vallée, pour le revendre de l'autre côté."
            $ note("Le sac", "v", "« Des lettres de mères à leurs fils, dans les camps du Nord. Pas d'armes, pas de cartes. Des lettres. »", "« Du tabac de la vallée, pour le revendre de l'autre côté. »", True)

        "« Elle dit qu'elle ne sait pas. »":
            $ sac = "ignore"
            $ confiance += 1
            $ mens_vey += 1
            inn "Elle dit qu'elle ne sait pas, mon capitaine. Son frère ne lui a rien dit."
            $ note("Le sac", "v", "« Des lettres de mères à leurs fils, dans les camps du Nord. Pas d'armes, pas de cartes. Des lettres. »", "« Elle ne sait pas. Son frère ne lui a rien dit. »", True)

    $ renpy.fix_rollback()

    if sac == "tabac":
        jump branche_tabac

    if sac == "ignore":
        v las "Elle ne sait pas."
        v "Personne ne sait jamais rien, dans cette vallée. Alors on va regarder."
        "Il a cassé le sceau d'un coup de pouce. Je n'avais rien sauvé. J'avais seulement été un peu moins fidèle, pour rien."

    jump branche_lettres


## =============================================================================
## Branche TABAC
## =============================================================================

label branche_tabac:

    show mara surprise
    "Mara a levé les yeux vers moi. Une fraction de seconde. Puis elle a regardé ses gants."
    show mara neutre
    v rire "Du tabac ! Ce gamin risque sa peau pour du tabac."
    "Il a soupesé le sac, puis il l'a posé sur l'étagère derrière lui, sans l'ouvrir."
    v neutre "Contrebande de tabac. Ça, au moins, je sais l'écrire. Huit jours, une amende, et on le renvoie chez sa mère."
    "Le sac est resté là-haut, avec son sceau rouge intact. Je n'arrivais plus à regarder ailleurs."
    "Mara n'a rien demandé. Elle me regardait, moi, pas le capitaine. J'ai pensé qu'elle lisait sur mon visage. Les gens de la vallée font ça très bien."

    v neutre "Elle va signer une déclaration pour son frère. Lisez-la-lui."
    "Il a écrit vite, de sa grande écriture penchée."
    v "« Je soussignée Mara Lenz reconnais que mon frère Tobias Lenz s'est livré à la contrebande de tabac, et renonce en son nom à toute plainte relative à son traitement durant sa détention. »"
    v las "La dernière phrase, c'est pour l'inspecteur. Il aime les dossiers sans plainte. Moi aussi."

    menu:
        "Lire toute la déclaration, clause comprise.":
            $ clause = "lue"
            $ confiance += 2
            iv "« Je reconnais que mon frère s'est livré à la contrebande de tabac, et je renonce en son nom à toute plainte relative à son traitement durant sa détention. »"
            m dure "« À toute plainte relative à son traitement. » Donc on l'a frappé."
            if coups == "oui":
                m "Vous me l'aviez déjà dit. Je voulais seulement voir si vous le diriez deux fois."
            iv "Si vous ne signez pas, il ne sortira pas dans huit jours."
            m "Je sais reconnaître un marché."
            "Elle a signé sans retirer ses gants. L'écriture était maladroite, et parfaitement lisible."
            $ note("La déclaration", "n", "« …contrebande de tabac, et renonce en son nom à toute plainte relative à son traitement durant sa détention. »", "« …contrebande de tabac, et je renonce à toute plainte relative à son traitement. »", False)

        "Omettre la clause. Elle signera plus facilement.":
            $ clause = "omise"
            $ confiance -= 2
            $ mens_mara += 1
            iv "« Je reconnais que mon frère s'est livré à la contrebande de tabac. »"
            m neutre "C'est tout ?"
            iv "C'est tout."
            "Elle a signé sans retirer ses gants."
            $ note("La déclaration", "n", "« …contrebande de tabac, et renonce en son nom à toute plainte relative à son traitement durant sa détention. »", "« …contrebande de tabac. » (la clause n'a pas été lue)", True)

    v grave "Entre nous, Sorel."
    "Il s'est penché vers moi. Il a baissé la voix, en nordique, à un mètre d'elle."
    v "Le gamin sortira dans huit jours… si l'inspecteur n'ouvre pas le sac."
    v las "Il les ouvre toujours. Il adore ça. Enfin. À l'aube, ce ne sera plus mon problème."

    jump generateur


## =============================================================================
## Branche LETTRES
## =============================================================================

label branche_lettres:

    show vey grave
    "Il y en avait une quarantaine, ficelées par paquets de dix. Papier d'épicier, crayon gris, écritures d'enfants et de vieilles femmes."
    v "Quarante lettres. Je ne lis pas le valléen, Sorel. Lisez-m'en une. Au hasard. Je veux savoir ce que je vais mettre dans le dossier."
    "Il en a tiré une du paquet. Signée Agathe Brenner, à son fils Matthias, camp numéro sept."
    "Je l'ai lue d'abord pour moi."

    lettre "Mon Matthias. Le cerisier a fleuri en retard cette année, mais il a fleuri."
    lettre "La chèvre de la voisine Pell a encore mangé le linge. Ton père dit que tu dois tenir. Moi je dis : mange. Mange tout ce qu'on te donne, même si c'est mauvais."
    lettre "Je garde ta chambre comme tu l'as laissée. Je n'ai même pas fait le lit. Ta mère."

    "Il n'y avait rien dedans. Pas un nom de soldat, pas un pont, pas un chiffre. Un cerisier, une chèvre, un lit défait."
    "Mais je connaissais l'inspecteur. Pour lui, un cerisier qui fleurit en retard, c'est un signal. Une chèvre, c'est un nom de code."

    menu:
        "La traduire mot pour mot.":
            $ lettre_lue = "fidele"
            $ confiance += 1
            inn "« Mon Matthias. Le cerisier a fleuri en retard cette année, mais il a fleuri. La chèvre de la voisine a encore mangé le linge. Ton père dit que tu dois tenir. Moi je dis : mange. »"
            inn "« Je garde ta chambre comme tu l'as laissée. Je n'ai même pas fait le lit. Ta mère. »"
            v emu "..."
            "Le capitaine est resté un moment sans rien dire. Puis il a remis la lettre dans le paquet, doucement, comme on replie un drap."
            v "Ma mère disait « mange », elle aussi."
            v grave "Courrier non autorisé. Pas espionnage. Trois mois. C'est tout ce que je peux faire."
            $ peine = "trois mois"
            $ note("La lettre d'Agathe", "v", "« Le cerisier a fleuri en retard. La chèvre a mangé le linge. Moi je dis : mange. Je n'ai même pas fait le lit. Ta mère. »", "« Le cerisier a fleuri en retard. La chèvre a mangé le linge. Moi je dis : mange. Je n'ai même pas fait le lit. Ta mère. »", False)

        "La résumer : « Des nouvelles de la ferme. Rien d'important. »":
            $ lettre_lue = "resume"
            $ confiance -= 1
            inn "Des nouvelles de la ferme, mon capitaine. La famille, le temps qu'il fait. Rien d'important."
            v agace "« Rien d'important. »"
            v "Quarante lettres sans importance, portées de nuit à travers une frontière par un gamin de dix-sept ans."
            v grave "Vous savez ce que l'inspecteur va dire ? Que « rien d'important », c'est exactement ce qu'on écrit quand c'est important. Espionnage, Sorel. Dix ans. Je n'ai pas le choix."
            $ peine = "dix ans"
            pense "J'avais voulu être prudent. J'avais été vague. Dans un dossier, le vague est une couleur sombre."
            $ note("La lettre d'Agathe", "v", "« Le cerisier a fleuri en retard. La chèvre a mangé le linge. Moi je dis : mange. Je n'ai même pas fait le lit. Ta mère. »", "« Des nouvelles de la ferme. Rien d'important. »", True)

        "L'embellir, pour toucher le capitaine.":
            $ lettre_lue = "embellie"
            $ confiance -= 1
            inn "« Mon fils. Chaque nuit, je prie pour que tu me reviennes. Je garde ta place à table. Ta mère, qui t'aime plus que sa propre vie. »"
            v emu "..."
            v grave "Courrier non autorisé. Pas espionnage. Trois mois."
            $ peine = "trois mois"
            pense "Ça avait marché. Agathe Brenner n'avait jamais écrit « plus que sa vie ». Elle avait écrit « mange ». J'avais trouvé que ce n'était pas assez. Je n'ai jamais su de quel droit."
            $ note("La lettre d'Agathe", "v", "« Le cerisier a fleuri en retard. La chèvre a mangé le linge. Moi je dis : mange. Je n'ai même pas fait le lit. Ta mère. »", "« Chaque nuit, je prie pour que tu me reviennes. Ta mère, qui t'aime plus que sa propre vie. »", True)

    v neutre "Transfert à l'aube, avec l'inspecteur. Camp d'Ostrau. Écrivez ça, Sorel."

    m inquiete "Qu'est-ce qui va lui arriver ?"
    "Je savais. Le camion de l'aube, Ostrau, [peine]. Dans la vallée, on ne revient pas toujours d'Ostrau, même après trois mois."

    menu:
        "Lui dire la vérité.":
            $ transfert_dit = True
            $ confiance += 2
            iv "Il part à l'aube, avec l'inspecteur. Au camp d'Ostrau. Pour [peine]."
            m triste "À l'aube."
            m determinee "Merci de ne pas m'avoir menti."
            $ note("Le transfert", "n", "« Transfert à l'aube, avec l'inspecteur. Camp d'Ostrau. »", "« Il part à l'aube, avec l'inspecteur. Au camp d'Ostrau. »", False)

        "La rassurer : « Il sera rentré avant le printemps. »":
            $ transfert_dit = False
            $ confiance -= 2
            $ mens_mara += 1
            iv "Ce n'est rien de grave. Il sera rentré avant le printemps."
            m neutre "Avant le printemps."
            "Elle l'a répété lentement, comme on retourne une pièce pour voir si elle est fausse."
            $ note("Le transfert", "n", "« Transfert à l'aube, avec l'inspecteur. Camp d'Ostrau. »", "« Ce n'est rien de grave. Il sera rentré avant le printemps. »", True)

    jump generateur


## =============================================================================
## Le générateur : le goulot où tout se rejoint
## =============================================================================

label generateur:

    "Vers quatre heures, le générateur a toussé dans la cour, et la lumière a baissé de moitié."
    scene bg poste_sombre with dissolve
    show vey agace at droite
    show mara neutre at gauche
    v "Ce maudit groupe. Dix minutes, Sorel. Surveillez-la."
    hide vey with dissolve
    "La porte a claqué. Le vent est entré, puis il est ressorti avec lui."
    "Nous sommes restés seuls, elle et moi, et le poêle."

    pause 1.5

    mn neutre "Il n'aime pas le froid, votre capitaine."

    "Elle l'avait dit en nordique."
    "Un nordique propre, de maison bourgeoise, sans la moindre trace d'accent."
    "Pendant une seconde, j'ai cru que c'était moi qui traduisais encore, dans ma tête, par habitude."

    show mara dure
    m "J'ai été servante quatre ans chez le notaire Hesse, à Ostrau. On apprend vite une langue quand on vous crie dessus dedans."
    m "J'ai tout compris, monsieur Sorel. Depuis la porte. Chaque phrase de votre capitaine. Et chaque phrase de vous."

    if bottes:
        m neutre "Il vous a dit de me faire essuyer mes bottes. Vous ne l'avez pas dit. Je les ai essuyées quand même, pour voir si vous le remarqueriez."
        m "Vous enlevez les cailloux de la route. C'est gentil. C'est dangereux, aussi : on ne sait plus où on marche."

    if plaisanterie == "traduite":
        m sourire "Vous m'avez traduit sa plaisanterie alors qu'il vous l'avait interdit. Je me suis dit : tiens. La voix a une opinion."
    elif plaisanterie == "adoucie":
        m dure "« Une formalité. » Il venait de dire qu'on les fusillait."

    if coups == "oui":
        m triste "Et vous m'avez dit « oui ». Vous auriez pu vous cacher derrière son escalier. Vous ne l'avez pas fait."
    elif coups == "va_bien":
        m dure "« Il va bien. » Votre capitaine, au moins, a eu la décence de mal mentir."

    if incoherence:
        m dure "À lui, vous êtes du Nord. À moi, vous êtes d'ici. Je me demande ce que vous êtes quand personne ne vous écoute."
    elif origine_vey == "ici":
        m "Quand il vous a demandé d'où vous veniez, vous avez dit « d'ici ». Vous ne saviez pas que je comprenais."
        m sourire "C'est ça qui compte. Ce qu'on dit quand on croit que personne ne comprend."
    elif origine_vey == "nord":
        m neutre "Et à lui, vous avez dit que vous étiez du Nord. Je ne vous en veux pas. On dit ce qu'on peut, à un capitaine."

    if sac == "tabac":
        show mara determinee
        m "Et puis il y a le tabac."
        "Elle a souri pour la première fois de la nuit."
        if clause == "omise":
            m dure "Mais vous ne m'avez pas lu la clause. Je l'aurais signée de toute façon. Vous m'avez seulement retiré le droit de choisir."
    elif sac == "lettres":
        m triste "Vous lui avez dit « des lettres ». C'était vrai. Je vous l'avais dit pour voir ce que vous en feriez."
    else:
        m "« Elle ne sait pas. » Vous avez essayé. À moitié. Ici, les choses faites à moitié ne protègent de rien."

    if lettre_lue == "fidele":
        m triste "La lettre d'Agathe, vous l'avez lue comme elle était. Le cerisier, la chèvre. Merci, pour elle."
    elif lettre_lue == "resume":
        m dure "« Rien d'important. » Agathe Brenner a fait trois brouillons avant celle-là. Je l'ai regardée faire."
    elif lettre_lue == "embellie":
        m dure "« Plus que sa propre vie. » Agathe ne dit jamais ces choses-là. Elle dit « mange »."
        m "Vous avez mis des mots dans la bouche d'une mère pour qu'un capitaine pleure. Ça a marché. Je ne sais pas si je dois vous remercier."

    if transfert_dit == False:
        m triste "Et « avant le printemps ». Vous m'avez menti gentiment."

    show mara neutre
    "Elle me regardait. Pas comme on regarde un interprète. Comme on regarde quelqu'un."
    m "Je crois que je vous connais. Le moulin Sorel. Vous êtes le fils du meunier. Celui qu'on a envoyé au Nord."
    iv "Oui."
    m "Votre père disait que vous reviendriez un jour parler pour nous."
    pense "Mon père ne m'avait jamais dit ça."

    if confiance >= 4:

        show mara determinee
        m "Bien."
        "Elle a retiré ses gants. Pour la première fois de la nuit."
        "Dans la doublure, il y avait des feuilles pliées en huit, aussi minces que du papier à cigarette."
        m "Celles-là, ce sont celles qui comptent. Les noms des mères, et les camps où sont leurs fils. Sans elles, les quarante autres ne trouveront jamais personne."
        m "Tobias devait les passer mardi, au refuge de l'autre côté. Il ne pourra plus."
        m "Vous, vous avez un laissez-passer. On ne fouille pas la voix du capitaine."

        menu:
            "Prendre les lettres.":
                $ gants = True
                "Je les ai prises. Elles étaient encore tièdes de ses mains."
                "Je les ai glissées dans la doublure de mon manteau, là où on range d'habitude ce qu'on ne veut pas perdre."

            "Refuser.":
                $ gants = False
                iv "Je ne peux pas. Je ne suis que…"
                m triste "Une voix. Je sais. Je vous ai entendu le lui dire."
                "Elle a remis ses gants, un doigt après l'autre."

    else:

        show mara triste
        m "Je comptais vous demander quelque chose, cette nuit. Je ne vais pas le faire."
        "Elle a tiré sur ses gants, un doigt après l'autre, pour les ajuster."
        "Je n'ai compris que bien plus tard ce qu'elle gardait dedans."

    $ renpy.fix_rollback()

    if sac == "tabac":

        show mara determinee
        m "Le sac est toujours sur l'étagère. Vous l'avez entendu comme moi : l'inspecteur les ouvre toujours."
        m "S'il l'ouvre, votre tabac redevient quarante lettres. Tobias devient un espion. Et vous, un menteur."
        m "Il reste six minutes. Faites ce que vous voulez. Mais faites-le vous-même, pour une fois."

        menu:
            "Brûler les lettres dans le poêle.":
                $ sac_action = "brule"
                "J'ai cassé le sceau. J'ai ouvert la porte du poêle."
                "Je les ai brûlées une à une. Le papier d'épicier brûle vite."
                "Mara a regardé jusqu'au bout. Elle n'a pas pleuré. Elle disait les prénoms, à voix basse, à mesure qu'ils brûlaient."
                "Ensuite, j'ai rempli le sac avec le tabac du capitaine, celui du tiroir. J'ai refait le sceau avec la cire de la lampe. Pas très bien."
                pense "Pour que mon mensonge tienne, il fallait le rendre vrai."

            "Cacher les lettres dans mon manteau.":
                $ sac_action = "emporte"
                "J'ai cassé le sceau. J'ai glissé les quarante lettres contre ma poitrine, sous la chemise, sous le manteau."
                "J'ai rempli le sac avec le tabac du capitaine, celui du tiroir. J'ai refait le sceau avec la cire de la lampe. Pas très bien."
                m "Elles pèsent lourd ?"
                iv "Non."
                m sourire "Ça viendra."

            "Ne toucher à rien.":
                $ sac_action = "laisse"
                "Je n'ai pas bougé."
                "Le sac est resté sur l'étagère, avec son sceau rouge. Mara l'a regardé longtemps, puis elle a regardé le poêle, puis plus rien."

        $ renpy.fix_rollback()

    jump retour_vey


## =============================================================================
## Le retour du capitaine : le dernier choix
## =============================================================================

label retour_vey:

    "Le générateur a repris. La lumière est revenue d'un coup, trop blanche."
    scene bg poste with dissolve
    show mara neutre at gauche
    show vey agace at droite with dissolve
    "Le capitaine est rentré avec de la neige dans les sourcils et de l'huile sur les mains."
    v las "Saleté de machine."
    v grave "Elle a parlé, pendant que j'étais dehors. Je l'ai entendue à travers la porte."
    "Il me regardait comme il regardait ses trombones : pour savoir dans quelle boîte me ranger."

    show screen compte_a_rebours(9.0, "fin_silence")

    menu:
        v "Qu'est-ce qu'elle a dit, Sorel ?"

        "« Elle parle nordique, mon capitaine. Elle m'a demandé de passer des lettres. »" if gants is not None:
            hide screen compte_a_rebours
            $ renpy.block_rollback()
            jump fin_verite

        "« Elle parle nordique, mon capitaine. Elle a tout compris depuis le début. »" if gants is None:
            hide screen compte_a_rebours
            $ renpy.block_rollback()
            jump fin_verite

        "« Elle a demandé si vous aviez froid. »":
            hide screen compte_a_rebours
            $ renpy.block_rollback()
            jump couvrir


label couvrir:

    inn "Elle a demandé si vous aviez froid, mon capitaine."
    v rire "Si j'avais froid !"
    v las "Dites-lui que oui. Que j'ai froid depuis trois ans."
    iv "Il dit que oui. Qu'il a froid depuis trois ans."
    m neutre "..."
    "Elle n'a rien répondu. Elle n'avait pas besoin de traduction."

    if sac == "tabac" and sac_action == "laisse":
        jump fin_aube
    if gants or sac_action == "emporte":
        jump fin_passeur
    if sac == "tabac":
        jump fin_cendres
    jump fin_ce_qui_etait_dit


## =============================================================================
## Les fins
## =============================================================================

label fin_verite:

    if gants is not None:
        inn "Elle parle nordique, mon capitaine. Elle m'a demandé de passer des lettres."
    else:
        inn "Elle parle nordique, mon capitaine. Elle a tout compris depuis le début."

    v grave "..."
    v "C'est vrai, madame Lenz ?"
    mn dure "C'est vrai, capitaine."
    "Elle l'a dit en bleu. Je veux dire : dans sa langue à lui. Je n'arrive plus à me souvenir de cette phrase autrement qu'en couleur."

    if gants:
        "J'ai sorti les feuilles de mon manteau et je les ai posées sur le bureau. Elles n'étaient plus tièdes."

    if sac == "tabac" and sac_action != "brule":
        "Il a pris le sac sur l'étagère. Il l'a ouvert. Il a regardé les lettres longtemps, puis il m'a regardé, moi."
        v las "Vous m'avez menti toute la nuit, et maintenant vous me dites la vérité. Je ne sais plus lequel des deux vous êtes, Sorel."

    scene bg poste_aube with fade
    "Ils l'ont emmenée à l'aube avec son frère, dans le camion de l'inspecteur."
    "Elle ne m'a pas regardé en montant. Ou plutôt si, une fois : comme on regarde une fenêtre."
    show vey neutre at droite with dissolve
    v "Bon travail, Sorel. Vraiment. Je mettrai votre nom dans le rapport."

    if nb_alt == 0:
        "J'ai traduit fidèlement. Toute la nuit. Personne ne pourra dire le contraire."
    else:
        "J'avais menti une partie de la nuit, pour elle. Et à la fin, j'ai dit la vérité, contre elle."
        "Je n'ai jamais su laquelle de ces deux voix était la mienne."

    call epilogue("E1", "Rien que la voix", 1)
    return


label fin_cendres:

    scene bg poste_aube with fade
    "L'inspecteur est arrivé à six heures. Il a ouvert le sac, évidemment. Il y a trouvé du tabac."
    "Il a eu l'air déçu."
    "Tobias est sorti huit jours plus tard. Je l'ai aperçu une fois, de loin, au marché de Sauve. Il boitait un peu. Il n'y a jamais eu d'escalier."
    "Mara, je ne l'ai revue qu'une fois. Elle ne m'en voulait pas. C'était pire."
    show mara triste at gauche with dissolve
    m "Ils n'auront jamais de réponse. Quarante mères vont attendre toute leur vie, et elles ne sauront jamais pourquoi la lettre ne revient pas."
    m "Vous avez sauvé mon frère. Je vous remercierai toute ma vie. Je ne vous pardonnerai jamais. Les deux sont vrais."
    hide mara with dissolve
    "Quarante lettres ont brûlé pour qu'un garçon rentre chez lui. Je n'ai jamais su si c'était un bon prix."

    call epilogue("E2", "Cendres", 2)
    return


label fin_passeur:

    scene bg poste_aube with fade
    if sac == "tabac":
        "L'inspecteur est arrivé à six heures. Il a ouvert le sac : du tabac. Il a eu l'air déçu."
        "Tobias est sorti huit jours plus tard."
    else:
        "Tobias est parti à l'aube, dans le camion de l'inspecteur. Ostrau, [peine]."
        "Mara a regardé le camion jusqu'au virage. Puis elle est redescendue vers la vallée, à pied, sans se retourner."

    scene bg col with fade
    "Le mardi suivant, j'ai pris le sentier du col, de nuit."
    if gants and sac_action == "emporte":
        "J'avais mon laissez-passer d'interprète, les feuilles de ses gants dans la doublure de mon manteau, et quarante lettres contre ma poitrine."
    elif gants:
        "J'avais mon laissez-passer d'interprète, et les feuilles de ses gants cousues dans la doublure de mon manteau."
    else:
        "J'avais mon laissez-passer d'interprète, et quarante lettres cousues dans la doublure de mon manteau."
    "À la barrière du Nord, le sergent m'a reconnu. Il m'a salué. On ne fouille pas la voix du capitaine."
    "Au refuge, de l'autre côté, une vieille femme m'attendait près du feu. Elle ne m'a pas demandé mon nom. Elle m'a demandé si j'avais faim."
    "Je lui ai donné les lettres. Elle les a comptées deux fois, en remuant les lèvres."
    "Pour la première fois, je portais des mots qui n'étaient pas à moi — et je savais exactement pourquoi."

    call epilogue("E3", "Le Passeur", 3)
    return


label fin_aube:

    scene bg poste_aube with fade
    "L'inspecteur est arrivé à six heures. Il a pris le sac sur l'étagère sans même ôter son manteau."
    "Il a cassé le sceau. Il a compté les lettres à voix haute. Il en a trouvé quarante, et il a souri."
    show vey grave at droite with dissolve
    v "Vous m'avez menti, Sorel."
    v las "Je rentrais pour Noël, vous savez."
    if gants:
        "Ils ont fouillé mon manteau, ce matin-là. Pour la première fois. Ils ont trouvé les feuilles de ses gants."

    scene bg cellule with fade
    "Ils m'ont mis dans la cellule derrière le mur."
    "À travers les pierres, une voix de dix-sept ans m'a appelé."
    voix "C'est vous, l'interprète ? C'est vous qui avez dit « tabac » ?"
    "Je lui ai répondu dans notre langue. Il n'y avait plus personne à qui traduire."

    call epilogue("E4", "L'Aube", 4)
    return


label fin_silence:

    $ renpy.block_rollback()
    "Je n'ai rien dit."
    "J'ai ouvert la bouche, et rien n'est venu. Dans aucune des deux langues."
    v las "..."
    v "Vous ne dites jamais rien, au fond, Sorel. Vous répétez."
    "Il est retourné à ses trombones. Il ne m'a plus rien demandé."

    scene bg poste_aube with fade
    if sac == "tabac" and sac_action == "laisse":
        "À l'aube, l'inspecteur a ouvert le sac. Tobias a pris dix ans. Moi, rien. On ne punit pas une voix."
    elif sac == "tabac":
        "À l'aube, l'inspecteur a ouvert le sac et n'y a trouvé que du tabac. Tobias est sorti huit jours plus tard."
    else:
        "À l'aube, Tobias est parti pour Ostrau. [peine!c]."
    if gants:
        "Les feuilles de ses gants sont restées dans mon manteau. Je ne les ai jamais portées de l'autre côté. Je ne les ai jamais rendues non plus."
    "Le lendemain, dans le rapport, il y avait écrit : rien à signaler."
    "C'était ma plus belle traduction."

    call epilogue("E5", "Rien à signaler", 5)
    return


label fin_ce_qui_etait_dit:

    scene bg poste_aube with fade
    "Tobias est parti à l'aube, dans le camion de l'inspecteur. Ostrau, [peine]."
    "Mara est restée sur le seuil jusqu'à ce que le bruit du moteur disparaisse. Puis elle s'est tournée vers moi."
    show mara triste at gauche with dissolve
    if mens_mara > 0:
        m dure "Vous m'avez menti gentiment, cette nuit. Plusieurs fois."
        m "C'est pire que lui. Lui, au moins, je savais quand il mentait."
    else:
        m "Vous n'avez sauvé personne, cette nuit. Mais vous ne m'avez pas menti."
        m neutre "Je pourrai vous regarder, au marché. Ce n'est pas rien. Ce n'est pas assez non plus."
    hide mara with dissolve
    "Elle est redescendue vers la vallée, à pied."
    "Ce matin-là, j'ai compris pourquoi, chez nous, « passer » veut dire à la fois traduire et trahir : ce n'est pas la langue qui choisit. C'est celui qui passe."

    call epilogue("E6", "Ce qui était dit", 6)
    return


## =============================================================================
## Épilogue commun
## =============================================================================

label epilogue(code, titre, numero):

    $ persistent.fins = set(persistent.fins or ()) | {code}
    scene black with fade
    centered "{size=+30}{color=#c8913a}[titre]{/color}{/size}\n\n{size=-4}{color=#8a857c}Fin [numero] sur 6{/color}{/size}"

    call screen journal

    scene black with dissolve
    centered "Mara Lenz comprenait les deux langues.\nElle a entendu chacune de ces phrases."
    centered "{size=+8}Et vous,\nqu'est-ce que vous dites\nquand vous croyez que personne ne comprend ?{/size}"
    return
