import random
import string

from cms.models import User, reverse
from django.db import models


class OrganisationManager(models.Manager):
    def get_user_organisations(self, user):
        return self.get_queryset().filter(owner=user).all()

    def get_by_public_key(self, public_key):
        return self.get_queryset().filter(public_key=public_key)[:1].get()

    def get_by_organization_request_key(self, unique_key):
        query_set = self.get_queryset().filter(
            organisationrequest__in=OrganisationRequest.objects.filter(unique_key=unique_key))
        if not query_set.exists():
            return None
        return query_set[:1].get()


class OrganisationRequestManager(models.Manager):
    def get_by_key(self, unique_key):
        query_set = OrganisationRequest.objects.filter(unique_key=unique_key)
        if not query_set.exists():
            return None
        return query_set[:1].get()

    def allow(self, unique_key, auth_token, fields_json, is_subscribe):
        organization_request = self.get_by_key(unique_key)
        if organization_request is None:
            return None
        organization_request.status = STATUS_CHOICES_ALLOW
        organization_request.auth_token = auth_token
        organization_request.data = fields_json
        organization_request.is_subscribe = is_subscribe
        organization_request.save()

        return organization_request.status

    def disallow(self, unique_key):
        organization_request = self.get_by_key(unique_key)
        if organization_request is None:
            return None
        organization_request.status = STATUS_CHOICES_DISALLOW
        organization_request.auth_token = None
        organization_request.data = None
        organization_request.save()
        return organization_request.status


class OrganisationItem(models.Model):
    title = models.CharField(max_length=200, help_text="Enter organisation name", null=True, blank=False)

    public_key = models.CharField(max_length=200, help_text="Public key", null=True, blank=False)

    private_key = models.CharField(max_length=200, help_text="Private key", null=True, blank=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=False,
                              null=True)

    # Metadata
    class Meta:
        ordering = ["-pk"]

    # Methods

    def get_absolute_url(self):
        return self.get_edit_url()

    def get_edit_url(self) -> object:
        return reverse('organisation:organisation-edit-item', args=[str(self.id)])

    def get_qr_request_url(self):
        if self.public_key:
            return '/organisation/qr/?text=' + self.public_key
        return ''

    def init_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def __str__(self):
        return self.name

    def get_script(self):
        return '<div id="forus_button"></div><script type="text/props" id="forus_params"> { "FORUS_API_KEY": "' + self.public_key + '" } </script> <script async src="http://136.144.185.49/static/login.js/" type="text/javascript"></script>'

    def save(self, *args, **kwargs):
        if not self.public_key:
            self.public_key = self.init_key()
        if not self.private_key:
            self.private_key = self.init_key()

        super(OrganisationItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = OrganisationManager()


STATUS_CHOICES_NEW = 'new'
STATUS_CHOICES_ALLOW = 'allow'
STATUS_CHOICES_DISALLOW = 'disallow'
STATUS_CHOICES = (
    (STATUS_CHOICES_NEW, "NEW"),
    (STATUS_CHOICES_ALLOW, "ALLOW"),
    (STATUS_CHOICES_DISALLOW, "DISALLOW"),
)


class OrganisationRequest(models.Model):
    unique_key = models.CharField(max_length=200, null=False, blank=False, unique=True)

    organisation = models.ForeignKey(OrganisationItem, on_delete=models.CASCADE,
                                     blank=False,
                                     null=False)

    status = models.CharField(max_length=9,
                              choices=STATUS_CHOICES,
                              default=STATUS_CHOICES_NEW)

    auth_token = models.CharField(max_length=200, null=True, blank=True)

    is_subscribe = models.BooleanField(default=False, null=False, blank=False)

    data = models.CharField(max_length=1000, null=True, blank=True)

    # Metadata
    class Meta:
        ordering = ["-pk"]

    # Methods

    def init_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(80))

    def save(self, *args, **kwargs):
        if not self.unique_key:
            self.unique_key = self.init_key()

        super(OrganisationRequest, self).save(*args, **kwargs)

    objects = OrganisationRequestManager()
