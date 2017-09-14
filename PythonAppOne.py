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
import pickle  
import KDJmatlab

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        #if isinstance(obj, datetime):
            #return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def TestSaveMongo(code,df):
    post=connectMongoDB(code)
    dfJson=df.to_json(orient='records')
    #dfJson=dfJson.replace("[","").replace("]","") 
    objJson=json.loads(dfJson)
    post.insert_one(objJson[0])

def TuShareBatchInsert(code,stockJson):
    post=connectMongoDB(code)
    post.insert_many(stockJson)


def connectMongoDB(cllnName):
    client=MongoClient('127.0.0.1',27017)
    db=client.TuShare
    collection=db[cllnName]
    # for data in collection.find():  
    #     print(data )
    # collection.remove({'name':'123'})
    # collection.insert_one({'name':'123'})
    return collection
def GetStockFromMongo(code):
    collection=connectMongoDB(code)
    stkJson=collection.find();
    

def printDataBase(cllnName):     
    db=client.TuShare
    collection=db[cllnName]
    for data in collection.find():
        print(data)

def SaveCodeToMongoDB(datalist):
    for o in datalist:       
        TuShareBatchInsert(o[0],o[1])

# today = datetime.datetime.today();
# start = datetime.datetime(today.year-1,today.month,today.day)
today = datetime.datetime(2017,8,17)
start = datetime.datetime(2016,8,16)
#showMatlab()
st = start.strftime("%Y-%m-%d")
ed = today.strftime("%Y-%m-%d")
# db=connectMongoDB()
code='000848'
kdj = KDJmatlab.KDJ_method()
stk="000848"
#df = ts.get_hist_data(stk,st,ed)
#TestSaveMongo(stk,df)
data=KDJmatlab.StockData()
stock=data.getData(code,st,ed)
# datalist = kdj.formatMatLab(code,stock)
# kdj.showKDJ_Code(datalist)
jsonList=kdj.formatJson(code,stock)
SaveCodeToMongoDB(jsonList)
#kdj.showKDJ_Code(datalist)
#printDataBase(codes[0])

# averageList=AverageLine(10,datalist[0][3])
#SaveCodeToMongoDB(datalist)


#show_AverageLine(datalist[0][0],datalist[0][1],averageList)
#show_data(list)
#show_data(datalist)