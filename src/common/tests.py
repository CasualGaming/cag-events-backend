from django.test import TestCase

from .permissions import generate_default_permissions


class GenerateDefaultPermissionsTestCase(TestCase):

    def test1(self):
        expected_set = [
            ("view_arealayout", "(Admin panel) View area layout"),
            ("add_arealayout", "(Admin panel) Add area layout"),
            ("change_arealayout", "(Admin panel) Change area layout"),
            ("delete_arealayout", "(Admin panel) Delete area layout"),
        ]
        actual_set = generate_default_permissions("AreaLayout", "area layout")

        self.assertEqual(expected_set, actual_set)
