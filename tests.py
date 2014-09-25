import unittest

from gen import (
    Field,
    Model,
    Module,
    module_builder,
)

class GenTester(unittest.TestCase):

    def test_charfield(self):
        field = Field('f1','CharField', max_length=200)
        self.assertEqual('f1 = models.CharField(max_length=200)', field.as_str())

    def test_integerfield(self):
        field = Field('f1', 'IntegerField')
        self.assertEqual('f1 = models.IntegerField()', field.as_str())

    def test_textfield(self):
        field = Field('f1', 'TextField')
        self.assertEqual('f1 = models.TextField()', field.as_str())

    def test_foreignkey(self):
        field = Field('f1', 'ForeignKey', 'F2')
        self.assertEqual('f1 = models.ForeignKey(F2)', field.as_str())

    def test_emptymodel(self):
        model = Model('Foo', [])
        expected = """class Foo(models.Model):\n    pass"""
        self.assertEqual(expected, model.as_str())

    def test_modelwithmanyfields(self):
        f1 = Field('f1', 'CharField', max_length=200)
        f2 = Field('f2', 'IntegerField')
        f3 = Field('f3', 'TextField')
        f4 = Field('f4', 'ForeignKey', 'F2')
        model = Model('Foo', [f1, f2, f3, f4])

        expected = """class Foo(models.Model):
    f1 = models.CharField(max_length=200)
    f2 = models.IntegerField()
    f3 = models.TextField()
    f4 = models.ForeignKey(F2)"""

        self.assertEqual(expected, model.as_str())

    def test_emptymodule(self):
        m1 = Module('models.py', [])
        expected = """from django.db import models\n\n\n"""
        self.assertEqual(expected, m1.as_str())

    def test_modulewithmanymodels(self):
        f1 = Field('f1', 'CharField', max_length=200)
        f2 = Field('f2', 'IntegerField')
        f3 = Field('f3', 'TextField')
        f4 = Field('f4', 'ForeignKey', 'F2')
        foo = Model('Foo', [f1, f2, f3, f4])
        bar = Model('Bar', [])
        m1 = Module('models.py', [foo, bar])

        expected = """from django.db import models


class Foo(models.Model):
    f1 = models.CharField(max_length=200)
    f2 = models.IntegerField()
    f3 = models.TextField()
    f4 = models.ForeignKey(F2)


class Bar(models.Model):
    pass"""

        self.assertEqual(expected, m1.as_str())

    def test_modulebuilderonemoduleonemodel(self):
        modules = module_builder(1, 1)

        expected = """from django.db import models


class M1(models.Model):
    f1 = models.CharField(max_length=200)
    f2 = models.IntegerField()
    f3 = models.TextField()"""

        self.assertEqual(expected, modules[0].as_str())

    def test_modulebuildermanymodulesmanymodels(self):
        modules = module_builder(2, 4)

        expected_m1 = """from django.db import models


class M1(models.Model):
    f1 = models.CharField(max_length=200)
    f2 = models.IntegerField()
    f3 = models.TextField()


class M2(models.Model):
    f4 = models.CharField(max_length=200)
    f5 = models.IntegerField()
    f6 = models.TextField()"""

        expected_m2 = """from django.db import models


class M3(models.Model):
    f7 = models.CharField(max_length=200)
    f8 = models.IntegerField()
    f9 = models.TextField()


class M4(models.Model):
    f10 = models.CharField(max_length=200)
    f11 = models.IntegerField()
    f12 = models.TextField()"""

        self.assertEqual(expected_m1, modules[0].as_str())
        self.assertEqual(expected_m2, modules[1].as_str())
