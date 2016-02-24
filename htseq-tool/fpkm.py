import os
import numpy

def protein_coding(gtf, outdir):

    """
    gets names of protein coding genes from the annotation file
    """

    annotation = open(gtf, "r")

    #skip initial five lines of gtf which do not have gene informaiton
    for i in xrange(5):
        annotation.readline()

    protein_coding = set()

    for line in annotation:
        line = line.split("\t")
        elem_type = line[2] #checks whether element is exon/gene/CDS etc.
        start = line[3] #starting location of element on chromosome
        end = line[4] #ending location of element on chromosome

        if (elem_type == "gene"):
            gene_id = line[-1].split("\"")[1]
            if("gene_type \"protein_coding\"" in line[len(line) - 1]):
                protein_coding.add(gene_id)


    annotation.close()
    return protein_coding

def get_protein_coding_read_count(pcgenes, counts_file):

    """
    gets the counts of fragments mapped to protein coding genes by
    selecting the protein coding genes from the entire quantification data
    """

    read_count = dict()
    protein_coding_reads = 0

    rc = open(counts_file, "r")
    for line in rc:
        line = line.rstrip().split("\t")
        if len(line) == 2:
            gene_id = line[0]
            raw_count = int(line[1])
            read_count[gene_id] = raw_count

    for gene in pcgenes:
        if gene in read_count:
            protein_coding_reads += read_count[gene]

    rc.close()
    return protein_coding_reads, read_count

def get_gene_length(fname):
    """ get gene length from file """

    gene_length = dict()

    f = open(fname, "r")
    f.readline()

    for line in f:
        line = line.split("\t")
        gene_id = line[0]
        length = float(line[1])
        if gene_id in gene_length:
            raise Exception ("Entry for gene_id : %s already exists" % gene_id)
        gene_length[gene_id] = length

    return gene_length

def calculate_fpkm(all_read_count, pc_frag_count, all_gene_length, outdir, uuid, logger):

    """
    calculates the FPKM and FPKM-UQ
    """

    fpkm = open(os.path.join(outdir, "%s.FPKM.txt" %uuid), "w")
    fpkm_uq = open(os.path.join(outdir, "%s.FPKM-UQ.txt" %uuid), "w")


    #quantification results are assigned to five more categories
    #these are "no_feature", "ambiguous", "too_low_aQual", "not_aligned" and "alignment_not_unique"
    #thus the number of genes are the total number of entities in count minus five.

    if not (len(all_gene_length) == len(all_read_count) - 5):
        raise Exception ("Unequal length and counts of genes")

    all_reads = numpy.array(all_read_count.values())
    upper_quantile = numpy.percentile(all_reads, 75)

    for gene in all_gene_length:
        if not gene in all_read_count:
            raise Exception ("Read count for gene %s not found" %gene)

        C = all_read_count[gene]
        L = all_gene_length[gene]

        FPKM = (C * pow(10.0, 9))/ (pc_frag_count * L)
        fpkm.write("%s\t%s\n" %(gene, FPKM))

        if(upper_quantile == 0):
             logger.error("The upper quantile value for all reads or length of gene %s is zero. Assigning a very small value of 0.1^9" %gene)
             upper_quantile = pow(0.1, 9)

        if(L == 0):
            logger.error("The length of gene %s is zero. Assigning a very small value of 0.1^9" %gene)
            L = pow(0.1, 9)

        FPKM_UQ = (C * pow(10.0, 9)) / (upper_quantile * L)
        fpkm_uq.write("%s\t%s\n" %(gene, FPKM_UQ))

    fpkm.close()
    fpkm_uq.close()

def get_fpkm_files(counts_file, gtf, outdir, uuid, genelens, logger):

    pcgenes = protein_coding(gtf, outdir)
    gene_length = get_gene_length(genelens)
    pc_frag_count, read_count = get_protein_coding_read_count(pcgenes, counts_file)
    calculate_fpkm(read_count, pc_frag_count, gene_length, outdir, uuid, logger)

