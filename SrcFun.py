import requests , json , datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time

def Standard_Deviation(stocknumber):
    #su = stocknumber
    #su = str(su)
    #return 'WTF'
    #return stocknumber
    ##############################################################################
    #                     股票機器人 標準差分析（簡易板）
    ##############################################################################
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20180814&stockNo=' + stocknumber
    #url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20180814&stockNo=2330'
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson = json.loads(soup.text)

    # 判斷請求是否成功
    if getjson['stat'] != '很抱歉，沒有符合條件的資料!':
        stocklist = [getjson['data']]
    else:
        stocklist = ''  # 請求失敗回傳空值

    # 判斷是否為空值
    if len(stocklist) != 0:
        stockdf = pd.DataFrame(
            list(stocklist[0]),
            columns=[
                "日期", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差",
                "成交筆數"
            ])
        stockaverage = pd.to_numeric(stockdf['收盤價']).mean()
        stockstd = pd.to_numeric(stockdf['收盤價']).std()

        # 看看這隻股票現在是否便宜（平均-兩倍標準差）
        buy = '很貴不要買'
        if pd.to_numeric(
                stockdf['收盤價'][-1:]).values[0] < stockaverage - (2 * stockstd):
            buy = '這隻股票現在很便宜喔！'
        context=''
        # 顯示結果
        a = ('收盤價 ＝ ' + stockdf['收盤價'][-1:].values[0])
        b = ('\n中間價 ＝ ' + str(round(stockaverage,3)))
        c = ('\n線距 ＝ ' + str(round(stockstd,3)))
        context = a + b + c + '\n' + buy
        return context
        #print(context)
    else:
        return '請求失敗，請檢查您的股票代號'

def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('div.movielist_info h2 a')
    content = ""
    count = 0
    for i in data:
        if count < 8:
            title = i.text
            link =  i['href']
            content += '{}\n{}\n'.format(title, link)
            count = count + 1
    #print(content)
    return content

def time():
    datetime_dt = datetime.datetime.today()# 獲得當地時間
    context = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")  # 格式化日期
    return context


def get_stocknum(datastr):
    msg = datastr
    msg2 = []
    num = len(msg)
    for n in range(0, num):
        if msg[n] == 's':
            for n1 in range(1,num):
                msg2.append(msg[n1])  
    msg2 = ''.join(msg2)
    msg2 = str(msg2)
    return msg2
