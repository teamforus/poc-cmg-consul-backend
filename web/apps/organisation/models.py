import random
import string

from cms.models import User
from django.db import models


class OrganisationManager(models.Manager):

    def get_user_organisations(self, user):
        return self.get_queryset().filter(owner=user).all()

    def get_by_public_key(self, public_key):
        return self.get_queryset().filter(public_key=public_key)[:1].get()

    def get_by_organization_request_key(self, unique_key):
        query_set = OrganisationRequest.objects.filter(unique_key=unique_key)
        if not query_set.exists():
            return None
        organisation_request = query_set[:1].get()
        return organisation_request.organisation


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
        return '1'  # reverse('model-detail-view', args=[str(self.id)])

    def get_qr_request_url(self):
        if self.public_key:
            return '/organisation/qr/?text=' + self.public_key
        return ''

    def init_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.public_key:
            self.public_key = self.init_key()
        if not self.private_key:
            self.private_key = self.init_key()

        super(OrganisationItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = OrganisationManager()


STATUS_CHOICES = (
    ("new", "NEW"),
    ("allow", "ALLOW"),
    ("disallow", "DISALLOW"),
)

class OrganisationRequest(models.Model):
    unique_key = models.CharField(max_length=200, null=False, blank=False, unique=True)

    organisation = models.ForeignKey(OrganisationItem, on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    status = models.CharField(max_length=9,
                             choices=STATUS_CHOICES,
                             default="new")

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

