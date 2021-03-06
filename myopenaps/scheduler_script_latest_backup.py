from subprocess import call
import json
import datetime
#from datetime import datetime,timedelta
import time
import os


#Input to the algo_bw.js. algo_bw.js format all the info and send to glucosym server. An algorithm is running in glucosym server that calculated next glucose and send the value back.
algo_input_list = {"index":0,"BGTarget":120,"sens":45,"deltat_v":20,"dia":4,"dt":5.0,"time":1000,"bioavail":6.0,"Vg":253.0,"IRss":1.3,"events":{"bolus":[{ "amt": 0.0, "start":250}],"basal":[{ "amt":0, "start":50,"length":30}],"carb":[{"amt":0.0,"start":0,"length":0},{"amt":0.0,"start":0,"length":0}]}}

#write the algo_input_list to a file named algo_input.json so that algo_bw.js can read the input from that file
with open("../glucosym/closed_loop_algorithm_samples/algo_input.json", "w") as write_algo_input_init:
	json.dump(algo_input_list, write_algo_input_init, indent=4)
	write_algo_input_init.close()


suggested_data_to_dump = {}
list_suggested_data_to_dump = []

for _ in range(20):
	
	with open("monitor/glucose.json") as f:
		data = json.load(f)
		f.close()

	
	
	
	##For the very first time get the time of 5 minutes ago from now and set it to the first glucose data
	#if _==0:
	#	call("date -Ins -s $(date -Ins -d '-5 minute')", shell=True)
	#	data[0]["date"]=int(time.time())*1000
	#	print(data[0])
	#	print(data[0]["date"])
	#	with open("monitor/glucose.json", "w") as dump_first_glucose:
	#		json.dump(data[0], dump_first_glucose, indent=4)
	#		dump_first_glucose.close()	
	#	#print(data_to_prepend["date"])	
	


	call(["openaps", "report", "invoke", "monitor/iob.json"])
	
        #run openaps to get suggested tempbasal
	
	call(["openaps", "report", "invoke", "enact/suggested.json"])
	
	current_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S-07:00')
	
	#read the output in suggested.json and append it to list_suggested_data_to_dump list. Basically we are trying to get all the suggest	    ed data and dump make a list lf that and then dump it to all_suggested.json file		
	with open("enact/suggested.json") as read_suggested:
		loaded_suggested_data = json.load(read_suggested)
		list_suggested_data_to_dump.append(loaded_suggested_data)
		read_suggested.close()
	
	
	#Update pumphistory only if there is value of temp basal. For 0 temp basal, no need to update pumphistory
	if loaded_suggested_data['duration'] != 0:
	
		with open("monitor/pumphistory.json") as read_pump_history:
			loaded_pump_history = json.load(read_pump_history) # read whole pump_history.json
			pump_history_0 = loaded_pump_history[0].copy()	#load first element
			pump_history_1 = loaded_pump_history[1].copy() #load second element, fist and second are both for one temp basal
			pump_history_0['duration (min)'] = loaded_suggested_data['duration'] #update the values
			pump_history_1['rate'] = loaded_suggested_data['rate']
			pump_history_0['timestamp'] = current_timestamp
			pump_history_1['timestamp'] = current_timestamp
			
			loaded_pump_history.insert(0, pump_history_1) # insert second element back to whatever we loaded from pumphistory
			loaded_pump_history.insert(0, pump_history_0) #insert first element back to whatever we loaded from pumphistory
			
			read_pump_history.close();
	
		with open("monitor/pumphistory.json", "w") as write_pump_history:
			json.dump(loaded_pump_history, write_pump_history, indent=4)
			
	
	
	#print(suggested_data_to_dump)
	#write the list_suggested_data_to_dump into all_suggested.json file
	with open("enact/all_suggested.json", "w") as dump_suggested:
		json.dump(list_suggested_data_to_dump, dump_suggested, indent=4)
		dump_suggested.close()	


	#update the insulin parameter input of glucosym. This insulin parameters is received from openaps(suggested.json)
	algo_input_list["events"]['basal'][0]['amt'] = loaded_suggested_data['rate']
	algo_input_list["events"]['basal'][0]['length'] = loaded_suggested_data['duration']
	algo_input_list["events"]['basal'][0]['start'] = _*5
	
	
	
	#os.chdir("../glucosym/closed_loop_algorithm_samples")
	call(["node", "../glucosym/closed_loop_algorithm_samples/algo_bw.js"]);
	algo_input_list['index']=algo_input_list['index']+1

	#print(algo_input_list)

	with open("../glucosym/closed_loop_algorithm_samples/algo_input.json", "w") as write_algo_input:
		json.dump(algo_input_list, write_algo_input, indent=4)
	#os.chdir("../../myopenaps")

	
		
	data_to_prepend = data[0].copy()
	#current_time = data_to_prepend["display_time"]
	#mytime = datetime.strptime(current_time,"%Y-%m-%dT%H:%M:%S-07:00")
	#dt = timedelta(minutes = 5)
	#mytime += dt

	#make_time_str = str(mytime).split(' ')
	#new_time_str = make_time_str[0]+"T"+make_time_str[1]+"-07:00"

	#data_to_prepend["display_time"] = new_time_str
	#data_to_prepend["dateString"] = new_time_str

	#current_time = data_to_prepend["system_time"]
	#mytime = datetime.strptime(current_time,"%Y-%m-%dT%H:%M:%S-07:00")
	#dt = timedelta(minutes = 5)
	#mytime += dt

	#make_time_str = str(mytime).split(' ')
	#new_time_str = make_time_str[0]+"T"+make_time_str[1]+"-07:00"

	#data_to_prepend["system_time"] =  new_time_str

	read_glucose_from_glucosym = open("../glucosym/closed_loop_algorithm_samples/glucose_output_algo_bw.txt", "r")
	loaded_glucose = read_glucose_from_glucosym.read()

	#data_to_prepend["glucose"] = int(data_to_prepend["glucose"])-5
	data_to_prepend["glucose"] = loaded_glucose
	
	data_to_prepend["date"]+= 300000
	call("date -Ins -s $(date -Ins -d '+5 minute')", shell=True)	
	data.insert(0, data_to_prepend)
	

	with open('monitor/glucose.json', 'w') as outfile:
		json.dump(data, outfile, indent=4)
		outfile.close()
