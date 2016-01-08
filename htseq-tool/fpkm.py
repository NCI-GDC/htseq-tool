import os
import numpy

def protein_coding(gtf, outdir):

    """
    gets the protein coding genes from the annotation file
    and the gene length of all the genes.
    """

    annotation = open(gtf, "r")

    #skip initial five lines of gtf which do not have gene informaiton
    for i in xrange(5):
        annotation.readline()

    count = 0
    gene_length = dict()
    protein_coding = set()

    for line in annotation:
        line = line.split("\t")
        elem_type = line[2] #checks whether element is exon/gene/CDS etc.
        start = line[3] #starting location of element on chromosome
        end = line[4] #ending location of element on chromosome

        if (elem_type == "gene"):
            chunks = line[-1].split("\"")
            assert("gene_id" in chunks[0])
            gene_id = chunks[1]
            if("gene_type \"protein_coding\"" in line[-1]):
                protein_coding.add(gene_id)
                count += 1
            length = int(end) - int(start) + 1
            gene_length[gene_id] = length
            #gl_handle.write("%s\t%s\n" %(gene_id, length))


    annotation.close()
    return(count, protein_coding, gene_length)

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
        gene_id = line[0]
        raw_count = int(line[1])
        read_count[gene_id] = raw_count

    for gene in pcgenes:
        if gene in read_count:
            protein_coding_reads += read_count[gene]

    rc.close()
    return protein_coding_reads, read_count

def calculate_fpkm(all_read_count, pc_frag_count, all_gene_length, outdir, uuid):

    """
    calculates the FPKM and FPKM-UQ
    """

    fpkm = open(os.path.join(outdir, "%s.FPKM.txt" %uuid), "w")
    fpkm_uq = open(os.path.join(outdir, "%s.FPKM-UQ.txt" %uuid), "w")

    #print len(all_gene_length)
    #print len(all_read_count)

    #quantification results are assigned to five more categories
    #these are "no_feature", "ambiguous", "too_low_aQual", "not_aligned" and "alignment_not_unique"
    #thus the number of genes are the total number of entities in count minus five.

    if not (len(all_gene_length) == len(all_read_count) - 5):
        raise Exception ("Unequal length and counts of genes")

    all_reads = numpy.array(all_read_count.values())
    upper_quantile = numpy.percentile(all_reads, 75)
    #print upper_quantile

    for gene in all_gene_length:
        if not gene in all_read_count:
            raise Exception ("Read count for gene %s not found" %gene)

        C = all_read_count[gene]
        L = all_gene_length[gene]

        FPKM = (C * pow(10.0, 9))/ (pc_frag_count * L)
        fpkm.write("%s\t%s\n" %(gene, FPKM))

        FPKM_UQ = (C * pow(10.0, 9)) / (upper_quantile * L)
        fpkm_uq.write("%s\t%s\n" %(gene, FPKM_UQ))

    fpkm.close()
    fpkm_uq.close()

def get_fpkm_files(counts_file, gtf, outdir, uuid):

    gene_count, pcgenes, gene_length = protein_coding(gtf, outdir)
    frag_count, read_count = get_protein_coding_read_count(pcgenes, counts_file)
    calculate_fpkm(read_count, frag_count, gene_length, outdir, uuid)

