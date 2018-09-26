from apps.organisation.models import OrganisationRequest, OrganisationItem


class LoginMixin(object):

    def create_login(self, public_key):
        request = OrganisationRequest()
        request.organisation = OrganisationItem.objects.get_by_public_key(public_key)

        request.save()
        return request.unique_key

    def get_info(self, key):
        return OrganisationItem.objects.get_by_organization_request_key(key)


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

