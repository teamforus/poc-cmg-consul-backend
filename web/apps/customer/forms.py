import string

from cms.models import User
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from apps.customer.utils import normalise_email



def generate_username():
    letters = string.ascii_letters
    allowed_chars = letters + string.digits + '_'
    uname = get_random_string(length=30, allowed_chars=allowed_chars)
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname


class PasswordResetForm(auth_forms.PasswordResetForm):
    """
    This form takes the same structure as its parent from django.contrib.auth
    """
    communication_type_code = "PASSWORD_RESET"

    def save(self, domain_override=None, use_https=False, request=None,
             **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        site = get_current_site(request)
        if domain_override is not None:
            site.domain = site.name = domain_override
        email = self.cleaned_data['email']
        active_users = User.objects.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            reset_url = self.get_reset_url(site, request, user, use_https)
            ctx = {
                'user': user,
                'site': site,
                'reset_url': reset_url}
            # messages = CommunicationEventType.objects.get_and_render(
            #     code=self.communication_type_code, context=ctx)
            # Dispatcher().dispatch_user_messages(user, messages)

    def get_reset_url(self, site, request, user, use_https):
        # the request argument isn't used currently, but implementors might
        # need it to determine the correct subdomain
        reset_url = "%s://%s%s" % (
            'https' if use_https else 'http',
            site.domain,
            get_password_reset_url(user))

        return reset_url


class EmailAuthenticationForm(AuthenticationForm):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    auth backend.
    """
    username = forms.EmailField(label=_('Email address'))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url


class ConfirmPasswordForm(forms.Form):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    auth backend.
    """
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(
                _("The entered password is not valid!"))
        return password


class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email address'))
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput)
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """
        Checks for existing users with the supplied email address.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("A user with that email address already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        validate_password(password2, self.instance)
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if 'username' in [f.name for f in User._meta.fields]:
            user.username = generate_username()
        if commit:
            user.save()
        return user
