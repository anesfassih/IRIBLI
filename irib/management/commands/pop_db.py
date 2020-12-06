from irib.models import *
import pyarabic.araby as araby
from xml.dom import minidom
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Populate the data from ressource files in /Res'

    def handle(self, *args, **options):
        # Chargement des mots spécifiques :

        mots_outils_doc = minidom.parse('Res/toolwords.xml')
        noms_propres_doc = minidom.parse('Res/propernouns.xml')
        mots_except_doc = minidom.parse('Res/exceptionalwords.xml')

        mots_outils_items = mots_outils_doc.getElementsByTagName('toolword')
        noms_propres_items = noms_propres_doc.getElementsByTagName('propernoun')
        mots_except_items = mots_except_doc.getElementsByTagName('exceptionalword')

        for item in mots_outils_items:
            ToolWord.objects.create(
              priority=item.attributes['priority'].value,
              prefixe_class=item.attributes['prefixeclass'].value,
              suffixe_class=item.attributes['suffixeclass'].value,
              ttype=item.attributes['type'].value,
              voweled_form=item.attributes['voweledform'].value,
              unvoweled_form=araby.strip_diacritics(item.attributes['voweledform'].value)
              )
        self.stdout.write(self.style.SUCCESS('ToolWords Populated !'))

        for item in noms_propres_items:
            ProperNoun.objects.create(
              voweled_form=item.attributes['voweledform'].value,
              unvoweled_form=item.attributes['unvoweledform'].value,
              ptype=item.attributes['type'].value
              )
        self.stdout.write(self.style.SUCCESS('ProperNouns Populated !'))

        for item in mots_except_items:
            ExceptionalWord.objects.create(
              stem=item.attributes['stem'].value,
              prefixe=item.attributes['prefix'].value,
              suffixe=item.attributes['suffix'].value,
              etype=item.attributes['type'].value,
              voweled_form=item.attributes['voweledform'].value,
              unvoweled_form=item.attributes['unvoweledform'].value
              )
        self.stdout.write(self.style.SUCCESS('ExceptionalWords Populated !'))
        # --------------------------------------------------------------------------------------------

        pref_doc = minidom.parse('Res/prefixes.xml')
        suff_doc = minidom.parse('Res/suffixes.xml')

        pref_items = pref_doc.getElementsByTagName('prefixe')
        suff_items = suff_doc.getElementsByTagName('suffixe')

        # Chargement des clitiques et infixes :


        for item in pref_items:
            Prefixe.objects.create(
              classe=item.attributes['classe'].value,
              description=item.attributes['desc'].value,
              voweled_form=item.attributes['voweledform'].value,
              unvoweled_form=item.attributes['unvoweledform'].value
              )
        self.stdout.write(self.style.SUCCESS('Prefixes Populated !'))

        for item in suff_items:
            Suffixe.objects.create(
              classe=item.attributes['classe'].value,
              description=item.attributes['desc'].value,
              voweled_form=item.attributes['voweledform'].value,
              unvoweled_form=item.attributes['unvoweledform'].value
              )
        self.stdout.write(self.style.SUCCESS('Suffixes Populated !'))
        # Chargement des racines :

        racines = {}
        lines = open('Res/racines.txt', 'r', encoding="UTF-8").readlines()
        for l in lines:
            hrf, msdr = l.split(':')
            racines[hrf] = msdr.split()

        for r in racines.values():
            for rr in r:
                Racine.objects.create(unvoweled_form=rr)
        self.stdout.write(self.style.SUCCESS('Roots Populated !'))
        # --------------------------------------------------------------------------------------------

        # Chargement des shémes :

        for line in open('Res/translated_patterns.txt', 'r', encoding='UTF-8').readlines():
            pattern, type, nType, vType, isBrokenPlural, comment = line.split('\t')
            pattern = pattern[8:]
            type = type[5:]
            nType = nType[6:]
            vType = vType[6:]
            isBrokenPlural = isBrokenPlural[15:]
            if isBrokenPlural == 'yes':
                isBrokenPlural = True
            else:
                isBrokenPlural = False
            comment = comment[8:].replace('\n', '')
            Pattern.objects.create(
              voweled_form=pattern,
              unvoweled_form=araby.strip_diacritics(pattern),
              ptype=type,
              ntype=nType,
              vtype=vType,
              broken_plural=isBrokenPlural,
              comment=comment
              )
        self.stdout.write(self.style.SUCCESS('Patterns Populated !'))

        # Instanciation d'un ensemble de régles :

        # RP = RulePack.objects.create(name="AutoINIT")
        # try:
        #     State.objects.get(rule_pack=RP, label="START")
        # except State.DoesNotExists:
        #     State.objects.create(rule_pack=RP, label="START", is_start=True, is_end=False)

        self.stdout.write(self.style.SUCCESS('Successfully populated data !'))



