#!/usr/bin/env bash
#
# Export all environment variables
#$ -V
#
# Use current working directory
#$ -cwd
#
# Use bash as the executing shell
#$ -S /bin/bash
# 
# Set job name 
#$ -N j2015-01-10_14-08-49_echo_etal
# 
# Set task concurrency (max array jobs running simultaneously) 
#$ -tc 50
# 
# Set array job range (1 to number of commands in cmd file) 
#$ -t 1-4
# 
# Output files for stdout and stderr 
#$ -o j2015-01-10_14-08-49_echo_etal
#$ -e j2015-01-10_14-08-49_echo_etal
# 
# Set filelimit 
#$ -l h_fsize=500G
# 
# Set memory requested and max memory 
#$ -l mem_free=4G
#$ -l h_vmem=4G
# 
# Request some processors 
#$ -pe thread 1
# 
# Set path 
export PATH=/home/cgrb/oneils/local/bin/scripts/assemblyStats:/home/cgrb/oneils/local/bin/scripts:/home/cgrb/oneils/local/bin:/local/cluster/sge/bin/lx24-amd64:/bin:/local/cluster/jre1.6.0_23/bin:/home/cgrb/oneils/scripts:/home/cgrb/oneils/bin:/usr/bin:/local/cluster/bin:/usr/local/bin:/local/cluster/mpich/bin:/usr/local/share/ncbi/bin:/local/cluster/hdf5-1.8.13/hdf5/bin:/local/cluster/genome/bin:/local/cluster/RECON1.05/scripts:/local/cluster/MUMmer:/local/cluster/amos/bin:/local/cluster/velvet/velvet:/local/cluster/oases:/local/cluster/mira/bin:/local/cluster/abyss/bin:/local/cluster/cutadapt/bin:/local/cluster/edena2.1.1_linux64:/local/cluster/MAKER/bin:/local/cluster/mcl/bin:/local/cluster/YASRA/bin:/local/cluster/miRanda/bin:/local/cluster/ea-utils/bin:/local/cluster/RAxML/bin:/local/cluster/MOSAIK/bin:/local/cluster/hmmer/bin:/local/cluster/tmhmm/bin:/local/cluster/wgs/Linux-amd64/bin:/local/cluster/amber12/bin:/local/cluster/mpich2-1.2.1p1/bin:/usr/lib64/lam/bin:/local/cluster/mockler/bin:/local/cluster/carrington/bin:/local/cluster/variscan-2.0.3/bin/Linux-i386:/local/cluster/Roche/454/bin:/local/cluster/MaSuRCA/bin:/local/cluster/shore:/local/cluster/SHOREmap:/local/cluster/BEAST/bin:/local/cluster/BEDTools/bin:/local/cluster/genomemapper:/local/cluster/iprscan/bin:/local/cluster/trinityrnaseq:/local/cluster/Cerulean/bin:/local/cluster/Quake/bin:/local/cluster/glimmer/bin:/local/cluster/SPAdes-3.1.1-Linux/bin:/local/cluster/RAPSearch2.16_64bits/bin:/local/cluster/last-418/bin:/local/cluster/rnammer:/local/cluster/SHRiMP/bin:/local/cluster/homer/bin:/local/cluster/cd-hit:/local/cluster/augustus/bin:/local/cluster/ETA/bin:/local/cluster/structure_linux_console/bin:/local/cluster/stampy:/local/cluster/infernal/binaries:/local/cluster/rtax:/local/cluster/pandaseq/bin:/local/cluster/GARM:/local/cluster/AmpliconNoise/ampliconnoise/Scripts:/local/cluster/AmpliconNoise/ampliconnoise:/local/cluster/pplacer-v1.1:/local/cluster/microbiomeutil/WigeoN:/local/cluster/microbiomeutil/TreeChopper:/local/cluster/microbiomeutil/NAST-iEr:/local/cluster/microbiomeutil/ChimeraSlayer:/local/cluster/AmosCmp16Spipeline:/local/cluster/Tisean_3.0.0/bin:/local/cluster/allpathslg/bin:/local/cluster/NAMD:/local/cluster/vcf/bin:/local/cluster/iRODS/clients/icommands/bin:/local/cluster/SVMerge/bin:/local/cluster/pindel/bin:/local/cluster/breakdancer-1.1.2/bin:/local/cluster/cnD/bin:/local/cluster/nextclip/bin:/local/cluster/prokka-1.9/bin:/local/cluster/CEGMA_v2.5/bin:/local/cluster/julia-0.3.3/bin:/usr/X11R6/bin:/usr/X/bin:./:/raid1/home/cgrb/oneils/local/bin:/raid1/home/cgrb/oneils/local/bin/scripts:.
# 
echo "  Started on:           " `/bin/hostname -s` 
echo "  Started at:           " `/bin/date` 
# Run the command through time with memory and such reporting. 
# warning: there is an old bug in GNU time that overreports memory usage 
# by 4x; this is compensated for in the SGE_Plotdir script. 
/usr/bin/env time -f " \\tFull Command:                      %C \\n\\tMemory (kb):                       %M \\n\\t# SWAP  (freq):                    %W \\n\\t# Waits (freq):                    %w \\n\\tCPU (percent):                     %P \\n\\tTime (seconds):                    %e \\n\\tTime (hh:mm:ss.ms):                %E \\n\\tSystem CPU Time (seconds):         %S \\n\\tUser   CPU Time (seconds):         %U " \
sed "$SGE_TASK_ID q;d" j2015-01-10_14-08-49_echo_etal/commands.txt | bash -e 
echo "  Finished at:           " `date` 
