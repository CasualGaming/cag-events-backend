from django.test import TestCase

from .permissions import generate_default_permissions


class GenerateDefaultPermissionsTestCase(TestCase):

    def test1(self):
        expected_set = [
            ("view_arealayout", "View area layout"),
            ("add_arealayout", "Add area layout"),
            ("change_arealayout", "Change area layout"),
            ("delete_arealayout", "Delete area layout"),
        ]
        actual_set = generate_default_permissions("AreaLayout", "area layout")

        self.assertEqual(expected_set, actual_set)
