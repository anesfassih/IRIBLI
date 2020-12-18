from django import forms
from .models import *
import pyarabic.araby as araby
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML, Field, ButtonHolder
from django.core.exceptions import ValidationError

class AddRule(forms.Form):
    state = forms.ModelChoiceField(label='الإعراب المناسب :', 
        help_text="إن لم يوجد إعراب مناسب، يرجى ترك الإختيار فارغاً و إدخال الإعراب يدوياً مع إختيار معلومات طرف الكلام.", 
        required=False, queryset=State.objects.all(), widget=forms.Select(attrs={'dir': "rtl", 'lang': 'AR', 'style': 'width: 100%;'}))
    pos = forms.CharField(label="معلومات طرف الكلام :", required=False, widget=forms.Select(choices=[('', '-------')], attrs={'dir': "rtl", 'lang': 'AR', 'style': 'width: 100%;'}))
    label = forms.CharField(label='إدخال الإعراب :', max_length = 250, required=False, widget=forms.TextInput(attrs={'dir': "rtl", 'lang': 'AR', 'style': 'width: 100%;'}))

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
        self.helper.form_show_errors = False
    
    def clean(self):
        cleaned_data = super().clean()
        state = cleaned_data.get("state")
        pos = cleaned_data.get("pos")
        label = cleaned_data.get("label")

        if not state:
            # Only do something if both fields are valid so far.
            if not (pos and label):
                raise ValidationError(
                    "يرجى ملأ المعلومات"
                )

    




        