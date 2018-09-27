import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from apps.organisation.forus import ForusApi
from apps.organisation.models import OrganisationRequest, OrganisationItem


class LoginError(Exception):
    def __init__(self, message, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message)
        self.message = message
        self.http_status = http_status


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class LoginMixin(object):

    FIELDS = ['primary_email', 'given_name', 'family_name', 'bsn']

    def create_login(self, public_key):
        request = OrganisationRequest()
        request.organisation = OrganisationItem.objects.get_by_public_key(public_key)

        request.save()
        return request.unique_key

    def get_info(self, key):
        organisation_request = OrganisationRequest.objects.get_by_key(key)
        organisation = OrganisationItem.objects.get_by_organization_request_key(key)
        if organisation_request is None or organisation is None:
            raise LoginError('Key is invalid', status.HTTP_404_NOT_FOUND)

        return {'key': organisation_request.unique_key, 'data': organisation_request.data, 'status': organisation_request.status, 'auth_token': organisation_request.auth_token, 'data': organisation_request.data,
                'organization': {'title': organisation.title, 'owner': organisation.owner.email, 'public_key': organisation.public_key}}

    def allow(self, key, auth_token):
        organization_request = OrganisationRequest.objects.get_by_key(key)
        if not organization_request:
            raise LoginError('Key is invalid', status.HTTP_404_NOT_FOUND)

        if not ForusApi.check_token(auth_token):
            raise LoginError('Token not active', status.HTTP_403_FORBIDDEN)

        fields = []
        records = ForusApi.get_records(auth_token)
        for record in records:
            for field in self.FIELDS:
                if record['key'] == field:
                    fields.append({'key': field, 'value': record['value']})
                    break

        fields_json = json.dumps(fields)
        return OrganisationRequest.objects.allow(key, auth_token, fields_json)

    def disallow(self, key):
        organization_request = OrganisationRequest.objects.get_by_key(key)
        if not organization_request:
            raise LoginError('Key is invalid', status.HTTP_404_NOT_FOUND)

        return OrganisationRequest.objects.disallow(key)


class RegisterOrganisationMixin(object):
    def edit_register_organisation(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        organisation = form.save()

        return organisation

    def register_organisation(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        organisation = form.save()
        organisation.owner = self.request.user
        organisation.save()

        return organisation

