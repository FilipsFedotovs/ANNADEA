#Current version 1.1 - add change sys path capability

########################################    Import essential libriries    #############################################
import argparse
import sys


#Setting the parser - this script is usually not run directly, but is used by a Master version Counterpart that passes the required arguments
parser = argparse.ArgumentParser(description='select cut parameters')
parser.add_argument('--i',help="Set number", default='1')
parser.add_argument('--j',help="Subset number", default='1')
parser.add_argument('--k',help="SubSubset number", default='1')
parser.add_argument('--Z_overlap',help="Enter Z id", default='1')
parser.add_argument('--Y_overlap',help="Enter Y id", default='1')
parser.add_argument('--X_overlap',help="Enter X id", default='1')
parser.add_argument('--stepX',help="Enter X step size", default='0')
parser.add_argument('--stepY',help="Enter Y step size", default='0')
parser.add_argument('--stepZ',help="Enter Z step size", default='0')
parser.add_argument('--EOS',help="EOS directory location", default='.')
parser.add_argument('--AFS',help="AFS directory location", default='.')
parser.add_argument('--PY',help="Python libraries directory location", default='.')
parser.add_argument('--zOffset',help="Data offset on z", default='0.0')
parser.add_argument('--yOffset',help="Data offset on y", default='0.0')
parser.add_argument('--xOffset',help="Data offset on x", default='0.0')
parser.add_argument('--cut_dt',help="Cut on angle difference", default='1.0')
parser.add_argument('--cut_dr',help="Cut on angle difference", default='4000')
parser.add_argument('--Log',help="Pull out stats?", default='No')
parser.add_argument('--ModelName',help="Name of the model to use?", default='0')
parser.add_argument('--BatchID',help="Give name to this train sample", default='')
parser.add_argument('--p',help="Path to the output file", default='')
parser.add_argument('--o',help="Path to the output file name", default='')
parser.add_argument('--pfx',help="Path to the output file name", default='')
parser.add_argument('--sfx',help="Path to the output file name", default='')

#Working out where are the Py libraries
args = parser.parse_args()
#Loading Directory locations
EOS_DIR=args.EOS
AFS_DIR=args.AFS
PY_DIR=args.PY

if PY_DIR!='': #Temp solution
    sys.path=['',PY_DIR]
    sys.path.append('/usr/lib64/python36.zip')
    sys.path.append('/usr/lib64/python3.6')
    sys.path.append('/usr/lib64/python3.6/lib-dynload')
    sys.path.append('/usr/lib64/python3.6/site-packages')
    sys.path.append('/usr/lib/python3.6/site-packages')
sys.path.append(AFS_DIR+'/Code/Utilities')
import pandas as pd #We use Panda for a routine data processing
######################################## Set variables  #############################################################
Z_overlap=int(args.Z_overlap)
Y_overlap=int(args.Y_overlap)
X_overlap=int(args.X_overlap)
Z_ID=int(args.k)/Z_overlap
Y_ID=int(args.j)/Y_overlap
X_ID=int(args.i)/X_overlap
Z_ID_n=int(args.k)
Y_ID_n=int(args.j)
X_ID_n=int(args.i)
stepX=float(args.stepX) #The coordinate of the st plate in the current scope
stepZ=float(args.stepZ)
stepY=float(args.stepY)
z_offset=float(args.zOffset)
y_offset=float(args.yOffset)
x_offset=float(args.xOffset)
cut_dt=float(args.cut_dt)
cut_dr=float(args.cut_dr)
Log=args.Log.upper()
ModelName=args.ModelName
RecBatchID=args.BatchID
p=args.p
o=args.o
sfx=args.sfx
pfx=args.pfx

import UtilityFunctions as UF #This is where we keep routine utility functions

