# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from .backends import OidcAuthBackend


class OidcAuthBackendTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.claims = {
            "one": "en",
            "two": "to",
            "three": None,
            "membership_years_empty": "",
            "membership_years_2011": "2011",
            "membership_years_2012_2013": "2012,2013",
            "membership_years_2010_comma": "2010,",
            "membership_years_malformed": "20122013",
        }

    def test_get_claim(self):
        self.assertEqual(OidcAuthBackend.get_claim(self.claims, "one"), "en")
        self.assertEqual(OidcAuthBackend.get_claim(self.claims, "two"), "to")
        self.assertRaises(ImproperlyConfigured, OidcAuthBackend.get_claim, self.claims, "three")
        self.assertRaises(ImproperlyConfigured, OidcAuthBackend.get_claim, self.claims, "four")

    def test_get_membership_years(self):
        self.assertRaises(ImproperlyConfigured, OidcAuthBackend.get_membership_years,
                          self.claims, key="membership_years_missing", year="2000")
        self.assertRaises(ImproperlyConfigured, OidcAuthBackend.get_membership_years,
                          self.claims, key="membership_years_malformed", year="2000")
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_empty", year="2010"), ("", False))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2011", year="2010"), ("2011", False))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2011", year="2011"), ("2011", True))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2012"), ("2012,2013", True))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2013"), ("2012,2013", True))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2014"), ("2012,2013", False))
        self.assertEqual(OidcAuthBackend.get_membership_years(
                         self.claims, key="membership_years_2010_comma", year="2010"), ("2010,", True))
