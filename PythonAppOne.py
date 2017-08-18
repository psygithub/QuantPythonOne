import datetime
from matplotlib import finance, mlab
import numpy as np
import matplotlib.pyplot as plt 
import urllib
from  matplotlib.finance import quotes_historical_yahoo_ochl as yahoo 
from  datetime import date
import pandas as pd
import os
import tushare as ts

def loadTushare_data(code,startdate,enddate):
    df = ts.get_hist_data(code,startdate,enddate,)
    print (df)
    return df 

def writeToCsv(name,data):
    dir='D:/Python36/Stock/'
    fileName= dir+ name + ".csv"
    if not os.path.exists(dir):
       os.makedirs(dir)
    data.to_csv(fileName)    
    

def writeToExl(name,data):
    dir='D:/Python36/Stock/'
    fileName= dir+ name + ".xlsx"
    if not os.path.exists(dir):
       os.makedirs(dir)
    data.to_excel(fileName)    

def readFromCsv(name):
    dir='D:/Python36/Stock/'
    fileName= dir+ name + ".csv"
    if os.path.exists(fileName):
       data=pd.read_csv(fileName,na_values=['NA'])
       return data
    return pd.DataFrame();

def readFromExl(name):
    dir='D:/Python36/Stock/'
    fileName= dir+ name + ".xlsx"
    if os.path.exists(fileName):
       data=pd.read_excel(fileName,na_values=['NA'])
       return data
    return pd.DataFrame();
    

def show_data(datalist):
    
    fig=plt.figure(figsize=(12,4),frameon=False) 
    plt.subplots_adjust(right=0.98,left=0.05,top=0.98)
    #xs = np.linspace(0, 1, 20); ys = np.sin(xs)
    #axes = fig.add_subplot(1,1,1)
    #axes.plot(xs, ys)
    #fig.tight_layout()

    #绘制方格
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    #设置坐标标签
    plt.xlabel('Date')
    plt.ylabel('p_change')
    #将x坐标日期进行倾斜
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    for d in datalist:
          plt.plot(d[1], d[2],label=d[0])
    plt.legend(loc='upper left',)
    
    plt.show()

def show_AverageLine(lable,dates,dataList):    
    fig=plt.figure(figsize=(12,4),frameon=False) 
    plt.subplots_adjust(right=0.98,left=0.05,top=0.98)
    #xs = np.linspace(0, 1, 20); ys = np.sin(xs)
    #axes = fig.add_subplot(1,1,1)
    #axes.plot(xs, ys)
    #fig.tight_layout()

    #绘制方格
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    #设置坐标标签
    plt.xlabel('Date')
    plt.ylabel('p_change')
    #将x坐标日期进行倾斜
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    plt.plot(dates, dataList,label=lable)
    plt.legend(loc='upper left',)
    
    plt.show()
def showMatlab():
       x = np.linspace(0, 10, 1000)
       y = np.sin(x)
       z = np.cos(x ** 2)

       plt.figure(figsize=(8,4)) 

       plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2) 
       plt.plot(x,z,"b--",label="$cos(x^2)$") 
       plt.legend(loc='upper left',)
       plt.xlabel("Time(s)") 
       plt.ylabel("Volt")
       plt.title("PyPlot First Example")
       plt.ylim(-1.2,1.2)
       plt.legend()

       plt.show() 
    
#def getPricePercent(hprc,lprc,oprc,cprc):      
#      for i in range(hprc.len):
            

def getStock(codes,start,end):
     #code = '000615',"hs300"
     datalist = []
     for c in codes:
          if c=='':
             break
          fileName=c+"_"+start.replace('-','')+"-"+end.replace('-','')
          df = readFromCsv(fileName)
          if  df.empty:
              df = loadTushare_data(c,start,end)    
              writeToCsv(fileName,df)
              #重新读硬盘上的数据
              df = readFromCsv(fileName)
          dayarr = []
          price=[]
          for i in range(df.index.size): 
                dateStr = df.date[i] 
                year = int(dateStr[0:4])
                month = int(dateStr[5:7])
                day = int(dateStr[8:])
                curdate = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
                dayarr.append(curdate)
                hprc=df.high
                lprc=df.low
                oprc=df.open
                cprc=df.close
                #p=[df.open[i],df.close[i],df.high[i],df.low[i],df.p_change[i],df.volume[i]]
                #price.append(p)
                #price=df.close           
          #price=[df.open,df.close,df.high,df.low,df.p_change,df.volume]
          #自定义要比较的价格,c:名称，dayarr:日期，price:比较的价格
          data = [c,dayarr,df.open,df.close,df.high,df.low,df.p_change,df.volume]
          datalist.append(data)
     return datalist

