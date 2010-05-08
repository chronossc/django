from django.db import models
from django.contrib.localflavor.us.models import USStateField

class USPlace(models.Model):
    state = USStateField(blank=True)
    state_req = USStateField()
    state_default = USStateField(default="CA", blank=True)
    name = models.CharField(max_length=20)
    class Meta:
        app_label = 'localflavor_regress'
