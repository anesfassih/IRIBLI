import pyarabic.araby as araby
from .utils import *
from .models import *
import copy
import itertools


# def is_muaaraf(pos):
#     """ Input : [prefixe, type, stype, suffixe] """
#     if pos['stype'] in ['adjectival', 'nominal'] and 'التعريف' in pos['prefixe'] or \
#             pos['stype'] in ['except', 'prop'] or \
#             pos['type'] == 'اسم إشارة':
#         return True
#     return False


def halat_al_irab(word):
    # المثنى وما يلحق به : يرفع بالألف ، وينصب ويجر بالياء
    if araby.strip_diacritics(word)[-2:] == 'ان':
        return 'raf3'
    elif araby.strip_diacritics(word)[-2:] == 'ين':
        return 'nasb', 'jarr'
    if word[-1] in araby.HARAKAT:
        if word[-1] in [araby.DAMMA, araby.DAMMATAN]:
            return 'raf3'
        elif word[-1] in [araby.FATHA, araby.FATHATAN]:
            return 'nasb'
        elif word[-1] in [araby.KASRA, araby.KASRATAN]:
            return 'jarr'
        elif word[-1] == araby.SUKUN:
            return 'jazm'
    else:
        return None


# ---------------------------------- Fonctions de traitement ---------------------------------
def decoupage(word):
    """Découpe le mot donné en entrée (word) en (préfixes, racine et suffixes). La sortie de la fonction est une liste
    de dictionnaires regroupant toutes les combinaisons syntaxiquement correctes d'aprés la compatibilitée entre les
     préfixes et sufixes détéctés et la taille de la racine."""
    word_unvocalized = araby.strip_diacritics(word)
    prefixes, suffixes = [""], [""]
    combinaisons_possibles = []
    for p in Prefixe.objects.all():
        if word_unvocalized.startswith(p.unvoweled_form):
            # print("p:"+p.unvoweled_form)
            if araby.is_vocalized(word):
                if araby.vocalizedlike(word[:len(p.voweled_form)], p.voweled_form):
                    prefixes.append(p)
            else:
                prefixes.append(p)
    for s in Suffixe.objects.all():
        if word_unvocalized.endswith(s.unvoweled_form):
            if araby.is_vocalized(word):
                if araby.vocalizedlike(word[-len(s.voweled_form):], s.voweled_form):
                    suffixes.append(s)
            else:
                suffixes.append(s)

    for pr in prefixes:
        for sf in suffixes:
            # Validation criteria
            if pr != "" and sf != "":
                if (len(word_unvocalized) - len(pr.unvoweled_form) - len(sf.unvoweled_form)) <= 2 or \
                    (len(word_unvocalized) - len(pr.unvoweled_form) - len(sf.unvoweled_form)) > 9:
                    continue
                if ((pr.classe[0] == 'N' and sf.classe[0] == 'V') or
                        (pr.classe[0] == 'V' and sf.classe[0] == 'N') or
                        (pr.classe in ['N1', 'N2', 'N3', 'N5'])):
                    continue
            # Si on est là -> le préfixe est compatible avec le suffixe, et la taille de la base est accéptable
            base = word
            # Supprimer le prefixe de la base // En gardant le Tachkil
            if pr:
                for char in pr.unvoweled_form:
                    while char != base[0]:
                        base = base[1:]
                    base = base[1:]
                while araby.is_tashkeel(base[0]):
                    base = base[1:]

            # Supprimer le suffixe de la base // En gardant le Tachkil
            if sf:
                r_sf = [c for c in sf.unvoweled_form]
                r_sf.reverse()
                for char in r_sf:
                    base = base[:base.rindex(char)]

            combinaisons_possibles.append({'Base': base, 'Préfixe': pr, 'Suffixe': sf})

    return combinaisons_possibles


