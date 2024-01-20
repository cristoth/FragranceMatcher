from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms.models import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button
from .models import Fragrance, Perfume, Perfume_Fragrance



class FragranceSearchForm(forms.ModelForm):
    class Meta:
        model = Fragrance
        fields = ['name']


# class MyDateInput(forms.widgets.DateInput):
#     input_type = 'date'

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        # fields = ['name', 'description', 'duration_time', 'servings', 'protein', 'fat', 'carb', 'cals']
        exclude = ['author', 'fragrances', 'protein', 'fat', 'carb', 'cals', 'sugar',]  # exclude fields

        # name = forms.CharField()
        date_posted = forms.DateField(widget=forms.SelectDateWidget)#, input_formats=['%d-%m-%Y'])
        duration_time = forms.DurationField()
        widgets = {'duration_time': forms.TextInput(
            attrs={'placeholder': '00:10:00'})}

    # def calculate_nutritional_value(self):
    #     instance = super().save(commit=False)
    #     instance.protein = 0
    #     instance.fat = 0
    #     instance.carb = 0
    #     instance.cals = 0
    #     instance.sugar = 0
    #     total_quantity = 0
        
    #     for ingr in instance.recipe_ingredient_set.all():
    #         factor = {
    #                 'lb': 453.59237,
    #                 'oz': 28.3495231,
    #                 'tsp': 5.9,
    #                 'tbsp': 17.07,
    #                 'gal': 3753.46037,
    #                 'ml': 1,
    #                 'l': 1000,
    #                 'g': 1,
    #                 'kg': 1000,
    #             }.get(ingr.unit, 100)  # 100 will be returned default if unit is not found, as in 100g
    #         total_quantity += factor * ingr.quantity
    #         factor = (factor / 100) * ingr.quantity
    #         instance.protein += factor * ingr.ingredient.protein
    #         instance.fat += factor * ingr.ingredient.fat
    #         instance.carb += factor * ingr.ingredient.carb
    #         instance.cals += factor * ingr.ingredient.cals
    #         instance.sugar += factor * ingr.ingredient.sugar
        
    #     instance.protein = round(instance.protein * 100 / total_quantity, 2)
    #     instance.fat = round(instance.fat * 100 / total_quantity, 2)
    #     instance.carb = round(instance.carb * 100 / total_quantity, 2)
    #     instance.cals = round(instance.cals * 100 / total_quantity, 2)
    #     instance.sugar = round(instance.sugar * 100 / total_quantity, 2)
    #     return instance


class PerfumeFragranceForm(forms.ModelForm):
    class Meta:
        model = Perfume_Fragrance
        fields = ['fragrance', 'quantity', 'unit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].required = False

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.render_required_fields = True
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div('fragrance', css_class='col-md-3 me-3'),
                Div('quantity', css_class='col-md-3 me-2'), 
                Div('unit', css_class='col-md-3'), 
                Div('DELETE', css_class='col-2 align-self-center'), 
                css_class='row fragrance-form'
            ), 
        )


PerfumeFragranceFormSet = modelformset_factory(Perfume_Fragrance, form=PerfumeFragranceForm, extra=0, can_delete=True)
