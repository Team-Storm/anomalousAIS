

import pandas as pd
import numpy as np
from math import radians,tan,sin,cos,atan2,sqrt,pi,ceil
import random
import pickle
from sklearn.cluster import DBSCAN

class TrajectoryPoint:
    def __init__(self,mmsi,timeStamp,lat,lng,COG,SOG):
        self.mmsi = mmsi
        self.timeStamp = timeStamp
        self.lat = lat
        self.lng = lng
        self.COG = COG
        self.SOG = SOG
        self.isVisited = False
        self.isCorePoint = False

class Cluster:  
    def __init__(self):
        self.cluster = {} # Dictionary of trajectory points
        self.avgCOG = 0.0
    def calculateAvgDirection(self):
        avgDirection = 0.0
        for k in self.cluster:
            avgDirection += k.COG
        avgDirection /= len(self.cluster)
        return avgDirection

class DBScanSD:
    def __init__(self):
        self.resultCluster = []
        
    def isCorePoint( self , lst , p , eps , minPoints , maxSpd , maxDir , isStopPoint):
        count = 0
        tempList = {}
        for q in lst:
            if(self.densityReachable(p,q,eps,minPoints,maxSpd,maxDir,isStopPoint)):
                count += 1
                tempList[p] = p
                    
        if(count>=minPoints):
            p.isCorePoint = True
            return tempList
        return None
    
    def applyDBScanSD(self,pointList,eps,minPoints,maxSpd,maxDir,isStopPoint):
        for index in range(len(pointList)):
            p = pointList[index]
            if(p.isVisited):
                continue
            p.isVisited = True
            temp = self.isCorePoint(pointList,p,eps,minPoints,maxSpd,maxDir,isStopPoint)
            if(temp!=None):
                c = Cluster()
                c.cluster = temp
                self.resultCluster.append(c)
                
        length = len(self.resultCluster)
        for i in range(length):
            for j in range(length):
                if(i!=j):
                     if(self.mergeCluster(self.resultCluster[i] , self.resultCluster[j])):
                            del self.resultCluster[j]
        return self.resultCluster
    
    def mergeCluster( self , clusterA , clusterB):
        merge = False
        if(len(clusterA.cluster)==0 and len(clusterB.cluster)==0):
            return merge
        for k in clusterB.cluster:
            p = k
            if(p.isCorePoint and p in clusterA.cluster):
                merge = True
                for j in range(len(clusterB.cluster)):
                    clusterA.cluster[clusterB.cluster[j]] = clusterB.cluster[j]
                break
        return merge
    
   
                
    
    def densityReachable(self , p,q,eps,minPoints,maxSpd,maxDir,isStopPoint):
        if(self.gpsDistance(p.lat,p.lng,q.lat,q.lng) <= eps):
            if(isStopPoint):
                return True
            if(abs(p.SOG - q.SOG)<=maxSpd and abs(p.COG-q.COG)<=maxDir):
                return True
        return False
        
    def gpsDistance(self,lat1,lng1,lat2,lng2):
        earthRadius = 3958.75
        dLat = radians(lat2-lat1)
        dLng = radians(lng2-lng1)
        a = sin(dLat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earthRadius * c
        meterConversion = 1609
        return distance*meterConversion
    
class GravityVector:
     def __init__(self,longitude,latitude,COG,SOG,medianDistance):
        self.longitude = longitude
        self.latitude = latitude
        self.COG = COG
        self.SOG = SOG
        self.medianDistance = medianDistance
        
class MappingPoint:
    def __init__(self,longitude,latitude,mappingtude,COG,SOG):
        self.longitude = longitude
        self.latitude = latitude
        self.mappingtude = mappingtude 
        self.COG = COG
        self.SOG = SOG
    def convertPointToMappingPoint(p ,avgCOG ):
        mappingtude1 = 0
        angle = (avgCOG/180) * pi
        if((avgCOG>=0) & (avgCOG<90)):
            mappingtude1 = (p.lng + ((1/tan(angle)) * p.lat)) * sin(angle)
        elif((avgCOG>=270)&(avgCOG<360)):
            mappingtude1 = (p.lat - (tan((pi/2)-angle) * p.lng))* cos((pi/2)-angle)
        elif((avgCOG>=90) & (avgCOG<180)):
            mappingtude1 = ((tan(pi-angle) * p.lng) - p.lat) * cos(pi-angle)
        elif((avgCOG>=180)&(avgCOG<270)):
            mappingtude1 = -((1/tan(angle-pi)) * p.lat + p.lng) * sin(angle-pi)
        mp = MappingPoint(p.lng,p.lat,mappingtude1,p.COG,p.SOG)
        return mp
        
class GravityVectorExtraction:
        
    def extractGravityVector(self,cluster):
        avgCOG = calculateAvgDirection(cluster)
        mpLst = []
        for k in cluster.cluster:
            mp = MappingPoint.convertPointToMappingPoint(k,avgCOG)
            mpLst.append(mp)
        self.insertionSort(mpLst)
        ppL = []
        count=0
        k=0
        sum_x=0
        sum_y=0
        sum_SOG=0
        sum_COG=0
        traPointsTMP = []
        meanDistance=0
        
        while count <= len(mpLst):
            if (count<len(mpLst) and (mpLst[count].mappingtude - mpLst[k].mappingtude)<0.01):
                sum_x = sum_x + mpLst[count].longitude
                sum_y = sum_y + mpLst[count].latitude
                sum_SOG = sum_SOG + mpLst[count].SOG
                sum_COG = sum_COG + mpLst[count].COG
                traPointsTMP.append(mpLst[count])
                count=count+1
            else:
                x=0
                y=0
                sog=0
                cog=0
                x = sum_x/(count-k)
                y = sum_y/(count-k)
                sog = sum_SOG/(count-k)
                cog = sum_COG/(count-k)
                
                distances = []
                
                for i in range(len(traPointsTMP)):
                    lon = traPointsTMP[i].longitude
                    lat = traPointsTMP[i].latitude
                    dist = gpsDistance(lat,lon,y,x)
                
                meanDistance = self.quartile(distances,50)
                
                gv = GravityVector(x,y,cog,sog,meanDistance)
                ppL.append(gv)
                sum_x=0
                sum_y=0
                sum_COG=0
                sum_SOG=0
                k=count
                traPointsTMP = [] 
                if count==len(mpLst):
                    break
        return ppL
    def insertionSort(self,mpl):
        for i in range(len(mpl)):
            k=i
            mp = mpl[i]
            insertAlready = False
            while (mpl[i].mappingtude < mpl[k-1].mappingtude):
                if k==1 :
                    mpl.remove(i)
                    mpl.insert(0,mp)
                    insertAlready = True
                    break
                k=k-1
            if insertAlready==False :
                del mpl[i]
                mpl.insert(k,mp)
    
    def quartile(self,values,lowerPercent):
        if values is None or len(values)==0 :
            ## throw exception
            return -1
        v = []
        v.sort()
        n=0
        
        if len(v)==1 :
            n=0
        else :
            n = (len(v)*lowerPercent)/100
        return v[n]
            
            

def calculateAvgDirection(cluster):
        avgDirection = 0.0
        for i in range(len(cluster.cluster)):
            avgDirection += cluster.cluster[i].COG
        avgDirection /= len(cluster.cluster)
        return avgDirection

def gpsDistance(lat1,lng1,lat2,lng2):
        earthRadius = 3958.75
        dLat = radians(lat2-lat1)
        dLng = radians(lng2-lng1)
        a = sin(dLat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earthRadius * c
        meterConversion = 1609
        return distance*meterConversion

df = pd.read_csv('data.csv')
pointList = []
MovingDataFrame = df[df.SPEEDOVERGROUND > 0.5]

for index, row in MovingDataFrame.iterrows():
     point = TrajectoryPoint(row.ID,row.Timestamp,row.LATITUDE,row.LONGITUDE,row.COURSEOVERGROUND,row.SPEEDOVERGROUND)
     pointList.append(point)
pointList1 = pointList[:3000]
eps = 1000
minPoints = 10
maxSpd = 5.0
maxDir = 5.0
clusterList = DBScanSD().applyDBScanSD(pointList1,eps,minPoints,maxSpd,maxDir,False)

GV =[]
for i in range(len(clusterList)):
    gv = GravityVectorExtraction().extractGravityVector(clusterList[i])
    GV.append(gv)


fileName = "GravityVector"
fileObject = open(fileName,'wb')

pickle.dump(GV,fileObject)
fileObject.close()


# # SSP Extraction


#Extract List of SSP from stopping dataset.Stopping dataset includes points which have SOG<=0.5 Knots

class StoppingPoint:
    def __init__(self,lat,lng,COG,SOG):
        self.lat = lat
        self.lng = lng
        self.COG = COG
        self.SOG = SOG
class StoppingPointCluster:
    def __init__(self,clusterId,points):
        self.clusterId = clusterId
        self.points = points
        

    
def extractSSP(stoppingPointClusters,eps,minPoints):
    #stoppingPointClusters is the list of cluster after applying DBSCAN algorithm on StoppingPoints
    resultSSP = []
    lat1 = 0.0
    lat2 = 1000.0
    lon1 = 0.0
    lon2 = 1000.0
    for k in range(len(stoppingPointClusters)):
        cluster = stoppingPointClusters[k]
        for point in cluster.points:
            lat1 = max(lat1,point.lat)
            lat2 = min(lat2,point.lat)
            lon1 = max(lon1,point.lng)
            lon2 = min(lon2,point.lng)
        area = abs((lat1-lat2) * (lon1-lon2))
        if(area==0):
            sample_size = 1
        else:
            sample_size = ceil(area/(pi*eps*eps))
        
        count = 0
        while(count<sample_size):
            index = random.randint(0,len(cluster.points)-1)
            p = cluster.points[index]
            if(len(resultSSP)==0):
                resultSSP.append(p)
            else:
                nearFlag = False
                for q in resultSSP:
                    if(gpsDistance(p.lat,p.lng,q.lat,q.lng) < eps):
                        nearFlag = True
                        break
                if(nearFlag==False):
                    resultSSP.append(p)
            count+=1        
    return resultSSP

stoppingData = df[df.SPEEDOVERGROUND<=0.5]


dbscan = DBSCAN(eps=1000,min_samples=10).fit_predict(stoppingData)
stoppingData['label'] = dbscan
stoppingData.sort_values(by = 'label' , inplace=True)

clusterList = []
cluster = []
prevLabel = stoppingData.iloc[0,:].label
for _, row in stoppingData.iterrows():
     stoppingPoint = StoppingPoint(row.LATITUDE , row.LONGITUDE , row.COURSEOVERGROUND , row.SPEEDOVERGROUND)
     if(prevLabel==row.label):
        cluster.append(stoppingPoint)
     else:
        stoppingCluster = StoppingPointCluster(prevLabel,cluster)
        clusterList.append(stoppingCluster)
        cluster = []
        prevLabel = row.label
stoppingCluster = StoppingPointCluster(prevLabel,cluster)
clusterList.append(stoppingCluster)


resultSSP = extractSSP(clusterList,1000,10)


clusterList.append(stoppingCluster)
fileName = "SSPVector"
fileObject = open(fileName,'wb')

pickle.dump(clusterList,fileObject)
fileObject.close()




