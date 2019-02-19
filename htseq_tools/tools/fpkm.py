"""Module to calculate FPKM and FPKM-UQ from an htseq count
file. Our implementation uses only the protein coding genes 
for upper quantile and FPKM denominator.
"""
import numpy as np

from htseq_tools.utils import get_logger, get_open_function

def load_protein_coding_ids(fil):
    """Extract the protein coding genes from the length TSV"""
    count = 0
    gene_length = dict()
    protein_coding = list()

    ofunc = get_open_function(fil)
    head = []
    with ofunc(fil, 'rt') as fh:
        for line in fh:
            if not head:
                head = line.rstrip('\r\n').split('\t')
            else: 
                dat = dict(zip(head, line.rstrip('\r\n').split('\t')))
                gene_id = dat['gene_id']
                if dat['gene_type'] == 'protein_coding':
                    protein_coding.append(gene_id)
                    count += 1 
                length = int(dat['aggregate_length']) 
                gene_length[gene_id] = length
    return count, set(protein_coding), gene_length

def get_protein_coding_read_count(pcgenes, count_file):
    """
    Extract the counts of fragments mapped to protein coding genes.
    """

    ofunc = get_open_function(count_file)
    protein_coding_reads = 0
    read_count = dict()
    glist = []
    with ofunc(count_file, 'rt') as fh:
        for line in fh:
            cols = line.rstrip('\r\n').split('\t')
            gid = cols[0]
            if gid.startswith('__'): continue
            frags = int(cols[1])
            if gid in pcgenes:
                protein_coding_reads += frags 
            read_count[gid] = frags
            glist.append(gid)
    return protein_coding_reads, read_count, glist

def calculate_fpkm(all_read_count, pc_frag_count, all_gene_length, pc_genes, glist, out_prefix, logger):
    """
    calculates the FPKM and FPKM-UQ
    """
    if len(all_gene_length) != len(all_read_count):
        msg = "Unequal length and counts of genes"
        logger.error(msg)
        raise Exception(msg)

    pc_reads = np.array([all_read_count[i] for i in list(pc_genes)])
    upper_quantile = np.percentile(pc_reads, 75)
    if upper_quantile == 0:
        msg = 'Upper quantile is 0!'
        logger.error(msg)
        raise ValueError(msg)

    logger.info("Upper quantile: {0}".format(upper_quantile))

    # Outputs
    out_fpkm = '{0}.FPKM.txt.gz'.format(out_prefix)
    out_fpkm_uq = '{0}.FPKM-UQ.txt.gz'.format(out_prefix)
    ofpkm_func = get_open_function(out_fpkm)
    ofpkm_uq_func = get_open_function(out_fpkm_uq)

    # Process and write
    with ofpkm_func(out_fpkm, 'wt') as ofpkm, ofpkm_uq_func(out_fpkm_uq, 'wt') as ofpkm_uq:
        for gene in glist: 
            if gene in all_gene_length:
                C = all_read_count[gene] 
                L = all_gene_length[gene]
                if L == 0:
                    msg = "The length of gene {0} is zero.".format(gene)
                    logger.error(msg)
                    raise ValueError(msg)

                fpkm = (C * pow(10.0, 9)) / (pc_frag_count * L)
                ofpkm.write('{0}\t{1:.4f}\n'.format(gene, fpkm))
                
                fpkm_uq = (C * pow(10.0, 9)) / (upper_quantile * L)
                ofpkm_uq.write('{0}\t{1:.4f}\n'.format(gene, fpkm_uq))

def main(args):
    """
    Main entry point for FPKM and FPKM-UQ quantification.
    """
    logger = get_logger('fpkm')

    logger.info("Extracting protein-coding genes...")
    gene_count, \
    pcgenes, \
    gene_length = load_protein_coding_ids(args.aggregate_length_file)

    logger.info("Getting fragment counts...")
    total_pc_frag_count, \
    read_count_dic, \
    gene_list = get_protein_coding_read_count(pcgenes, args.htseq_counts)

    logger.info("Calculating FPKM and FPKM-UQ")
    calculate_fpkm(read_count_dic, total_pc_frag_count, gene_length, pcgenes, 
        gene_list, args.output_prefix, logger)
