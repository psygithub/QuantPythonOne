import datetime
import KDJmatlab

def showKdjMapbycode():
    today = datetime.datetime.today()
    # start = datetime.datetime(today.year-1,today.month,today.day)
    # today = datetime.datetime(2017,5,1)
    start = datetime.datetime(2017,1,1)
    st = start.strftime("%Y-%m-%d")
    ed = today.strftime("%Y-%m-%d")
    while True:
        #print('input a stock code:')
        inputStr=input('input a stock code:')
        if (inputStr=='exit'):
            break;
        stkCode=str(inputStr)
        # stock=data.getData(stkCode,st,ed)
        stock=data.getMongoData(stkCode,st,ed)     
        if len(stock)==0:
            data.PushDataToMongoDB(stkCode)
            stock=data.getMongoData(stkCode,st,ed) 
        datalist = kdj.formatMongoDB(stkCode,stock)   
        # if len(stock)!=0:
        #     datalist = kdj.formatMongoDB(stkCode,stock)
        # else:
        #     df=data.loadTushare_data(stkCode,st,ed)
        #     datalist=kdj.formatDataFrame(stkCode,df)
        collection=data.connectMongoDB("Stock")
        stkName=collection.find_one({'code':stkCode})
        if stkName==None:
            print('stock %s not found'%(stkCode))
            return
        kdj.showKDJ_Code(stkName['name']+str(datalist[0][0]),datalist)

def InitialStock():
    datalist=data.GetStockBasics()
    data.TuShareBatchInsert('Stock',datalist)


def InitAndUpdateStock():
    while True:
        inputStr=input('input a code:')
        if (inputStr=='exit'):
            break;
        stkCode=str(inputStr)
        data.PushDataToMongoDB(stkCode)

def BenXi(amount,ratio_Y,month):    
    # amount=145000
    # ratio_Y=0.02684
    # month=60
    ratio_M=ratio_Y/12
    factor=(1+ratio_M)**month
    pay_m=(ratio_M*factor*amount)/(factor-1)
    intst=pay_m-amount/month
    totalIntst=intst*month
    print('等额本息还款法')
    print('本金：%s,分期期数(按月)：%s,年利率：%s,月利率：%s'%(amount,month,ratio_Y,ratio_M))
    print('总还款：%s,总利息：%s,分期还款：%s,分期利息：%s'%(pay_m*month,totalIntst,pay_m,intst))

def BenJin(amount,ratio_Y,month):
    # amount=145000
    # ratio_Y=0.02684
    # month=60
    ratio_M=ratio_Y/12
    amount_m=amount/month
    totalIntst=ratio_M*(amount*month-(amount/month*(month*(month-1)/2)))
    print('等额本金还款法')
    print('本金：%s,分期期数(按月)：%s,总利息：%s,年利率：%s,月利率：%s'%(amount+totalIntst,month,totalIntst,ratio_Y,ratio_M))
#stkName=stkData.GetClassStock()
data=KDJmatlab.StockData()
kdj = KDJmatlab.KDJ_method()
# InitAndUpdateStock()
showKdjMapbycode()
# amount=100000
# ratio_Y=0.05
# month=24
# BenXi(amount,ratio_Y,month)
# BenJin(amount,ratio_Y,month)
#002352   600233   300013  601228 000760  600519 002326 601168


#测试从tushare下载数据日期到今天的数据
#stockMongo=data.PushDataToMongoDB(stkCode)
