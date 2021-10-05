import os 
import glob
import re

#base directory of the data files
basedir = os.path.expandvars("$PWD/data")

#identifier of the data kind etc (part of the prod_filename)
tag = "Tl208_NEW_v1_03_01_nexus_v5_03_04_"

#subdirectory where the files to be processed are located,
#it changes depending on the last city of the origin data
indir   = basedir + "/{in_city}_data/" 

#city of the origin data
in_city = "penthesilea" 

#cities to run
cities  = ["beersheba"] 

#number of jobs to launch (max is 200 so we leave a couple free)
queue_limit = 198

#directories of the Templates for the configs and job
jobTemp_dir    = os.path.expandvars("$PWD/templates/")
configTemp_dir = os.path.expandvars("$PWD/templates/")

#names of the in/out files, config and job templates. 
#In/out files are specific for the current task 
#(because the file names are weird), but the others can remain standard
prod_filename       = "{tag}cut{cut_num}.{city}_{num}.root.h5"
jobTemp_filename    = "jobTemplate.sh"
configTemp_filename = "{city}Template.conf"

#function to get the cut num and the num of each file (as Marija has named them)
#this is also specific for the current data, and may be changed later
def get_cut_and_num(filename):
	cut = filename.split("/")[-1].split("_")[-2].split(".")[0]
	num = filename.split("/")[-1].split("_")[-1].split(".")[0]
	match = re.match(r"([a-z]+)([0-9]+)", cut, re.I)
	if match:
		items = match.groups()
	cut_num = items[-1]
	return cut_num, num

##############
 INPUT FILES
##############

#takes all the .h5 files in the specified indir (which has the city of origin in it)
files_in = glob.glob(indir.format(in_city = in_city) + "/*.h5")

#maybe i should do a function to check that all the files in the last list 
#agree with the name structure :)

#sorts all the files, first in the cut number and then in the number
files_in = sorted(files_in, key = get_cut_and_num)

##############
 JOB LAUNCH
##############

#aqui cositas del job q hare luego
