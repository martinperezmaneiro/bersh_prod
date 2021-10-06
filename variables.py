import os 
import glob
import re

#base directory of the data files
basedir = os.path.expandvars("$PWD/data")

#directory of the output files (the production, config and jobs,
#and the logs of the process
out_dir = basedir +  "/output_files"

#identifier of the data kind etc (part of the prod_filename)
tag = "Tl208_NEW_v1_03_01_nexus_v5_03_04"

#subdirectory where the files to be processed are located,
#it changes depending on the last city of the origin data
indir   = basedir + "/{in_city}_data/" 
 

#origin city followed by cities to run
#as Marija data is identified by "cdst", I will call esmeralda data as this
#and the script will produce the same name structure changing cdst for beersheba
cities  = ["cdst", "beersheba"] 

#number of jobs to launch (max is 200 so we leave a couple free)
queue_limit = 198

#directories of the Templates for the configs and job
jobTemp_dir    = os.path.expandvars("$PWD/templates/")
configTemp_dir = os.path.expandvars("$PWD/templates/")

#names of the in/out files, config and job templates. 
#In/out files are specific for the current task 
#(because the file names are weird), but the others can remain standard
prod_filename       = "{tag}_cut{cutnum}.{city}_{num}.root.h5"
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
	cutnum = items[-1]
	return cutnum, num

#function to ensure that all the files have the correct structure
#as the previous one, it is specific for the current data
def check_filename_structure(filename):
    name_parts = filename.split("/")[-1].rsplit("_", 2)
    prod_parts = prod_filename.split("_")
    cutnum, num = get_cut_and_num(filename)
    
    assert len(name_parts) == len(prod_parts)
    assert name_parts[0] == tag
    assert name_parts[1] == "cut" + str(cutnum) + ".cdst"
    assert name_parts[2] == str(num) + ".root.h5" 

#function to check if a directory exists; if not, the function creates it
def checkmakedir(path):
	if os.path.isdir(path):
		print('hey, directory already exists!:\n' + path)
	else:
		os.makedirs(path)
		print('creating directory...\n' + path)

##############
# INPUT FILES
##############

#takes all the .h5 files in the specified indir (which 
#has the city of origin in it)
files_in = glob.glob(indir.format(in_city = cities[1]) + "/*.h5")

for f in files_in: 
	check_filename_structure(f)

#sorts all the files, first in the cut number and then in the number
files_in = sorted(files_in, key = get_cut_and_num)

##############
# JOB LAUNCH
##############

#aqui cositas del job q hare luego