#Specifying the full path to input/output files
input_file_location=EOS_DIR+'/ANNDEA/Data/REC_SET/RTr1_'+RecBatchID+'_hits.csv'
output_file_location=EOS_DIR+p+'/'+pfx+'_'+RecBatchID+'_hit_cluster_rec_set_'+str(X_ID_n)+'_'+str(Y_ID_n)+'_'+str(Z_ID_n)+sfx

print(UF.TimeStamp(), "Modules Have been imported successfully...")
print(UF.TimeStamp(),'Loading pre-selected data from ',input_file_location)

data=pd.read_csv(input_file_location,header=0,usecols=["Hit_ID","x","y","z","tx","ty"])[["Hit_ID","x","y","z","tx","ty"]]
data["x"] = pd.to_numeric(data["x"],downcast='float')
data["y"] = pd.to_numeric(data["y"],downcast='float')
data["z"] = pd.to_numeric(data["z"],downcast='float')
data['x']=data['x']-x_offset
data['y']=data['y']-y_offset
data["Hit_ID"] = data["Hit_ID"].astype(str)
data['z']=data['z']-z_offset
print(UF.TimeStamp(),'Preparing data... ')
data.drop(data.index[data['z'] >= ((Z_ID+1)*stepZ)], inplace = True)  #Keeping the relevant z slice
data.drop(data.index[data['z'] < (Z_ID*stepZ)], inplace = True)  #Keeping the relevant z slice
data.drop(data.index[data['x'] >= ((X_ID+1)*stepX)], inplace = True)  #Keeping the relevant z slice
data.drop(data.index[data['x'] < (X_ID*stepX)], inplace = True)  #Keeping the relevant z slice
data.drop(data.index[data['y'] >= ((Y_ID+1)*stepY)], inplace = True)  #Keeping the relevant z slice
data.drop(data.index[data['y'] < (Y_ID*stepY)], inplace = True)  #Keeping the relevant z slice
data_list=data.values.tolist()

if Log!='NO':
    print(UF.TimeStamp(),'Preparing MC data... ')
    input_file_location=EOS_DIR+'/ANNDEA/Data/TEST_SET/ETr1_'+RecBatchID+'_hits.csv'
    print(UF.TimeStamp(),'Loading pre-selected data from ',input_file_location)
    MCdata=pd.read_csv(input_file_location,header=0,
                                usecols=["Hit_ID","x","y","z","tx","ty",'MC_Mother_Track_ID'])[["Hit_ID","x","y","z","tx","ty",'MC_Mother_Track_ID']]
    MCdata["x"] = pd.to_numeric(MCdata["x"],downcast='float')
    MCdata["y"] = pd.to_numeric(MCdata["y"],downcast='float')
    MCdata["z"] = pd.to_numeric(MCdata["z"],downcast='float')
    MCdata["Hit_ID"] = MCdata["Hit_ID"].astype(str)
    MCdata['z']=MCdata['z']-z_offset
    MCdata['x']=MCdata['x']-x_offset
    MCdata['y']=MCdata['y']-y_offset
    MCdata.drop(MCdata.index[MCdata['z'] >= ((Z_ID+1)*stepZ)], inplace = True)  #Keeping the relevant z slice
    MCdata.drop(MCdata.index[MCdata['z'] < (Z_ID*stepZ)], inplace = True)  #Keeping the relevant z slice
    MCdata.drop(MCdata.index[MCdata['x'] >= ((X_ID+1)*stepX)], inplace = True)  #Keeping the relevant z slice
    MCdata.drop(MCdata.index[MCdata['x'] < (X_ID*stepX)], inplace = True)  #Keeping the relevant z slice
    MCdata.drop(MCdata.index[MCdata['y'] >= ((Y_ID+1)*stepY)], inplace = True)  #Keeping the relevant z slice
    MCdata.drop(MCdata.index[MCdata['y'] < (Y_ID*stepY)], inplace = True)  #Keeping the relevant z slice
    MCdata_list=MCdata.values.tolist()

