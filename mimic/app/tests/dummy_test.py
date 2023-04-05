from django.test import TestCase


class DummyTestCase(TestCase):
    """ A Dummy test case to help setup testing.
    """

    def test_something(self):
        """ Check that 1 == 1.
        """

        self.assertEqual(1, 1, "DummyTestCase is failing. Something is wrong.")
