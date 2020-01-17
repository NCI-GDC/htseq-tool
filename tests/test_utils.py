import gzip
import unittest

from htseq_tools.utils import get_open_function


class TestUtils(unittest.TestCase):

    def test_get_open_function_ascii(self):
        fname = 'test.txt'
        ofunc = get_open_function(fname)
        self.assertEqual(ofunc, open)

    def test_get_open_function_gz(self):
        fname = 'test.txt.gz'
        ofunc = get_open_function(fname)
        self.assertEqual(ofunc, gzip.open)
