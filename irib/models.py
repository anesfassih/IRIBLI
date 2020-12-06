from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length, 'length')

# To populate data from ressources files, type in the command line : python manage.py pop_db

WORD_SUBTYPES = [
    ("nominal", "إسم"),
    ("verbs", "فعل"),
    ("tool", "أداة"),
    ("except", "إسم خاص"),
    ("prop", "إسم علم"),
    ("Comparative", "مقارنة"),
    ("Masdar", "مصدر"), 
    ("Miscellaneous", "متنوع"), 
    ("active_participle", "نعت"), 
    ("artificial_masdar", "مصدر صناعي"), 
    ("brokenPlural", "جمع التكسير"), 
    ("instrument", "إسم أداة"), 
    ("marrah", "إسم مرة"), 
    ("mubalagah", "مبالغة"), 
    ("mushabbaha", "مشبهة"), 
    ("nisbah", "نسبة"), 
    ("passive_participle", "النعت السلبي"), 
    ("place", "إسم مكان"), 
    ("regular_feminine_dual", "مثنى مؤنث"),
    ("singular_forms-broken_plural_forms", "إسم مفرد"), 
    ("singular_forms-fem_plural_forms", "إسم مؤنث"), 
    ("singular_forms-no_plural_forms", "..."), 
    ("singular_forms-reg_plural_forms", "...")
]
WORD_TYPES = [
    ("adjectival", "صفة"),
    ("nominal", "إسم"),
    ("nominal/adjectival", "إسم - صفة"),
    ("participial", "مكون من إسم الفاعل أو المفعول"),
    ("1", "فعل من الشكل 1"),
    ("2", "فعل من الشكل 2"),
    ("3", "فعل من الشكل 3"),
    ("4", "فعل من الشكل 4"),
    ("5", "فعل من الشكل 5"),
    ("6", "فعل من الشكل 6"),
    ("7", "فعل من الشكل 7"),
    ("8", "فعل من الشكل 8"),
    ("9", "فعل من الشكل 9"),
    ("present", "فعل مضارع"),
    ("نسبة إلى اسم علم", "نسبة إلى اسم علم"),
    ("اسم علم", "اسم علم"), 
    ("اسم الجلالة", "اسم الجلالة"), 
]
HALAT_AL_IRAB = [
    ("raf3", "رفع"),
    ("nasb", "نصب"),
    ("jarr", "جر"),
    ("jazm", "جزم")
]

