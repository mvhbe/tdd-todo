from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):

    def testBadMaths(self):
        self.assertEqual(1 + 1, 3)
