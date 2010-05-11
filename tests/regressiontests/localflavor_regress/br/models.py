from django.db import models
from django.contrib.localflavor.br.models import BRCPFField, BRCNPJField

class BRCPFCNPJ(models.Model):

    cpf = BRCPFField()
    cnpj = BRCNPJField()

    def __unicode__(self):
        return u"%s ,  %s" % (self.cpf,self.cnpj)

    class Meta:
        app_label = 'localflavor_regress'
