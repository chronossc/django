<<<<<<< HEAD:tests/regressiontests/localflavor/forms.py
from us.forms import *
=======
from django.forms import ModelForm
from models import USPlace

class USPlaceForm(ModelForm):
    """docstring for PlaceForm"""
    class Meta:
        model = USPlace
>>>>>>> ticket13495:tests/regressiontests/localflavor_regress/us/forms.py
