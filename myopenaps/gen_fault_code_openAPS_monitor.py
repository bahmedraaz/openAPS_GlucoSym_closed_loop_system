import os
import numpy as np
import random

	
def gen_add_code(trigger_code,trigger, trigger_time,stop_time, variable, stuck_value, additional_code=''):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s+=%s' % (variable,stuck_value)
	code = code + l
	return code


def gen_sub_code(trigger_code,trigger, trigger_time, stop_time,variable, stuck_value,additional_code=''):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s-=%s' % (variable,stuck_value)
	code = code + l
	return code + additional_code

	
def gen_stuck_code(trigger_code,trigger, trigger_time, stop_time,variable, stuck_value):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s=%s' % (variable,stuck_value)
	code = code + l
	return code
######################################################################
def gen_add_glucose_code(trigger_code,trigger, trigger_time, stop_time,variable, stuck_value):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s=str(float(loaded_glucose)+%s)' % (variable,stuck_value)
	code = code + l
	return code

def gen_sub_glucose_code(trigger_code,trigger, trigger_time, stop_time,variable, stuck_value,additional_code=''):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s=str(float(loaded_glucose)-%s)' % (variable,stuck_value)
	code = code + l
	return code + additional_code

	
def gen_stuck_glucose_code(trigger_code,trigger, trigger_time, stop_time,variable, stuck_value):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s and %s<%s:'%(trigger,trigger_time,trigger,stop_time)
	l = '//%s=str(%s)' % (variable,stuck_value)
	code = code + l
	return code
# def gen_intermittent_code(variable, trigger, trigger_prob, random_value):
# 	#code = 'fault_prob = random.randint(1,100)'
# 	code = 'if %s<=%s:'%(trigger,trigger_prob)
# 	l = '//%s=%s' % (variable,random_value)
# 	code = code + l
# 	return code
	
### Write codes to fault library file
def write_to_file(code, exp_name, target_file, faultLoc):
	if os.path.isdir('fault_library_monitor') != True:
		os.makedirs('fault_library_monitor')
	fileName = 'fault_library_monitor/scenario_'+str(sceneNum)
	out_file = fileName+'.txt'
	#param_file = fileName+'_params.csv'

	with open(out_file, 'w') as outfile:
		#print out_file
		outfile.write('title:' + exp_name + '\n')
		outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
		for i, line in enumerate(code):
			outfile.write('fault ' + str(i+1) + '//' + line + '\n')
		outfile.write('Total number of fault cases: '+str(i+1))

	with open('run_fault_inject_campaign.sh', 'a+') as runFile:
		runFile.write('python run_openAPS.py '+fileName+'\n')

############################################################################

def write_to_file_STPA(code, exp_name, target_file, faultLoc):
	if os.path.isdir('fault_library_monitor_STPA') != True:
		os.makedirs('fault_library_monitor_STPA')
	fileName = 'fault_library_monitor_STPA/scenario_'+str(sceneNum)
	out_file = fileName+'.txt'
	#param_file = fileName+'_params.csv'

	with open(out_file, 'w') as outfile:
		#print out_file
		outfile.write('title:' + exp_name + '\n')
		outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
		for i, line in enumerate(code):
			outfile.write('fault ' + str(i+1) + '//' + line + '\n')
		outfile.write('Total number of fault cases: '+str(i+1))

	with open('run_fault_inject_STPA_campaign.sh', 'a+') as runFile:
		runFile.write('python run_openAPS.py '+fileName+'\n')

def write_both_to_file(code,code_STPA, title, fileLoc, faultLoc):
	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)	
#################################################################################3

