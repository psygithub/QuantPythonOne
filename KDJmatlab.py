import datetime
from matplotlib import finance, mlab
import numpy as np
import matplotlib.pyplot as plt 
from  datetime import date
import pandas as pd
import os
import tushare as ts
import pymongo
from pymongo import MongoClient
import json  

class KDJ_method:
    def __init__(self):
        pass

    def show_data(self,datalist):
    
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

    def show_AverageLine(self,lable,dates,dataList):
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

    def showMatlab(self):
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
            

    def formatMatLab(self,code,df):        
        #code = '000615',"hs300"
        datalist = []         
        dayarr = []
        price=[]        
        for i in range(df.index.size): 
            dateStr = df.date[i] 
            year = int(dateStr[0:4])
            month = int(dateStr[5:7])
            day = int(dateStr[8:])
            curdate = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
            dayarr.append(curdate)
                # hprc=df.high
                # lprc=df.low
                # oprc=df.open
                # cprc=df.close
                #p=[df.open[i],df.close[i],df.high[i],df.low[i],df.p_change[i],df.volume[i]]
                #price.append(p)
                #price=df.close           
                #price=[df.open,df.close,df.high,df.low,df.p_change,df.volume]
          #自定义要比较的价格,c:名称，dayarr:日期，price:比较的价格
        data = [code,dayarr,df.open.values,df.close.values,df.high.values,df.low.values,df.p_change.values,df.volume.values]
        datalist.append(data)
        return datalist

    def formatJson(self,code,df):        
     #code = '000615',"hs300"
        datalist = []
        jsonList=[]
        for i in range(df.index.size):
            stk=StockClass()
            stk.date=df.date[i] 
            stk.open=df.open[i]
            stk.close=df.close[i]
            stk.high=df.high[i]     
            stk.low=df.low[i]
            stk.p_change=df.p_change[i]
            stk.price_change=df.price_change[i]
            stk.volume=df.volume[i]
            stk.ma5=df.ma5[i]
            stk.ma10=df.ma10[i]
            stk.ma20=df.ma20[i]
            stk.v_ma5=df.v_ma5[i]
            stk.v_ma10=df.v_ma10[i]
            stk.v_ma20=df.v_ma20[i]
            stk.turnover=df.turnover[i]
            strJson=json.dumps(stk,default=lambda obj: obj.__dict__)
            obj=json.loads(strJson,object_hook=self.dict2obj)
            jsonList.append(obj)
        data = [code,jsonList]
        datalist.append(data)
        return datalist
   
    def obj2dict(self,obj):
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

    def dict2obj(self,d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items())
            instance = class_(**args)
        else:
            instance = d
        return instance
    # 斜率
    def GetGardientRatioPara(self,startP,endP,days):
        curRt=(startP-endP)/days *100    
        return round(curRt,2)
    #每天10%的斜率
    def GetTenPctRatio(self,startP,days):
        curRt=1
        for d in days:
            curRt=curRt*1.1
        curRt=startP*((curRt/days)*100)
        return round(curRt,2)

    #avDay:平均线的天数，
    def AverageLine(self,avDay,dataList):
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


    def show_KDJLine(self,dates,ks,ds,js):
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
        plt.plot(dates, js,label='J_line')
        plt.legend(loc='upper left',)
        plt.axis([dates[len(dates)-1],dates[0],0,100])

        plt.show()

    def kdjLine(self,curP,lowP,highP,n,m1,m2):
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
                    lp=self.GetLowPPastDays(tmpLowP)
                    hp=self.GetHighPastDays(tmpHighP)
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



    def GetLowPPastDays(self,lowP):
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

    def GetHighPastDays(self,highP):
        cP=highP[0]
        hp=highP[0]
        size=len(highP)
        for i in range(size):
            cP=highP[i]
            if hp<cP:
                hp=cP
        return hp

    def showKDJ_Code(self,datalist):
        dates=datalist[0][1]
        curPs=datalist[0][3]
        hightPs=datalist[0][4]
        lowPs=datalist[0][5]
        kdj=self.kdjLine(curPs,lowPs,hightPs,20,3,3)
        self.show_KDJLine(dates,kdj[0],kdj[1],kdj[2])


class StockData:
    def __init__(self):
        pass
    def getData(self,code,start,end):    
        fileName=code+"_"+start.replace('-','')+"-"+end.replace('-','')
        df = self.readFromCsv(fileName)
        if  df.empty:
            df = self.loadTushare_data(code,start,end)    
            self.writeToCsv(fileName,df)
            #重新读硬盘上的数据
            df = self.readFromCsv(fileName)
        return df   

    def loadTushare_data(self,code,startdate,enddate):
        df = ts.get_hist_data(code,startdate,enddate,)
        print (df)
        return df 

    def writeToCsv(self,name,data):
        dir='D:/Python36/Stock/'
        fileName= dir+ name + ".csv"
        if not os.path.exists(dir):
            os.makedirs(dir)
        data.to_csv(fileName)    

    def writeToExl(self,name,data):
        dir='D:/Python36/Stock/'
        fileName= dir+ name + ".xlsx"
        if not os.path.exists(dir):
            os.makedirs(dir)
        data.to_excel(fileName)    

    def readFromCsv(self,name):
        dir = 'D:/Python36/Stock/'
        fileName = dir + name + ".csv"
        if os.path.exists(fileName):
            data = pd.read_csv(fileName, na_values=['NA'])
            return data
        return pd.DataFrame()

    def readFromExl(self,name):
        dir='D:/Python36/Stock/'
        fileName= dir+ name + ".xlsx"
        if os.path.exists(fileName):
            data=pd.read_excel(fileName,na_values=['NA'])
            return data
        return pd.DataFrame();


class StockClass:
    pass

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

class MyJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict2obj)
    
    def dict2obj(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items())
            instance = class_(**args)
        else:
            instance = d
        return instance
        