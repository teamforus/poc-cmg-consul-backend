from cms.models import User

from apps.customer.signals import user_registered

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate


class RegisterOrganisationMixin(object):
    def register_organisation(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        organisation = form.save()
        organisation.owner = self.request.user
        organisation.save()

        return organisation

