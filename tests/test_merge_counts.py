import unittest
import os
import logging
import gzip

from htseq_tools.tools.merge_counts import merge_files

logger = logging.getLogger()


class TestMergeCounts(unittest.TestCase):
    len_file = os.path.join(os.path.dirname(__file__),
                            'etc/test_lengths.txt')
    ct_file_1 = os.path.join(os.path.dirname(__file__),
                             'etc/test_counts_1.txt')
    ct_file_2 = os.path.join(os.path.dirname(__file__),
                             'etc/test_counts_2.txt')
    exp_counts_file = os.path.join(os.path.dirname(__file__),
                                   'etc/test_counts_merge_2_expected.txt.gz')
    out_counts_file = os.path.join(os.path.dirname(__file__),
                                   'etc/test_counts_merge.txt.gz')

    def test_merge_files_one(self):
        merge_files([self.ct_file_1], self.out_counts_file, logger)
        with open(self.ct_file_1, 'rt') as fh, gzip.open(
                  self.out_counts_file, 'rt') as ofh:
            exp = fh.read()
            found = ofh.read()
            self.assertEqual(exp, found)
            os.remove(self.out_counts_file)

    def test_merge_files_two(self):
        merge_files([self.ct_file_1, self.ct_file_2],
                    self.out_counts_file, logger)
        with gzip.open(self.exp_counts_file, 'rt') as fh, gzip.open(
                  self.out_counts_file, 'rt') as ofh:
            exp = fh.read()
            found = ofh.read()
            self.assertEqual(exp, found)
            os.remove(self.out_counts_file)

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists(self.out_counts_file):
            os.remove(self.out_counts_file)
