# -*- coding: utf-8 -*-
# Tests for the contrib/localflavor/ BR form fields.

tests = r"""
# BRZipCodeField ############################################################
>>> from django.contrib.localflavor.br.forms import BRZipCodeField
>>> f = BRZipCodeField()
>>> f.clean('12345-123')
u'12345-123'
>>> f.clean('12345_123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('1234-123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('abcde-abc')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('12345-')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('-123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('')
Traceback (most recent call last):
...
ValidationError: [u'This field is required.']
>>> f.clean(None)
Traceback (most recent call last):
...
ValidationError: [u'This field is required.']

>>> f = BRZipCodeField(required=False)
>>> f.clean(None)
u''
>>> f.clean('')
u''
>>> f.clean('-123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('12345-')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('abcde-abc')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('1234-123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('12345_123')
Traceback (most recent call last):
...
ValidationError: [u'Enter a zip code in the format XXXXX-XXX.']
>>> f.clean('12345-123')
u'12345-123'

# BRPhoneNumberField #########################################################

>>> from django.contrib.localflavor.br.forms import BRPhoneNumberField
>>> f = BRPhoneNumberField()
>>> f.clean('41-3562-3464')
u'41-3562-3464'
>>> f.clean('4135623464')
u'41-3562-3464'
>>> f.clean('41 3562-3464')
u'41-3562-3464'
>>> f.clean('41 3562 3464')
u'41-3562-3464'
>>> f.clean('(41) 3562 3464')
u'41-3562-3464'
>>> f.clean('41.3562.3464')
u'41-3562-3464'
>>> f.clean('41.3562-3464')
u'41-3562-3464'
>>> f.clean(' (41) 3562.3464')
u'41-3562-3464'
>>> f.clean(None)
Traceback (most recent call last):
...
ValidationError: [u'This field is required.']
>>> f.clean('')
Traceback (most recent call last):
...
ValidationError: [u'This field is required.']

>>> f = BRPhoneNumberField(required=False)
>>> f.clean('')
u''
>>> f.clean(None)
u''
>>> f.clean(' (41) 3562.3464')
u'41-3562-3464'
>>> f.clean('41.3562-3464')
u'41-3562-3464'
>>> f.clean('(41) 3562 3464')
u'41-3562-3464'
>>> f.clean('4135623464')
u'41-3562-3464'
>>> f.clean('41 3562-3464')
u'41-3562-3464'

# BRStateSelect ##############################################################

>>> from django.contrib.localflavor.br.forms import BRStateSelect
>>> w = BRStateSelect()
>>> w.render('states', 'PR')
u'<select name="states">\n<option value="AC">Acre</option>\n<option value="AL">Alagoas</option>\n<option value="AP">Amap\xe1</option>\n<option value="AM">Amazonas</option>\n<option value="BA">Bahia</option>\n<option value="CE">Cear\xe1</option>\n<option value="DF">Distrito Federal</option>\n<option value="ES">Esp\xedrito Santo</option>\n<option value="GO">Goi\xe1s</option>\n<option value="MA">Maranh\xe3o</option>\n<option value="MT">Mato Grosso</option>\n<option value="MS">Mato Grosso do Sul</option>\n<option value="MG">Minas Gerais</option>\n<option value="PA">Par\xe1</option>\n<option value="PB">Para\xedba</option>\n<option value="PR" selected="selected">Paran\xe1</option>\n<option value="PE">Pernambuco</option>\n<option value="PI">Piau\xed</option>\n<option value="RJ">Rio de Janeiro</option>\n<option value="RN">Rio Grande do Norte</option>\n<option value="RS">Rio Grande do Sul</option>\n<option value="RO">Rond\xf4nia</option>\n<option value="RR">Roraima</option>\n<option value="SC">Santa Catarina</option>\n<option value="SP">S\xe3o Paulo</option>\n<option value="SE">Sergipe</option>\n<option value="TO">Tocantins</option>\n</select>'

# BRStateChoiceField #########################################################
>>> from django.contrib.localflavor.br.forms import BRStateChoiceField
>>> f = BRStateChoiceField()
>>> ', '.join([f.clean(s) for s, _ in f.widget.choices])
u'AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO'
>>> f.clean('')
Traceback (most recent call last):
...
ValidationError: [u'This field is required.']
>>> f.clean('pr')
Traceback (most recent call last):
...
ValidationError: [u'Select a valid brazilian state. That state is not one of the available states.']
"""
