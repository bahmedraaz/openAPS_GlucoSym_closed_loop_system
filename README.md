# Running closed loop simulation with openaps and GlucoSym
To run the closed loop simulation with both openAPS and Glucosym, the following steps should be taken

Install openaps into your machine. You can find the whole installation process in this link https://openaps.readthedocs.io/en/latest/docs/Build%20Your%20Rig/OpenAPS-install.html

Add the Virtual Devices in openaps. Go to the following link and follow the instructions to add virtual devices and create the environment to run openaps. https://openaps.readthedocs.io/en/stable/docs/walkthrough/phase-2/Using-oref0-tools.html

After you are done with the previeous two steps, you will get a folder just like the "openaps" folder with some subfolder in this repository. However, you will not have all the files that this openaps folder has. You will create files as you need. When you go into the openaps folder, you will see lots of files and folders. But there are two main scripts that we need frequently. The first one is "initialize.py" and second one is "updated_ct_script_iob_based.py".

Now here starts the process to run the closed loop simulation:

Put both the openaps and GlucoSym folder in a same directory Go into GlucoSym folder and run the command "npm start" Then open a browser and naviget to http://localhost:3000, it will open a window where you can select different patient.

Go into the openaps folder. You have to initialize differnt inputs that openaps needs by running initialize.py. Please open this file and change the initial value of blood glucose, insulin rate or duration as you need. Then run this command "python initialize.py". It will initialize the inputs and also it will automatically initialize the time so that openaps does not think that the inputs are too old.

After initialization, you will run the main script named "updated_ct_script_iob_based.py". You can eidt this file as you need. You may want to change the number of iteration based on how long you want to run the simulation. Every iteration is treated as 5 minutes. You have to run this file as root, otherwise it will not work properly. Running this file will start simulation for your desired time. When the simulation is done, to collect the result in a csv file, you may want to run another file named "updated_collected.py". You will find this file in the openaps folder. After running "updated_collected.py", you will find a filed called data.csv in the same directory where you will find the simulation result.
