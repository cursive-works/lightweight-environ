import os
from unittest import TestCase, mock

from lightweight_environ import Env


TEST_ENVIRON = {
    "MY_STRING": "Ford Prefect",
    "MY_INTEGER": "42",
    "MY_FLOAT": "6.283",
    "MY_BOOLEAN": "True",
    "MY_LIST": "DONT,PANIC",
}


@mock.patch.dict(os.environ, TEST_ENVIRON)
class LightweightEnvironTestSuite(TestCase):

    def test_missing_var_raises_exception(self):
        with self.assertRaises(KeyError):
            Env.get('A_MISSING_VAR')

    def test_missing_var_returns_default(self):
        self.assertEqual(Env.get('A_MISSING_VAR', 'foo'), 'foo')

    def test_get_a_string(self):
        self.assertEqual('Ford Prefect', Env.get('MY_STRING'))

    def test_get_int_string(self):
        self.assertEqual('42', Env.get('MY_INTEGER'))

    def test_get_int(self):
        self.assertEqual(42, Env.int('MY_INTEGER'))

    def test_get_boolean(self):
        self.assertTrue(Env.bool('MY_BOOLEAN'))

    def test_missing_boolean_is_false(self):
        self.assertFalse(Env.bool('A_MISSING_VALUE'))

    def test_missing_boolean_default(self):
        self.assertTrue(Env.bool('A_MISSING_VALUE', True))

    def test_get_float(self):
        self.assertEqual(6.283, Env.float('MY_FLOAT'))

    def test_non_float_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Env.float('MY_STRING')

    def test_non_int_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Env.float('MY_LIST')

    def test_get_int_with_float_raises_value_error(self):
        with self.assertRaises(ValueError):
            Env.int('MY_FLOAT')

    def test_get_float_from_int(self):
        self.assertEqual(42.0, Env.float('MY_INTEGER'))


    def test_get_list(self):
        my_list = Env.list('MY_LIST')
        self.assertIn('DONT', my_list)
        self.assertIn('PANIC', my_list)

    def test_list_default_string(self):
        my_list = Env.list('A_MISSING_VALUE', 'Oh,freddled,gruntbuggly')
        self.assertIn('Oh', my_list)
        self.assertIn('freddled', my_list)
        self.assertIn('gruntbuggly', my_list)

    def test_list_default_list(self):
        my_list = Env.list('A_MISSING_VALUE', ['Oh', 'freddled', 'gruntbuggly'])
        self.assertIn('Oh', my_list)
        self.assertIn('freddled', my_list)
        self.assertIn('gruntbuggly', my_list)

    def test_has_variable(self):
        self.assertTrue(Env.has('MY_STRING'))

    def test_has_not_variable(self):
        self.assertFalse(Env.has('A_MISSING_VARIABLE'))
