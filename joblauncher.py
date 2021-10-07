import glob
import subprocess

from variables import queue_limit
from variables import jobsdir
from variables import get_cut_and_num
from variables import queue_state_command
from variables import joblaunch_command


jobs = glob.glob(jobsdir + "/*")
jobs = sorted(jobs, key = get_cut_and_num)

def check_jobs(cmd, nmin=10, wait=1):
    j = nmin
    while j>nmin-1:
        j = subprocess.run(cmd, shell=True, capture_output=True)
        j = int(j.stdout)
        sleep(wait)

############
# LAUNCHER
############


for job in jobs:

	check_jobs(queue_state_command, nmin = queue_limit)

	#launch job
	cmd = joblaunch_command.format(filename = job)
	print("Launching job", job)
	subprocess.run(cmd, shell = True)
