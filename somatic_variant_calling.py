#functions for somatic variant calling WGS

import sys
import subprocess
import os
import argparse
import time
import socket
import shutil

###############################################################################
# Helper function to run commands, handle return values and print to log file
def runCMD(cmd):
    val = subprocess.Popen(cmd, shell=True).wait()
    if val == 0:
        pass
    else:
        print('command failed')
        print(cmd)
        sys.exit(1)
###############################################################################
def run_strelka2(myData, run=True):
    # Run Strelka2, only option is to not run the program, use in reset mode
    s = 'Starting Strelka2'
    print(s, flush=True)
    myData['logFile'].write('\n' + s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')

    myData['logFile'].flush()

    strelka_dir = myData['tmpDir'] + myData['sampleName']
    
    if os.path.isdir(strelka_dir) is True:
        s = '%s exists!' % strelka_dir
        print(s, flush=True)
        myData['logFile'].write(s + '\n')
    else:
        cmd = 'mkdir %s' % strelka_dir
        myData['logFile'].write(cmd + '\n')
        runCMD(cmd)

    strelka_cmd = '/strelka-2.9.10.centos6_x86_64/bin/configureStrelkaSomaticWorkflow.py --normalBam %s --tumorBam %s --referenceFasta %s --runDir %s' % (
        myData['normalBam'], myData['tumorBam'], myData['referenceFasta'], strelka_dir)

    if run is True:
        print(strelka_cmd)
        myData['logFile'].write(strelka_cmd + '\n')
        myData['logFile'].flush()
        runCMD(strelka_cmd)

        run_workflow_cmd = '%s/runWorkflow.py -m local -j %i' % (strelka_dir, myData['threads'])
        print(run_workflow_cmd)
        myData['logFile'].write(run_workflow_cmd + '\n')
        myData['logFile'].flush()
        runCMD(run_workflow_cmd)

        mv_snvs_cmd = 'mv %s/results/variants/somatic.snvs.vcf.gz %s.strelka.somatic.snvs.vcf.gz' % (strelka_dir, myData['sampleName'])
        mv_indels_cmd = 'mv %s/results/variants/somatic.indels.vcf.gz %s.strelka.somatic.indels.vcf.gz' % (strelka_dir, myData['sampleName'])

        print(mv_snvs_cmd)
        print(mv_indels_cmd)
        myData['logFile'].write(mv_snvs_cmd + '\n')
        myData['logFile'].write(mv_indels_cmd + '\n')
        myData['logFile'].flush()

        runCMD(mv_snvs_cmd)
        runCMD(mv_indels_cmd)

    else:
        s = 'skipping run_strelka2'
        print(s, flush=True)
        myData['logFile'].write(s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()
############################################################################# 
def run_mutect(myData, run=True):
    s = 'Starting Mutect2'
    print(s, flush=True)
    myData['logFile'].write('\n' + s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')

    myData['logFile'].flush()

    cmd = "gatk Mutect2 --verbosity ERROR --callable-depth {RDP} --minimum-allele-fraction {VAF} --min-base-quality-score {Qual} -R {Reference} -I {sample} -O {output} --native-pair-hmm-threads 9 -L {bed} --QUIET {max_mnp_distance}".format(
        RDP=myData['RDP'],
        VAF=myData['VAF'],
        Qual=myData['Qual'],
        Reference=myData['Reference'],
        sample=myData['sample'],
        output=myData['output'],
        bed=myData['bed'],
        max_mnp_distance=myData['max_mnp_distance']
    )

    if run is True:
        print(cmd)
        myData['logFile'].write(cmd + '\n')
        myData['logFile'].flush()
        runCMD(cmd)
    else:
        s = 'skipping run_mutect'
        print(s, flush=True)
        myData['logFile'].write(s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()
############################################################################# 
def run_filter_mutect(myData, run=True):
    s = 'Starting FilterMutectCalls'
    print(s, flush=True)
    myData['logFile'].write('\n' + s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')

    myData['logFile'].flush()

    cmd = "gatk FilterMutectCalls --verbosity ERROR --min-allele-fraction {VAF} -R {Reference} -V {sample} -O {output} --QUIET".format(
        VAF=myData['VAF'],
        Reference=myData['Reference'],
        sample=myData['sample'],
        output=myData['output']
    )

    if run is True:
        print(cmd)
        myData['logFile'].write(cmd + '\n')
        myData['logFile'].flush()
        runCMD(cmd)
    else:
        s = 'skipping run_filter_mutect'
        print(s, flush=True)
        myData['logFile'].write(s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()
#############################################################################     
    def run_vardict(myData, run=True):
    s = 'Starting VarDict'
    print(s, flush=True)
    myData['logFile'].write('\n' + s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')

    myData['logFile'].flush()

    cmd = "~/.conda/pkgs/vardict-java-1.8.2-hdfd78af_3/bin/vardict-java -f {VAF} -th 9 -G {Reference} -b {sample} -q {Qual} -c 1 -S 2 -E 3 {bed} > {output}".format(
        VAF=myData['VAF'],
        Reference=myData['Reference'],
        sample=myData['sample'],
        Qual=myData['Qual'],
        bed=myData['bed'],
        output=myData['output']
    )

    if run is True:
        print(cmd)
        myData['logFile'].write(cmd + '\n')
        myData['logFile'].flush()
        runCMD(cmd)
    else:
        s = 'skipping run_vardict'
        print(s, flush=True)
        myData['logFile'].write(s + '\n')

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()