class Suffixe(models.Model):
    classe = models.CharField(verbose_name="Classe", max_length=2)
    description = models.CharField(verbose_name="Description", max_length=50)
    voweled_form = models.CharField(verbose_name="Forme voyéllé", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllé", max_length=50)
    

    class Meta:
        verbose_name = "Suffixe"
        verbose_name_plural = "Suffixes"

    def __str__(self):
        return self.voweled_form



class Prefixe(models.Model):
    classe = models.CharField(verbose_name="Classe", max_length=2)
    description = models.CharField(verbose_name="Description", max_length=50)
    voweled_form = models.CharField(verbose_name="Forme voyéllé", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllé", max_length=50)
    

    class Meta:
        verbose_name = "Préfixe"
        verbose_name_plural = "Préfixe"

    def __str__(self):
        return self.voweled_form



class ProperNoun(models.Model):
    ptype = models.CharField(verbose_name="Type", max_length=50)
    voweled_form = models.CharField(verbose_name="Forme voyéllé", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllé", max_length=50)


    class Meta:
        verbose_name = "Nom propre"
        verbose_name_plural = "Noms propres"

    def __str__(self):
        return self.voweled_form


class ToolWord(models.Model):

    priority = models.IntegerField(verbose_name="Priorité")
    prefixe_class = models.CharField(verbose_name="Classe du préfixe", max_length=50)
    suffixe_class = models.CharField(verbose_name="Classe du suffixe", max_length=50)
    ttype = models.CharField(verbose_name="Type du mot outil", max_length=50)
    voweled_form = models.CharField(verbose_name="Forme voyéllée", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllée", max_length=50)

    class Meta:
        verbose_name = "ToolWord"
        verbose_name_plural = "ToolWords"

    def __str__(self):
        return self.voweled_form


class ExceptionalWord(models.Model):

    prefixe = models.CharField(verbose_name="Préfixe", max_length=50)
    suffixe = models.CharField(verbose_name="Suffixe", max_length=50)
    stem = models.CharField(verbose_name="Racine", max_length=50)
    etype = models.CharField(verbose_name="Type", max_length=50)
    voweled_form = models.CharField(verbose_name="Forme voyéllée", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllée", max_length=50)

    class Meta:
        verbose_name = "ExceptionnalWord"
        verbose_name_plural = "ExceptionnalWords"

    def __str__(self):
        return self.voweled_form


class Racine(models.Model):

    unvoweled_form = models.CharField(verbose_name="Forme non voyéllée", max_length=50)

    class Meta:
        verbose_name = "Racine"
        verbose_name_plural = "Racines"

    def __str__(self):
        return self.unvoweled_form


class Pattern(models.Model):

    voweled_form = models.CharField(verbose_name="Forme voyéllée", max_length=50)
    unvoweled_form = models.CharField(verbose_name="Forme non voyéllée", max_length=50)
    ptype = models.CharField(verbose_name="Type", max_length=50)
    ntype = models.CharField(verbose_name="Sous type nominal", null=True, max_length=50)
    vtype = models.CharField(verbose_name="Sous type verbal", null=True, max_length=50)
    broken_plural = models.BooleanField(verbose_name="جمع تكسير")
    comment = models.CharField(verbose_name="Commentaire", max_length=50)


    class Meta:
        verbose_name = "Pattern"
        verbose_name_plural = "Patterns"

    def __str__(self):
        return self.voweled_form


class RulePack(models.Model):
    
    name = models.CharField(verbose_name="Nom de l'ensemble", max_length=50)
    active = models.BooleanField(verbose_name="Activité de l'ensemble")


    class Meta:
        verbose_name = "Ensemble de régles"
        verbose_name_plural = "Ensembles de régles"

    def __str__(self):
        return self.name
    
    def add_state(self, label, is_start=False, is_end=False):
        s = State.objects.create(rule_pack=self, label=label, is_start=is_start, is_end=is_end, active=True)
        return s


    def add_transition(self, **kwargs):
        try:
            t = Transition.objects.get(rule_pack=self, active=True, **kwargs)
        except Transition.DoesNotExist:
            t = Transition.objects.create(rule_pack=self, active=True, **kwargs)
        return t
    

    def get_transition(self, **kwargs):
        try:
            t = Transition.objects.get(rule_pack=self, active=True, **kwargs)
        except Transition.DoesNotExist:
            return None
        return t
    
    
    def get_start_states(self):
        return State.objects.filter(rule_pack=self, is_start=True, active=True)


    def get_next_states(self, state, **kwargs):
        states = []
        
        trts = state.next_transitions.filter(
            rule_pack=self, active=True, **kwargs
        )
        for t in trts:
            states.append(t.to_state)
        return states
    

    def r_parser(self, sent_transitions, actual_state=None):
        """
            sent_transitions doit étre une liste de simples transitions, pas de doublons.
        """
        out = []
        if not actual_state:
            actual_states = self.get_start_states()
            for s in actual_states:
                tmp = self.r_parser(sent_transitions, actual_state=s)
                # if tmp :
                for suit in tmp:
                    if suit:
                        out.append(suit)
        else:
            if len(sent_transitions) == 0:
                if actual_state.is_end:
                    return actual_state
                else:
                    return None
            nexts = self.get_next_states(actual_state, **sent_transitions[0])
            for n in nexts:
                rest = self.r_parser(sent_transitions[1:], actual_state=n)
                if rest:
                    if type(rest) == list:
                        for suit in rest:
                            if suit:
                                out.append([actual_state] + suit)
                    else:
                        out.append([actual_state, rest])
                else:
                    out.append(None)
        return out


class State(models.Model):

    rule_pack = models.ForeignKey(RulePack, verbose_name="Ensemble de régles", on_delete=models.CASCADE)
    label = models.CharField(verbose_name="Libelé", max_length=100)
    is_start = models.BooleanField(verbose_name="Possibilité d'un départ")
    is_end = models.BooleanField(verbose_name="Possibilité de fin")
    active = models.BooleanField(verbose_name="Activité de l'état", default=True)
    
    class Meta:
        verbose_name = "Etat"
        verbose_name_plural = "Etats"

    def __str__(self):
        return self.label


class Transition(models.Model):

    rule_pack = models.ForeignKey(RulePack, verbose_name="Ensemble de régles", on_delete=models.CASCADE)
    from_state = models.ForeignKey(State, verbose_name="Etat de provenance", related_name="next_transitions", on_delete=models.CASCADE, null=True, blank=True)
    to_state = models.ForeignKey(State, verbose_name="Etat de destination", related_name="prev_transitions", on_delete=models.CASCADE)

    word_type = models.CharField(verbose_name="نوع الكلمة", max_length=40, choices=WORD_TYPES, null=True)
    word_subtype = models.CharField(verbose_name="تكمبل نوع الكلمة", max_length=40, null=True)
    halat_al_irab = models.CharField(verbose_name="حالة الإعراب", max_length=20, choices=HALAT_AL_IRAB, null=True)
    is_muaaraf = models.BooleanField(verbose_name="معرف", null=True)

    occ = models.IntegerField(verbose_name="Poids de la transition", default=0)

    active = models.BooleanField(verbose_name="Activité de la transition", default=True)
    

    class Meta:
        verbose_name = "Transition"
        verbose_name_plural = "Transitions"

    def __str__(self):
        return str(self.from_state) + " -> " + str(self.to_state)
    

class MissingPos(models.Model):

    word = models.CharField(verbose_name="Mot à POSER !", max_length=30)
    missing_date = models.DateTimeField(verbose_name="Date de la problématique", auto_now=True)
    fixed_date = models.DateTimeField(verbose_name="Date de maintenance", null=True)
