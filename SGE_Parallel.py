#!/usr/bin/env python2.7
import sys
import io
import re
import argparse
import datetime
import os
import subprocess
import shutil
import time
import textwrap

### Input parsing. Returns an environment with members like args.queue, args.commands, args.filelimit, etc. 
def parse_input():
	
	parser = argparse.ArgumentParser(description='Runs a list of commands specified on stdin as an SGE array job. \nExample usage: cat commands.txt | SGE_Parallel')
	parser.add_argument('-c', '--commandsfile', required = False, dest = "commandsfile", default = "-", help = "The file to read commands from. Default: -, meaning standard input.")
	parser.add_argument('-q', '--queue', required = False, dest = "queue", help = "The queue(s) to send the commands to. Default: all queues you have access to.")
	parser.add_argument('-m', '--memory', required = False, dest = "memory", default = "4G", help = "Amount of free RAM to request for each command, and the maximum that each can use without being killed. Default: 4G")
	parser.add_argument('-f', '--filelimit', required = False, dest = "filelimit", default = "500G", help = "The largest file a command can create without being killed. (Preserves fileservers.) Default: 500G")
	parser.add_argument('-b', '--concurrency', required = False, dest = "concurrency", default = "50", help = "Maximum number of commands that can be run simultaneously across any number of machines. (Preserves network resources.) Default: 50")
	parser.add_argument('-P', '--processors', required = False, dest = "processors", default = "1", help = "Number of processors to reserve for each command. Default: 1")
	parser.add_argument('-r', '--rundir', required = False, dest = "rundir", help = "Job name and the directory to create or OVERWRITE to store log information and standard output of the commands. Default: 'jYEAR-MON-DAY_HOUR-MIN-SEC_<cmd>_etal' where <cmd> is the first word of the first command.")
	parser.add_argument('-p', '--path', required = False, dest = "path", help = "What to use as the PATH for the commands. Default: whatever is output by echo $PATH.")
	parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s 0.6')
	parser.add_argument('--showchangelog', required = False, action = 'store_true', dest = "showchangelog", help = "Show the changelog for this program.")

	changelog = textwrap.dedent('''\
		Version 0.6: Initial version. Reads commands on stdin or from a file, runs them as an array job.
		''')

	## Parse the arguments
	args = parser.parse_args()
	
	if args.showchangelog:
		print(changelog)
		quit()

	## Read the commands on standard input, showing an error if there is no stdin
	cmds = None
	if args.commandsfile == "-":
		if sys.stdin.isatty():
			print(parser.format_help())
			quit()
		cmds = sys.stdin.read().strip().split('\n')
	else:
		cmdsh = io.open(args.commandsfile, "rb")
		cmds = cmdsh.read().strip().split('\n')

	args.commands = cmds

	## Set the rundir and path if not already set
	if args.rundir == None:
		rundir = datetime.datetime.now().strftime("j%Y-%m-%d_%H-%M-%S_" + re.split("\s+", cmds[0])[0] + "_etal")
		args.rundir = rundir
	if args.path == None:
		args.path = os.environ['PATH']	

	return args




########## make dir
def make_rundir(rundir):
	if not os.path.exists(rundir):
		os.makedirs(rundir)
	else:
		print("WARNING: deleting logdir '" + rundir + "' and recreating it in:")
		for i in [" 3..", " 2..", " 1.."]:
			print(i)
			time.sleep(2)
		shutil.rmtree(rundir)
		os.makedirs(rundir)


########## write commands.txt
def write_commands(cmds, rundir):
	commandsh = io.open(rundir + "/commands.txt", "wb")
	for cmd in cmds:
		commandsh.write(cmd + "\n")
	commandsh.close()



########## write the qsub script to args.rundir/args.rundir.sh
def write_qsub(args):
	scripth = io.open(args.rundir + "/" + args.rundir + ".sh", "wb")

	scripth.write(textwrap.dedent('''\
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
		# \n'''))
	scripth.write("# Set job name \n")
	scripth.write("#$ -N " + str(args.rundir) + "\n")
	scripth.write("# \n")

	scripth.write("# Set task concurrency (max array jobs running simultaneously) \n")
	scripth.write("#$ -tc " + str(args.concurrency) + "\n")
	scripth.write("# \n")
	
	scripth.write("# Set array job range (1 to number of commands in cmd file) \n")
	scripth.write("#$ -t 1-" + str(len(args.commands)) + "\n")
	scripth.write("# \n")

	scripth.write("# Output files for stdout and stderr \n")
	scripth.write("#$ -o " + args.rundir + "\n")
	scripth.write("#$ -e " + args.rundir + "\n")
	scripth.write("# \n")

	if args.queue != None:
		scripth.write("# Set queues to use \n")
		scripth.write("#$ -1 " + str(args.queue) + "\n")
		scripth.write("# \n")

	scripth.write("# Set filelimit \n")
	scripth.write("#$ -l h_fsize=" + str(args.filelimit) + "\n")
	scripth.write("# \n")
	
	scripth.write("# Set memory requested and max memory \n")
	scripth.write("#$ -l mem_free=" + str(args.memory) + "\n")
	scripth.write("#$ -l h_vmem=" + str(args.memory) + "\n")
	scripth.write("# \n")
	
	scripth.write("# Request some processors \n")
	scripth.write("#$ -pe thread " + str(args.processors) + "\n")
	scripth.write("# \n")
	
	scripth.write("# Set path \n")
	scripth.write("export PATH=" + str(args.path) + "\n")
	
	scripth.write("# \n")
	scripth.write("echo \"  Started on:           \" `/bin/hostname -s` \n")
	scripth.write("echo \"  Started at:           \" `/bin/date` \n")

	scripth.write("# Run the command through time with memory and such reporting. \n")
	scripth.write("# warning: there is an old bug in GNU time that overreports memory usage \n")
	scripth.write("# by 4x; this is compensated for in the SGE_Plotdir script. \n")
	scripth.write("/usr/bin/time -f \" \\\\tFull Command:                      %C \\\\n\\\\tMemory (kb):                       %M \\\\n\\\\t# SWAP  (freq):                    %W \\\\n\\\\t# Waits (freq):                    %w \\\\n\\\\tCPU (percent):                     %P \\\\n\\\\tTime (seconds):                    %e \\\\n\\\\tTime (hh:mm:ss.ms):                %E \\\\n\\\\tSystem CPU Time (seconds):         %S \\\\n\\\\tUser   CPU Time (seconds):         %U \" \\ \n")
	scripth.write("sed \"$SGE_TASK_ID q;d\" " + args.rundir + "/commands.txt | bash -e \n")
	scripth.write("echo \"  Finished at:           \" `date` \n")
	
	scripth.close()


## executes qsub args.rundir/args.rundir.sh
def exec_qsub(args):
	res = subprocess.check_output("qsub '" + args.rundir + "/" + args.rundir + ".sh'", stderr=subprocess.STDOUT, shell = True)
	print(res)

args = parse_input()
make_rundir(args.rundir)
write_commands(args.commands, args.rundir)
write_qsub(args)
exec_qsub(args)


