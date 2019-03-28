## offline Wrapper

import pandas as pd


file_name = "data_patientE_220_stuck_300.csv"
data = pd.read_csv(file_name, error_bad_lines=False)

thBg = 0
thBgFall = -0.3
thBgRise = 0.3

thIob = 0

thRate = 0
thRateFall = -0.20
thRateRise = 0.20

bgTarget = 120
bgLowerTh = 75

data["detection"] = 0
data["unsafe_action_reason"]= "Null"
initialGlucose = data["CGM_glucose"][0]
#print("initial glucose: ",initialGlucose)

for i in range(1,len(data.index)):

    bg = data["CGM_glucose"][i]
    iob = data["IOB"][i]
    insulinRate = data["rate"][i]

    delBg = data["CGM_glucose"][i] - data["CGM_glucose"][i-1]
    delIob = data["IOB"][i] - data["IOB"][i-1]
    delInsulinRate = data["rate"][i] - data["rate"][i-1]

    if bg < bgLowerTh:
        if delInsulinRate != 0: # row_38
            data["detection"][i] = 100
            data["unsafe_action_reason"][i] = "row_38"

    elif bg > bgTarget:
        #if delBg >= -3:
        if insulinRate == 0: # row_37
            data["detection"][i] = 100
            data["unsafe_action_reason"][i] = "row_37"

        #elif delBg > 0:
        # checking if BG is rising
        if delBg > 0:
            if delIob > 0: # row_1
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_1"
            #if delBg < 0:
            if delIob < thIob: # row_2
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_2"
            if delIob == thIob: # row_3
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_3"

        elif delBg < 0:

            # checking if BG is falling more than the threshold
            #if delBg > thBgFall:
            if delIob > 0: # row_4
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_4"
            if delIob < 0: # row_5
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_5"
            if delIob == 0: # row_6
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_6"

        elif delBg == thBg:
            if delIob > 0: # row_7
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_7"
            if delIob < 0: # row_8
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_8"
            if delIob == 0: # row_9
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_9"
        

    elif bg < bgTarget:

        if delBg > 0:
            # checking if BG is rising more than the threshold

            #if delBg < 0.
            if delIob > 0:
                if delInsulinRate > 0: # row_29
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_29"
            #if delBg > thBgRise:
            if delIob < 0:
                if delInsulinRate > 0: # row_28
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_28"
            if delIob == thIob:
                if delInsulinRate > 0: # row_30
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_30"
        
        elif delBg < 0:
            # checking if BG is falling more than the threshold
            #if delBg < thBgFall:
            if delIob > 0: # row_31
                if delInsulinRate > 0:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_31"
            if delIob < 0: # row_32
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_32"
            if delIob == thIob: # row_33
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_33"

        elif delBg == 0:
            if delIob > 0:
                if delInsulinRate > 0: # row_34
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_34"
            if delIob < 0: # row_35
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_35"
            if delIob == 0: # row_36
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_36"
        
data.to_csv("labeled_"+file_name);    
