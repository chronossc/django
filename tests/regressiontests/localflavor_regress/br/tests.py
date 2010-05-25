from django.test import TestCase
from django import forms
from django.contrib.localflavor.br.br_cpfcnpj import CPF, CNPJ, CPFGenerator,\
    CNPJGenerator
from django.contrib.localflavor.br import forms as brforms
from models import BRCPFCNPJ, BRCPFCNPJ2
from forms import BRCPFCNPJForm

from random import choice

class BRCPFCNPJTests(TestCase):

    @property
    def randomcpf(self):
        return CPFGenerator()

    @property
    def randomcnpj(self):
        return CNPJGenerator()

    def test_cpf_type(self):
        """ make tests on cpf class """
        cpf = '43502207046'

        # test wrong size
        try:
            CPF(cpf[:-1])
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['max_digits'],))

        # test digits only
        try:
            CPF(cpf.replace('0','a'))
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['digits_only'],))

        # test invalid cpf
        try:
            CPF(cpf[:-1]+'5')
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['invalid'],))

        # test valid cpf
        try:
            cpfn = CPF(cpf)
        except ValueError,err:
            self.fail(str(err))
    
    def test_cnpj_type(self):
        """ make tests on cnpj type """
        cnpj = '59430995000173'

        # test wrong size
        try:
            CNPJ(cnpj[:-1])
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['max_digits'],))

        # test digits only
        try:
            CNPJ(cnpj.replace('0','a'))
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['digits_only'],))

        # test invalid cnpj
        try:
            CNPJ(cnpj[:-1]+'5')
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['invalid'],))

        # test valid cnpj
        try:
            cnpjn = CNPJ(cnpj)
        except ValueError,err:
            self.fail(str(err))

    def test_cpf_generator(self):
        # create 100 CPFS with generator
        for i in xrange(100):
            try:
                CPF(self.randomcpf)
            except ValueError,err:
                self.fail(str(err))

    def test_cnpj_generator(self):
        # create 100 CNPJS with generator
        for i in xrange(100):
            try:
                CNPJ(self.randomcnpj)
            except ValueError,err:
                self.fail(str(err))

    def test_cpfcnpj_form_and_model(self):
        # inserts 100 register on cpfcnpj model with form
        for i in xrange(100):
            cpf = self.randomcpf
            cnpj = self.randomcnpj

            # just choice over full number cpf/cnpj, normal string or with
            # additional characters, so we test with that various formats on
            # form input
            cpf_to_form = choice([cpf,str(CPF(cpf)),CPF(cpf).single])
            cnpj_to_form = choice([cnpj,str(CNPJ(cnpj)),CNPJ(cnpj).single])
            
            f = BRCPFCNPJForm(data={'cpf':cpf_to_form,'cnpj':cnpj_to_form})

            if f.is_valid():
                f.save()
            else:
                # show any errors
                self.fail(u"\n".join(["\n%s: %s" % (k.upper(),u', '.join(v)) for k,v in f.errors.items()]))
                break

            try:
                inst = BRCPFCNPJ.objects.get(cpf=cpf,cnpj=cnpj)
            except BRCPFCNPJ.DoesNotExist:
                self.fail("Failed on get saved cpf/cnpj with form")
                break
            else:
                # check if numbers are equal
                self.assertEqual(cpf,inst.cpf.single)
                self.assertEqual(cnpj,inst.cnpj.single)


    def test_cpfcnpj_simpleform(self):
        """ test single form with blank value and normal value """

        class Form1(forms.Form):
            cpf = brforms.BRCPFField(required=False)
            def save(self):
                return self.cleaned_data
        class Form2(forms.Form):
            cnpj = brforms.BRCNPJField(required=False)
            def save(self):
                return self.cleaned_data


        cpf = CPFGenerator()
        cnpj = CNPJGenerator()

        """ with cpf """
        f = Form1(data={'cpf':cpf})
        self.assertEqual(f.is_valid(),True)
        self.assertEqual({'cpf':cpf},f.save())
        """ without cpf """
        f = Form1(data={'cpf':''})
        self.assertEqual(f.is_valid(),True)
        self.assertEqual({'cpf':''},f.save())


        """ with cnpj """
        f = Form2(data={'cnpj':cnpj})
        self.assertEqual(f.is_valid(),True)
        self.assertEqual({'cnpj':cnpj},f.save())
        """ without cnpj """
        f = Form2(data={'cnpj':''})
        self.assertEqual(f.is_valid(),True)
        self.assertEqual({'cnpj':''},f.save())

    def test_cpfcnpj_blank_model_form(self):
        """ test blank=True for models and forms """

        class Form1(forms.ModelForm):

            class Meta:
                model = BRCPFCNPJ2

        f = Form1(data={'cpf':'','cnpj':''})
        self.assertEqual(f.is_valid(),True)
        self.assertEqual({'cnpj':'','cpf':''},f.cleaned_data)
        f.save()
        m = BRCPFCNPJ2.objects.get(pk=1)
        self.assertEqual(m.cpf,'')
        self.assertEqual(m.cnpj,'')


