import os
import glob

from variables import *

city_input = dict(zip(cities[1:], cities[:-1]))

filename_structure = "{dir}/{city}/" + prod_filename

if __name__ == "__main__":
	
	job_temp  = jobTemp_dir + jobTemp_filename
	job_file = open(job_temp).read() #opening the job template
	
	for f in files_in:
		cutnum, num   = get_cut_and_num(f)
		city_commands = ""
		
		#check if the job already exists
		job = jobsdir + f"cut{cutnum}_{num}.job"
		if os.path.exists(job):
			continue

		#create job and config
		for i, city in enumerate(cities):
			if i != 0:
				file_in  = filename_structure.format(
							dir    = proddir,
							city   = city_input[city],
							tag    = tag,
							cutnum = cutnum,
							num    = num)
				file_out = filename_structure.format(
							dir    = proddir,
							city   = city
							tag    = tag,
							cutnum = cutnum,
							num    = num)

				config_temp = configTemp_dir + configTemp_filename.format(city = city)
				config_file = open(config_temp).read() #opening the config template
				config = confdir + city + f"_cut{cutnum}_{num}.conf"
				with open(config, "w") as config_write:
					config_write.write(config_file.format(
									file_in  = file_in,
									file_out = file_out)
				city_commands += f"city {city} {config}\n"

				with open(job, "w") as job_write:
					job_write.write(job_file.format(
								jobname     = f"cut{cutnum}_{num}"
								logfilename = f"cut{cutnum}_{num}.log"
								errfilename = f"cut{cutnum}_{num}.err"
								cities      = city_commands)

