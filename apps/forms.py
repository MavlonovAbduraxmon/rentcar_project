from django.forms.models import ModelForm

from apps.models import User


class CustomUserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'