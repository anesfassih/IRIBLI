from django.shortcuts import render, redirect
from .processor import *
from .rule_manager import *
from .models import RulePack
from .forms import AddRule

TRANSLATE = {
    "nominal": "إسم",
    "verbs": "فعل",
    "tool": "أداة",
    "except": "إسم خاص",
    "prop": "إسم علم",
    "Comparative": "مقارنة",
    "Masdar": "مصدر", 
    "Miscellaneous": "متنوع", 
    "active_participle": "نعت", 
    "artificial_masdar": "مصدر صناعي", 
    "brokenPlural": "جمع التكسير", 
    "instrument": "إسم أداة", 
    "marrah": "إسم مرة", 
    "mubalagah": "مبالغة", 
    "mushabbaha": "مشبهة", 
    "nisbah": "نسبة", 
    "passive_participle": "النعت السلبي", 
    "place": "إسم مكان", 
    "regular_feminine_dual": "مثنى مؤنث",
    "singular_forms-broken_plural_forms": "إسم مفرد", 
    "singular_forms-fem_plural_forms": "إسم مؤنث", 
    "singular_forms-no_plural_forms": "...", 
    "singular_forms-reg_plural_forms": "...",
    "adjectival": "صفة",
    "nominal": "إسم",
    "nominal/adjectival": "إسم - صفة",
    "participial": "مكون من إسم الفاعل أو المفعول",
    "1": "فعل من الشكل 1",
    "2": "فعل من الشكل 2",
    "3": "فعل من الشكل 3",
    "4": "فعل من الشكل 4",
    "5": "فعل من الشكل 5",
    "6": "فعل من الشكل 6",
    "7": "فعل من الشكل 7",
    "8": "فعل من الشكل 8",
    "9": "فعل من الشكل 9",
    "present": "فعل مضارع",
    "نسبة إلى اسم علم": "نسبة إلى اسم علم",
    "اسم علم": "اسم علم", 
    "اسم الجلالة": "اسم الجلالة", 
    "raf3": "رفع",
    "nasb": "نصب",
    "jarr": "جر",
    "jazm": "جزم",
    "word_type": "نوع الكلمة",
    "word_subtype": "تكمبل نوع الكلمة",
    "halat_al_irab": "حالة الإعراب",
    "is_muaaraf": "معرف",
    "True": "نعم",
    "False": "لا"
}

def home(request):

    return render(request, 'irib/home.html', locals())

def process(request):
    RP = RulePack.objects.get(active=True)
    start_state = State.objects.get(rule_pack = RP, label="START")
    if request.POST:
        try:
            text_phrase = request.POST['sent_text']
            phrase = araby.tokenize(text_phrase)
            posed_phrase = []
            posed_phrase_list = []
            accepted = []
            for w in phrase:
                pos = pos_word(w)
                posed_phrase.append({'word': w, 'pos': pos})
                posed_phrase_list.append(pos)
            sent_combinations = to_combs(posed_phrase_list)
            for sent in sent_combinations:
                tmp = RP.r_parser(sent)
                proposition = []
                trans = []
                for t in tmp:
                    # print(t)
                    for i, irab in enumerate(t[1:]):
                        proposition.append({
                            'word': phrase[i], 
                            'irab': irab, 
                            'trans': RP.get_transition(
                                from_state=t[i], 
                                to_state=t[i+1], **sent[i])
                            })
                        trans.append(RP.get_transition(
                                from_state=t[i], 
                                to_state=t[i+1], **sent[i]).id)
                    if proposition:
                        if {'proposition': proposition, 'trans': trans} not in accepted:
                            accepted.append({'proposition': proposition, 'trans': trans})
            if not accepted:
                return redirect('feed', sent_text=request.POST['sent_text'], actual_state=start_state.id, word_position=0)
                # accepted += RP.r_parser(sent)

        except RulePack.DoesNotExist:
            return redirect("activate_rpack")

    return render(request, 'irib/process.html', locals())


def validate(request, trans):
    
    trans = [int(t) for t in trans.split(',')]
    transitions = Transition.objects.filter(id__in=trans)
    for t in transitions:
        t.occ += 1
        t.save()
    
    return redirect('home')


def feed(request, sent_text, actual_state, word_position):
    RP = RulePack.objects.get(active=True)
    phrase = araby.tokenize(sent_text)
    word_position = int(word_position)
    state = State.objects.get(pk=actual_state)
    
    form = AddRule(request.POST or None)

    potential_states = []

    tmp_pos = pos_word(phrase[word_position])

    if form.is_valid():
        if form.cleaned_data['state']: # Etat éxistant ------------------------------------
            # form.cleaned_data['state'].prev_transitions.get() ### Incrémenter le poids de la transition...
            if word_position == len(phrase) - 1:
                form.cleaned_data['state'].is_end = True
                form.cleaned_data['state'].save()
                return redirect('home')
            return redirect('feed', sent_text=sent_text, actual_state=form.cleaned_data['state'].id, word_position=word_position+1)
        else:
            if form.cleaned_data['pos'] != -1 and form.cleaned_data['label']: # Etat non éxistant et informations de l'irab saisis --
                is_end = False; is_start=False
                if word_position == len(phrase) - 1:
                    is_end = True
                if word_position == 0:
                    is_start = True
                s = RP.add_state(label=form.cleaned_data['label'], is_start=is_start, is_end=is_end)
                t = RP.add_transition(from_state=state, to_state=s, **tmp_pos[int(form.cleaned_data['pos'])])
                if is_end:
                    return redirect('home')
                else:
                    return redirect('feed', sent_text=sent_text, actual_state=s.id, word_position=word_position+1)
    
    for pos in tmp_pos:
        trans = state.next_transitions.filter(**pos)
        for t in trans:
            potential_states.append(t.to_state)
    POS_CHOICES = []
    for i, p in enumerate(tmp_pos):
        POS_CHOICES.append(
            (
                i,
                " - ".join(
                        [TRANSLATE[key] + " : "+ TRANSLATE[str(value)] for key, value in p.items()]
                    )
            )
        )
    form.fields['state'].queryset = State.objects.filter(pk__in=[s.id for s in potential_states])
    form.fields['pos'].widget.choices += POS_CHOICES

        
    
    return render(request, 'irib/feed.html', locals())