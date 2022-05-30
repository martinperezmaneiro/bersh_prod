import os
import glob
import re

'''
DIRECTIONS:

-We should check that the basedir is already created with the structure
basedir/prod/input_city_name/all_input_data
This has to be mentioned here as we will usually have this folder in the $LUSTRE directory,
and the executables in the $HOME directory
-We should locate the input files in the previous directory
-The output folders will be created in the data folder
-The cities variable should contain the names of the origin city and the ones
that we want to obtain
-The directories of the templates should be also checked. We will usually locate them
in the same directory as the python executables, in a folder /templates/
This doesn't have to be like this, we can just specity the directory, but it is worth mention
-Regarding the particular name of the files to be processed, the variable prod_filename and
the functions get_cut_and_num and check_filename_structure should be renewed to fit it.
-REMEMBER to adapt the jobtime
'''

#base directory of the data files
#this will contain the input (data to be processed) and the output (the processed data,
#the configs and jobs, and the logs of the process). The folder prod will contain the
#folder named as the city with the input data, and the output cities' folders will be
#created
basedir = os.path.expandvars("$LUSTRE/NEW_0nubb_data")

#origin city followed by cities to run
cities  = ["beersheba", "isaura"]

#identifier of the data kind etc (part of the prod_filename)
#tag = "Tl208_NEW_v1_03_01_nexus_v5_03_04"
tag = "0nubb"

#number of jobs to launch (max is 200 so we leave a couple free)
queue_limit = 198

#database for the used detector
#the different classes can be found in invisible_cities/database/load_db
detector_db = 'new'

#directories of the Templates for the configs and job
jobTemp_dir    = os.path.expandvars("$PWD/templates/")
configTemp_dir = os.path.expandvars("$PWD/templates/")

#names of the in/out files, config and job templates.
#In/out files are specific for the current task
#(because the file names are weird), but the others can remain standard
#prod_filename       = "{tag}_cut{cutnum}.{city}_{num}.root.h5"
prod_filename       = "{city}_{cutnum}_{tag}.h5"
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
	else:
		cutnum = cut
	return cutnum, num

#function to ensure that all the files have the correct structure
#as the previous one, it is specific for the current data
def check_filename_structure(filename, prod_filename, tag):
    name_parts = filename.split("/")[-1].rsplit("_", 2)
    prod_parts = prod_filename.split("_")
    cutnum, num = get_cut_and_num(filename)

    assert len(name_parts)               == len(prod_parts)
    #assert name_parts[0]                 == tag
    #assert name_parts[1].split(".")[0]   == "cut" + str(cutnum)
    #assert name_parts[2]                 == str(num) + ".root.h5"
	assert name_parts[1]               == cutnum
	assert name_parts[2].split(".")[0] == tag

#function to check if a directory exists; if not, the function creates it
def checkmakedir(path):
	if os.path.isdir(path):
		print('hey, directory already exists!:\n' + path)
	else:
		os.makedirs(path)
		print('creating directory...\n' + path)

#function to create the output directories
def create_out_dirs():
        proddir = basedir + "/prod/"
        jobsdir = basedir + "/jobs/"
        confdir = basedir + "/config/"
        logsdir = basedir + "/logs/"
        checkmakedir(jobsdir)
        checkmakedir(confdir)
        checkmakedir(logsdir)
        for city in cities:
                checkmakedir(proddir + city)
        return proddir, jobsdir, confdir, logsdir

proddir, jobsdir, confdir, logsdir = create_out_dirs()

#This is the directory for the input files
indir = proddir + cities[0]

##############
# INPUT FILES
##############

#takes all the .h5 files in the specified indir (which
#has the city of origin in it)
files_in = glob.glob(indir + "/*.h5")

for f in files_in:
	check_filename_structure(f, prod_filename, tag)

#sorts all the files, first in the cut number and then in the number
files_in = sorted(files_in, key = get_cut_and_num)

##############
# JOB LAUNCH
##############

#commands for CESGA
queue_state_command = "squeue |grep usciempm |wc -l"
joblaunch_command   = "sbatch {filename}"
jobtime             = "1:00:00"
