# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:34:40 2017

@author: GangTimes
"""

import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
import  Pedigree as pd
import copy
np.random.seed(1)

class Kmeans:
    def __init__(self,data):
        self.shuffle(data)
        self.limit=3
        self.error=0.1
        self.cls=dict()
        self.centers=dict()
        self.get_matrix()
   
        
    def get_matrix(self):
        rows=len(self.data)-1
        cols=len(self.data[0])-1
        self.mat=np.matrix(np.zeros((rows,cols)))
        for di in self.data:
            if di==0:
                continue
            self.mat[di-1]=self.data[di][:-1]
        
    def shuffle(self,data):
        self.rows=len(data)
        self.data=dict()
        
        self.data[0]=data[0]
        rl=[]
        [rl.append(i) for i in range(1,self.rows)]
        shuffle(rl)
        for di in range(1,self.rows):
            self.data[di]=data[rl[di-1]]
                

    
    def finish_class(self):
        self.data[0].append('T')
        count=1
        indexs=dict()
        for i in self.cls:
            indexs[i]=count
            count+=1
            
        for ci in self.cls:
            for di in self.cls[ci]:
                self.data[di].append(str(indexs[ci]))
        
        
    def plot_data(self):
        color=['r','b','g','y','k']
        mydata=dict()
        
        for di in self.data.keys():
            if di==0:
                continue
            
            key=self.data[di][-1]
            
            if key not in mydata.keys():
                mydata[key]=np.matrix(self.data[di][:-2])
                continue
            
            temp=np.matrix(self.data[di][:-2])
            mydata[key]=np.vstack((mydata[key],temp))
        
        for ik in mydata.keys():     
           plt.plot(mydata[ik][:,0],mydata[ik][:,1],'*'+color[int(ik)-1])
           
           
    def sample_data(self):
        temp=dict()
        num=3
        count=1
        temp[0]=self.data[0]
        for di in self.data:
            if di==0:
                continue
            if di%num==0:
                temp[count]=copy.deepcopy(self.data[di])
                count+=1
        
        return temp
    
    def init_center(self):
        temp=self.sample_data()
        pedigree=pd.Cluster(temp)
        pedigree.limit=self.limit
        pedigree.cluster()
        self.centers=pedigree.centers
    
    def centers_dis(self,index):
        distance=dict()
        
        
        for ci in self.centers:
            error=self.centers[ci]-self.mat[index-1,:]
            dis=np.exp(-1*np.dot(error,error.T))
            distance[ci]=dis[0,0]
                    
        return distance


    
    def min_dict(self,dic):
        center=sorted(dic.items(),key=lambda x:x[1],reverse=False)
        return center[0][0]
    def max_dict(self,dic):
        center=sorted(dic.items(),key=lambda x:x[1],reverse=True)
        return center[0][0]
    
    
    def append_class(self,di,cls):
        
        for ci in self.cls:
            if di in self.cls[ci]:
                self.cls[ci].remove(di)
            
            if cls==ci:
                if di not in self.cls[cls]:
                    self.cls[cls].append(di)
    def update_center(self):
        col=self.mat.shape[1]
        for ic in self.cls:
            temp=np.matrix(np.zeros((1,col)))
            for ir in self.cls[ic]:
                
                data=self.mat[ir-1,:]
                temp+=data
            
            
        
            center=temp/len(self.cls[ic])
            self.centers[ic]=center
    def center_error(self,pre):
        cur=self.centers
        temp=0
        for ic in cur:
            error=cur[ic]-pre[ic]
            dis=np.dot(error,error.T)
            temp+=dis[0,0]
            
        return temp/len(self.centers)
    
    def cluster(self):
        self.init_center()
        while(True):
            
            for di in self.data:
                if di==0:
                    continue
                dis=self.centers_dis(di)
                cls=self.max_dict(dis)
                self.cls[cls]=self.cls.get(cls,[])
                self.append_class(di,cls)
            
            pre=copy.deepcopy(self.centers)
            self.update_center()
            error=self.center_error(pre)

            if error<=self.error:
                break
            
            
        
        self.finish_class()
        self.plot_data() 
        
    
def create_data():
    n1=28
    n2=12
    n3=16

    c1=1*np.matrix(np.random.randn(n1,2))+np.matrix([1,1])
    c2=1.5*np.matrix(np.random.randn(n2,2))+np.matrix([3,4])
    c3=0.5*np.matrix(np.random.randn(n3,2))+np.matrix([5,2])
    c=np.vstack((c1,c2,c3))
    
    rows=c.shape[0]
    cols=c.shape[1]
    data=dict()
    data[0]=['X','Y','V']
    for ri in range(rows):
        data[ri+1]=[]
        for ci in range(cols):
            data[ri+1].append(c[ri,ci])
        
        if ri<=n1-1:
            data[ri+1].append('1')
        elif ri>=n1 and ri<=n1+n2-1:
            data[ri+1].append('2')
        else:
            data[ri+1].append('3')
    
    write_class(data)
                
def write_class(data):
    fid=open('data.txt','wt')
    cols=len(data[0])
    for di in data.keys():
        fid.write("%4d"%(di))
        if di==0:
            for ci in range(cols):
                fid.write(",%16s"%(data[di][ci]))
            fid.write("\n")
            continue
        
        for ci in range(cols):
            fid.write(",%16s"%(str(data[di][ci])))
        fid.write("\n")    
    fid.close()
    
def read_data(file_name):
    file=open(file_name)
    lines=file.readlines()
    data=dict()
    for line in lines:
  
        temp=line.strip('\n').split(',')
        num,temp=transfer(temp)
        data[num]=temp
    return data

def transfer(ls):
    num=int(ls[0].strip())
    temp=[]
    if num==0:
        [temp.append(li.strip()) for li in ls[1:]]
        return num,temp

    [temp.append(float(li.strip())) for li in ls[1:-1]]
    temp.append(ls[-1].strip())
    return num,temp

def plot_data(data):
    mydata=dict()
    for di in data.keys():
        if di==0:
            continue
        key=data[di][-1]
        if key not in mydata.keys():
            mydata[key]=np.matrix(data[di][:-1])
            continue
        temp=np.matrix(data[di][:-1])
        mydata[key]=np.vstack((mydata[key],temp))
    
    plt.plot(mydata['1'][:,0],mydata['1'][:,1],'or')
    plt.plot(mydata['2'][:,0],mydata['2'][:,1],'ob')
    plt.plot(mydata['3'][:,0],mydata['3'][:,1],'ok')

if __name__=='__main__':
    create_data()
    data=read_data('data.txt')
    plot_data(data)
    cluster=Kmeans(data)

    cluster.cluster()