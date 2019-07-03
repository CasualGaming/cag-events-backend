from copy import deepcopy

from django.core.exceptions import SuspiciousOperation
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
        cls.user_claims = {
            "sub": "714e166c-2a44-4c92-a1b5-7d34feadaa08",
            "username": "UsEr",
            "pretty_username": "UsEr",
            "given_name": "Use",
            "family_name": "Userson",
            "email": "user@example.net",
            "birth_date": "2000-01-01",
            "gender": "female",
            "phone_number": "1234567890",
            "address": {
                "country": "Norway",
                "postal_code": "1234",
                "street_address": "Street 123",
            },
            "membership_years": "2010,2012",
            "groups": ["user"],
        }

    def test_get_claim(self):
        self.assertEqual(OidcAuthBackend.get_claim(self.claims, "one"), "en")
        self.assertEqual(OidcAuthBackend.get_claim(self.claims, "two"), "to")
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.get_claim, self.claims, "three")
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.get_claim, self.claims, "four")

    def test_user_attributes_valid1(self):
        # No changes
        attributes = OidcAuthBackend.decode_attributes(self.user_claims)
        OidcAuthBackend.validate_attributes(attributes)

    def test_user_attributes_valid2(self):
        # No membership years and groups is fine
        claims = deepcopy(self.user_claims)
        claims["membership_years"] = ""
        claims["groups"] = []
        attributes = OidcAuthBackend.decode_attributes(claims)
        OidcAuthBackend.validate_attributes(attributes)

    def test_user_attributes_valid3(self):
        # Uppercase email address domain is fine
        claims = deepcopy(self.user_claims)
        claims["email"] = "USER@EXAMPLE.NET"
        attributes = OidcAuthBackend.decode_attributes(claims)
        OidcAuthBackend.validate_attributes(attributes)

    def test_user_attributes_invalid_sub1(self):
        # Missing subject ID
        claims = deepcopy(self.user_claims)
        claims["sub"] = ""
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_username1(self):
        # Missing username
        claims = deepcopy(self.user_claims)
        claims["username"] = ""
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_username2(self):
        # Invalid characters in username
        claims = deepcopy(self.user_claims)
        claims["username"] = "Håvard"
        attributes = OidcAuthBackend.decode_attributes(claims)
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.validate_attributes, attributes)

    def test_user_attributes_invalid_username3(self):
        # Invalid characters in username
        claims = deepcopy(self.user_claims)
        claims["username"] = "HON 123"
        attributes = OidcAuthBackend.decode_attributes(claims)
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.validate_attributes, attributes)

    def test_user_attributes_invalid_username4(self):
        # Too short username
        claims = deepcopy(self.user_claims)
        claims["username"] = "H"
        attributes = OidcAuthBackend.decode_attributes(claims)
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.validate_attributes, attributes)

    def test_user_attributes_invalid_username5(self):
        # Too long username
        claims = deepcopy(self.user_claims)
        claims["username"] = "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
        attributes = OidcAuthBackend.decode_attributes(claims)
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.validate_attributes, attributes)

    def test_user_attributes_invalid_pretty_username1(self):
        # Missing pretty username
        claims = deepcopy(self.user_claims)
        claims["pretty_username"] = ""
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_pretty_username2(self):
        # Pretty username does not match username
        claims = deepcopy(self.user_claims)
        claims["username"] = "UsEr"
        claims["pretty_username"] = "UsErr"
        attributes = OidcAuthBackend.decode_attributes(claims)
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.validate_attributes, attributes)

    def test_user_attributes_invalid_email1(self):
        # Missing email address
        claims = deepcopy(self.user_claims)
        claims["email"] = ""
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_email2(self):
        # Malformed email address
        claims = deepcopy(self.user_claims)
        claims["email"] = "hon"
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_membership_years1(self):
        # Malformed list of membership years
        claims = deepcopy(self.user_claims)
        claims["membership_years"] = "abc"
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_user_attributes_invalid_membership_years2(self):
        # Malformed list of membership years
        claims = deepcopy(self.user_claims)
        claims["membership_years"] = "1234,567A"
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_attributes, claims)

    def test_decode_membership_years(self):
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_membership_years,
                          self.claims, key="membership_years_missing", year="2000")
        self.assertRaises(SuspiciousOperation, OidcAuthBackend.decode_membership_years,
                          self.claims, key="membership_years_malformed", year="2000")
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_empty", year="2010"), ("", False))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2011", year="2010"), ("2011", False))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2011", year="2011"), ("2011", True))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2012"), ("2012,2013", True))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2013"), ("2012,2013", True))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2012_2013", year="2014"), ("2012,2013", False))
        self.assertEqual(OidcAuthBackend.decode_membership_years(
                         self.claims, key="membership_years_2010_comma", year="2010"), ("2010,", True))
