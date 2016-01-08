import logging
import os
import setupLog
import htseq
import argparse
import pipelineUtil
import fpkm

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Raw counts using HT-seq")
    required = parser.add_argument_group("Required input paramters")
    required.add_argument("--bam", default=None, help="path to BAM file", required=True)
    required.add_argument("--genome_annotation", default=None, help="path to annotation file", required=True)
    required.add_argument("--outdir", default="./", help="path to output directory")

    optional = parser.add_argument_group("optional input parameters")
    optional.add_argument("--id", default="unknown", help="unique identifer")
    #optional.add_argument("--tobucket", default="s3://bioinformatics_scratch/")
    #optional.add_argument("--s3cfg", default="/home/ubuntu/.s3cfg")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    log_file = "%s.htseq.log" % os.path.join(args.outdir, args.id)
    logger = setupLog.setup_logging(logging.INFO, args.id, log_file)

    #download from object store if not a local path
    bam = args.bam
    if not os.path.isfile(args.bam):
        raise Exception("Cannot find bam file %s. Please check that the file exists and is in the correct path" %bam)
        #logger.info("Downloading %s" %args.id)
        #pipelineUtil.download_from_cleversafe(logger, args.bam, args.outdir, args.s3cfg)
        #bam = os.path.join(args.outdir, os.path.basename(args.bam))


    #get htseq counts
    exit_code, out_file_name = htseq.htseq_count(bam, args.id, args.genome_annotation, args.outdir, logger)
    #upload results to object store
    if not exit_code:
	    #pipelineUtil.upload_to_cleversafe(logger, os.path.join(args.tobucket, "htseq-counts/"),
        #                                  out_file_name, args.s3cfg)

       	#pipelineUtil.upload_to_cleversafe(logger, os.path.join(args.tobucket, "htseq-logs/"),
        #                                 log_file, args.s3cfg)

        fpkm_file, fpkm_uq_file = fpkm.get_fpkm_files(out_file_name, args.genome_annotation, args.outdir, args.id)

       	#pipelineUtil.upload_to_cleversafe(logger, os.path.join(args.tobucket, "htseq-fpkm/"),
        #                                 fpkm_file, args.s3cfg)

       	#pipelineUtil.upload_to_cleversafe(logger, os.path.join(args.tobucket, "htseq-fpkm-uq/"),
        #                                 fpkm_uq_file, args.s3cfg)
        #os.remove(out_file_name)
        #os.remove(log_file)
        #os.remove(fpkm_file)
        #os.remove(fpkm_uq_file)

    #remove files from local drive
    #os.remove(bam)
    #os.remove(out_file_name)
    #os.remove(log_file)
    #if os.listdir(args.outdir) == []:
    #    os.rmdir(args.outdir)
