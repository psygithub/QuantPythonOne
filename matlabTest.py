from matplotlib import finance, mlab
import matplotlib.pyplot as plt
import numpy as np
import urllib
from  datetime import date
import pandas as pd
import os
import tushare as ts
import datetime

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

def readFromCsv(name):
    dir='D:/Python36/Stock/'
    fileName= dir+ name + ".csv"
    if os.path.exists(fileName):
       data=pd.read_csv(fileName,na_values=['NA'])
       return data
    return pd.DataFrame();

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
          dayarr=[]
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
            tmpLowP.append(lowP[i])
            tmpHighP.append(highP[i])
        else:
            if len(tmpLowP)>0:
                tmpLowP.remove(tmpLowP[0])
            tmpLowP.append(lowP[i])
            if len(tmpHighP)>0:
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
    st=dates[len(dates)-1]
    ed=dates[0]
    aias=plt.axis()
    aias=plt.axis([st,ed,0,100])
    

    plt.show()

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
            pStartDay=0
            for j in range(avDay):
                if(i==10 and j==2):
                    print(i,j)
                avSumP+=round(closeP[pStartDay],2)
                pStartDay+=1
            avLineP=avSumP/avDay
        avLine.append(avLineP)
    return avLine
def GetLowPPastDays(lowP):
    cP=lowP[0]
    lP=lowP[0]
    size=len(lowP)
    for i in range(size):
        cP=lowP[i]
        if lP>cP:
            lP=cP
        if lP==0:
            lP=1
    return lP

def GetHighPastDays(highP):
    cP=highP[0]
    hp=highP[0]
    size=len(highP)
    for i in range(size):
        cP=highP[i]
        if hp<cP:
            hp=cP
    return hp

today = datetime.datetime(2017,9,8)
start = datetime.datetime(2016,8,17)
#showMatlab()
st=start.strftime("%Y-%m-%d")
ed=today.strftime("%Y-%m-%d")
codes='300685',''
datalist=getStock(codes,st,ed)
averageList=AverageLine(10,datalist[0][3])
dates=datalist[0][1]
#avg=['20Tavg',dates,averageList]
#close=['收盘价',dates,datalist[0][3]]
# list=[]
# list.append(avg)
# list.append(close)
curPs=datalist[0][3]
hightPs=datalist[0][4]
lowPs=datalist[0][5]
kdj=kdjLine(curPs,lowPs,hightPs,20,3,3)
show_KDJLine(dates,kdj[0],kdj[1],kdj[2])
