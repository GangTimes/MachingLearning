# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 23:15:28 2017

@author: GangTimes
"""
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
np.random.seed(1)

class NearFun:
    def __init__(self,data):
        self.shuffle(data)
        self.get_matrix()
        self.dis_matrix()
        self.near_matrix()
        self.coeff_matrix()
        print(self.dis_mat)
        print(self.near_two)
        print(self.near_one)
        print(self.coeff_mat)
    def out_class(self,key):
        flag=True
        for keys in self.cls:
            if key in self.cls[keys]:
                flag=False
                break
            
        return flag
    def scan_rows(self,col,row):
        rows=self.mat.shape[0]
        
        for ic in range(col,rows):
            if self.coeff_mat[row,ic]==0:
                return True,ic
        return False,0
    
    def scan_cols(self,col,row):
        rows=self.mat.shape[0]
        
        for ir in range(row,rows):
            if self.coeff_mat[ir,col]==0:
                return True,ir
        return False,0
    
    def init_class(self):
        rows=self.mat.shape[0]
        self.cls=dict()
        count=0
        for ir in range(rows):
            flag=self.out_class(ir+1)
            if flag==True:
                count+=1
                col=ir
                cls=[]
                row=col
                flag2=True
                while(True):
                    if flag2==False:
                        break
                    cls.append(col+1)
                    flag2,row=self.scan_cols(col,row+1)
                    if flag2==False:
                        break
                    cls.append(row+1)
                    flag2,col=self.scan_rows(col+1,row)
                
                self.cls[count]=cls
                    
                 
    def cluster(self):
        self.init_class()
        count=0
        while(True):
            flag=False
            for ikey in self.cls:
                max1=self.max_in(ikey)
                count+=1
                for jkey in self.cls:
                    if jkey==ikey:
                        continue
                    
                    max2=self.max_in(jkey)
                    max12=self.max_out(ikey,jkey)
                    
                    if max1>max12 or max2>max12:
                        self.cls[ikey]=self.cls[ikey]+self.cls[jkey]
                        del self.cls[jkey]
                        flag=True
                        count=0
                        break
                if flag==True:
                    break
            if count==len(self.cls):
                break
                
                        
   
                
    def max_out(self,key1,key2):
        value=0
        for ir in self.cls[key1]:
            for ic in self.cls[key2]:
                temp=self.coeff_mat[ir-1,ic-1]
                if value<=temp:
                    value=temp
        
        return value
            
    def max_in(self,key):
        value=0
        for ir in self.cls[key]:
            for ic in self.cls[key]:
                if ir==ic:
                    temp=0
                else:
                    temp=self.coeff_mat[ir-1,ic-1]
                if value<=temp:
                    value=temp
        
        return value
    def dis_matrix(self):
        rows=len(self.data)
        self.dis_mat=np.matrix(np.zeros((rows-1,rows-1)))
        for ir in range(rows-1):
            x1=self.mat[ir,:]
            for ic in range(rows-1):
                x2=self.mat[ic,:]
                dis=np.dot((x1-x2),(x1-x2).T)
                self.dis_mat[ir,ic]=np.sqrt(dis[0,0])
                
    def order(row,col):
        pass
    def near_matrix(self):
        rows=self.dis_mat.shape[0]
        self.near_one=np.matrix(np.zeros((rows,rows)),dtype=int)
        self.near_two=np.matrix(np.zeros((rows,rows)),dtype=int)
        for ir in range(rows):
            tempr1=self.dis_mat[ir,:]
            temps1=tempr1.argsort()
            
            tempr2=self.dis_mat[:,ir]
            temps2=tempr2.T.argsort()
            
            for ic in range(rows):
                self.near_one[ir,temps1[0,ic]]=ic
                self.near_two[temps2[0,ic],ir]=ic

                         
    def coeff_matrix(self):
        rows=self.dis_mat.shape[0]
        self.coeff_mat=np.matrix(np.zeros((rows,rows)),dtype=int)
        
        for ir in range(rows):
            for ic in range(rows):
                if ir==ic:
                    self.coeff_mat[ir,ic]=2*rows
                    continue
                self.coeff_mat[ir,ic]=self.near_one[ir,ic]+self.near_two[ic,ir]-2
                              
                             
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
            self.data[di]=data[di]
            
def create_data():
    n1=4
    n2=6
    n3=4

    c1=1*np.matrix(np.random.rand(n1,2))+np.matrix([1,1])
    #c2=1.5*np.matrix(np.random.rand(n2,2))+np.matrix([3,4])
    c3=0.5*np.matrix(np.random.rand(n3,2))+np.matrix([5,2])
    c=np.vstack((c1,c3))
    
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
    #plt.plot(mydata['3'][:,0],mydata['3'][:,1],'ok')

if __name__=='__main__':
    #create_data()
    data=read_data('data.txt')
    plot_data(data)
    cluster=NearFun(data)

    cluster.cluster()
    print(cluster.cls)