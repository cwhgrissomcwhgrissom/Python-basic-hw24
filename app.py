from flask import Flask,request,abort
from bs4 import BeautifulSoup
import pandas as pd
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import requests , json , datetime , time ,os ,SrcFun ,EmilyAssItem, linecache


app=Flask(__name__)
# Channel Access Token
line_bot_api=LineBotApi('Enter your information')
# Channel Secret
handler=WebhookHandler('Enter your information')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback",methods=['GET','POST'])
def callback():
    # get X-Line-Signature header value
    signature=request.headers['X-Line-Signature']
    # get request body as text
    body=request.get_data(as_text=True)
    app.logger.info("Request body: "+body)
    # handle webhook body
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower() #將輸入的msg都切換成小寫
    # reply_message = TextSendMessage(text='請輸入正確指令')
    # 根據使用者輸入 event.message.text 條件判斷要回應哪一種訊息
    if "movie" in user_message :
        # pass
        reply_message = TextSendMessage(SrcFun.movie())
    elif 'music' in user_message :
        # pass
        url = 'https://www.youtube.com/watch?v=NWIveC8i_E4'
        reply_message = TextSendMessage(url)

    elif 'eps' in user_message :
        msg_num = user_message[-4:]    #(最後四位數為股票代碼)
        # SrcFun.get_stocknum(event.message.text) == a+'1':
        ass1_result = EmilyAssItem.get_ass1_result(msg_num)
        ass2_result = EmilyAssItem.get_ass2_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass1_result+"\n"+ass2_result))

    elif '本業比' in user_message :
        msg_num = user_message[-4:]
        ass4_result = EmilyAssItem.get_ass4_result(msg_num)
        ass5_result = EmilyAssItem.get_ass5_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass4_result+"\n"+ass5_result))

    elif '現金流' in user_message :
        msg_num = user_message[-4:]    #(最後四位數為股票代碼)
        ass6_result = EmilyAssItem.get_ass6_result(msg_num)
        ass7_result = EmilyAssItem.get_ass7_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass6_result+"\n"+ass7_result))

    elif '負載比' in user_message :
        msg_num = user_message[-4:]    #(最後四位數為股票代碼)
        ass8_result = EmilyAssItem.get_ass8_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass8_result))

    elif '資本額' in user_message :
        msg_num = user_message[-4:]    #(最後四位數為股票代碼)
        ass3_result = EmilyAssItem.get_ass3_result(msg_num)
        ass3a_result = EmilyAssItem.get_ass3a_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass3_result+"\n"+ass3a_result))

    elif '法人持股比' in user_message :
        msg_num = user_message[-4:]    #(最後四位數為股票代碼)
        ass9_result = EmilyAssItem.get_ass9_result(msg_num)
        ass10_result = EmilyAssItem.get_ass10_result(msg_num)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ass9_result+"\n"+ass10_result))

    elif '快速選單' in user_message :
        pass
    
    elif user_message.find("Menu") >= 0 or user_message.find("menu") >= 0 or user_message.find("Help") >= 0 or user_message.find("help") >= 0:
        # pass
        context = '''Menu 功能說明:
movie : 目前上映中電影
eps+股票代碼 : EPS & 再投資率
本業比+股票代碼 : 本業收入比 & 業外損失比
現金流+股票代碼 : 營收灌水比 & 營業 /自由活動現金流 & 連續8年發放股利
負載比+股票代碼 : 負債比 & 速動比 / 流動比 & 利息保障倍
資本額+股票代碼 : 上市時間(年) & 資本額 & 近一季的淨值
法人持股比+股票代碼 : 股本膨脹比率 & 董監事與法人持股比率 & 董監事股票質押比
'''
        reply_message = TextSendMessage(text=context)

    line_bot_api.reply_message(
        event.reply_token,
        reply_message)      

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
