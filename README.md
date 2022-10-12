# ANNADEA
Artificial Neural Network Driven Emulsion Analysis
This README just serves as a very short user guide, the documentation will be written much later.
## Hints and Tips

1) It is recomended to run those processes on lxplus in the tmux shell as some scripts can take up to several hours to execute.
2) The first letter of the script name prefixes indicate what kind of operations this script perform: R is for actual reconstruction routines, E for evaluation and M for model creation and training. I for Classification tasks.
3) The second letter of the script name prefixes indicates the subject of the reconstruction. H - hits, S - Track Segments, T- tracks, V - Vertices and E - events.
4) In general the numbers in prefixes reflect the order at which scripts have to be executed e.g: MH1, MH2,MH3. If there is no number then the script is independent or optional.
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
8) Once the program successfully executes it will leave a following message before exiting: 
   "###### End of the program #####"

## Tracking Module
The tracking module takes hits as an input and assigns the common ID - hence it clusters them into tracks.
All modules 
### Requirements

### Installation steps
1) go to your home directory in afs where you would like to install the package
2) git clone https://github.com/FilipsFedotovs/ANNADEA/
3) cd ANNADEA/
4) python setup.py
5) The installation will require an EOS directory, please enter the location on EOS where you would like to keep data and the models. An example of the input is /eos/experiment/ship/user/username (but create the directory there first).
6) The installation will ask whether you want to copy default training and validation files (that were prepared earlier). Unless you have your own, please enter Y.     The installer will copy and analyse existing data, it might take 5-10 minutes
7) if the message 'ANNADEA setup is successfully completed' is displayed, it means that the package is ready for work

### Creating training files -------
1) Go to ANNADEA directory on AFS
2) cd Code
3) python3 MH1_GenerateTrainClusters.py --TrainSampleID Test_Sample_1
4) The script will ask which samples to use. Please type D and press ENTER.The script will send HTCondor jobs and exit.
5) After a day or so please run: python Model_Training.py --MODE C
6) This process is repeated multiple times until the model is sufficinetly trained

------- Track reconstruction --------
1) Go to EDER_TRAN directory on AFS
2) cd Code 
3) tmux (please note the number of lxplus machine at which tmux session is logged in)
4) kinit username@CERN.CH -l 24h00m
5) python3 Track_Reconstructor.py 
   The process can take many hours, log out of tmux by using ctrl+b

------ Hit utilisation Analysis -------
1) Relogin to the same machine by using ssh -XY username@lxplus#.cern.ch where # is the recorded number.
2) tmux a -t 0
3) if the green message "The reconstruction has completed # tracks have been recognised' is displayed, it means that the reconstruction is finished.
4) kinit username@CERN.CH
5) cd Utilisation
6) python Analyse_Hit_Utilisation.py --metric TRANN
