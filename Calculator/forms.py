from django.forms import ModelForm, forms
from .models import Profile, FoodItem


class DesirableIntakeForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["desirable_intake"]


class AddFoodForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["foods"]


