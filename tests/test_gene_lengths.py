import unittest
import os

from htseq_tools.tools.gene_lengths import (
    extract_gene_data,
    extract_metadata)


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
