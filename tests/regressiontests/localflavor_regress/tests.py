import unittest
from django.test import TestCase

# just import your tests here
from us.tests import *


# Get every subclass of TestCase and add to suite
# Now script check for every imported class, if is a subclass of TestCase add
# to testlist, and then suite create a TestSuite with these clases.
testlist=[]
for i in locals().values():
    try:
        if issubclass(i,TestCase) and i is not TestCase:
            testlist.append(unittest.TestLoader().loadTestsFromTestCase(i))
    except TypeError:
        pass

def suite():
    return unittest.TestSuite(list(testlist))

