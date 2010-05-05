from django.db import models
from django.contrib.localflavor.br.br_cpfcnpj import CPF,CNPJ
from django.contrib.localflavor.br import forms


class BRCPFField(models.CharField):
    """ CPF Model field """
    description = "The Brazilian CPF Field"

    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kwargs):
        self.longformat = kwargs.pop('longformat',False)
        kwargs['max_length'] = 14 if self.longformat else 11
        super(BRCPFField,self).__init__(*args,**kwargs)

    def formfield(self,**kwargs):
        defaults = {'form_class': forms.BRCPFField}
        defaults.update(kwargs)
        return super(BRCPFField,self).formfield(**defaults)

    def to_python(self,value):
        """ convert string from base to a CPF instance """
        if isinstance(value,CPF) or value is None:
            return value
        try:
            return CPF(value)
        except TypeError:
            return None

    def get_prep_value(self,value):
        value = self.to_python(value)
        if not value:
            return None
        if self.longformat:
            return value.__unicode__
        else:
            return value.single

class BRCNPJField(models.CharField):
    """ CNPJ Model field """
    description = "The Brazilian CNPJ Field"

    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kwargs):
        self.longformat = kwargs.pop('longformat',False)
        kwargs['max_length'] = 18 if self.longformat else 14
        super(BRCNPJField,self).__init__(*args,**kwargs)

    def formfield(self,**kwargs):
        defaults = {'form_class': forms.BRCNPJField}
        defaults.update(kwargs)
        return super(BRCNPJField,self).formfield(**defaults)

    def to_python(self,value):
        """ convert string from base to a CNPJ instance """
        if isinstance(value,CNPJ) or value is None:
            return value
        try:
            return CNPJ(value)
        except TypeError:
            return None

    def get_prep_value(self,value):
        value = self.to_python(value)
        if not value:
            return None
        if self.longformat:
            return value.__unicode__
        else:
            return value.single
