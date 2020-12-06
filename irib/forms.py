from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML, Field, ButtonHolder

class AddRule(forms.Form):
    state = forms.ModelChoiceField(label='الإعراب المناسب', 
        help_text="إن لم يوجد إعراب مناسب، يرجى ترك الإختيار فارغاً و إدخال الإعراب يدوياً مع إختيار معلومات طرف الكلام.", 
        required=False, queryset=State.objects.all(), widget=forms.Select(attrs={'style': 'width: 100%;'}))
    pos = forms.CharField(label="معلومات طرف الكلام", required=False, widget=forms.Select(choices=[('', '-------')], attrs={'style': 'width: 100%;'}))
    label = forms.CharField(label='إدخال الإعراب', max_length = 100, required=False, widget=forms.TextInput(attrs={'style': 'width: 100%;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('state', css_class="col-sm-12"),
                css_class = 'row state'
            ),
            Div(
                Div('pos', css_class="col-sm-12"),
                css_class = 'row pos'
            ),
            Div(
                Div('label', css_class="col-sm-12"),
                css_class = 'row label'
            ),
            Div(
                Submit('submit', 'قدم', css_class="col-sm-6", style="display: block; margin-top:15px; margin-left: auto; margin-right: auto;"),
                css_class = 'row'
            ),
            
        )
        # self.helper.add_input(Submit('submit', 'قدم', css_class="col-sm-6 mx-auto", style="display: block; margin-left: auto; margin-right: auto;"))
        
    




        