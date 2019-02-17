from subprocess import call
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##########################################################
#initial_glucose = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]
initial_glucose = [80, 100]
cmd_main = 'python '+'updated_ct_script_iob_based.py'
browser = webdriver.Firefox()
browser.get("http://localhost:3000/")
input_text = browser.find_element_by_id("initialglucose")

for i in browser.find_elements_by_xpath("//*[@type='radio']"):
	i.click()
	time.sleep(1)
	for ig in initial_glucose:
		cmd_initialize = 'python '+'initialize.py '+ str(ig)
		input_text.clear()
		input_text.click()
		input_text.send_keys(str(ig))
		input_text.send_keys(Keys.RETURN)
		#time.sleep(1)
		os.system(cmd_initialize)
		os.system(cmd_main)
#**************************************************************


##########################################################
##initial_glucose = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]
#ig = 300
#cmd_main = 'python '+'updated_ct_script_iob_based.py'
#browser = webdriver.Firefox()
#browser.get("http://localhost:3000/")
#input_text = browser.find_element_by_id("initialglucose")
#
#for i in browser.find_elements_by_xpath("//*[@type='radio']"):
#	i.click()
#	#for ig in initial_glucose:
#	#cmd_initialize = 'python '+'initialize.py '+ str(ig)
#	input_text.clear()
#	input_text.click()
#	input_text.send_keys(str(ig))
#	input_text.send_keys(Keys.RETURN)
#	call(["node", "../glucosym/closed_loop_algorithm_samples/old_algo_bw.js"])
#	#time.sleep(1)
#	#os.system(cmd_initialize)
#	#os.system(cmd_main)
#	break
#	
##**************************************************************
