###This file contains the utility functions that are commonly used in ANNDEA packages


import math

import numpy as np





class HitCluster:
      def __init__(self,ClusterID, Step):
          self.ClusterID=ClusterID
          self.Step=Step
      def __eq__(self, other):
        return ('-'.join(str(self.ClusterID))) == ('-'.join(str(other.ClusterID)))
      def __hash__(self):
        return hash(('-'.join(str(self.ClusterID))))
      def LoadClusterHits(self,RawHits): #Decorate hit information
           self.ClusterHits=[]
           self.ClusterHitIDs=[]
           __ClusterHitsTemp=[]
           for s in RawHits:
               if s[1]>=self.ClusterID[0]*self.Step[0] and s[1]<((self.ClusterID[0]+1)*self.Step[0]):
                   if s[2]>=self.ClusterID[1]*self.Step[1] and s[2]<((self.ClusterID[1]+1)*self.Step[1]):
                          __ClusterHitsTemp.append([(s[1]-(self.ClusterID[0]*self.Step[0]))/self.Step[2],(s[2]-(self.ClusterID[1]*self.Step[1]))/self.Step[2], (s[3]-(self.ClusterID[2]*self.Step[2]))/self.Step[2],((s[4])+1)/2, ((s[5])+1)/2])
                          self.ClusterHitIDs.append(s[0])
                          self.ClusterHits.append(s)
           self.ClusterSize=len(__ClusterHitsTemp)
           self.RawClusterNodes=__ClusterHitsTemp #Avoiding importing torch without a good reason (reduce load on the HTCOndor initiative)
           del __ClusterHitsTemp

      def GenerateSeeds(self, cut_dt, cut_dr, cut_dz, l, MaxEdges, SeedFlowLog): #Decorate hit information
           #New workaround: instead of a painful Pandas outer join a loop over list is performed
           _Hits=self.ClusterHits
           _Hits= sorted(_Hits, key=lambda x: x[3], reverse=True) #Sorting by z
           _Seeds=[] #Initiate the empty container for seeds
           _sp,_ep=HitCluster.SplitJob(l,MaxEdges,self.ClusterSize)


           _SeedFlowLabels=['All','Excluding self-permutations', 'Excluding duplicates','Excluding seeds on the same plate', 'Cut on dz', 'Cut on dtx', 'Cut on dty' , 'Cut on drx', 'Cut on dry', 'MLP filter', 'GNN filter', 'Tracking process' ]
           _SeedFlowValuesAll=[len(_Hits)**2,(len(_Hits)**2)-len(_Hits), int(((len(_Hits)**2)-len(_Hits))/2), 0, 0, 0, 0, 0, 0, 0, 0, 0]
           _SeedFlowValuesTrue=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

           if SeedFlowLog:

               for l in range(_sp,min(_ep,self.ClusterSize-1)):
                    for r in range(l+1,len(_Hits)):
                        FitSeed=HitCluster.FitTrackSeed(_Hits[l],_Hits[r],cut_dt,cut_dr,cut_dz)
                        _SeedFlowValuesAll = [a + b for a, b in zip(_SeedFlowValuesAll, FitSeed[1])]
                        _SeedFlowValuesTrue = [a + b for a, b in zip(_SeedFlowValuesTrue, FitSeed[2])]
                        if FitSeed[0]:
                           # [HitID, x , y , z, tx, ty, HitID, x , y , z, tx, ty]
                           #TH = _Hits[l][:-1]+_Hits[r][:-1]
                           h1,h2,x1,x2,y1,y2,z1,z2, tx1, tx2, ty1, ty2, l1, l2=_Hits[r][0],_Hits[l][0],_Hits[r][1],_Hits[l][1],_Hits[r][2],_Hits[l][2],_Hits[r][3],_Hits[l][3],_Hits[r][4],_Hits[l][4],_Hits[r][5],_Hits[l][5],_Hits[r][6],_Hits[l][6]
                           print(h1,h2)
                           print(x1,x2,y1,y2,z1,z2)
                           print(tx1, tx2, ty1, ty2)
                           print(l1, l2)
                           # _dl= (math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2) + ((TH[9]-TH[3])**2)))
                           # for i in range(1,4):TH[i]=TH[i]/self.Step[2]
                           # for i in range(7,10):TH[i]=TH[i]/self.Step[2]
                           # TH.append('N/A')
                           # TH.append((math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2) + ((TH[9]-TH[3])**2))))
                           # TH.append(math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2)))
                           # TH.append(abs(TH[9]-TH[3]))
                           # TH.append(abs(TH[4]-TH[10]))
                           # TH.append(abs(TH[5]-TH[11]))
                           # del TH[1:6]
                           # del TH[2:7]
                           # print(TH)
                           x=input()
                               #_Seeds.append(_Hits[l]+_Hits[r])

               print(_SeedFlowValuesAll)
               print(_SeedFlowValuesTrue)





           # print('Number of all  hit combinations passing fiducial cuts:',len(_Tot_Hits))
           # self.HitPairs=[]
           # for TH in _Tot_Hits:
           #     self.HitPairs.append([TH[0],TH[3], TH[6],TH[9]])
           # for TH in _Tot_Hits:
           #     for i in range(1,4):TH[i]=TH[i]/self.Step[2]
           #     for i in range(7,10):TH[i]=TH[i]/self.Step[2]
           #     if len(MCHits)>0:
           #          TH.append(HitCluster.LabelLinks(TH,MCHits))
           #     else:
           #          TH.append('N/A')
           #     TH.append((math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2) + ((TH[9]-TH[3])**2))))
           #     TH.append(math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2)))
           #     TH.append(abs(TH[9]-TH[3]))
           #     TH.append(abs(TH[4]-TH[10]))
           #     TH.append(abs(TH[5]-TH[11]))
           #     del TH[1:6]
           #     del TH[2:7]
           # self.RawEdgeGraph=_Tot_Hits
           return True
           #  def GenerateSeeds(self, cut_dt, cut_dr, cut_dz, SeedClassifier='N/A', l=-1, MaxEdges=-1): #Decorate hit information
           # #New workaround: instead of a painful Pandas outer join a loop over list is performed
           # _Hits=self.ClusterHits
           # _Hits= sorted(_Hits, key=lambda x: x[3], reverse=True) #Sorting by z
           # _Tot_Hits=[]
           # print('Initial number of all possible hit combinations is:',len(_Hits)**2)
           # print('Number of all possible hit combinations without self-permutations:',(len(_Hits)**2)-len(_Hits))
           # print('Number of all possible hit  combinations with enforced one-directionality:',int(((len(_Hits)**2)-len(_Hits))/2))
           # if l>-1 and MaxEdges>-1:
           #     n_edg=len(self.RawClusterGraph)
           #     job_iter=0
           #     acc_edg=0
           #     start_pos=0
           #     end_pos=n_edg
           #     for n_e in range(1,n_edg+1):
           #         acc_edg+=n_edg-n_e
           #         if acc_edg>=MaxEdges:
           #             job_iter+=1
           #             acc_edg=0
           #             if job_iter==l+1:
           #                end_pos=n_e
           #                break
           #             else:
           #                start_pos=n_e
           # else:
           #     start_pos=0
           #     end_pos=len(_Hits)-1
           # for l in range(start_pos,min(end_pos,len(_Hits)-1)):
           #     for r in range(l+1,len(_Hits)):
           #         if HitCluster.JoinHits(_Hits[l],_Hits[r],cut_dt,cut_dr,cut_dz):
           #                _Tot_Hits.append(_Hits[l]+_Hits[r])
           #
           # print('Number of all  hit combinations passing fiducial cuts:',len(_Tot_Hits))
           # self.HitPairs=[]
           # for TH in _Tot_Hits:
           #     self.HitPairs.append([TH[0],TH[3], TH[6],TH[9]])
           # for TH in _Tot_Hits:
           #     for i in range(1,4):TH[i]=TH[i]/self.Step[2]
           #     for i in range(7,10):TH[i]=TH[i]/self.Step[2]
           #     if len(MCHits)>0:
           #          TH.append(HitCluster.LabelLinks(TH,MCHits))
           #     else:
           #          TH.append('N/A')
           #     TH.append((math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2) + ((TH[9]-TH[3])**2))))
           #     TH.append(math.sqrt(((TH[8]-TH[2])**2) + ((TH[7]-TH[1])**2)))
           #     TH.append(abs(TH[9]-TH[3]))
           #     TH.append(abs(TH[4]-TH[10]))
           #     TH.append(abs(TH[5]-TH[11]))
           #     del TH[1:6]
           #     del TH[2:7]
           # self.RawEdgeGraph=_Tot_Hits
           # return True
      def GenerateEdgeGraph(self, MCHits): #Decorate hit information
           import torch
           from torch_geometric.data import Data
           self.ClusterGraph=Data(x=torch.Tensor(self.RawClusterGraph), edge_index=None, y=None)
           self.ClusterGraph.edge_index=torch.tensor((HitCluster.GenerateLinks(self.RawEdgeGraph,self.ClusterHitIDs)))
           self.ClusterGraph.edge_attr=torch.tensor((HitCluster.GenerateEdgeAttributes(self.RawEdgeGraph)))
           if len(MCHits)>0:
            self.ClusterGraph.y=torch.tensor((HitCluster.GenerateEdgeLabels(self.RawEdgeGraph)))
           self.edges=[]
           for r in self.RawEdgeGraph:
               self.edges.append(r[:2])
           if len(self.ClusterGraph.edge_attr)>0:
               return True
           else:
               return False
      @staticmethod

      def SplitJob(_l,_MaxEdges, _n_hits):
        if _l>-1 and _MaxEdges>-1:
               _job_iter=0
               _acc_edg=0
               _start_pos=0
               _end_pos=_n_hits
               for _n_e in range(1,_n_hits+1):
                   _acc_edg+=_n_hits-_n_e
                   if _acc_edg>=_MaxEdges:
                       _job_iter+=1
                       _acc_edg=0
                       if _job_iter==_l+1:
                          _end_pos=_n_e
                          break
                       else:
                          _start_pos=_n_e
               return _start_pos, _end_pos
        else:
            return 0, _n_hits-1

      def GenerateLinks(_input,_ClusterID):
          _Top=[]
          _Bottom=[]
          for ip in _input:
              _Top.append(_ClusterID.index(ip[0]))
              _Bottom.append(_ClusterID.index(ip[1]))
          return [_Top,_Bottom]
      def LabelLinks(_hit,_MCHits):
          for h1 in _MCHits:
              if _hit[0]==h1[0]:
                 for h2 in _MCHits:
                     if _hit[6]==h2[0]:
                        if h1[1]==h2[1]:
                            return int(h1[1].__contains__('--')==False)
                        else:
                            return 0
          return 0
      def FitSeed(_H1, _H2, _cdt, _cdr, _cdz):
          if _H1[3]==_H2[3]: #Ensuring hit combinations are on different plates
              return False
          elif abs(_H1[3]-_H2[3])>=_cdz:
              return False
          else:
              if abs(_H1[4]-_H2[4])>=_cdt:
                  return False
              else:
                  if abs(_H1[5]-_H2[5])>=_cdt:
                      return False
                  else:
                      if abs(_H2[1]-(_H1[1]+(_H1[4]*(_H2[3]-_H1[3]))))>=_cdr:
                         return False
                      else:
                          if abs(_H2[2]-(_H1[2]+(_H1[5]*(_H2[3]-_H1[3]))))>=_cdr:
                             return False
          return True

      def FitTrackSeed(_H1, _H2, _cdt, _cdr, _cdz): #A more involved option that involves producing the seed cutflow and the truth distribution if the MC data available.
          _ts=int(((_H1[6]==_H2[6]) and ('--' not in _H1[6])))
          if _H1[3]==_H2[3]: #Ensuring hit combinations are on different plates
                return False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [_ts, _ts, _ts, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          elif abs(_H1[3]-_H2[3])>=_cdz:
              return False, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [_ts, _ts, _ts, _ts, 0, 0, 0, 0, 0, 0, 0, 0]
          else:
              if abs(_H1[4]-_H2[4])>=_cdt:
                  return False, [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [_ts, _ts, _ts, _ts, _ts, 0, 0, 0, 0, 0, 0, 0]
              else:
                  if abs(_H1[5]-_H2[5])>=_cdt:
                      return False, [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [_ts, _ts, _ts, _ts, _ts, _ts, 0, 0, 0, 0, 0, 0]
                  else:
                      if abs(_H2[1]-(_H1[1]+(_H1[4]*(_H2[3]-_H1[3]))))>=_cdr:
                         return False, [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], [_ts, _ts, _ts, _ts, _ts, _ts, _ts, 0, 0, 0, 0, 0]
                      else:
                          if abs(_H2[2]-(_H1[2]+(_H1[5]*(_H2[3]-_H1[3]))))>=_cdr:
                             return False, [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [_ts, _ts, _ts, _ts, _ts, _ts, _ts, _ts, 0, 0, 0, 0]
          return True, [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], [_ts, _ts, _ts, _ts, _ts, _ts, _ts, _ts, _ts, 0, 0, 0]

      def GenerateEdgeAttributes(_input):
          _EdgeAttr=[]
          for ip in _input:
              _EdgeAttr.append(ip[3:])
          return _EdgeAttr
      def GenerateEdgeLabels(_input):
          _EdgeLbl=[]
          for ip in _input:
              _EdgeLbl.append(ip[2])
          return _EdgeLbl
      def UnloadClusterGraph(self):
          del self.ClusterGraph
          del self.HitLinks

def ErrorOperations(a,b,a_e,b_e,mode):
    if mode=='+' or mode == '-':
        c_e=math.sqrt((a_e**2) + (b_e**2))
        return(c_e)
    if mode=='*':
        c_e=a*b*math.sqrt(((a_e/a)**2) + ((b_e/b)**2))
        return(c_e)
    if mode=='/':
        c_e=(a/b)*math.sqrt(((a_e/a)**2) + ((b_e/b)**2))
        return(c_e)