if Log=='KALMAN':
    print(UF.TimeStamp(),'Preparing KALMAN data... ')
    input_file_location=EOS_DIR+'/ANNDEA/Data/TEST_SET/KTr1_'+RecBatchID+'_hits.csv'
    print(UF.TimeStamp(),'Loading pre-selected data from ',input_file_location)
    FEDRAdata=pd.read_csv(input_file_location,header=0,
                                usecols=["Hit_ID","x","y","z","tx","ty",'Rec_Track_ID'])[["Hit_ID","x","y","z","tx","ty",'Rec_Track_ID']]
    FEDRAdata["x"] = pd.to_numeric(FEDRAdata["x"],downcast='float')
    FEDRAdata["y"] = pd.to_numeric(FEDRAdata["y"],downcast='float')
    FEDRAdata["z"] = pd.to_numeric(FEDRAdata["z"],downcast='float')
    FEDRAdata["Hit_ID"] = FEDRAdata["Hit_ID"].astype(str)
    FEDRAdata['z']=FEDRAdata['z']-z_offset
    FEDRAdata['x']=FEDRAdata['x']-x_offset
    FEDRAdata['y']=FEDRAdata['y']-y_offset
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['z'] >= ((Z_ID+1)*stepZ)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['z'] < (Z_ID*stepZ)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['x'] >= ((X_ID+1)*stepX)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['x'] < (X_ID*stepX)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['y'] >= ((Y_ID+1)*stepY)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata.drop(FEDRAdata.index[FEDRAdata['y'] < (Y_ID*stepY)], inplace = True)  #Keeping the relevant z slice
    FEDRAdata_list=FEDRAdata.values.tolist()

print(UF.TimeStamp(),'Preparing the model')
import torch
EOSsubDIR=EOS_DIR+'/'+'ANNDEA'
EOSsubModelDIR=EOSsubDIR+'/'+'Models'
Model_Meta_Path=EOSsubModelDIR+'/'+args.ModelName+'_Meta'
Model_Path=EOSsubModelDIR+'/'+args.ModelName
ModelMeta=UF.PickleOperations(Model_Meta_Path, 'r', 'N/A')[0]
Acceptance=ModelMeta.TrainSessionsData[-1][-1][3]
device = torch.device('cpu')
model = UF.GenerateModel(ModelMeta).to(device)
model.load_state_dict(torch.load(Model_Path))
model.eval()
print(UF.TimeStamp(),'Creating the clusters')
HC=UF.HitCluster([X_ID,Y_ID,Z_ID],[stepX,stepY,stepZ])
print(UF.TimeStamp(),'Decorating the clusters')
HC.LoadClusterHits(data_list)
print(UF.TimeStamp(),'Generating the edges...')
GraphStatus = HC.GenerateEdges(cut_dt, cut_dr)
combined_weight_list=[]
if HC.ClusterGraph.num_edges>0:
            print(UF.TimeStamp(),'Classifying the edges...')
            w = model(HC.ClusterGraph.x, HC.ClusterGraph.edge_index, HC.ClusterGraph.edge_attr)
            w=w.tolist()
            for edge in range(len(HC.edges)):
                combined_weight_list.append(HC.edges[edge]+w[edge])
if Log!='NO':
                print(UF.TimeStamp(),'Tracking the cluster...')
                HC.LinkHits(combined_weight_list,True,MCdata_list,cut_dt,cut_dr,Acceptance)
                if Log=='KALMAN':
                       HC.TestKalmanHits(FEDRAdata_list,MCdata_list)

else:
    print(UF.TimeStamp(),'Tracking the cluster...')
    HC.LinkHits(combined_weight_list,False,[],cut_dt,cut_dr,Acceptance)
HC.UnloadClusterGraph()
print(UF.TimeStamp(),'Writing the output...')
print(output_file_location)
print(UF.PickleOperations(output_file_location,'w', HC))
#End of the script



