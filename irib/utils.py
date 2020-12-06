import copy


class DFA:
    """ This class represent any type of deterministic finite automaton."""

    def __init__(self, alphabet):
        """ Initialise the finite automaton.
            @param the alphabet of the automaton."""

        """ List of string corresponding to states name.
            States are always identificated by name."""
        self.states = []
        """ Dictionary using src state as key and mapping it to a list of
            pair (dest_state, symbol)."""
        self.transitions = {}
        """ The string corresponding to the name of the initial state."""
        self.init = None
        """ A list containing the name of the final states."""
        self.finals = []
        """ A string containing all symbols in the alphabet."""
        self.alphabet = []
        for s in alphabet:
            if s not in self.alphabet:
                self.alphabet.append(s)

    def add_state(self, state, final=False):
        """ Add a new state. Print error if the state already exists.
            @param state    the name of the new state.
            @param final    a boolean determining if the state is
                final"""
        if state in self.states:
            print("error : state '" + state + "' already exists.")
            return
        self.transitions[state] = []
        self.states.append(state)
        if final:
            self.finals.append(state)

    def valid_symbol(self, symbol):
        """ Returns true if the symbol is part of the alphabet,
            false otherwise.
            @param symbol the symbol to be tested """
        if symbol not in self.alphabet: return False
        return True

    def dst_state(self, src_state, symbol):
        """ Search the transition corresponding to the specified source state
            and symbol and returns the destination state. If the transition does
            not exists, return None.
            @param src_state the source state of the transition.
            @param symbol the symbol of the transition. """
        if src_state not in self.states:
            print("error : the state '" + src_state + "' is not an existing state.")
            return
        # dst_list = []
        for (s, dst_state) in self.transitions[src_state]:
            if s == symbol:
                # dst_list.append(dst_state)
                return dst_state
        # return dst_list
        return 

    def add_transition(self, src_state, symbol, dst_state):
        """ Add a transition to the FA. Print error if the automaton already have a
            transition for the specified source state and symbol.
            @param src_state the name of the source state.
            @param symbol the symbol of the transition
            @param dst_state the name of the destination state."""
        if not self.valid_symbol(symbol):
            print("error : the symbol '" + symbol + "' is not part of the alphabet.")
            return
        if src_state not in self.states:
            print("error : the state '" + src_state + "' is not an existing state.")
            return
        if dst_state not in self.states:
            print("error : the state '" + dst_state + "' is not an existing state.")
            return

        # if dst_state in self.dst_state(src_state, symbol):
        if dst_state == self.dst_state(src_state, symbol):
            print("error : the transition (" + src_state + ", " + symbol + ", ...) already exists.")
            return

        self.transitions[src_state].append((symbol, dst_state))
        return

    def clone(self):
        """ Returns a copy of the DFA."""
        a = DFA(self.alphabet)
        a.states = self.states.copy()
        a.init = self.init
        a.finals = self.finals
        a.transitions = copy.deepcopy(self.transitions)
        return a

    def __str__(self):
        ret = "FA :\n"
        ret += "   - alphabet   : '" + str(self.alphabet) + "'\n"
        ret += "   - init       : " + str(self.init) + "\n"
        ret += "   - finals     : " + str(self.finals) + "\n"
        ret += "   - states (%d) :\n" % (len(self.states))
        for state in self.states:
            ret += "       - (%s)" % (state)
            if len(self.transitions[state]) is 0:
                ret += ".\n"
            else:
                ret += ":\n"
                for (sym, dest) in self.transitions[state]:
                    ret += "          --(%s)--> (%s)\n" % (sym, dest)
        return ret



# def run(dfa, sentence, verbose = False):
#     """ Runs the specified DFA on a word and returns routes if the sentence (rule) is
#         accepted.
#         @param dfa      the DFA to be executed.
#         @param sentence     the sentence to be tested.
#         @param verbose  if True, more information are displayed about the
#             execution.
#         @return list of route if the sent is accepted, False otherwise."""
#     if dfa.init == None:
#         print("error : the automaton does not have any initial symbol.")
#         return False

#     current_state = dfa.init
#     route = [current_state]

#     i = 0
#     for symbol in sentence:
#         if verbose : print("configuration : (" + current_state + ", " + str(sentence[i:]) + ")")
#         if not dfa.valid_symbol(symbol):
#             print("error : the symbol '" + symbol + "' is not part of the alphabet. Abord.")
        
#         next_state = dfa.dst_state(current_state, symbol)
#         if next_state is None:
#             if verbose: print("no transition available for (" + current_state + ", " + str(symbol) + ").")
#             return False

#         current_state = next_state
#         route.append(current_state)
#         i = i+1

#     if current_state in dfa.finals:
#         if verbose: print("ending on final state '" + current_state + "'.")
#         return route
#     if verbose: print("ending on non accepting state '" + current_state + "'")
#     return False



# roles = [("nominal", "marfu3", True),
#          ("nominal", "marfu3", False),
#          ("nominal", "mansoub", ),
#          ("nominal", "majrour"),
#          ("verbs", "marfu3"),
#          ("verbs", "mansoub"),
#          ("verbs", "majzoum"),
#          ("tool", ""),
#          ("dhamir_mouttasil", ""),
#          ("dhamir_mounfasil", "")]

# roles.append("DEBUT")
# # states = ["marfu3", "mansoub", "majrour", "majzoum"]

# rules = DFA(roles)

# rules.add_state("DEBUT")
# rules.init = "DEBUT"
# ## rules.add_state("فعل ماضي مبني على الفتح")
# rules.add_state("مبتدأ مرفوع و علامة رفعه الضمة الضاهرة")
# rules.add_state("خبر مرفوع و علامة رفعه الضمة الضاهرة")

# rules.add_transition("DEBUT",
#                      ("nominal", "marfu3", True),
#                      "مبتدأ مرفوع و علامة رفعه الضمة الضاهرة")
# rules.add_transition("مبتدأ مرفوع و علامة رفعه الضمة الضاهرة",
#                      ("nominal", "marfu3", False),
#                      "خبر مرفوع و علامة رفعه الضمة الضاهرة")

# rules.finals = ["خبر مرفوع و علامة رفعه الضمة الضاهرة"]

# print(rules)

# exemple = [("nominal", "marfu3", True), ("nominal", "marfu3", False)]

# route = run(rules, exemple, verbose=True)

# for c in route:
#     print(" --> "+str(c))