def attach_sheme(combos):
    """Filtre les compositions extraites de la fonction découpage() pour donner en sortie les compositions qui
    accéptent l'un des shémes de la BDD. La sortie est une liste de dictionnaires ou chaque dictionnaire est une
    composition avec un champs supplémentaire : le shéme adéquat. """
    good_sheme_comb = []
    for comb in combos:
        # for pat in Pattern.objects.filter(unvoweled_form__length=len(comb['Base'])):
        for pat in Pattern.objects.all():
            if araby.waznlike(comb['Base'], pat.voweled_form):
                if comb['Préfixe'] != '' and (
                        (comb['Préfixe'].classe[0] == 'N' and pat.ntype == 'unspec') or (
                        comb['Préfixe'].classe[0] == 'V' and pat.vtype == 'unspec')):
                    continue
                if comb['Suffixe'] != '' and (
                        (comb['Suffixe'].classe[0] == 'N' and pat.ntype == 'unspec') or (
                        comb['Suffixe'].classe[0] == 'V' and pat.vtype == 'unspec')):
                    continue
                else:
                    if pat.vtype != 'unspec':
                        stype = pat.vtype
                    else:
                        stype = pat.ntype
                    good_sheme_comb.append({
                        'Base': comb['Base'],
                        'Préfixe': comb['Préfixe'],
                        'Suffixe': comb['Suffixe'],
                        'pattern': pat,
                        'type': pat.ptype,
                        'stype': stype
                    })
    return good_sheme_comb


def attach_racine(combos):
    """Filtre les compositions extraites de la fonction attach_sheme() pour donner en sortie les compositions dont la
    racine nettoyée des caractéres flexionnels existe dans notre BDD des racines. En sortie : les composition avec
    deux champs supplementaires : la racine nettoyée et le type du mot(à partir du shéme -- reste à développer !). """
    good_comb = []
    for comb in combos:
        word_racine = araby.strip_diacritics(comb['Base'])
        striped_sheme = comb['pattern'].unvoweled_form
        for i in range(len(striped_sheme)):
            if striped_sheme[i] not in [araby.FEH, araby.AIN, araby.LAM]:
                word_racine = word_racine[:i] + word_racine[i + 1:]

        if Racine.objects.filter(unvoweled_form=word_racine).exists():
            if {
                'Base': comb['Base'],
                'Préfixe': comb['Préfixe'],
                'Suffixe': comb['Suffixe'],
                'pattern': comb['pattern'],
                'type': comb['type'],
                'stype': comb['stype'],
                'root': word_racine
            } not in good_comb:
                good_comb.append({
                    'Base': comb['Base'],
                    'Préfixe': comb['Préfixe'],
                    'Suffixe': comb['Suffixe'],
                    'pattern': comb['pattern'],
                    'type': comb['type'],
                    'stype': comb['stype'],
                    'root': word_racine
                })
    return good_comb


def mot_outil(word):
    """Détecte si un mot donné en entrée est un mot outil ou non par rapport à la BDD."""
    mo_combs = []
    combs = decoupage(word)
    for c in combs:
        for mo in ToolWord.objects.filter(unvoweled_form=araby.strip_diacritics(c['Base'])):
            if araby.vocalizedlike(c['Base'], mo.voweled_form):
                dico = {'tw_object': mo}
                dico['Préfixe'] = c['Préfixe']
                dico['Suffixe'] = c['Suffixe']
                mo_combs.append(dico)
    return mo_combs


def nom_propre(word):
    """Détecte si un mot donné en entrée est un mot spécifique ou non par rapport à la BDD."""
    np_combs = []
    combs = decoupage(word)
    for c in combs:
        for np in ProperNoun.objects.filter(unvoweled_form=araby.strip_diacritics(c['Base'])):
            if araby.vocalizedlike(c['Base'], np.voweled_form):
                dico = {'pn_object': np}
                dico['Base'] = c['Base']
                dico['Préfixe'] = c['Préfixe']
                dico['Suffixe'] = c['Suffixe']
                np_combs.append(dico)
    return np_combs


