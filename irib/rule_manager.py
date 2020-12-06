from .processor import *
from .models import *


def init_rule_pack(name, active=True):
    p = RulePack.objects.create(name=name, active=active)
    return p


def add_state(pack, label, is_start=False, is_end=False):
    s = State.objects.create(rule_pack=pack, label=label, is_start=is_start, is_end=is_end)
    return s


def add_transition(pack, from_state, to_state, word_type=None, word_subtype=None, halat_al_irab=None, is_muaaraf=None, active=True):
    t = Transition.objects.create(rule_pack=pack, from_state=from_state, to_state=to_state, 
        word_type=word_type, word_subtype=word_subtype, halat_al_irab=halat_al_irab, is_muaaraf=is_muaaraf, active=active)
    return t


def get_next_states(pack, state, transition=None):
    states = []
    if not transition:
        # trts = Transition.objects.filter(rule_pack=pack, from_state=state)
        trts = state.next_transitions.all()
    else:
        trts = state.next_transitions.filter(
            rule_pack=pack, 
            word_type=transition['stype'], 
            word_subtype=transition['type'], 
            halat_al_irab=transition['halat_al_irab'],
            is_muaaraf=transition['muaaraf']
        )
    for t in trts:
        states.append(t.to_state)
    return states


# def Union(lsts):
#     final_list = lsts[0]
#     for l in lsts:
#         final_list = list(set(final_list) | set(l)) 
#     return final_list 


def r_parser(pack, sent_transitions, actual_state=None):
    """
        sent_transitions doit étre une liste de simple transitions, pas de doublons.
    """
    out = []
    if not actual_state:
        actual_state = State.objects.filter(rule_pack=pack, is_start=True)
        nexts = []
        for s in actual_state:
            nexts = get_next_states(pack, s, transition=sent_transitions[0])
            for n in nexts:
                for suit in r_parser(pack, sent_transitions[1:], n):
                    if suit:
                        out.append([s] + suit)
    else:
        if len(sent_transitions) == 0:
            if actual_state.is_end:
                return actual_state
            else:
                return None
        nexts = get_next_states(pack, actual_state, transition=sent_transitions[0])
        for n in nexts:
            rest = r_parser(pack, sent_transitions[1:], n)
            if rest:
                for suit in rest:
                    out.append([actual_state] + suit)
            else:
                return None
    return out


def add_rule_from_sent(pack, sent):
    """
        Ajoute la régle que suit la phrase dans le package des régles
    """
    
    return