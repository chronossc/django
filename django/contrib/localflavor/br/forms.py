# -*- coding: utf-8 -*-
"""
BR-specific Form helpers
"""

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, CharField, Select
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.br.br_cpfcnpj import CPF,CNPJ
import re

phone_digits_re = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')

class BRZipCodeField(RegexField):
    default_error_messages = {
        'invalid': _('Enter a zip code in the format XXXXX-XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(BRZipCodeField, self).__init__(r'^\d{5}-\d{3}$',
            max_length=None, min_length=None, *args, **kwargs)

class BRPhoneNumberField(Field):
    default_error_messages = {
        'invalid': _('Phone numbers must be in XX-XXXX-XXXX format.'),
    }

    def clean(self, value):
        super(BRPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        m = phone_digits_re.search(value)
        if m:
            return u'%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        raise ValidationError(self.error_messages['invalid'])

class BRStateSelect(Select):
    """
    A Select widget that uses a list of Brazilian states/territories
    as its choices.
    """
    def __init__(self, attrs=None):
        from br_states import STATE_CHOICES
        super(BRStateSelect, self).__init__(attrs, choices=STATE_CHOICES)

class BRStateChoiceField(Field):
    """
    A choice field that uses a list of Brazilian states as its choices.
    """
    widget = Select
    default_error_messages = {
        'invalid': _(u'Select a valid brazilian state. That state is not one of the available states.'),
    }

    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text=None):
        super(BRStateChoiceField, self).__init__(required, widget, label,
                                                 initial, help_text)
        from br_states import STATE_CHOICES
        self.widget.choices = STATE_CHOICES

    def clean(self, value):
        value = super(BRStateChoiceField, self).clean(value)
        if value in EMPTY_VALUES:
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        valid_values = set([smart_unicode(k) for k, v in self.widget.choices])
        if value not in valid_values:
            raise ValidationError(self.error_messages['invalid'])
        return value

class BRCPFField(CharField):
    """
    This field validate a CPF number or a CPF string. A CPF number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.

    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
    """
    default_error_messages = {
        'invalid': _("Invalid CPF number."),
        'max_digits': _("This field requires at most 11 digits or 14 characters."),
        'digits_only': _("This field requires only numbers."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        kwargs['min_length'] = 11
        super(BRCPFField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Value can be either a string in the format XXX.XXX.XXX-XX or an
        11-digit number.
        """
        value = super(BRCPFField, self).clean(value)

        try:
            cpf = CPF(value)
        except ValueError,err:
            # CPF class already raise internal erros if cpf isn't valid
            raise ValidationError(_(err.message))

        return value

class BRCNPJField(CharField):
    """
    This field validate a CNPJ number or a CNPJ string. A CNPJ number is
    compounded by XX.XXX.XXX/XXXX-VD. The two last digits are check digits.
    """

    def __init__(self,*args,**kwargs):
        kwargs['max_length'] = 18
        kwargs['min_length'] = 14
        super(BRCNPJField,self).__init__(*args,**kwargs)

    def clean(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        value = super(BRCNPJField, self).clean(value)

        try:
            cnpj = CNPJ(value)
        except ValueError,err:
            # CNPJ class already raise internal errors if CNPJ isn't valid
            raise ValidationError(_(err.message))

        return value
