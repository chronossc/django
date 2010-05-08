import unittest
from django.test import TestCase

from us.tests import *




# Get every subclass of TestCase and add to suite

testlist=[]

for i in locals().values():
    try:
        if issubclass(i,TestCase) and i is not TestCase:
            testlist.append(unittest.TestLoader().loadTestsFromTestCase(i))
    except TypeError:
        pass


def suite():
    return unittest.TestSuite(list(testlist))