def gen_belowTarget_noinc_add_rate(sceneNum):
	title = str(sceneNum)+'_belowTarget_add_rate_H2'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose < bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(10,350,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_add_code('',trigger, trigger_time,stop_time, variable, delta/100.0))
		code_STPA.append(gen_add_code(trigger_code,trigger,stop_time, trigger_time, variable, delta/100.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_belowTarget_inc_stuck_rate(sceneNum):
	title = str(sceneNum)+'_belowTarget_stuck_rate_H2'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose < bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(100,350,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_stuck_code('',trigger, trigger_time, stop_time,variable, delta/100.0))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time,stop_time, variable, delta/100.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_nodec_sub_rate(sceneNum):
	title = str(sceneNum)+'_aboveTarget_sub_rate_H1'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose > bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(10,350,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_sub_code('',trigger, trigger_time,stop_time, variable, delta/100.0,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		code_STPA.append(gen_sub_code(trigger_code,trigger, trigger_time, stop_time,variable, delta/100.0,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

##########################################################################################################
def gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable,newvalue,newvalue2=0):
		
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if xxxxx:' #wait to change to 27 rules in the context table
	code = []
	code_STPA=[]
	#param = []

	valuelist = []
	valuelist.append(newvalue)
	if newvalue2:
		valuelist.append(newvalue2)
	for valueitem in valuelist:
		for starttime in [10,100]: #10~99, 100~190 
			trigger_time = random.randint(starttime,starttime+90)
			duration = int((199 - trigger_time)/4) #divided into four parts
			for i in np.arange(trigger_time,199,duration):
				if i+duration <= 199: #make sure the stop time is no more than 199
					stop_time = random.randint(i+1,i+duration) #hong long fault will last, at least one iteration
					code.append(gen_stuck_code('',trigger, trigger_time,stop_time, variable, valueitem))
					code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time,stop_time, variable, valueitem))
					#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	

	write_both_to_file(code,code_STPA, title, fileLoc, faultLoc)

def gen_add_code_common_multiplestoptime(title,fileLoc,faultLoc,variable,direction): #direction: 0-decreade, 1-increase
		
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if xxxxx:' #wait to change to 27 rules in the context table
	code = []
	code_STPA=[]
	#param = []


	additional_code=''
	if direction == True:
		func = gen_add_code
	else:
		func = gen_sub_code
		additional_code='//if '+variable+'<0:'+'//  '+variable+'= 0'

	if 'rate' in variable:
		# daterange=[0.125,0.25,0.5,1,1.5,2,2.5,3,3.5,4]
		daterange=[2,3,4]
	else:
		# daterange=[16,32,48,64,96,128,160,192,224,256]
		daterange=[32,64,128,192,256]
	
	for gain in daterange: #single or multiple bitflips
		for starttime in [10,100]: #10~99, 100~190 
			trigger_time = random.randint(starttime,starttime+90)
			# duration = int((199 - trigger_time)/4) #divided into four parts
			duration = (199 - trigger_time)/4 
			# for i in np.arange(trigger_time,199,duration):
			for i in range(4):
				time = int(trigger_time + i*duration)
				endpoint = time+int(duration)
				if endpoint <=199:
				# if i+duration <= 199: #make sure the stop time is no more than 199
					stop_time = random.randint(time+1,endpoint) #hong long fault will last, at least one iteration
					code.append(func('',trigger, trigger_time,stop_time, variable, gain,additional_code))
					code_STPA.append(func(trigger_code,trigger, trigger_time,stop_time, variable, gain,additional_code))
					#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_both_to_file(code,code_STPA, title, fileLoc, faultLoc)


def gen_lostconnection_hold_rate(sceneNum): #S9
	title = str(sceneNum)+'_lostconnection_hold_rate'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	variable = 'rate_refresh'
	newvalue = 0

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable,newvalue)

def gen_bitflip_double_rate(sceneNum): #S10
	title = str(sceneNum)+'_bitflip_double_rate'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	variable = 'loaded_suggested_data["rate"]'
	newvalue = '4*loaded_suggested_data["rate"]'
	newvalue2 = '8*loaded_suggested_data["rate"]'

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, newvalue,newvalue2)

def gen_bitflip_half_rate(sceneNum): #S11
	title = str(sceneNum)+'_bitflip_half_rate'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	variable = 'loaded_suggested_data["rate"]'
	newvalue = '0.25*loaded_suggested_data["rate"]'
	newvalue2 = '0.125*loaded_suggested_data["rate"]'

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, newvalue,newvalue2)

	
def gen_bitflip_add_rate(sceneNum): #S12
	title = str(sceneNum)+'_bitflip_add_rate'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	variable = 'loaded_suggested_data["rate"]'

	gen_add_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, True)

def gen_bitflip_sub_rate(sceneNum): #S13
	title = str(sceneNum)+'_bitflip_sub_rate'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	variable = 'loaded_suggested_data["rate"]'

	gen_add_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, False)
############========================#########################
def gen_lostconnection_hold_glucose(sceneNum):#S14
	title = str(sceneNum)+'_lostconnection_hold_glucose'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	variable = 'glucose_refresh'
	newvalue = 0

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable,newvalue)

def gen_bitflip_double_glucose(sceneNum): #S15
	title = str(sceneNum)+'_bitflip_double_glucose'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	variable = 'data_to_prepend["glucose"]'
	newvalue = '2*data_to_prepend["glucose"]'

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, newvalue)

