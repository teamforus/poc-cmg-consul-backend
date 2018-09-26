
from django import forms
from apps.organisation.models import OrganisationItem

from parler.models import TranslatedFields, TranslatableModel
from django.utils.translation import gettext_lazy as _


class OrganisationRegisterForm(forms.ModelForm):

    class Meta:
        model = OrganisationItem
        fields = ('title', )


class OrganisationEditForm(forms.ModelForm):
    class Meta:
        model = OrganisationItem
        fields = ('title', 'public_key', 'private_key' )
