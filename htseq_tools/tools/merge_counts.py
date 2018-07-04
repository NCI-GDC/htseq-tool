"""Module to merge SE and PE counts from htseq into 
a single file.
"""
from collections import OrderedDict

from htseq_tools.utils import get_logger, get_open_function

def merge_files(input_files, output_path, logger):
    """
    Performs the merging across N (usually 1 PE and 1 SE)
    htseq counts files. When only 1 is provided no changes are made;
    however, we use this as a tool to also gzip all outputs.
    """
    wfunc = get_open_function(output_path)
    with wfunc(output_path, 'wt') as o:
        if len(input_files) > 1:
            logger.info("Multiple files provided, will sum counts")
            dic = OrderedDict()
            for fil in input_files:
                logger.info("Processing {0}".format(fil))
                rfunc = get_open_function(fil)
                for line in rfunc(fil, 'rt'):
                    gid, counts = line.rstrip('\r\n').split('\t') 
                    if gid not in dic:
                        dic[gid] = 0 
                    dic[gid] += int(counts)

            # Write
            for key in dic:
                row = [key, str(dic[key])]
                o.write('\t'.join(row) + '\n')

        else:
            logger.info("Single input provided, no changes will be made")
            fil = input_files[0]
            rfunc = get_open_function(fil)
            for line in rfunc(fil, 'rt'):
                o.write(line)

def main(args):
    logger = get_logger('merge_counts')
    logger.info("Processing count files...") 
    merge_files(args.htseq_counts, args.out_file, logger) 
