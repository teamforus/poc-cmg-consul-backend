from apps.organisation.models import OrganisationRequest, OrganisationItem


class LoginMixin(object):

    def create_login(self, public_key):
        request = OrganisationRequest()
        request.organisation = OrganisationItem.objects.get_by_public_key(public_key)

        request.save()
        return request.unique_key

    def get_info(self, key):
        organisation_request = OrganisationRequest.objects.get_organization_request(key)
        organisation = OrganisationItem.objects.get_by_organization_request_key(key)
        if organisation_request is None or organisation is None:
            return None

        return {'key': organisation_request.unique_key, 'status': organisation_request.status, 'auth_token': organisation_request.auth_token,
                'organization': {'title': organisation.title, 'owner': organisation.owner.email, 'public_key': organisation.public_key}}

    def allow(self, key, auth_token):
        return OrganisationRequest.objects.allow(key, auth_token)

    def disallow(self, key):
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

