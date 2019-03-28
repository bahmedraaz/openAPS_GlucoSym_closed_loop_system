## offline wrapper with threshold
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
        if delBg >= -3: # modification: if bg falls below no more than 3 or equal to then this rule is valid. Otherwise if bg falls very faster (more than 3 unit), it might be ok to shut off the insulin flow for a while. Here, I arbitrary chose the value -3. We can further fine tune it.
            if insulinRate == 0: # row_37
                data["detection"][i] = 100
                data["unsafe_action_reason"][i] = "row_37"

        elif delBg > 0:
            # checking if BG is rising more than the threshold
            if delBg > 0.9:
                if delIob > thIob: # row_1
                    if delInsulinRate < -0.15: # modification: while BG is above target and and however as IOB is rising, some decrease might be tolerable. Here, I set that decrease of insulin more than 0.15 is not allwoed. Decrease in inulin delivery less than 0.15 unit is alllowed. We can further modify by putting constraint that more than n number of consecutive decrease in this context is not allowed.
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_1"
            if delBg > thBgRise:
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
            if delBg > thBgFall:
                #if delIob > thIob: # row_4
                #    if delInsulinRate < thRateFall:
                #        data["detection"][i] = 100
                #        data["unsafe_action_reason"][i] = "row_4"
                if delIob < thIob: # row_5
                    if delInsulinRate < thRateFall:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_5"
                if delIob == thIob: # row_6
                    if delInsulinRate < 0:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_6"

        elif delBg == thBg:
            if delIob > thIob: # row_7
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_7"
            if delIob < thIob: # row_8
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_8"
            if delIob == thIob: # row_9
                if delInsulinRate < 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_9"
        

    elif bg < bgTarget:

        if delBg > 0:
            # checking if BG is rising more than the threshold

            if delBg < 0.8:
                if iob < -0.7 and delIob < thIob:
                    if delInsulinRate > 0: # row_29
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_29"
            if delBg > thBgRise:
                if delIob > thIob:
                    if delInsulinRate > thRateRise: # row_28
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_28"
                if delIob == thIob:
                    if delInsulinRate > 0: # row_30
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_30"
        
        elif delBg < 0:
            # checking if BG is falling more than the threshold
            if delBg < thBgFall:
                if delIob > thIob: # row_31
                    if delInsulinRate > 0:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_31"
                if delIob > -0.02: # row_32
                    if delInsulinRate > 0:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_32"
                if delIob == thIob: # row_33
                    if delInsulinRate > 0:
                        data["detection"][i] = 100
                        data["unsafe_action_reason"][i] = "row_33"

        elif delBg == thBg:
            if delIob > thIob:
                if delInsulinRate > 0: # row_34
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_34"
            if delIob < thIob: # row_35
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_35"
            if delIob == thIob: # row_36
                if delInsulinRate > 0:
                    data["detection"][i] = 100
                    data["unsafe_action_reason"][i] = "row_36"
        
data.to_csv("labeled_wt_"+file_name);    
