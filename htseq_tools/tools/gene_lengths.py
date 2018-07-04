"""Module to extract the aggregate exon lengths per gene to use
for the FPKM conversion tool.
"""
import numpy as np

from htseq_tools.utils import get_logger, get_open_function

def extract_gene_data(info):
    """Extracts the gene id and type from the extracted info data"""
    gene_id = None
    gene_type = None
    for i in info:
        if i.startswith('gene_id'):
            gene_id = i.split(" ", 1)[1].replace('"', '')
        elif i.startswith('gene_type'):
            gene_type = i.split(" ", 1)[1].replace('"', '')

    if not gene_id:
        raise RuntimeException('No gene_id found {0}'.format(info))
    if not gene_type:
        raise RuntimeException('No gene_type found {0}'.format(info))
    return gene_id, gene_type

def extract_metadata(info_str):
    """Wrapper function to extract the gene id and type from the gtf info column string"""
    info = [i.strip() for i in info_str.split(';') if i.strip().startswith('gene_id') or i.strip().startswith('gene_type')]
    assert len(info) == 2, '{0}'.format(info) 
    gene_id, gene_type = extract_gene_data(info)
    return gene_id, gene_type

def load_gtf_data(fil):
    """Extract the exon start and stops from GTF""" 
    ofunc = get_open_function(fil)

    gene_data = {}
    exon_data = {}
    with ofunc(fil, 'rt') as fh:
        for line in fh:
            if line.startswith('#'): continue
            cols = line.rstrip('\r\n').split('\t')
            fclass = cols[2]
            if fclass == 'gene':
                gene_id, gene_type = extract_metadata(cols[8])
                gene_data[gene_id] = gene_type
            elif fclass == 'exon':
                gene_id, gene_type = extract_metadata(cols[8])
                if gene_id not in exon_data: exon_data[gene_id] = [] 
                val = (int(cols[3]), int(cols[4]))
                exon_data[gene_id].append(val) 
    return gene_data, exon_data 

def write_lengths(gene_data, exon_data, out_file):
    """Write the gene id, gene type, and aggregated length to a TSV file"""
    ofunc = get_open_function(out_file)
    with ofunc(out_file, 'wt') as o:
        o.write('gene_id\tgene_type\taggregate_length\n')
        for gene in sorted(exon_data):
            gtype = gene_data[gene]
            data = []
            for exon in exon_data[gene]:
                data.extend(range(exon[0], exon[1] + 1))
            o.write('{0}\t{1}\t{2}\n'.format(gene, gtype, len(set(data))))

def main(args):
    logger = get_logger('gene_lengths')
    logger.info("Extracting exons from GTF...") 
    gene_data, exon_data = load_gtf_data(args.gtf_file)

    logger.info("Calculating aggregated exon lengths and writing TSV...")
    write_lengths(gene_data, exon_data, args.out_file)
