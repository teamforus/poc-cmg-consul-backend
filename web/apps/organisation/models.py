import random
import string

from django.db import models

# Create your models here.
from parler.models import TranslatedFields, TranslatableModel
from django.utils.translation import gettext_lazy as _


class Organisation(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=767),
    )

    public_key = models.CharField(_('Public key'), max_length=767),
    secrete_key = models.CharField(_('Secrete key'), max_length=767),

    def __str__(self):
        return self.title


    #TODO Replace to core layer
    def init_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def save(self, *args, **kwargs):
        if not self.public_key:
            self.public_key = self.init_key()

        if not self.secrete_key:
            self.secrete_key = self.init_key()

        super(Organisation, self).save(*args, **kwargs)

