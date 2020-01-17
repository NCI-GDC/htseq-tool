import unittest
import os

from htseq_tools.tools.gene_lengths import (
    extract_gene_data,
    extract_metadata,
    load_gtf_data,
    write_lengths)


class TestGeneLengths(unittest.TestCase):

    def test_extract_gene_data(self):
        finfo_parts = [
            'gene_id "ENSG00000223972.5"',
            'gene_type "transcribed_unprocessed_pseudogene"']

        gene_id, gene_type = extract_gene_data(finfo_parts)
        self.assertEqual(gene_id, "ENSG00000223972.5")
        self.assertEqual(gene_type, "transcribed_unprocessed_pseudogene")

    def test_extract_gene_data_assert(self):
        finfo_parts = [
            'gene_i "ENSG00000223972.5"',
            'gene_type "transcribed_unprocessed_pseudogene"']

        with self.assertRaises(AssertionError):
            extract_gene_data(finfo_parts)

        finfo_parts = [
            'gene_id "ENSG00000223972.5"',
            'gene_typ "transcribed_unprocessed_pseudogene"']

        with self.assertRaises(AssertionError):
            extract_gene_data(finfo_parts)

    def test_extract_metadata(self):
        finfo_parts = [
            'gene_id "ENSG00000223972.5"',
            'gene_type "transcribed_unprocessed_pseudogene"',
            'gene_status "KNOWN"', 'gene_name "DDX11L1"',
            'transcript_type "processed_transcript"',
            'transcript_status "KNOWN"', 'transcript_name "DDX11L1-002"',
            'exon_number 1', 'exon_id "ENSE00002234944.1"', 'level 2',
            'tag "basic"']

        finfo_string = '; '.join(finfo_parts) + '; '
        gene_id, gene_type = extract_metadata(finfo_string)
        self.assertEqual(gene_id, 'ENSG00000223972.5')
        self.assertEqual(gene_type, "transcribed_unprocessed_pseudogene")

    def test_extract_metadata_assert(self):
        finfo_parts = [
            'gene_id "ENSG00000223972.5"',
            'gene_type "transcribed_unprocessed_pseudogene"',
            'gene_status "KNOWN"', 'gene_name "DDX11L1"',
            'transcript_type "processed_transcript"',
            'gene_id "ENSG00000223972.5"',
            'transcript_status "KNOWN"', 'transcript_name "DDX11L1-002"',
            'exon_number 1', 'exon_id "ENSE00002234944.1"', 'level 2',
            'tag "basic"']

        finfo_string = '; '.join(finfo_parts) + '; '
        with self.assertRaises(AssertionError):
            gene_id, gene_type = extract_metadata(finfo_string)

    def test_load_gtf_data(self):
        gtf_file = os.path.join(os.path.dirname(__file__), 'etc/test.gtf')
        gene_data, exon_data = load_gtf_data(gtf_file)

        expected_gene = {'FAKE.1': 'pseudogene', 'FAKE.2': 'protein_coding'}
        self.assertEqual(gene_data, expected_gene)

        expected_exon = {
            'FAKE.1': [(11869, 12227), (12613, 12721), (12010, 12057),
                       (12179, 12227)],
            'FAKE.2': [(29534, 29570)]
        }
        self.assertEqual(exon_data, expected_exon)

    def test_write_lengths(self):
        gtf_file = os.path.join(os.path.dirname(__file__), 'etc/test.gtf')
        exp_file = os.path.join(os.path.dirname(__file__),
                                'etc/test_lengths.txt')
        out_file = os.path.join(os.path.dirname(__file__),
                                'etc/test_lengths_out.txt')

        gene_data, exon_data = load_gtf_data(gtf_file)
        write_lengths(gene_data, exon_data, out_file)

        with open(exp_file, 'rt') as fh, open(out_file, 'rt') as ofh:
            exp = fh.read()
            found = ofh.read()
            self.assertEqual(exp, found)

    def setUp(self):
        pass

    def tearDown(self):
        out_file = os.path.join(os.path.dirname(__file__),
                                'etc/test_lengths_out.txt')
        if os.path.exists(out_file):
            os.remove(out_file)
