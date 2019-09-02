from subprocess import call
import json

initial_glucose = 140

with open("initial_file/glucose.json") as read_glucose:
	loaded_glucose = json.load(read_glucose)
	loaded_glucose[0]["bg"] = initial_glucose

with open("initial_file/glucose.json", "w") as write_glucose:
	json.dump(loaded_glucose, write_glucose, indent=4)	


call(["cp", "initial_file/glucose.json", "monitor/"])
call(["cp", "initial_file/pumphistory.json", "monitor/"])

to_glucosym = open('../glucosym/closed_loop_algorithm_samples/glucose_output_algo_bw.txt', 'w')
to_glucosym.write(str(initial_glucose))
