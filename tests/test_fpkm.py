import unittest
import os
import logging
import gzip

from htseq_tools.tools.fpkm import (
    load_protein_coding_ids,
    get_protein_coding_read_count,
    calculate_fpkm)

logger = logging.getLogger()


class TestFpkm(unittest.TestCase):
    len_file = os.path.join(os.path.dirname(__file__),
                            'etc/test_lengths.txt')
    ct_file_1 = os.path.join(os.path.dirname(__file__),
                             'etc/test_counts_1.txt')
    exp_fpkm = os.path.join(os.path.dirname(__file__),
                            'etc/test_counts_calc_fpkm.expected_fpkm.txt.gz')
    exp_fpkm_uq = os.path.join(os.path.dirname(__file__),
                               'etc/test_counts_calc_fpkm.' +
                               'expected_fpkm_uq.txt.gz')
    out_test_pfx = os.path.join(os.path.dirname(__file__),
                                'etc/test_counts_calc_fpkm')

    def test_load_protein_coding_ids(self):
        gene_count, pcgenes, gene_length = load_protein_coding_ids(
            self.len_file)

        self.assertEqual(1, gene_count)
        self.assertEqual(set(['FAKE.2']), pcgenes)
        self.assertEqual({'FAKE.1': 468, 'FAKE.2': 37}, gene_length)

    def test_get_protein_coding_read_count(self):
        gene_count, pcgenes, gene_length = load_protein_coding_ids(
            self.len_file)

        total_pc_frag_count, read_count_dic, gene_list = \
            get_protein_coding_read_count(pcgenes, self.ct_file_1)

        self.assertEqual(10, total_pc_frag_count)
        self.assertEqual({'FAKE.2': 10, 'FAKE.1': 200}, read_count_dic)
        self.assertEqual(['FAKE.1', 'FAKE.2'], gene_list)

    def test_calculate_fpkm(self):
        gene_count, pcgenes, gene_length = load_protein_coding_ids(
            self.len_file)

        total_pc_frag_count, read_count_dic, gene_list = \
            get_protein_coding_read_count(pcgenes, self.ct_file_1)

        calculate_fpkm(read_count_dic, total_pc_frag_count, gene_length,
                       pcgenes, gene_list, self.out_test_pfx, logger)

        with gzip.open(self.exp_fpkm, 'rt') as fh, gzip.open(
                  self.out_test_pfx + '.FPKM.txt.gz', 'rt') as ofh:
            exp = fh.read()
            found = ofh.read()
            self.assertEqual(exp, found)
            os.remove(self.out_test_pfx + '.FPKM.txt.gz')

        with gzip.open(self.exp_fpkm_uq, 'rt') as fh, gzip.open(
                  self.out_test_pfx + '.FPKM-UQ.txt.gz', 'rt') as ofh:
            exp = fh.read()
            found = ofh.read()
            self.assertEqual(exp, found)
            os.remove(self.out_test_pfx + '.FPKM-UQ.txt.gz')

    def setUp(self):
        pass

    def tearDown(self):
        for sfx in ['FPKM.txt.gz', 'FPKM-UQ.txt.gz']:
            fil = self.out_test_pfx + '.{0}'.format(sfx)
            if os.path.exists(fil):
                os.remove(fil)