def mot_except(word):
    """Détecte si un mot donné en entrée est un mot éxceptionnel ou non par rapport à la BDD."""
    combs = []
    for me in ExceptionalWord.objects.filter(unvoweled_form=araby.strip_diacritics(word)):
        if araby.vocalizedlike(word, me):
            combs.append(me)
    return combs


# Incomplet !!
def detailed_pos_word(word):
    combs = []
    if mot_outil(word):
        combs.append(mot_outil(word))
    elif mot_except(word):
        combs.append(mot_except(word))
    elif nom_propre(word):
        combs.append(nom_propre(word))
    else:
        combs.append(attach_racine(attach_sheme(decoupage(word))))
    return combs


def pos_word(word):
    combs = []
    if mot_outil(word):
        for comb in mot_outil(word):
            if comb['Préfixe'] != '':
                print(comb['Préfixe'])
                prefixe = comb['Préfixe'].description
            else:
                prefixe = ''
            if comb['Suffixe'] != '':
                suffixe = comb['Suffixe'].description
            else:
                suffixe = ''
            if comb['tw_object'].ttype == 'اسم إشارة':
                muaaraf = True
            else:
                muaaraf = False
            combs.append(
                {'prefixe': prefixe, 'word_type': 'tool', 'word_subtype': comb['tw_object'].ttype, 'suffixe': suffixe, 'is_muaaraf': muaaraf})
                # {'word_type': 'tool', 'word_subtype': comb['tw_object'].ttype, 'is_muaaraf': muaaraf})
    if mot_except(word):
        for comb in mot_except(word):
            combs.append({'prefixe': comb.prefixe, 'word_type': 'except', 'word_subtype': comb.etype, 'suffixe': comb.suffixe,
                          'is_muaaraf': True, 'halat_al_irab': halat_al_irab(comb.stem)})
            # combs.append({'word_type': 'except', 'word_subtype': comb.etype, 
            #               'is_muaaraf': True, 'halat_al_irab': halat_al_irab(comb.stem)})
    if nom_propre(word):
        for comb in nom_propre(word):
            if comb['Préfixe'] != '':
                prefixe = comb['Préfixe'].description
            else:
                prefixe = ''
            if comb['Suffixe'] != '':
                suffixe = comb['Suffixe'].description
            else:
                suffixe = ''
            combs.append({'prefixe': prefixe, 'word_type': 'prop', 'word_subtype': comb['pn_object'].ptype, 'suffixe': suffixe,
                          'is_muaaraf': True, 'halat_al_irab': halat_al_irab(comb['Base'])})
            # combs.append({'word_type': 'prop', 'word_subtype': comb['pn_object'].ptype, 
            #               'is_muaaraf': True, 'halat_al_irab': halat_al_irab(comb['Base'])})


    for comb in attach_racine(attach_sheme(decoupage(word))):
        # print(decoupage(word))
        muaaraf = False
        if comb['Préfixe'] != '':
            prefixe = comb['Préfixe'].description
            if 'التعريف' in prefixe:
                muaaraf = True
        else:
            prefixe = ''
        if comb['Suffixe'] != '':
            suffixe = comb['Suffixe'].description
        else:
            suffixe = ''
        tmp = {'prefixe': prefixe, 'word_type': comb['stype'], 'word_subtype': comb['type'], 'suffixe': suffixe, 'is_muaaraf': muaaraf}
        # tmp = {'word_type': comb['stype'], 'word_subtype': comb['type'], 'is_muaaraf': muaaraf}
        if halat_al_irab(comb['Base']):
            tmp['halat_al_irab'] = halat_al_irab(comb['Base'])
        if tmp not in combs:
            combs.append(tmp)
    return combs


def to_combs(pos_list):
    return list(itertools.product(*pos_list))


# def process_sent(sentence):
#     tokens = sentence.split()
#     routes = []
#     for tok in tokens:
