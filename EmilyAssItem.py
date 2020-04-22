
def get_ass1_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    date = datetime.datetime.now()
    int_years = date.year-1
    str_years = str(date.year-1)

    url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')

    eps_count = 0
    for n in range(0, 5):
            row_data = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')   
            if row_data[0].text == str_years:
                for m in range(n, 11):
                    net_profit_after_tax = soup.select('#row' + str(m) + ' > td:nth-child(19) > nobr > a')[0].text
                    net_profit_after_tax = float(net_profit_after_tax.replace(',',''))
                    if net_profit_after_tax > 0:
                        eps_count = eps_count + 1
                    #    print(net_profit_after_tax)
                    #else:
                    #    print(net_profit_after_tax)
    if eps_count >= 9:
        return ('連續9年以上EPS>0'+
                "\n---符合標準: Good!")
    else:
        pass
def get_ass2_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import datetime

    url = 'https://goodinfo.tw/stockinfo/stockfindetail.asp?step=data&stock_id='+stocknumber+'&rpt_cat=bs_m_year&qry_time=20194'
    headers = {'user-agent':'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.108 safari/537.36',
               'referer': 'https://goodinfo.tw/stockinfo/stockfindetail.asp?rpt_cat=bs_m_quar&stock_id='+stocknumber}
    list_req = requests.post(url, headers=headers)
    print(list_req)
    soup = BeautifulSoup(list_req.content, 'lxml')

    def get_sum_of_4years_eps():
        date = datetime.datetime.now()
        int_years = date.year-1
        str_years = str(date.year-1)

        url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='+stocknumber
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        datastream = requests.get(url, headers = headers)
        soup = BeautifulSoup(datastream.content,'lxml')

        for n in range(0, 5):
            row_data = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')   
            if row_data[0].text == str_years:
                net_profit_after_tax_2019 = soup.select('#row' + str(n) + '> td:nth-child(12) > nobr > a')[0].text
                net_profit_after_tax_2018 = soup.select('#row' + str(n+1) + '> td:nth-child(12) > nobr > a')[0].text
                net_profit_after_tax_2017 = soup.select('#row' + str(n+2) + '> td:nth-child(12) > nobr > a')[0].text
                net_profit_after_tax_2016 = soup.select('#row' + str(n+3) + '> td:nth-child(12) > nobr > a')[0].text
                net_profit_after_tax_2019 = net_profit_after_tax_2019.replace(',','')
                net_profit_after_tax_2018 = net_profit_after_tax_2018.replace(',','')
                net_profit_after_tax_2017 = net_profit_after_tax_2017.replace(',','')
                net_profit_after_tax_2016 = net_profit_after_tax_2016.replace(',','')
            else:
                pass

        sum = float(net_profit_after_tax_2019)+float(net_profit_after_tax_2018)+float(net_profit_after_tax_2017)+float(net_profit_after_tax_2016)
        return sum

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        if row_data1 == []:
            pass
        else:
            if row_data1[0].text == '固定資產合計':
                now = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
                now = now.replace(',','')
                pre4 = soup.select('#row' + str(n) + ' > td:nth-child(10) > nobr')[0].text
                pre4 = pre4.replace(',','')
            if row_data1[0].text == '長期投資合計':
                now1 = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
                now1 = now1.replace(',','')
                pre41 = soup.select('#row' + str(n) + ' > td:nth-child(10) > nobr')[0].text
                pre41 = pre41.replace(',','')

    calresult = (float(now)+float(now1))-(float(pre4)+float(pre41))  
    Reinvestment_Rate = calresult/get_sum_of_4years_eps()*100
    if Reinvestment_Rate < 40:
        return('Reinvestment_Rate<40%: {:.2f}%'.format(Reinvestment_Rate)+
               "\n---符合標準: Good!")
    elif Reinvestment_Rate > 80 and Reinvestment_Rate < 200:
        return('Reinvestment_Rate: {:.2f}%'.format(Reinvestment_Rate)+
               "\nReinvestment_Rate 沒有符合標準")
    else:
        return('Reinvestment_Rate: {:.2f}%'.format(Reinvestment_Rate)+
               "\nReinvestment_Rate 沒有符合標準")
def get_ass3_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    url = 'https://goodinfo.tw/StockInfo/BasicInfo.asp?STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    soup = soup.find('table', attrs={'class':'solid_1_padding_4_6_tbl'})
    soup = soup.find_all('td')

    for n in range(0, 80):
        if soup[n].text == '上市日期':
            data = soup[n+1].text
            #print(data)
        elif soup[n].text == '資本額':
            data1 = soup[n+1].text
            #print(data1)
            break
    data = list(data)
    date = []
    for i in range(0, 4):
        date.append(data[i])
    str_date = "".join(date)
    int_date = int(str_date)   
    datenow = datetime.datetime.now()
    yearnow = datenow.year
    total_money = []
    data1 = list(data1)
    for j in range(0, 5):
        if data[j] != '億':
            total_money.append(data1[j])
        else:
            pass
    str_total_money = "".join(total_money)
    int_total_money = float(str_total_money)

    print('上市時間(年)>7: '+ str(yearnow-int_date))
    print('資本額(億)>50: ' + str(int_total_money))
    
    if int_total_money > 50 and yearnow-int_date > 7:
        return ('上市時間(年)>7: '+ str(yearnow-int_date)+
                "\n"+'資本額(億)>50: ' + str(int_total_money)+
                "\n---符合標準: Good!")
    else:
        return ('上市時間 or 資本額 沒有符合標準')
def get_ass3a_result(stocknumber): 
    now2a = ''
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime
    url = 'https://goodinfo.tw/stockinfo/stockfindetail.asp?rpt_cat=bs_m_quar&stock_id='+stocknumber
    headers = {'user-agent':'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.108 safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    for n in range(55, 61):
        row_data2 = soup.select('#row' + str(n) + ' > td:nth-child(1)')
        if row_data2 == []:
            pass
        elif row_data2[0].text == '每股淨值(元)':
            now2a = soup.select('#row' + str(n) + ' > td:nth-child(2)')[0].text
            now2a = now2a.replace(',','')
            now2a = float(now2a)
        else:
            pass
    if now2a >= 15.0:
        return ("最近一季的淨值>15"+
                "\n---符合標準: Good!")
    else:
        return ('最近一季的淨值, 沒有符合標準')           
def get_ass4_result(stocknumber):

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    #print(soup)

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')

        # 取得最近一季的營業利益 and 取得最近一季的稅前利益
        if row_data1 == []:
            pass
        elif row_data1[0].text == '營業利益':
            now1a = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1a = now1a.replace(',','')
            #print(now1a)
        elif row_data1[0].text == '稅前淨利':
            now1b = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1b = now1b.replace(',','')
            #print(now1b)
        elif row_data1[0].text == '其他利益及損失':
            now1c = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1c = now1c.replace(',','')
            #print(now1c)
        elif row_data1[0].text == '合併稅後淨利':
            now1d = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1d = now1d.replace(',','')
            #print(now1d)

    # ------------------------------------合格標準: 本業收入比例 > 80%------------------------------------
    # 本業收入比率公式 = 近 1 季營業利益 / 近 1 季稅前利益
    income_ratio = (float(now1a) / float(now1b))*100
    if income_ratio > 80:
        return('本業收入比例: {:.2f}%'.format(income_ratio)+">80%"+
               "\n---符合標準: Good!")
    else:
        return("\n本業收入比例 沒有符合標準")
def get_ass5_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    #print(soup)

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        if row_data1 == []:
            pass
        elif row_data1[0].text == '營業利益':
            now1a = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1a = now1a.replace(',','')
        elif row_data1[0].text == '稅前淨利':
            now1b = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1b = now1b.replace(',','')
        elif row_data1[0].text == '其他利益及損失':
            now1c = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1c = now1c.replace(',','')
            #print(now1c)
        elif row_data1[0].text == '合併稅後淨利':
            now1d = soup.select('#row' + str(n) + ' > td:nth-child(3) > nobr')[0].text
            now1d = now1d.replace(',','')
            #print(now1d)
    # ------------------------------------合格標準: 業外損失比率 < 20%------------------------------------
    # 業外損失比率 = 近 1 季其他利益及損失 / 近 1 季稅後淨利
    loss_ratio_outside_business = (float(now1c) / float(now1d))*100
    if loss_ratio_outside_business < 20:
        return('業外損失比率: {:.2f}%'.format(loss_ratio_outside_business)+"< 20%"+
                "\n---符合標準: Good!")
    else:
        return('業外損失比率: {:.2f}%'.format(loss_ratio_outside_business)+"> 20% => fail"+
                "\n業外損失比率 沒有符合標準")
def get_ass6_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import datetime

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?STEP=DATA&STOCK_ID='+stocknumber+'&RPT_CAT=BS_M_YEAR&QRY_TIME=20194'
    headers = {'user-agent':'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.108 safari/537.36',
               'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID='+stocknumber}

    list_req = requests.post(url, headers=headers)
    list_req = requests.post(url, headers=headers)
    print(list_req)
    soup = BeautifulSoup(list_req.content, 'lxml')

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        if row_data1 == []:
            pass
        else:
            if row_data1[0].text == '應收帳款':
                a1 = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
                a1 = a1.replace(',','')
                #print(a1)
            elif row_data1[0].text == '存貨':
                a2 = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
                a2 = a2.replace(',','')
                #print(a2)
            else:
                pass

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?STEP=DATA&STOCK_ID='+stocknumber+'&RPT_CAT=IS_M_YEAR&QRY_TIME=20194'
    headers = {'user-agent':'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.108 safari/537.36',
               'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID='+stocknumber}
    list_req = requests.post(url, headers=headers)
    print(list_req)
    soup = BeautifulSoup(list_req.content, 'lxml')

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        if row_data1 == []:
            pass
        else:
            if row_data1[0].text == '營業收入':
                a3 = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
                a3 = a3.replace(',','')
                #print(a3)
    a1 = float(a1)
    a2 = float(a2)
    a3 = float(a3)
    result = ((a1+a2)/a3)*100
    if result < 30:
        #print('營收灌水比例: {:.2f}%'.format(result))
        return '營收灌水比例<30%: {:.2f}%'.format(result)+"\n---符合標準: Good!"
    else:
        return "\n營收灌水比例 沒有符合標準"
def get_ass7_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime
    url = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    datenow = datetime.datetime.now()
    yearnow = datenow.year
    str_yearnow = str(yearnow)
    soup = soup.find('div', attrs={'id':'divDetail'})
    soup = soup.find('table', attrs={'class':'solid_1_padding_4_0_tbl'})
    soup = soup.find_all('td')
    count = 0
    for q in range(yearnow, yearnow-8, -1):
        #print(q)
        for i in range(0, 600):
            #print(soup[i].text)
            if soup[i].text == str(q):
                #print(str(q)+'年發放股利: '+soup[i+1].text)
                if float(soup[i+1].text) > 0:
                    count = count + 1
                break
    #if count == 8:
        #print('符合條件: 連續'+str(count)+'年發放股利! Good!')
    #-------------------------------------------------------------------------------------------
    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=CF_M_QUAR_ACC&STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')
    #print(soup)

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1)')
        #print(row_data1)
        if row_data1 == []:
            pass
        elif row_data1[0].text == '營業活動之淨現金流入(出)':
            now1a = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
            now1a = now1a.replace(',','')
            #print(now1a)
        elif row_data1[0].text == '投資活動之淨現金流入(出)':
            now1b = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
            now1b = now1b.replace(',','')
            #print(now1b)

    now1a = float(now1a)
    now1b = float(now1b)
    FCF = now1a + now1b
    print("\n")
    #print('營業活動現金流: {:.2f}'.format(now1a))
    #print('自由活動現金流: {:.2f}'.format(FCF))
    if now1a and FCF > 0:
        #print('符合條件: 營業活動現金流 and 自由活動現金流 > 0, Good!')
        return '營業 and 自由活動現金流>0'+"\n連續"+str(count)+'年發放股利'+"\n---符合標準: Good!"
    else:
        return "\n營業or自由活動現金流 and 股利發放次數 沒有符合標準"
def get_ass8_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        #print(row_data1)
        if row_data1 == []:
            pass
        elif row_data1[0].text == '資產總額':
            now1a = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
            now1a = now1a.replace(',','')
            #print(now1a)
        elif row_data1[0].text == '負債總額':
            now1b = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
            now1b = now1b.replace(',','')
            #print(now1b)
        else:
            pass
    now1a = float(now1a)
    now1b = float(now1b)
    result = (now1b/now1a)*100
    print('負載比: {:.2f}'.format(result))

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')

    for q in range(60, 100):
        row_data = soup.select('#row' + str(q) + ' > td:nth-child(1) > nobr')
        #print(row_data)
        if row_data == []:
                pass
        elif row_data[0].text == '速動比':
            now1c = soup.select('#row' + str(q) + ' > td:nth-child(2) > nobr')[0].text
            now1c = now1c.replace(',','')
            #print(now1a)
        elif row_data[0].text == '流動比':
            now1d = soup.select('#row' + str(q) + ' > td:nth-child(2) > nobr')[0].text
            now1d = now1d.replace(',','')
            #print(now1d)
        elif row_data[0].text == '利息保障倍數':
            now1e = soup.select('#row' + str(q) + ' > td:nth-child(2) > nobr')[0].text
            now1e = now1e.replace(',','')
            #print(now1e)

    now1c = float(now1c)
    now1d = float(now1d)
    now1e = float(now1e)

    print('速動比: '+str(now1c))
    print('流動比: '+str(now1d))
    print('利息保障倍數: '+str(now1e))

    if now1c>100 and now1d>100 and now1e>5 and result<50:
        return("負債比<50; \n速動比 and 流動比>100" +"\n利息保障倍數>5"+"\n---符合標準: Good!")
    else:
        return "\n負債比 or 速動比 or 流動比 or 利息保障倍數 沒有符合標準"
def get_ass9_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?STEP=DATA&STOCK_ID='+stocknumber+'&RPT_CAT=BS_M_YEAR&QRY_TIME=20194'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID='+stocknumber}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')

    for n in range(0, 80):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr')
        #print(row_data1)
        if row_data1 == []:
            pass
        elif row_data1[0].text == '股本合計':
            now1a = soup.select('#row' + str(n) + ' > td:nth-child(2) > nobr')[0].text
            now1a = now1a.replace(',','')
            print(now1a)
            now1b = soup.select('#row' + str(n) + ' > td:nth-child(12) > nobr')[0].text
            now1b = now1b.replace(',','')
            print(now1b)
        else:
            pass
    now1a = float(now1a)
    now1b = float(now1b)
    result = ((now1a-now1b)/now1a)*100
    if result < 20:
        return('股本膨脹比率<20%: {:.2f}'.format(result)+"\n---符合標準: Good!")
    else:
        return "\n股本膨脹比率 沒有符合標準"
def get_ass10_result(stocknumber):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    url = 'https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID='+stocknumber
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    datastream = requests.get(url, headers = headers)
    soup = BeautifulSoup(datastream.content,'lxml')

    x = datetime.datetime.now()
    year = x.year
    month = x.month
    #print('{:0>2d}'.format(month))
    date_result = str(year)+'/'+str('{:0>2d}'.format(month))

    for n in range(0, 10):
        row_data1 = soup.select('#row' + str(n) + ' > td:nth-child(1) > nobr > a')
        #print(row_data1)
        if row_data1 == []:
            pass
        elif row_data1[0].text == date_result:
            da = soup.select('#row' + str(n) + ' > td:nth-child(17)')[0].text
            if da == '-':
                da = 0
            db = soup.select('#row' + str(n) + ' > td:nth-child(21) > nobr')[0].text
            if db == '-':
                db = 0
            dc = soup.select('#row' + str(n) + ' > td:nth-child(20)')[0].text
            if dc == '-':
                dc = 0
        else:
            pass
    da=float(da)
    db=float(db)
    dc=float(dc)
    result = da+db
    result2 = dc
    if result > 33 and result2 < 33:
        return('董監事與法人持股比率>33%: {:.2f}'.format(result)+
                "\n董監事股票質押比<33%: {:.2f}".format(result2)+
                "\n---符合標準: Good!")
    else:
        return "\n董監事與法人持股比率 or 董監事股票質押比 沒有符合標準"