# 斜率
def GetGardientRatioPara(startP,endP,days):
    curRt=(startP-endP)/days *100    
    return round(curRt,2)
#每天10%的斜率
def GetTenPctRatio(startP,days):
    curRt=1
    for d in days:
        curRt=curRt*1.1
    curRt=startP*((curRt/days)*100)
    return round(curRt,2)

#avDay:平均线的天数，
def AverageLine(avDay,dataList):
    pStartDay=0#每个时段的开始下标
    closeP=dataList
    avSumP=0#时段平均总价格
    avLineP=0#时段平均价格
    avLine=[]#平均线价格数组
    for i in range(len(closeP)):
        if i<avDay-1: 
             avLineP=closeP[i]
        else:
            if i>avDay:
                pStartDay=i-avDay+1   
            avSumP=0         
            for j in range(avDay):
                avSumP+=closeP[pStartDay]
                pStartDay+=1
            avLineP=avSumP/avDay
        avLine.append(avLineP)        
    return avLine

def kdjLine(curP,lowP,highP,n,m1,m2):
    size=len(curP)
    tmpLowP=[]
    tmpHighP=[]
    rsv=[]
    ks=[]
    ds=[]
    js=[]
    k=0
    d=0
    j=0
    try:
      for i in range(size):
        if i<n-1:
            rsv.append(curP[i])
        else:
            if len(tmpLowP)>0:
                tmpLowP.remove(tmpLowP[0])            
            tmpLowP.append(lowP[i])
            if len(tmpHighP):
                tmpHighP.remove(tmpHighP[0])            
            tmpHighP.append(highP[i])
            lp=GetLowPPastDays(tmpLowP)
            hp=GetHighPastDays(tmpHighP)
            r=((curP[i]-lp)/(hp-lp))*100
            rsv.append(r)
        if i==0:
            k=rsv[0]
            d=k
        else:
            #k=rsv/3+(2*(ks[i-1]))/3
            #d=k/3+(2*(ds([-1]))/3
            k=(m1* rsv[i]+(n-m1)*ks[i-1])/n
            d=(m2*k+(n-m2)*ds[i-1])/n
            j=3*d-2*k
        ks.append(k)
        ds.append(d)
        js.append(j)
        
    except Exception as e:      
        str=e.args
    return [ks,ds,js]

def show_KDJLine(dates,ks,ds,js):    
    fig=plt.figure(figsize=(12,4),frameon=False) 
    plt.subplots_adjust(right=0.98,left=0.05,top=0.98)
    #xs = np.linspace(0, 1, 20); ys = np.sin(xs)
    #axes = fig.add_subplot(1,1,1)
    #axes.plot(xs, ys)
    #fig.tight_layout()

    #绘制方格
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    #设置坐标标签
    plt.xlabel('Date')
    plt.ylabel('p_change')
    #将x坐标日期进行倾斜
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    plt.plot(dates, ks,label='K_line')
    plt.plot(dates, ds,label='D_line')
    #plt.plot(dates, js,label='J_line')
    plt.legend(loc='upper left',)
    
    plt.show()

def GetLowPPastDays(lowP):
    cP=0
    nextP=0
    lP=0
    size=len(lowP)
    for i in range(size):
        cp=lowP[i]
        if i<size-1:
            nextP=lowP[i+1]
        if cp>nextP:
            lP=nextP
        else:
            lP=cP
        i+=2
    return lP

def GetHighPastDays(highP):
    cP=0
    nextP=0
    lP=0
    size=len(highP)
    for i in range(size):
        cp=highP[i]
        if i<size-1:
            nextP=highP[i+1]
        if cp<nextP:
            lP=nextP
        else:
            lP=cP
        i+=2
    return lP

today = datetime.datetime.today();
start = datetime.datetime(today.year-1,today.month,today.day)
#showMatlab()
st=start.strftime("%Y-%m-%d")
ed=today.strftime("%Y-%m-%d")
codes='002128',''
datalist=getStock(codes,st,ed)
averageList=AverageLine(10,datalist[0][3])
dates=datalist[0][1]
avg=['20Tavg',dates,averageList]
close=['收盘价',dates,datalist[0][3]]
list=[]
list.append(avg)
list.append(close)
curPs=datalist[0][3]
hightPs=datalist[0][4]
lowPs=datalist[0][5]
kdj=kdjLine(curPs,lowPs,hightPs,20,3,3)
show_KDJLine(dates,kdj[0],kdj[1],kdj[2])
#show_AverageLine(datalist[0][0],datalist[0][1],averageList)
#show_data(list)
#show_data(datalist)