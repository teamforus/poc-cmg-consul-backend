from django.core.exceptions import PermissionDenied


from apps.organisation.models import OrganisationItem


def allow_user_organisations(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied
        organisation = OrganisationItem.objects.get(id=kwargs['id'])

        if organisation.owner == request.user:
            request.organisation = organisation
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


