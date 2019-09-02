import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import sys
from subprocess import call
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##########################################################
initial_glucose = [100]#80, 100, 120, 140, 160, 180, 200]
#initial_glucose = [80, 100]
#initial_glucose = [80]
# cmd_main = 'python '+'updated_ct_script_iob_based.py '#+sys.argv[1]
cmd_main = 'python '+'updated_ct_script_iob_based_mitigation.py '#+sys.argv[1]  mitigate the unsafe action

browser = webdriver.Firefox()
browser.get("http://localhost:3000/")
input_text = browser.find_element_by_id("initialglucose")

patient_name = ["patientA","patientB","patientC","patientD","patientE","patientF","patientG","patientH","patientI","patientJ"]
#patient_name = ["patientA"]
patient_id = 0

os.system('rm -r ./out/*') #clear the content in out folder 

for i in browser.find_elements_by_xpath("//*[@type='radio']"):
	i.click()
	time.sleep(1)
	patient = patient_name[patient_id]
	if patient_id == 7:#0 or patient_id == 7:#9
		for ig in initial_glucose:
			output_dir = 'out/'+patient+'/'+str(ig)+'/'
			if os.path.isdir(output_dir) != True:
				os.makedirs(output_dir)
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

			cmd = 'cp -a out/alerts.txt out/fault_times.txt out/hazards.txt'  + ' ' + output_dir
			os.system(cmd)
				
			directory = "./simulation_data/"+patient
			
			if not os.path.exists(directory):
				os.makedirs(directory)
			
			csv_file_name = 'data_'+patient+'_'+str(ig)+'.csv'
			cm_file_name = 'confustion_matrix_'+str(ig)+'.txt'
			f1_file_name = 'f1_score_'+str(ig)+'.txt'
			cmd_label_data = 'python '+'data_labeling_script.py'
			os.system(cmd_label_data)
			
			
			data = pd.read_csv("labeled_data.csv", error_bad_lines=False)
			y_pred = np.array(data["detection"].tolist())
			y_true = np.array(data["Label"].tolist())
			
			#conf_matrix = confusion_matrix(y_true, y_pred)
			#print(conf_matrix)
			#print(classification_report(y_true, y_pred))
			
			writeFile_CM = open("confusion_matrix.txt", "w+")
			writeFile_F1 = open("f1_score.txt", "w+")
			writeFile_CM.write(np.array2string(confusion_matrix(y_true, y_pred)))
			#writeFile_F1.write(classification_report(y_true, y_pred))
			writeFile_F1.write(str(f1_score(y_true, y_pred,average=None)))
			cmd_move_conf_matrix = 'mv '+'confusion_matrix.txt '+directory+'/'+cm_file_name
			cmd_move_f1_score = 'mv '+'f1_score.txt '+directory+'/'+f1_file_name
			os.system(cmd_move_conf_matrix)
			os.system(cmd_move_f1_score)
			
			cmd_move_data = 'mv '+'labeled_data.csv '+directory+'/'+csv_file_name
			os.system(cmd_move_data)

	patient_id = patient_id+1	

browser.close()
#**************************************************************
