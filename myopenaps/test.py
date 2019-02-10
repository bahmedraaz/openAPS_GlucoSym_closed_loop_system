#from subprocess import call
import os
#call(["run_fault_inject_campaign.sh"])
#cmd = "./run_fault_inject_campaign.sh"
#os.system(cmd)

name_id = []
fileNames = os.listdir("./result")
print("Num of Line",len(fileNames))
for name in fileNames:
	name_id.append(int(((name.split('_')[1])).split('.')[0]))


for i in name_id:
	print(i+1)
