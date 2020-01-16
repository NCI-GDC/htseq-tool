import argparse
import logging
import gzip
import numpy as np

import htseq_tools.tools.fpkm as fpkm
import htseq_tools.tools.gene_lengths as gene_lengths
import htseq_tools.tools.merge_counts as merge_counts

from htseq_tools.utils import get_logger


def load_args():
    """Load the argument parser object"""
    parser = argparse.ArgumentParser(description='htseq tools')

    sp = parser.add_subparsers(description='Select a tool', dest='choice')

    # Get Gene Lengths
    glen = sp.add_parser("gene_lengths",
                         description="Extract gene exon lengths from GTF")
    glen.add_argument("--gtf_file", required=True,
                      help="GTF file used for htseq count")
    glen.add_argument("--out_file", required=True,
                      help="Output TSV file to write to")

    # Merge counts
    merge = sp.add_parser("merge_counts",
                          description="Merge PE and SE counts from HTseq")
    merge.add_argument("--htseq_counts", required=True, action='append',
                       help="HTSeq count file. Use multiple times")
    merge.add_argument("--out_file", required=True,
                       help="Output TSV file to write to")

    # FPKM
    fpkm = sp.add_parser("fpkm", description="Get FPKM and FPKM-UQ")
    fpkm.add_argument("--aggregate_length_file", required=True,
                      help="Aggregate length TSV")
    fpkm.add_argument("--htseq_counts", required=True,
                      help="HTSeq counts txt file")
    fpkm.add_argument("--output_prefix", required=True,
                      help="The output prefix to use.")

    return parser.parse_args()


def main():
    """Main entry point for CLI"""
    logger = get_logger('htseq-tools')
    args = load_args()

    logger.info("Loading tool {0}".format(args.choice))
    tool = None
    if args.choice == 'fpkm':
        tool = fpkm
    elif args.choice == 'gene_lengths':
        tool = gene_lengths
    elif args.choice == 'merge_counts':
        tool = merge_counts

    tool.main(args)
    logger.info("Finished!")


if __name__ == '__main__':
    main()
