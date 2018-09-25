
from django import forms
from apps.organisation.models import Organisation

from parler.models import TranslatedFields, TranslatableModel
from django.utils.translation import gettext_lazy as _


class OrganisationRegisterForm(forms.ModelForm):

    class Meta:
        model = Organisation
        fields = ('title', )
