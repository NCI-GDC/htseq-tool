import os
import subprocess
import signal
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def htseq_count(bam, analysis_id, annotation, outdir, logger, strand="no"):
    """ Get raw counts using HTseq """

    if os.path.isfile(bam) and os.path.isfile(annotation):

        if not(strand=="yes" or strand=="no" or strand=="reverse"):
            raise Exception("Strand can only take three values: yes, no and reverse")

        outfilename = os.path.join(outdir, "%s.htseq.counts" %analysis_id)
        cmd = 'samtools view -F 4 %s | htseq-count -m intersection-nonempty --idattr gene_id -r pos --stranded %s - %s  > %s' %(bam, strand, annotation, outfilename)

        output = pipe_util.do_shell_command(cmd, logger)
        metrics = time_util.parse_time(output)
        return (metrics, outfilename)

    else:
        error_msg = "Invalid BAM file %s or annotation file %s. Please check the file exists and the path is correct." %(bam, annotation)
        logger.error(error_msg)
        raise Exception(error_msg)

