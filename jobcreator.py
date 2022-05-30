import os
import glob

from variables import *

city_input = dict(zip(cities[1:], cities[:-1]))

filename_structure = "{dir}{city}/" + prod_filename #not bar between dir and city because dir already has the last /

if __name__ == "__main__":

	job_temp  = jobTemp_dir + jobTemp_filename
	job_file = open(job_temp).read() #opening the job template

	for f in files_in:
		cutnum, num   = get_cut_and_num(f)
		city_commands = ""

		#create job and config
		for i, city in enumerate(cities):
			if i != 0:
				#check if the job already exists
				job = jobsdir + city + "_cut{cutnum}_{num}.job".format(cutnum = cutnum, num = num)

				if os.path.exists(job):
					continue

				file_in  = filename_structure.format(
							dir    = proddir,
							city   = city_input[city],
							tag    = tag,
							cutnum = cutnum,
							num    = num)
				file_out = filename_structure.format(
							dir    = proddir,
							city   = city,
							tag    = tag,
							cutnum = cutnum,
							num    = num)

				config_temp = configTemp_dir + configTemp_filename.format(city = city)
				config_file = open(config_temp).read() #opening the config template
				config = confdir + city + "_cut{cutnum}_{num}.conf".format(cutnum = cutnum, num = num)
				with open(config, "w") as config_write:
					config_write.write(config_file.format(file_in  = file_in, file_out = file_out, detector_db = detector_db))

				city_commands += "city {city_name} {config_directory} \n".format(city_name = city, config_directory = config)

		with open(job, "w") as job_write:
			job_write.write(job_file.format(
                                                jobtime     = jobtime,
						jobname     = city + "_cut{cutnum}_{num}".format(cutnum = cutnum, num = num),
						logfilename = logsdir + city + "_cut{cutnum}_{num}.log".format(cutnum = cutnum, num = num),
						errfilename = logsdir + city + "_cut{cutnum}_{num}.err".format(cutnum = cutnum, num = num),
						cities      = city_commands))
