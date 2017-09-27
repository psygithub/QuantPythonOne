import datetime
import KDJmatlab

def showKdjMapbycode():
    today = datetime.datetime.today()
    # start = datetime.datetime(today.year-1,today.month,today.day)
    #today = datetime.datetime(2017,8,17)
    start = datetime.datetime(2017,1,1)
    st = start.strftime("%Y-%m-%d")
    ed = today.strftime("%Y-%m-%d")
    while True:
        #print('input a stock code:')
        inputStr=input('input a stock code:')
        if (inputStr=='exit'):
            break;
        stkCode=str(inputStr)
        stock=data.getData(stkCode,st,ed)
        datalist = kdj.formatMatLab(stkCode,stock)
        collection=data.connectMongoDB("Stock")
        stkName=collection.find_one({'code':stkCode})
        if stkName==None:
            print('stock %s not found'%(stkCode))
            return
        kdj.showKDJ_Code(stkName['name']+str(datalist[0][0]),datalist)

def InitialStock():
    datalist=data.GetStockBasics()
    data.TuShareBatchInsert('stock',datalist)



#stkName=stkData.GetClassStock()
data=KDJmatlab.StockData()
kdj = KDJmatlab.KDJ_method()
InitialStock()



#002352   600233   300013  601228 000760  600519 002326 601168


#测试从tushare下载数据日期到今天的数据
#stockMongo=data.PushDataToMongoDB(stkCode)
