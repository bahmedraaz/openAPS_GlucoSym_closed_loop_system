import sys
from subprocess import call
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##########################################################
initial_glucose = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]
#initial_glucose = [80, 100, 120]
cmd_main = 'python '+'updated_ct_script_iob_based.py '+sys.argv[1]
browser = webdriver.Firefox()
browser.get("http://localhost:3000/")
input_text = browser.find_element_by_id("initialglucose")

patient_name = ["patientA","patientB","patientC","patientD","patientE","patientF","patientG","patientH","patientI","patientJ"]
patient_id = 0

for i in browser.find_elements_by_xpath("//*[@type='radio']"):
	i.click()
	time.sleep(1)
	patient = patient_name[patient_id]
	for ig in initial_glucose:
		cmd_initialize = 'python '+'initialize.py '+ str(ig)
		input_text.clear()
		input_text.click()
		input_text.send_keys(str(ig))
		input_text.send_keys(Keys.RETURN)
		#time.sleep(1)
		os.system(cmd_initialize)
		os.system(cmd_main)
		
		cmd_collect_data = 'python '+'updated_collected.py'
		os.system(cmd_collect_data)
			
		directory = "./simulation_data/"+patient
		
		if not os.path.exists(directory):
			os.makedirs(directory)
		
		file_name = 'data_'+patient+'_'+str(ig)+'.csv'
		cmd_label_data = 'python '+'data_labeling_script.py'
		os.system(cmd_label_data)
		cmd_move_data = 'mv '+'labeled_data.csv '+directory+'/'+file_name
		os.system(cmd_move_data)
		
	patient_id = patient_id+1	

#**************************************************************
