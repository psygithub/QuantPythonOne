import datetime
import KDJmatlab

today = datetime.datetime.today();
# start = datetime.datetime(today.year-1,today.month,today.day)
#today = datetime.datetime(2017,8,17)
start = datetime.datetime(2017,1,1)
#showMatlab()
st = start.strftime("%Y-%m-%d")
ed = today.strftime("%Y-%m-%d")
# db=connectMongoDB()

kdj = KDJmatlab.KDJ_method()
#002352   600233   300013  601228 000760  600519 002326 601168
code="601168"
#df = ts.get_hist_data(code,st,ed)
#TestSaveMongo(code,df)
data=KDJmatlab.StockData()

#测试从tushare下载数据库日期到今天的数据
#stockMongo=data.PushDataToMongoDB(code)

stock=data.getData(code,st,ed)
datalist = kdj.formatMatLab(code,stock)
kdj.showKDJ_Code(datalist)

#jsonList=kdj.formatJson(code,stock)
#SaveStockToMongoDB(jsonList)
#kdj.showKDJ_Code(datalist)
#printDataBase(codes[0])

# averageList=AverageLine(10,datalist[0][3])
#SaveCodeToMongoDB(datalist)


#show_AverageLine(datalist[0][0],datalist[0][1],averageList)
#show_data(list)
#show_data(datalist)