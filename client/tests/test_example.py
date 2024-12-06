"""This is an example TestCase."""
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
# ---------------------------------------------------------------------------------------------------------------------

class Example(TestCase):
    """TestCase."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def runTest(self):
        self.assertTrue(True)
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------
