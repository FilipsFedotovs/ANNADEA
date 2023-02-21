# ANNDEA
Artificial Neural Network Driven Emulsion Analysis.
This README just serves as a very short user guide, a more complete documentation can be found in the project wiki.

## 0. Hints and Tips
1) It is recommended to run those processes on lxplus in the tmux shell as some scripts can take up to several hours to execute.
2) The first letter of the script name prefixes indicate what kind of operations this script perform: R is for actual reconstruction routines, E for evaluation and M for model creation and training.
3) The second letter of the script name prefixes indicates the subject of the reconstruction. Tr- tracks, V - Vertices and E - events.
4) In general the numbers in prefixes reflect the order at which scripts have to be executed e.g: MTr1, MTr2, MTr3. If there is no number then the script is independent or optional.
4) --help argument provides all the available run arguments of a script and its purpose.
5) The output of each script has the same prefix as the script that generates it. Sometimes if there are multiple sub scripts then the a,b,c letters are added to indicate the order of the execution. This is done for scripts with 'sub' suffix.
6) The files that are the final output will not have any suffixes.
   Those files are not deleted after execution. 
7) The screen output of the scripts is colour coded: 
   - White for routine operations
   - Blue for the file and folder locations
   - Green for successful operation completions
   - Yellow for warnings and non-critical errors.
   - Red for critical errors.
8) The white coloured text outputs with the prefix *UF* are the messages that are generated by imported functions in **UtilityFunction.py** file
9) Once the program successfully executes it will leave a following message before exiting: 
   "###### End of the program #####"

## 1. Tracking Module
The tracking module takes hits as an input and assigns the common ID - hence it clusters them into tracks.
All modules 
### Requirements
Install PyTorch: 
1) pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html --target **/eos/user/x/xyyyyy/libs**
2) pip3 install torch-scatter -f https://data.pyg.org/whl/torch-1.9.0+cpu.html --target **/eos/user/x/xyyyy/libs**
3) pip3 install torch-sparse -f https://data.pyg.org/whl/torch-1.9.0+cpu.html --target **/eos/user/x/xyyyyy/libs**
4) pip3 install torch-geometric --target **/eos/user/x/xyyyyy/libs**

Please replace **x** and **xyyyyy** with first letter of your username and your username respectively.

Install Other libraries:
1) pip3 install pandas --target **/eos/user/x/xyyyyy/libs**
2) pip3 install tabulate --target **/eos/user/x/xyyyyy/libs**
3) pip3 install alive_progress --target **/eos/user/x/xyyyyy/libs**

### 1.1 Installation steps
1) go to your home directory in afs where you would like to install the package
2) **git clone https://github.com/FilipsFedotovs/ANNDEA/**
3) **cd ANNDEA/**
4) **python3 setup.py --PyPath /eos/user/x/xyyyyy/libs**
5) The installation will require an EOS directory, please enter the location on EOS where you would like to keep data and the models. An example of the input is /eos/experiment/ship/user/username (but create the directory there first).
6) The installation will ask whether you want to copy default training and validation files (that were prepared earlier). Unless you have your own, please enter **Y**.     The installer will copy and analyse existing data, it might take 5-10 minutes
7) if the message *'ANNDEA setup is successfully completed'* is displayed, it means that the package is ready for work

### 1.2 Creating training files 
*This part is only needed if a new model is required*
1) Go to ANNDEA directory on AFS
2) **cd Code**
3) **tmux**
4) **kinit username@CERN.CH -l 24h00m**
5) Enter your lxplus password
6) **python3 MTr1_GenerateTrainClusters.py --TrainSampleID Training_Sample --Xmin 200000 --Xmax 300000 --Ymin 0 --Ymax 70000**
7) After few minutes the script will ask for the user option (Warning, there are still x HTCondor jobs remaining). Type **R** and press **Enter**. The script will submit the subscript jobs and go to the autopilot mode.
8) Exit tmux (by using **ctrl + b** and then typing  **d**). It can take up to few hours for HTCondor jobs to finish.
9) Enter the same tmux session after some period (after overnight job for example) by logging to the same lxplus machine and then typing  **tmux a -t 0**. The program should finish with the message *'Training samples are ready for the model creation/training'*

### 1.3 Training a new model by using previously generated model
*This part is only needed if a new model is required*
1) Go to ANNDEA directory on AFS
2) **cd Code**
3) **tmux**
4) **kinit username@CERN.CH -l 24h00m**
5) Enter your lxplus password
6) **python3 MTr2_TrainModel.py --TrainSampleID Training_Sample --ModelName Test_Model --ModelParams '[1,20,1,20]' --TrainParams "[0.1,4,10,1]"**
7) The script will submit the subscript jobs and ask for your next steps. Enter 600 and press **Enter**
8) Exit tmux (by using **ctrl + b** and then typing  **d**). Script will keep running in the autopilot mode until all the steps in the hit reconstruction process have been completed.
9) Enter the same tmux session (after overnight job for example) by logging to the same lxplus machine and then typing  **tmux a -t 0**. The program should finish with the message *'Training is finished then, thank you and goodbye'*

### 1.4 Reconstructing a hit data using the new model 
1) Go to ANNDEA directory on AFS
2) **cd Code**
3) **tmux**
4) **kinit username@CERN.CH -l 24h00m**
5) Enter your lxplus password
6) **python3 RTr1_ReconstructTracks.py --ModelName MH_SND_Tracking_5_80_5_80 --Xmin 200000 --Xmax 230000 --Ymin 20000 --Ymax 40000 --X_overlap 1 --Y_overlap 1 --Z_overlap 1 --RecBatchID Test_Batch**
7) The script will submit the subscript jobs and go to the autopilot mode.
8) Exit tmux (by using **ctrl + b** and then typing  **d**). Script will keep running in the autopilot mode until all the steps in the hit reconstruction process have been completed.
9) Enter the same tmux session (after overnight job for example) by logging to the same lxplus machine and then typing  **tmux a -t 0**. The program should finish with the message *'Reconstruction has been completed'*


