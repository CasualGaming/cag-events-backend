from django.test import TestCase

from .permissions import generate_default_permissions
from .request_utils import get_query_param_bool, get_query_param_int, get_query_param_list, get_query_param_str, is_query_param_set


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


class GetRequestParamsTestCase(TestCase):

    class Object(object):
        pass

    @classmethod
    def setUpTestData(cls):
        class Object(object):
            pass

        cls.request = Object()
        cls.request.query_params = {
            "empty": "",
            "something": "alpha",
            "str1": "alpha",
            "bool_true1": "true",
            "bool_true2": "yes",
            "bool_true3": "1",
            "bool_false1": "false",
            "bool_false2": "no",
            "bool_false3": "0",
            "int1": "50",
            "int2": "-50",
            "list_some_empty_parts": ",a,,,b",
            "list1": "a",
            "list2": "a,b",
        }

    def test_is_set(self):
        self.assertFalse(is_query_param_set(self.request, "missing"))
        self.assertTrue(is_query_param_set(self.request, "empty"))
        self.assertTrue(is_query_param_set(self.request, "something"))

    def test_str(self):
        self.assertEqual(get_query_param_str(self.request, "missing"), None)
        self.assertEqual(get_query_param_str(self.request, "missing", missing_default="missing_default"), "missing_default")
        self.assertEqual(get_query_param_str(self.request, "empty"), "")
        self.assertEqual(get_query_param_str(self.request, "str1"), "alpha")

    def test_bool(self):
        self.assertEqual(get_query_param_bool(self.request, "missing"), None)
        self.assertEqual(get_query_param_bool(self.request, "missing", missing_default=False), False)
        self.assertEqual(get_query_param_bool(self.request, "empty"), True)
        self.assertEqual(get_query_param_bool(self.request, "empty", empty_default=False), False)
        self.assertEqual(get_query_param_bool(self.request, "bool_true1"), True)
        self.assertEqual(get_query_param_bool(self.request, "bool_true2"), True)
        self.assertEqual(get_query_param_bool(self.request, "bool_true3"), True)
        self.assertEqual(get_query_param_bool(self.request, "bool_false1"), False)
        self.assertEqual(get_query_param_bool(self.request, "bool_false2"), False)
        self.assertEqual(get_query_param_bool(self.request, "bool_false3"), False)

    def test_int(self):
        self.assertEqual(get_query_param_int(self.request, "missing"), None)
        self.assertEqual(get_query_param_int(self.request, "missing", missing_default=5), 5)
        self.assertEqual(get_query_param_int(self.request, "empty"), None)
        self.assertEqual(get_query_param_int(self.request, "empty", empty_default=5), 5)
        self.assertEqual(get_query_param_int(self.request, "int1"), 50)
        self.assertEqual(get_query_param_int(self.request, "int2"), -50)

    def test_list(self):
        self.assertEqual(get_query_param_list(self.request, "missing"), None)
        self.assertEqual(get_query_param_list(self.request, "missing", missing_default=["a"]), ["a"])
        self.assertEqual(get_query_param_list(self.request, "empty"), [])
        self.assertEqual(get_query_param_list(self.request, "empty", empty_default=["a"]), ["a"])
        self.assertEqual(get_query_param_list(self.request, "list1"), ["a"])
        self.assertEqual(get_query_param_list(self.request, "list2"), ["a", "b"])
        self.assertEqual(get_query_param_list(self.request, "list_some_empty_parts"), ["a", "b"])
        self.assertEqual(get_query_param_list(self.request, "list_some_empty_parts", remove_empty=False), ["", "a", "", "", "b"])
