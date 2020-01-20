# GDC Base Template
![Version badge](https://img.shields.io/badge/htslib-1.8-<COLOR>.svg)
![Version badge](https://img.shields.io/badge/samtools-1.8-<COLOR>.svg)
![Version badge](https://img.shields.io/badge/HTSeq-0.6.1p1-<COLOR>.svg)

Contains dockerfile and HTSeq utility tools for running the GDC HTSeq
expression quantification workflows. See https://github.com/NCI-GDC/htseq-cwl
for more information about the GDC workflow associated with this.

## Usage

### `gene_lengths`

Generate the gene exon lengths from GTF for use in normalization.

```
usage: htseq-tools gene_lengths [-h] --gtf_file GTF_FILE --out_file OUT_FILE

Extract gene exon lengths from GTF

optional arguments:
  -h, --help           show this help message and exit
  --gtf_file GTF_FILE  GTF file used for htseq count
  --out_file OUT_FILE  Output TSV file to write to
```

### `merge_counts`

When an aliquot has a mixture of paired- and single-end, this will
merge the counts to a single file.

```
usage: htseq-tools merge_counts [-h] --htseq_counts HTSEQ_COUNTS --out_file
                                OUT_FILE

Merge PE and SE counts from HTseq

optional arguments:
  -h, --help            show this help message and exit
  --htseq_counts HTSEQ_COUNTS
                        HTSeq count file. Use multiple times
  --out_file OUT_FILE   Output TSV file to write to
```

### `fpkm`

Normalize the raw counts using the FPKM and FPKM-UQ methods.

```
usage: htseq-tools fpkm [-h] --aggregate_length_file AGGREGATE_LENGTH_FILE
                        --htseq_counts HTSEQ_COUNTS --output_prefix
                        OUTPUT_PREFIX

Get FPKM and FPKM-UQ

optional arguments:
  -h, --help            show this help message and exit
  --aggregate_length_file AGGREGATE_LENGTH_FILE
                        Aggregate length TSV
  --htseq_counts HTSEQ_COUNTS
                        HTSeq counts txt file
  --output_prefix OUTPUT_PREFIX
                        The output prefix to use.
```
