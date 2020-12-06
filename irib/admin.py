from django.contrib import admin
from .models import *


class SuffixeAdmin(admin.ModelAdmin):
    list_display = ('classe', 'description', 'voweled_form', 'unvoweled_form')
    list_filter = ('classe',)
    ordering = ('classe', 'description', 'unvoweled_form')
    search_fields = ('classe', 'description',)


class PrefixeAdmin(admin.ModelAdmin):
    list_display = ('classe', 'description', 'voweled_form', 'unvoweled_form')
    list_filter = ('classe',)
    ordering = ('classe', 'description', 'unvoweled_form')
    search_fields = ('classe', 'description',)


class ProperNounAdmin(admin.ModelAdmin):
    list_display = ('ptype', 'voweled_form', 'unvoweled_form')
    list_filter = ('ptype',)
    ordering = ('ptype', 'unvoweled_form')
    search_fields = ('ptype', 'unvoweled_form', 'voweled_form')


class ToolWordAdmin(admin.ModelAdmin):
    list_display = ('priority', 'prefixe_class', 'suffixe_class', 'ttype', 'voweled_form', 'unvoweled_form')
    list_filter = ('priority', 'prefixe_class', 'suffixe_class', 'ttype')
    ordering = ('ttype', 'priority', 'prefixe_class', 'suffixe_class', 'voweled_form')
    search_fields = ('ttype', 'voweled_form',)


class ExceptionalWordAdmin(admin.ModelAdmin):
    list_display = ('prefixe', 'suffixe', 'stem', 'etype', 'voweled_form', 'unvoweled_form')
    list_filter = ('etype',)
    ordering = ('etype', 'unvoweled_form')
    search_fields = ('etype', 'unvoweled_form')


class RacineAdmin(admin.ModelAdmin):
    list_display = ('unvoweled_form',)
    ordering = ('unvoweled_form',)
    search_fields = ('unvoweled_form',)


class PatternAdmin(admin.ModelAdmin):
    list_display = ('voweled_form', 'unvoweled_form', 'ptype', 'ntype', 'vtype', 'broken_plural', 'comment')
    list_filter = ('ptype', 'ntype', 'vtype')
    ordering = ('ptype', 'voweled_form')
    search_fields = ('voweled_form', 'ptype', 'ntype', 'vtype', 'comment')


class RulePackAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active', )
    ordering = ('active', 'name')
    search_fields = ('name', )


class StateAdmin(admin.ModelAdmin):
    list_display = ('rule_pack', 'label', 'is_start', 'is_end')
    list_filter = ('rule_pack', 'is_start', 'is_end')
    ordering = ('rule_pack', 'is_start', 'is_end')
    search_fields = ('label', 'rule_pack')


class TransitionAdmin(admin.ModelAdmin):
    list_display = ('rule_pack', 'occ', 'from_state', 'to_state', 'word_type', 'word_subtype', 'halat_al_irab', 'is_muaaraf', 'active')
    list_filter = ('rule_pack', 'active', 'word_type', 'word_subtype', 'halat_al_irab', 'is_muaaraf', 'from_state', 'to_state')
    ordering = ('rule_pack', 'active', 'occ', 'from_state', 'to_state')
    search_fields = ('rule_pack', 'from_state', 'to_state', 'word_type', 'word_subtype', 'halat_al_irab')


class MissingPosAdmin(admin.ModelAdmin):
    list_display = ('missing_date', 'word', 'fixed_date')
    list_filter = ('fixed_date', )
    ordering = ('fixed_date', 'missing_date', 'word')
    search_fields = ('missing_date', 'word', 'fixed_date')


admin.site.register(Suffixe, SuffixeAdmin)
admin.site.register(Prefixe, PrefixeAdmin)
admin.site.register(ProperNoun, ProperNounAdmin)
admin.site.register(ToolWord, ToolWordAdmin)
admin.site.register(ExceptionalWord, ExceptionalWordAdmin)
admin.site.register(Racine, RacineAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(RulePack, RulePackAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(MissingPos, MissingPosAdmin)
