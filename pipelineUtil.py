import os
import sys
import subprocess
import logging
import time
import shutil

def retrieve_data(analysis_id, cghub_key, output_dir, logger=None):
    if not os.path.isdir(os.path.join(output_dir, analysis_id)):

        cmd = ['gtdownload', '-v', '-c', cghub_key, '-p', output_dir, analysis_id]
        run_command(cmd, logger)

        #os.system("gtdownload -v -c %s -p %s %s" %(cghub_key, output_dir, analysis_id))

def run_command(cmd, logger=None, shell_var=False):
    """ Run a subprocess command """

    #stdoutdata, stderrdata = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell_var)
    stdoutdata, stderrdata = child.communicate()
    exit_code = child.returncode

    #print stdoutdata, stderrdata
    if logger != None:
        logger.info(cmd)
        stdoutdata = stdoutdata.split("\n")
        for line in stdoutdata:
            logger.info(line)

        stderrdata = stderrdata.split("\n")
        for line in stderrdata:
            logger.info(line)

    return exit_code

def log_function_time(fn, analysis_id, cmd, logger=None, shell_var=False):
    """ Log the time taken by a command to the logger """

    start_time = time.time()
    exit_code = run_command(cmd, logger, shell_var)
    end_time = time.time()

    if logger != None:
        logger.info("%s_TIME\t%s\t%s" %(fn, analysis_id,  (end_time - start_time)/60.0))

    print "exit_code for %s is %s" %(cmd, exit_code)
    return exit_code

def download_from_cleversafe(logger, remote_input, local_output, config="/home/ubuntu/.s3cfg"):
    """ Download a file from cleversafe to a local folder """

    if (remote_input != ""):
        cmd = ['s3cmd', '-c', config, 'sync', remote_input, local_output]
        run_command(cmd, logger)
    else:
        raise Exception("invalid input %s" % remote_input)

def upload_to_cleversafe(logger, remote_output, local_input, config="/home/ubuntu/.s3cfg"):
    """ Upload a file to cleversafe to a folder """

    if (remote_output != "" and (os.path.isfile(local_input) or os.path.isdir(local_input))):
        cmd = ['s3cmd', '-c', config, 'sync', local_input, remote_output]
        run_command(cmd, logger)
    else:
        raise Exception("invalid input %s or output %s" %(local_input, remote_output))


def remove_dir(dirname):
    """ Remove a directory and all it's contents """

    if os.path.isdir(dirname):
        for filename in os.listdir(dirname):
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                os.remove(filename)
            else:
                shutil.rmtree(filename)
        assert(os.listdir(dirname) == [])
        os.rmdir(dirname)
    else:
        raise Exception("Invalid directory: %s" % dirname)
