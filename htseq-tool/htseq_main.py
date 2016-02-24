import logging
import os
import setupLog
import htseq
import argparse
import pipelineUtil
import fpkm
from cdis_pipe_utils import postgres

class Htseq(postgres.ToolTypeMixin, postgres.Base):

    __tablename__ = 'htseq_metrics'


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Raw counts using HT-seq")
    required = parser.add_argument_group("Required input paramters")
    required.add_argument("--bam", default=None, help="path to BAM file", required=True)
    required.add_argument("--case_id", default='unknown', help="gdc case id", required=True)
    required.add_argument("--gdc_id", default='unknown', help="gdc id for bam file", required=True)
    required.add_argument("--genome_annotation", default=None, help="path to annotation file", required=True)
    required.add_argument("--outdir", default="./", help="path to output directory")

    optional = parser.add_argument_group("optional input parameters")
    optional.add_argument("--id", default="unknown", help="unique identifer")
    optional.add_argument("--strand", default="no", help="strand specificity of experimental library")
    optional.add_argument("--gene_lengths", default="/home/ubuntu/bin/htseq-tool/expression_normalization/gene_length.txt", help="file for gene lengths")

    database = parser.add_argument_group("database paramters")
    database.add_argument("--record_metrics", default=0, help="record metrics for runs")
    database.add_argument("--drivername", default="postgres", help="drivername for database")
    database.add_argument("--host", default="pgreadwrite.osdc.io", help="hostname for database")
    database.add_argument("--port", default="5432", help="port number for connection")
    database.add_argument("--username", default=None, help="username for connection")
    database.add_argument("--password", default=None, help="password for connection")
    database.add_argument("--database", default="prod_bioinfo", help="name of database")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    log_file = "%s.htseq.log" % os.path.join(args.outdir, args.id)
    logger = setupLog.setup_logging(logging.INFO, args.id, log_file)

    bam = args.bam
    if not os.path.isfile(args.bam):
        raise Exception("Cannot find bam file %s. Please check that the file exists and is in the correct path" %bam)

    #get htseq counts
    metrics, out_file_name = htseq.htseq_count(bam, args.id, args.genome_annotation, args.outdir, logger, args.strand)

    if not metrics['exit_status']:

        if int(args.record_metrics):

            database = {
                    'drivername':args.drivername,
                    'host': args.host,
                    'port': args.port,
                    'username' : args.username,
                    'password' : args.password,
                    'database' : args.database
            }

            engine = postgres.db_connect(database)

            met = Htseq(case_id = args.case_id,
                        tool = 'htseq',
                        files = [args.gdc_id],
                        systime = metrics['system_time'],
                        usertime =  metrics['user_time'],
                        elapsed = metrics['wall_clock'],
                        cpu = metrics['percent_of_cpu'],
                        max_resident_time = metrics['maximum_resident_set_size'])

            postgres.create_table(engine, met)
            postgres.add_metrics(engine, met)


        fpkm.get_fpkm_files(out_file_name, args.genome_annotation, args.outdir, args.id, args.gene_lengths, logger)