def gen_bitflip_half_glucose(sceneNum): #S16
	title = str(sceneNum)+'_bitflip_half_glucose'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	variable = 'data_to_prepend["glucose"]'
	newvalue = '0.5*data_to_prepend["glucose"]'

	gen_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, newvalue)

def gen_bitflip_add_glucose(sceneNum): #S17
	title = str(sceneNum)+'_bitflip_add_glucose'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	variable = 'data_to_prepend["glucose"]'

	gen_add_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, True)

def gen_bitflip_sub_glucose(sceneNum): #S17
	title = str(sceneNum)+'_bitflip_sub_glucose'
	
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	variable = 'data_to_prepend["glucose"]'

	gen_add_code_common_multiplestoptime(title,fileLoc,faultLoc,variable, False)
##########################################################################################
def gen_aboveTarget_nodec_stuck_rate(sceneNum):
	title = str(sceneNum)+'_aboveTarget_stuck_rate_H1'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose > bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(0,200,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_stuck_code('',trigger, trigger_time,stop_time, variable, delta/1000.0))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time,stop_time, variable, delta/1000.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

###############glucose:HOOK#############
def gen_belowTarget_add_glucose(sceneNum):
	title = str(sceneNum)+'_belowTarget_add_glucose_H2'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if float(loaded_glucose) < 110:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(10,200,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_add_glucose_code('',trigger, trigger_time,stop_time, variable, delta))
		code_STPA.append(gen_add_glucose_code(trigger_code,trigger, trigger_time,stop_time, variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_belowTarget_stuck_glucose(sceneNum):
	title = str(sceneNum)+'_belowTarget_stuck_glucose_H2'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if float(loaded_glucose) < 110:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(120,300,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_stuck_glucose_code('',trigger, trigger_time, stop_time,variable, delta))
		code_STPA.append(gen_stuck_glucose_code(trigger_code,trigger, trigger_time, stop_time,variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_sub_glucose(sceneNum):
	title = str(sceneNum)+'_aboveTarget_sub_glucose_H1'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if float(loaded_glucose) > 120:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(10,300,30)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+29)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_sub_glucose_code('',trigger, trigger_time, stop_time,variable, delta,'//if float('+variable+')<0:'+'//  '+variable+"='0'"))
		code_STPA.append(gen_sub_glucose_code(trigger_code,trigger, trigger_time, stop_time,variable, delta,'//if float('+variable+')<0:'+'//  '+variable+"='0'"))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_stuck_glucose(sceneNum):
	title = str(sceneNum)+'_aboveTarget_stuck_glucose_H1'
	#faultLibFile = 'fault_library_monitor/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if float(loaded_glucose) > 120:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(30,70,10)
	for i in deltaRange:
		# for j in range(5):
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,199)
		stop_time = random.randint(trigger_time,200) #hong long fault will last
		code.append(gen_stuck_glucose_code('',trigger, trigger_time,stop_time, variable, delta))
		code_STPA.append(gen_stuck_glucose_code(trigger_code,trigger, trigger_time,stop_time, variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

###_main_###

with open('run_fault_inject_campaign.sh', 'w') as runFile:
    runFile.write('#Usage: python run_openAPS.py fault_library_monitor\n')

with open('run_fault_inject_STPA_campaign.sh', 'w') as runFile:
    runFile.write('#Usage: python run_openAPS.py target_fault_library_monitor\n')
	
scenarios = {
1 : gen_belowTarget_noinc_add_rate,
2 : gen_belowTarget_inc_stuck_rate,
3 : gen_aboveTarget_nodec_sub_rate,
4 : gen_aboveTarget_nodec_stuck_rate,
5 : gen_belowTarget_add_glucose,
6 : gen_belowTarget_stuck_glucose,
7 : gen_aboveTarget_sub_glucose,
8 : gen_aboveTarget_stuck_glucose,
9 : gen_lostconnection_hold_rate, #hardware error
10 : gen_bitflip_double_rate,
11 : gen_bitflip_half_rate,
12 : gen_bitflip_add_rate,
13 : gen_bitflip_sub_rate,
14 : gen_lostconnection_hold_glucose, #hardware error
15 : gen_bitflip_double_glucose,
16 : gen_bitflip_half_glucose,
17 : gen_bitflip_add_glucose,
18 : gen_bitflip_sub_glucose,

}

for sceneNum in [9,10,11,12,13,14,15,16,17,18]:
	scenarios[sceneNum](sceneNum)

